"""VOID Sovereign Flet application; all inference and storage live in brain.py."""
from __future__ import annotations
import asyncio
import html
import logging
import os
import re
import shutil
import tempfile
import threading
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
import flet as ft
from brain import AdaptiveBrain, LocalEngine, Storage, safe_display

BG, GLASS, EDGE = '#07080c', '#12131c', '#1e202e'
CYAN, PURPLE, WHITE, MUTED = '#00f0ff', '#c5a3ff', '#f1efff', '#9295aa'
MOTION = ft.Animation(300, ft.AnimationCurve.EASE_OUT)
NAV = {
    'CHAT & INTELLIGENCE': ['VOID Core (Adaptive Chat)', 'Adaptive Learning Lab'],
    'POLYGLOT LAB': ['Polyglot Language Lab'],
    'EXPERT SUITE': ['Expert Domain Suite'],
    'PERSONAL VAULT': ['My Files & Photos', 'File & Photo Factory'],
    'CREATE & FORGE': ['Creative Studio', 'Codex & App Forge'],
    'LIFE & LIVE DATA': ['Life Command Deck', 'Live Data Hub', 'Newsroom'],
    'CONTROL CENTER': ['Security & Ethics Center', 'Customization Center', 'Engine Doctor & Telemetry'],
}
ALIASES = {
    'My Files & Photos': 'vault file upload search', 'File & Photo Factory': 'create file photo pdf',
    'Live Data Hub': 'weather stocks crypto', 'Newsroom': 'news rss headlines',
    'Life Command Deck': 'calendar appointment booking tasks', 'Polyglot Language Lab': 'translate hindi languages',
    'Engine Doctor & Telemetry': 'diagnostic errors status', 'Adaptive Learning Lab': 'learning brain memory',
}
CHAT_MODES = {'VOID Core (Adaptive Chat)', 'Polyglot Language Lab', 'Expert Domain Suite', 'Adaptive Learning Lab'}
DATA_DIR = Path(os.getenv('VOID_DATA_DIR', str(Path.home() / '.void_sovereign')))
_STORE: Storage | None = None
_STORE_LOCK = threading.Lock()

# Replace this value with the full Search Console token if the supplied ellipsis
# is an abbreviation. The optional environment override supports deployment.
GOOGLE_SITE_VERIFICATION = os.getenv(
    'GOOGLE_SITE_VERIFICATION', 'Vmq-IlyBC-OsAR4vf0...'
)


@contextmanager
def verified_web_assets():
    """Supply Flet with an index.html containing the tag in the initial HTML head.

    Flet copies index.html from assets_dir before applying its own web settings;
    all other packaged runtime files continue to be served by Flet normally.
    """
    from flet_web import get_package_web_dir

    original_assets = Path(__file__).resolve().parent / 'assets'
    with tempfile.TemporaryDirectory(prefix='void-web-assets-') as directory:
        assets = Path(directory)
        if original_assets.is_dir():
            shutil.copytree(original_assets, assets, dirs_exist_ok=True)
        index = assets / 'index.html'
        if not index.is_file():
            shutil.copyfile(Path(get_package_web_dir()) / 'index.html', index)
        source = index.read_text(encoding='utf-8')
        tag = '<meta name="google-site-verification" content="{}" />'.format(
            html.escape(GOOGLE_SITE_VERIFICATION, quote=True)
        )
        pattern = r'<meta\b(?=[^>]*\bname\s*=\s*[\"\']google-site-verification[\"\'])[^>]*>'
        source = re.sub(pattern, '', source, flags=re.IGNORECASE)
        source, count = re.subn(r'</head\s*>', lambda _: '  ' + tag + '\n</head>',
                                source, count=1, flags=re.IGNORECASE)
        if count != 1:
            raise RuntimeError('Unable to add verification tag: HTML head is missing')
        index.write_text(source, encoding='utf-8')
        yield str(assets)


def get_store() -> Storage:
    global _STORE
    with _STORE_LOCK:
        if _STORE is None:
            _STORE = Storage(DATA_DIR / 'void.sqlite3')
        return _STORE


