import asyncio
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import pytest
from brain import AdaptiveBrain, LocalEngine, Storage, normalize_profile, safe_display, validate_local_url


class Handler(BaseHTTPRequestHandler):
    attempts = []
    def log_message(self, *args): pass
    def do_GET(self):
        body = json.dumps({'models': [{'name': 'first:latest'}, {'name': 'second:latest'}]}).encode()
        self.send_response(200); self.end_headers(); self.wfile.write(body)
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        model = body['model']
        Handler.attempts.append(model)
        if model == 'first:latest':
            self.send_response(429); self.end_headers(); self.wfile.write(b'private vendor error'); return
        self.send_response(200); self.send_header('Content-Type', 'application/x-ndjson'); self.end_headers()
        for obj in ({'message': {'content': 'Hello'}}, {'message': {'content': ' operator'}, 'done': True}):
            self.wfile.write((json.dumps(obj) + '\n').encode()); self.wfile.flush()

@pytest.fixture
def core():
    Handler.attempts = []
    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    yield f'http://127.0.0.1:{server.server_port}'
    server.shutdown(); server.server_close(); thread.join()


def test_profile_safeguards():
    for item in (None, {}, {'learning': None}, {'learning': 'bad'}, {'learning': {'topic_affinity': None, 'seen_examples': None}, 'prefs': 'bad'}):
        brain = AdaptiveBrain(item)
        brain.record_interaction('hello world')
        assert brain.learning['seen_examples'] == 1
        assert brain.learning['topic_affinity']['hello'] == 1
        assert isinstance(brain.profile['prefs'], dict)
    assert normalize_profile({'old_data': 42})['old_data'] == 42


def test_pool_isolates_owners_and_handles_threads(tmp_path):
    store = Storage(tmp_path / 'test.sqlite', 3)
    cid = store.new_chat('alice')
    def add(i): store.add_message('alice', cid, 'user', str(i))
    with ThreadPoolExecutor(max_workers=8) as executor:
        list(executor.map(add, range(30)))
    assert store.counts('alice') == (30, 1)
    assert store.history('other', cid) == []
    with pytest.raises(ValueError): store.add_message('other', cid, 'user', 'oops')
    store.save_profile('alice', {'prefs': None, 'learning': None})
    assert store.profile('alice')['learning']['seen_examples'] == 0
    assert store.list_chats('alice')[0][0] == cid
    store.close()


@pytest.mark.parametrize('url', ['http://example.com:11434', 'https://127.0.0.1:11434',
    'http://127.0.0.1@evil.example', 'http://localhost:11434', 'http://127.0.0.1:11434/path'])
def test_non_loopback_rejected(url):
    with pytest.raises(ValueError): validate_local_url(url)


def test_fallback_and_no_identifiers_in_diagnostics(core):
    engine = LocalEngine(base_url=core)
    events = list(engine.stream([{'role':'user', 'content':'hi'}]))
    assert Handler.attempts == ['first:latest', 'second:latest']
    assert ''.join(e.text for e in events if e.kind == 'token') == 'Hello operator'
    assert events[-1].kind == 'done'
    assert any(e.kind == 'diagnostic' and e.text == '[ROUTING FALLBACK ENGAGED]' for e in events)
    assert all('first:latest' not in e.text and 'second:latest' not in e.text for e in events)


def test_async_bridge_and_missing_core(core):
    async def collect():
        return [e async for e in LocalEngine(base_url=core).astream([])]
    events = asyncio.run(collect())
    assert events[-1].kind == 'done'
    unavailable = list(LocalEngine(base_url='http://127.0.0.1:1', timeout=(0.2,0.2)).stream([]))
    assert unavailable[-1].kind == 'error'
    assert 'http' not in unavailable[-1].text.lower()


def test_partial_stream_does_not_concatenate_fallback():
    class Response:
        status_code = 200
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def iter_lines(self, **kw):
            yield json.dumps({'message': {'content': 'partial'}})
            yield json.dumps({'error': 'some provider secret'})
    class Session:
        def post(self, *a, **kw): return Response()
        def close(self): pass
    events = list(LocalEngine(models=('first','second'), session_factory=Session).stream([]))
    assert ''.join(e.text for e in events if e.kind == 'token') == 'partial'
    assert events[-1].kind == 'error'
    assert 'provider' not in events[-1].text
    assert sum(e.kind == 'attempt' for e in events) == 1


def test_safe_display():
    value = safe_display('OpenRouter and nvidia/nemotron plus gemini and local-model:latest', ('local-model:latest',))
    assert all(s not in value.lower() for s in ('openrouter','nvidia','nemotron','gemini','local-model'))


def test_cloud_marked_models_are_skipped():
    class Session:
        def post(self, *args, **kwargs):
            raise AssertionError('cloud model must never be requested')
        def close(self): pass
    events = list(LocalEngine(models=('model:cloud', 'model:120b-cloud'), session_factory=Session).stream([]))
    assert events[-1].kind == 'error'
    assert not any(e.kind == 'attempt' for e in events)


def test_research_searches_both_and_cites(monkeypatch):
    import brain
    payloads = []
    def fake_get(url, params, limit=1_000_000):
        payloads.append((url, params))
        if 'bing.com' in url:
            return b'''<rss><channel><item><title>Solar guide</title><link>https://example.org/solar</link><description>A &lt;b&gt;useful&lt;/b&gt; overview.</description></item><item><title>Bad</title><link>javascript:alert(1)</link></item></channel></rss>'''
        return json.dumps({'query': {'search': [{'title': 'Solar power', 'snippet': 'A &lt;span&gt;solar&lt;/span&gt; source'}]}}).encode()
    monkeypatch.setattr(brain, '_bounded_get', fake_get)
    result = brain.research_web('  solar power  ')
    assert len(result.sources) == 2 and not result.unavailable
    assert result.sources[0].snippet == 'A useful overview.'
    assert [s.provider for s in result.sources] == ['Bing', 'Wikipedia']
    assert '[1]' in brain.format_research_context(result)
    assert 'https://example.org/solar' in brain.format_sources(result)
    assert len(payloads) == 2
    assert all('solar power' in str(p) for _, p in payloads)


def test_research_empty_and_provider_failure(monkeypatch):
    import brain
    def fail(*args, **kwargs): raise RuntimeError('private error')
    monkeypatch.setattr(brain, '_bounded_get', fail)
    assert brain.research_web('').sources == ()
    result = brain.research_web('weather')
    assert result.sources == () and set(result.unavailable) == {'Bing', 'Wikipedia'}
    assert 'private error' not in str(result)


def test_research_sources_escape_markdown():
    from brain import ResearchResult, WebSource, format_sources
    result = ResearchResult((WebSource('a ](javascript:attack)', 'https://example.org/a(b)', 'text', 'Wikipedia'),))
    rendered = format_sources(result)
    assert '\\]' in rendered and 'https://example.org/a%28b%29' in rendered


def test_web_results_reject_private_addresses():
    from brain import _public_url
    for url in ('http://127.0.0.1/private', 'http://192.168.1.1/', 'http://localhost/', 'javascript:alert(1)', 'https://user:pass@example.org/'):
        assert not _public_url(url)
    assert _public_url('https://example.org/source')