def main(page: ft.Page):
    page.title = 'VOID MA · Sovereign OS'
    page.bgcolor = BG
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    store = get_store()
    owner = uuid.uuid4().hex
    brain = AdaptiveBrain(store.profile(owner))
    try:
        engine = LocalEngine()
    except ValueError:
        # Treat invalid configuration as an unavailable local core, never redirect to a remote host.
        engine = None
    state = {'chat': store.new_chat(owner), 'mode': 'VOID Core (Adaptive Chat)', 'busy': False,
             'runs': 0, 'prism': False, 'closed': False, 'attachment': None, 'diagnostics': []}

    def txt(value, size=12, color=MUTED, **kwargs):
        return ft.Text(value, size=size, color=color, **kwargs)

    def caption(value):
        return txt(value, 10, '#828699', weight=ft.FontWeight.BOLD)

    def glass(content, **kwargs):
        return ft.Container(content=content, bgcolor='#e612131c', blur=ft.Blur(8, 8),
                            border=ft.Border.all(1, EDGE), border_radius=16, **kwargs)

    def update():
        if not state['closed']:
            page.update()

    def hover(e):
        control = e.control
        active = str(e.data).lower() == 'true'
        control.scale = 1.025 if active else 1
        control.bgcolor = '#252438' if active else control.data
        control.update()

    def pill(content, on_click, *, color='#1a1b28', tooltip=None):
        return ft.Container(content=content, padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                            bgcolor=color, data=color, border=ft.Border.all(1, '#292b3e'), border_radius=30,
                            on_hover=hover, on_click=on_click, animate_scale=MOTION, animate=MOTION,
                            scale=1, ink=True, tooltip=tooltip)

    status = txt('VOID SECURE CORE · ACTIVE', 10, CYAN, weight=ft.FontWeight.BOLD)
    counter_msgs, counter_chats, counter_runs = txt('0', 17, WHITE), txt('1', 17, WHITE), txt('0', 17, WHITE)
    mode_title = txt('VOID Core (Adaptive Chat)', 11, '#c5a3ff', weight=ft.FontWeight.BOLD)
    mode_notice = txt('', 11, '#ddba8c', visible=False)
    notice_text = txt('', 12, WHITE, expand=True)
    notification = glass(ft.Row([ft.Icon(ft.Icons.INFO_OUTLINE, color=CYAN, size=17), notice_text], spacing=10),
                         padding=12, visible=False, animate_opacity=MOTION, opacity=1)
    diagnostic_lines = ft.Column([txt('READY', 11, CYAN)], spacing=6, scroll=ft.ScrollMode.AUTO, height=105)
    diagnostic_panel = glass(ft.Column([caption('CORE DIAGNOSTICS'), diagnostic_lines], spacing=8),
                             padding=14, visible=False, animate_opacity=MOTION)
    chat = ft.ListView(expand=True, spacing=14, padding=ft.Padding.symmetric(horizontal=2, vertical=12),
                       auto_scroll=True, auto_scroll_animation=0)
    command = ft.TextField(hint_text='Ask VOID anything…', multiline=True, min_lines=1, max_lines=5,
                           shift_enter=True, border=ft.NoInputBorder(), text_size=14, expand=True,
                           content_padding=12, color=WHITE, cursor_color=CYAN)
    send = ft.IconButton(icon=ft.Icons.ARROW_UPWARD_ROUNDED, icon_color=BG, bgcolor=CYAN,
                         tooltip='Send', animate_scale=MOTION)
    attach_label = txt('', 11, CYAN, visible=False)
    attach = ft.IconButton(icon=ft.Icons.ATTACH_FILE_ROUNDED, icon_color=MUTED, tooltip='Attach a text file', animate_scale=MOTION)
    clear_attach = ft.IconButton(icon=ft.Icons.CLOSE_ROUNDED, icon_color=MUTED, icon_size=15,
                                tooltip='Remove attachment', visible=False)
    new_session = ft.Button(content='+ New Session', bgcolor='#302341', color=WHITE, width=245, animate_scale=MOTION)
    sessions = ft.Dropdown(label='Current session', text_size=11, height=60,
                           border=ft.OutlineInputBorder(side=ft.BorderSide(1, EDGE), border_radius=10))
    search = ft.TextField(hint_text='Search dimensions…', prefix_icon=ft.Icons.SEARCH, text_size=12,
                          height=43, border=ft.OutlineInputBorder(side=ft.BorderSide(1, EDGE), border_radius=10),
                          content_padding=10)
    tool_column = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)
    prism = ft.Switch(value=False, active_color=PURPLE, label='VOID Prism Panel')
    stage_body = ft.Column(expand=True, spacing=12, animate_opacity=MOTION, opacity=1)
    quick_buttons = []
    style = ft.MarkdownStyleSheet(
        p_text_style=ft.TextStyle(color='#ebeaf5', size=14, height=1.5),
        strong_text_style=ft.TextStyle(color=WHITE, weight=ft.FontWeight.BOLD),
        code_text_style=ft.TextStyle(color=CYAN, font_family='monospace', size=13),
        list_bullet_text_style=ft.TextStyle(color=PURPLE, size=14),
        block_spacing=12, list_indent=22, codeblock_padding=12,
        codeblock_decoration=ft.BoxDecoration(bgcolor='#090a10', border=ft.Border.all(1, '#292b3e'), border_radius=10))

    def display(value):
        return safe_display(value, engine.known_models if engine else ())

    def bubble(role, value):
        user = role == 'user'
        md = ft.Markdown(value=display(value), selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                         auto_follow_links=False, fit_content=True, md_style_sheet=style)
        card = ft.Container(ft.Column([txt('OPERATOR' if user else '✦  VOID INTELLIGENCE', 10,
                    PURPLE if user else CYAN, weight=ft.FontWeight.BOLD), md], spacing=8),
                    bgcolor='#1c1829' if user else '#12131c', border=ft.Border.all(1, '#33283f' if user else EDGE),
                    border_radius=16, padding=16, expand=True, animate_opacity=MOTION)
        chat.controls.append(ft.Row([card], alignment=ft.MainAxisAlignment.END if user else ft.MainAxisAlignment.START))
        return md

    def inform(message):
        notice_text.value = display(message)
        notification.visible = True
        notification.opacity = 1

    def add_diagnostic(message):
        state['diagnostics'].append(display(message))
        state['diagnostics'] = state['diagnostics'][-20:]
        diagnostic_lines.controls = [txt(item, 11, CYAN) for item in state['diagnostics']]

    def update_counts():
        msgs, chats = store.counts(owner)
        counter_msgs.value, counter_chats.value, counter_runs.value = str(msgs), str(chats), str(state['runs'])

    def update_sessions():
        entries = store.list_chats(owner)
        total = len(entries)
        sessions.options = [ft.DropdownOption(key=cid, text=f'Session {total-index}  ·  {time.strftime("%H:%M", time.localtime(created))}')
                            for index, (cid, created) in enumerate(entries)]
        sessions.value = state['chat']

    def render_tools():
        query = (search.value or '').strip().lower()
        controls = []
        for group, names in NAV.items():
            matching = [name for name in names if not query or query in (name + ' ' + ALIASES.get(name, '') + ' ' + group).lower()]
            if not matching:
                continue
            radios = [ft.Radio(value=name, label=name, active_color=PURPLE,
                               label_style=ft.TextStyle(size=11, color=WHITE if name == state['mode'] else MUTED))
                      for name in matching]
            controls.append(ft.ExpansionTile(title=txt(group, 10, '#adb0c3', weight=ft.FontWeight.BOLD),
                controls=radios, expanded=bool(query) or state['mode'] in names, dense=True,
                tile_padding=ft.Padding.symmetric(horizontal=4), controls_padding=0,
                animation_style=ft.AnimationStyle(duration=300, curve=ft.AnimationCurve.EASE_OUT)))
        tool_column.controls = controls or [txt('No matching dimensions.', 12)]

    radio_group = ft.RadioGroup(content=tool_column, value=state['mode'])

    def filter_tools(e):
        render_tools()
        update()

    async def change_mode(e):
        state['mode'] = radio_group.value or 'VOID Core (Adaptive Chat)'
        mode_title.value = state['mode']
        pending = state['mode'] not in CHAT_MODES and state['mode'] != 'Engine Doctor & Telemetry'
        mode_notice.visible = pending
        mode_notice.value = 'This dimension is not connected yet; chat is available without external actions.' if pending else ''
        diagnostic_panel.visible = state['prism'] or state['mode'] == 'Engine Doctor & Telemetry'
        stage_body.opacity = 0.76
        render_tools()
        update()
        await asyncio.sleep(0.03)
        stage_body.opacity = 1
        update()

    def set_busy(busy):
        state['busy'] = busy
        send.disabled = new_session.disabled = sessions.disabled = attach.disabled = busy
        for control in quick_buttons:
            control.disabled = busy

    async def run_response(messages, response_md, chat_id):
        pieces = []
        failed = False
        previous_update = 0.0
        try:
            if engine is None:
                inform('Core configuration is invalid. Check local settings and retry.')
                failed = True
            else:
                async for event in engine.astream(messages):
                    if state['closed']:
                        return
                    if event.kind == 'attempt':
                        status.value = 'SYNCHRONIZING'
                        update()
                    elif event.kind == 'diagnostic':
                        add_diagnostic(event.text)
                        update()
                    elif event.kind == 'token':
                        pieces.append(event.text)
                        now = time.monotonic()
                        if now - previous_update >= 0.05:
                            response_md.value = display(''.join(pieces))
                            status.value = 'QUANTUM MESH ONLINE'
                            update()
                            previous_update = now
                    elif event.kind == 'error':
                        failed = True
                        inform(event.text)
                        add_diagnostic('CORE ATTENTION REQUIRED')
                        status.value = 'READY'
                        update()
                    elif event.kind == 'done':
                        status.value = 'READY'
            if state['closed']:
                return
            if pieces:
                actual = ''.join(pieces) + ('\n\n[Response interrupted. Please retry.]' if failed else '')
                store.add_message(owner, chat_id, 'assistant', actual)
                response_md.value = display(actual)
            elif failed:
                response_md.value = 'The core could not complete this request.'
            update_counts()
        except Exception:
            logging.getLogger('void.ui').error('Local session error')
            if not state['closed']:
                inform('Something interrupted this session. Please retry.')
                response_md.value = display(''.join(pieces)) if pieces else 'The core could not complete this request.'
                status.value = 'READY'
        finally:
            if not state['closed']:
                set_busy(False)
                update()

    def submit(value):
        value = (value or '').strip()
        if not value or state['busy'] or state['closed']:
            return
        try:
            attachment = state['attachment']
            stored = value
            if attachment:
                stored += '\n\n[Attached text: ' + attachment['name'] + ']\n' + attachment['text']
            store.add_message(owner, state['chat'], 'user', stored)
            brain.record_interaction(value)
            store.save_profile(owner, brain.profile)
            messages = [{'role': 'system', 'content': brain.system_prompt(value, state['mode'], state['prism'])}]
            messages += store.history(owner, state['chat'])
            bubble('user', value + ('\n\n📎 ' + attachment['name'] if attachment else ''))
            response_md = bubble('assistant', 'Preparing response…')
            state['attachment'] = None
            attach_label.visible = clear_attach.visible = False
            command.value = ''
            notification.visible = False
            state['diagnostics'] = []
            diagnostic_lines.controls = [txt('READY', 11, CYAN)]
            state['runs'] += 1
            set_busy(True)
            update_counts()
            update()
            page.run_task(run_response, messages, response_md, state['chat'])
        except Exception:
            set_busy(False)
            inform('Could not start this session. Please retry.')
            update()

    def new_chat(e):
        if state['busy']:
            return
        state['chat'] = store.new_chat(owner)
        state['attachment'] = None
        attach_label.visible = clear_attach.visible = False
        chat.controls.clear()
        notification.visible = False
        status.value = 'READY'
        update_sessions()
        update_counts()
        update()

    def select_chat(e):
        if state['busy'] or not sessions.value:
            return
        state['chat'] = sessions.value
        chat.controls.clear()
        for message in store.history(owner, state['chat'], 200):
            bubble(message.get('role', 'assistant'), message.get('content', ''))
        notification.visible = False
        update()

    async def choose_file(e):
        if state['busy']:
            return
        try:
            files = await ft.FilePicker().pick_files(allow_multiple=False, with_data=True,
                        file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=['txt', 'md', 'csv', 'json'])
            if not files:
                return
            item = files[0]
            if item.size > 100_000 or item.bytes is None:
                inform('Choose a UTF-8 text file smaller than 100 KB.')
            else:
                try:
                    content = item.bytes.decode('utf-8')
                except UnicodeDecodeError:
                    inform('The selected file is not UTF-8 text.')
                else:
                    state['attachment'] = {'name': Path(item.name).name[:120], 'text': content[:48_000]}
                    attach_label.value = display('Attached: ' + state['attachment']['name'])
                    attach_label.visible = clear_attach.visible = True
                    if len(content) > 48_000:
                        inform('The attachment was shortened to 48,000 characters.')
            update()
        except Exception:
            inform('The file could not be attached. Please try again.')
            update()

    def remove_file(e):
        state['attachment'] = None
        attach_label.visible = clear_attach.visible = False
        update()

    def toggle_prism(e):
        state['prism'] = bool(prism.value)
        diagnostic_panel.visible = state['prism'] or state['mode'] == 'Engine Doctor & Telemetry'
        update()

    search.on_change = filter_tools
    radio_group.on_change = change_mode
    sessions.on_change = select_chat
    prism.on_change = toggle_prism
    attach.on_click = choose_file
    clear_attach.on_click = remove_file
    send.on_click = lambda e: submit(command.value)
    command.on_submit = lambda e: submit(command.value)
    new_session.on_click = new_chat
    render_tools()
    update_sessions()

    quick_specs = [
        ('☀  Live Weather', 'Help me check current weather. Ask for my location and explain that live weather is not connected.'),
        ('अ  हिन्दी में पूछें', 'नमस्ते! कृपया मुझसे सरल हिंदी में बात करें और पूछें कि मुझे किस विषय में मदद चाहिए।'),
        ('♡  Emotional Support', 'I would like emotional support. Please listen kindly and ask what is on my mind.'),
        ('◷  Book Appointment', 'Help me prepare to book an appointment. Ask for details; do not claim that a booking was made.'),
    ]
    for label, prompt in quick_specs:
        button = pill(txt(label, 12, '#dfdce9'), lambda e, p=prompt: submit(p))
        quick_buttons.append(button)

    sidebar = ft.Container(width=290, padding=ft.Padding.symmetric(horizontal=18, vertical=22), bgcolor='#12131c',
        border=ft.Border.only(right=ft.BorderSide(1, EDGE)),
        content=ft.Column(expand=True, spacing=12, controls=[
            ft.Row([ft.Container(ft.Icon(ft.Icons.AUTO_AWESOME, color=WHITE, size=20), bgcolor='#684da0', border_radius=12, padding=9),
                    ft.Column([txt('VOID', 19, WHITE, weight=ft.FontWeight.BOLD), txt('MA  /  SOVEREIGN OS', 9, MUTED)], spacing=0),
                    ft.Container(txt('V9', 10, CYAN, weight=ft.FontWeight.BOLD), bgcolor='#17262b', border_radius=7, padding=6)]),
            ft.Divider(color=EDGE, height=1),
            ft.Row([ft.Container(ft.Icon(ft.Icons.PERSON_OUTLINE, color=PURPLE, size=18), bgcolor='#222033', border_radius=12, padding=9),
                    ft.Column([txt('CRISTIANO RONALDO', 11, WHITE, weight=ft.FontWeight.BOLD), txt('Class 8 Operator', 10)], spacing=3)]),
            caption('COMMAND SEARCH'), search, caption('DIMENSIONS'),
            ft.Container(content=radio_group, expand=True), new_session, sessions, prism,
            ft.Divider(color=EDGE, height=1), caption('LIVE TELEMETRY'),
            ft.Row([ft.Column([counter_msgs, txt('Msgs', 10)], spacing=2, expand=True),
                    ft.Column([counter_chats, txt('Chats', 10)], spacing=2, expand=True),
                    ft.Column([counter_runs, txt('Runs', 10)], spacing=2, expand=True)]),
            txt('SESSION  ·  LOCAL INFERENCE', 9, '#686d80')]))

    stage_body.controls = [
        ft.Row([status, ft.Container(expand=True), txt('READY', 10, CYAN, weight=ft.FontWeight.BOLD)]),
        ft.Divider(color=EDGE, height=4),
        ft.Row([ft.Column([txt('Hello, Operator', 30, WHITE, weight=ft.FontWeight.BOLD),
                           txt('Your intelligence workspace is ready. What shall we explore?', 13)], spacing=5, expand=True),
                glass(mode_title, padding=10)]),
        ft.Row(quick_buttons, wrap=True, spacing=8, run_spacing=8), mode_notice,
        chat, notification, diagnostic_panel,
        ft.Row([attach_label, clear_attach], spacing=2),
        glass(ft.Row([attach, command, send], spacing=4), padding=5),
        txt('Enter to send  ·  Shift+Enter for a new line  ·  Check important information', 10, '#717588')]
    # The colored circles are ornamental: window-manager actions differ across desktop and web.
    header = ft.Row([ft.Container(bgcolor=c, width=10, height=10, border_radius=10) for c in ('#ff6a61', '#f8bf55', '#4fd37b')], spacing=7)
    stage = ft.Container(expand=True, padding=ft.Padding.symmetric(horizontal=32, vertical=22),
                         content=ft.Column([header, stage_body], expand=True, spacing=18))
    page.on_disconnect = lambda e: state.update(closed=True)
    page.add(ft.Row([sidebar, stage], spacing=0, expand=True))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    # Web binding defaults to loopback for local runs; cloud platforms set PORT.
    port = int(os.getenv('PORT', os.getenv('FLET_PORT', '8550')))
    host = os.getenv('FLET_HOST', '0.0.0.0' if os.getenv('PORT') else '127.0.0.1')
    web = os.getenv('VOID_WEB') == '1' or bool(os.getenv('PORT'))
    with verified_web_assets() as web_assets:
        ft.run(main, host=host, port=port, assets_dir=web_assets,
               view=ft.AppView.WEB_BROWSER if web else ft.AppView.FLET_APP)
