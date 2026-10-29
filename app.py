"""VOID's Flet shell. AI, profiles and persistence live in brain.py."""
from __future__ import annotations
import logging
import os
import threading
import time
import uuid
from pathlib import Path
import flet as ft
from brain import AdaptiveBrain, OpenRouterEngine, Storage

NAV = {
    'CHAT & INTELLIGENCE': ['VOID Core (Adaptive Chat)', 'Polyglot Language Lab', 'Expert Domain Suite', 'Adaptive Learning Lab'],
    'PERSONAL VAULT': ['My Files & Photos', 'File & Photo Factory'],
    'CREATE & FORGE': ['Creative Studio', 'Codex & App Forge'],
    'LIFE & LIVE DATA': ['Life Command Deck', 'Live Data Hub', 'Newsroom'],
    'CONTROL CENTER': ['Security & Ethics Center', 'Customization Center', 'Engine Doctor & Telemetry'],
}
ALIASES = {'My Files & Photos': 'vault files search upload', 'File & Photo Factory': 'make pdf csv image',
           'Live Data Hub': 'weather stocks crypto live', 'Newsroom': 'news rss headlines',
           'Life Command Deck': 'calendar appointment booking tasks', 'Polyglot Language Lab': 'language translate hindi',
           'Engine Doctor & Telemetry': 'diagnostics error logs status', 'Adaptive Learning Lab': 'learning brain memory'}
CORE_MODES = set(NAV['CHAT & INTELLIGENCE'])
BG, PANEL, BORDER, MUTED, WHITE, PURPLE, CYAN = '#090a0f', '#11121c', '#29263a', '#8d91a8', '#f1efff', '#a979ff', '#69e9ee'


def main(page: ft.Page):
    page.title = 'VOID MA · Sovereign Intelligence'
    page.bgcolor = BG
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    # A random guest identity is deliberately NOT an email login. No founder privileges are granted.
    owner = uuid.uuid4().hex
    data_dir = Path(os.getenv('VOID_DATA_DIR', str(Path.home() / '.void_flet')))
    store = Storage(data_dir / 'void.sqlite3')
    brain = AdaptiveBrain(store.profile(owner))
    engine = OpenRouterEngine(allow_inkling=os.getenv('VOID_ALLOW_INKLING') == '1')
    state = {'chat': store.new_chat(owner), 'mode': NAV['CHAT & INTELLIGENCE'][0], 'busy': False,
             'runs': 0, 'prism': False, 'closed': False, 'diagnostics': []}
    lock = threading.RLock()

    def text(value, size=12, color=MUTED, **kw):
        return ft.Text(value, size=size, color=color, **kw)

    def panel(content, **kw):
        return ft.Container(content=content, bgcolor=PANEL, border=ft.Border.all(1, BORDER), border_radius=14, **kw)

    def label(value):
        return text(value, 10, '#85849d', weight=ft.FontWeight.BOLD)

    status = text('SYSTEM READY  ·  AWAITING COMMAND', 10, CYAN, weight=ft.FontWeight.BOLD)
    greeting = text('Hello, Guest Operator', 29, WHITE, weight=ft.FontWeight.BOLD)
    subtitle = text('Your intelligence workspace is online. What shall we explore?', 13)
    counter_msgs, counter_chats, counter_runs = text('0', 17, WHITE), text('1', 17, WHITE), text('0', 17, WHITE)
    diagnostics = ft.Column([text('No engine attempts yet.', 11)], spacing=6, scroll=ft.ScrollMode.AUTO, height=150)
    diag_panel = panel(ft.Column([ft.Row([ft.Icon(ft.Icons.MONITOR_HEART_OUTLINED, color=CYAN, size=17), label('ENGINE DIAGNOSTICS')]),
                                  text('Model attempts and exact errors appear here.', 11), diagnostics], spacing=8), padding=14, visible=False)
    mode_hint = text('', 11, '#d8ae7b', visible=False)
    chat = ft.ListView(expand=True, spacing=14, padding=ft.Padding.symmetric(horizontal=2, vertical=12),
                       auto_scroll=True, auto_scroll_animation=0)
    command = ft.TextField(hint_text='Message VOID…', multiline=True, min_lines=1, max_lines=4,
                           shift_enter=True, border=ft.NoInputBorder(), text_size=14, expand=True,
                           content_padding=14, color=WHITE, cursor_color=CYAN)
    send = ft.IconButton(icon=ft.Icons.ARROW_UPWARD_ROUNDED, icon_color=BG, bgcolor=CYAN, tooltip='Send message')
    new_session = ft.Button('+ New Session', bgcolor='#302145', color=WHITE, width=240)
    quick_buttons = []
    tool_column = ft.Column(spacing=0)
    search = ft.TextField(hint_text='Search 14 tools…', prefix_icon=ft.Icons.SEARCH, text_size=12,
                          height=42, border_color=BORDER, focused_border_color=PURPLE, border_radius=10,
                          content_padding=10)
    category = ft.Dropdown(value=list(NAV)[0], options=[ft.DropdownOption(key=k, text=k) for k in NAV],
                           text_size=11, height=45, border_color=BORDER, border_radius=10, content_padding=10)
    modes = ft.RadioGroup(value=state['mode'], content=tool_column)
    prism = ft.Switch(value=False, active_color=PURPLE, label='VOID Prism Panel')

    def refresh_counters():
        m, c = store.counts(owner)
        counter_msgs.value, counter_chats.value, counter_runs.value = str(m), str(c), str(state['runs'])

    def update():
        if not state['closed']:
            page.update()

    def render_tools():
        q = search.value.strip().lower()
        names = [name for items in NAV.values() for name in items if q in (name + ' ' + ALIASES.get(name, '')).lower()] if q else NAV.get(category.value, [])
        tool_column.controls = [ft.Radio(value=n, label=n, active_color=PURPLE,
                                      label_style=ft.TextStyle(size=12, color=WHITE if n == state['mode'] else MUTED)) for n in names]
        if not names:
            tool_column.controls = [text('No matching tools.', 12)]

    def on_filter(e):
        render_tools()
        update()

    def on_mode(e):
        state['mode'] = modes.value
        not_ported = state['mode'] not in CORE_MODES and state['mode'] != 'Engine Doctor & Telemetry'
        mode_hint.visible = not_ported
        mode_hint.value = ('This module is not migrated yet. Chat can discuss it, but no live data, files, or actions are connected.' if not_ported else '')
        diag_panel.visible = state['prism'] or state['mode'] == 'Engine Doctor & Telemetry'
        render_tools()
        update()

    def on_prism(e):
        state['prism'] = bool(prism.value)
        diag_panel.visible = state['prism'] or state['mode'] == 'Engine Doctor & Telemetry'
        update()

    def append_diagnostic(value):
        state['diagnostics'].append(value)
        state['diagnostics'] = state['diagnostics'][-30:]
        diagnostics.controls = [text(v, 11, '#ffd2a4' if ('HTTP ' in v or 'Error' in v or 'failed' in v or 'Missing' in v) else MUTED, selectable=True) for v in state['diagnostics']]

    def bubble(role, content):
        is_user = role == 'user'
        md = ft.Markdown(value=content, selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                         auto_follow_links=False, fit_content=True)
        card = ft.Container(content=ft.Column([text('OPERATOR' if is_user else '✦  VOID INTELLIGENCE', 10,
                        '#c5a3ff' if is_user else CYAN, weight=ft.FontWeight.BOLD), md], spacing=8),
                        bgcolor='#201a30' if is_user else '#131620', border=ft.Border.all(1, '#3d2e55' if is_user else '#252b3d'),
                        border_radius=15, padding=16, expand=True)
        chat.controls.append(ft.Row([card], alignment=ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START))
        return md

    def set_busy(busy):
        state['busy'] = busy
        send.disabled = new_session.disabled = busy
        for button in quick_buttons:
            button.disabled = busy

    def worker(messages, response_md, target_chat):
        output = []
        last_refresh = 0.0
        failed = False
        try:
            for event in engine.stream(messages):
                with lock:
                    if state['closed']:
                        return
                    if event.kind == 'attempt':
                        status.value = f'CONNECTING  ·  {event.model}'
                        append_diagnostic(event.text)
                        update()
                    elif event.kind == 'diagnostic':
                        append_diagnostic(event.text)
                        update()
                    elif event.kind == 'token':
                        output.append(event.text)
                        now = time.monotonic()
                        if now - last_refresh >= 0.05:
                            response_md.value = ''.join(output)
                            status.value = f'STREAMING  ·  {event.model}'
                            update()
                            last_refresh = now
                    elif event.kind == 'error':
                        failed = True
                        diag_panel.visible = True
                        response_md.value = (''.join(output) + '\n\n' if output else '') + '⚠️ ' + event.text
                        status.value = 'ENGINE ATTENTION REQUIRED  ·  SEE DIAGNOSTICS'
                        update()
                    elif event.kind == 'done':
                        status.value = f'COMPLETE  ·  {event.model}'
            with lock:
                if state['closed']:
                    return
                if output:
                    actual = ''.join(output)
                    if failed:
                        actual += '\n\n[Response interrupted; retry for a complete answer.]'
                    store.add_message(owner, target_chat, 'assistant', actual)
                    if not failed:
                        response_md.value = actual
                refresh_counters()
        except Exception as exc:
            logging.exception('VOID worker failed')
            with lock:
                if not state['closed']:
                    append_diagnostic(f'Local error: {type(exc).__name__}: {exc}')
                    diag_panel.visible = True
                    status.value = 'LOCAL ERROR  ·  SEE DIAGNOSTICS'
                    response_md.value = ''.join(output) + '\n\n⚠️ Local error; see diagnostics.'
        finally:
            with lock:
                if not state['closed']:
                    set_busy(False)
                    update()

    def submit(value):
        value = value.strip()
        with lock:
            if not value or state['busy'] or state['closed']:
                return
            try:
                target_chat = state['chat']
                store.add_message(owner, target_chat, 'user', value)
                brain.record_interaction(value)
                store.save_profile(owner, brain.profile)
                history = store.history(owner, target_chat)
                messages = [{'role': 'system', 'content': brain.system_prompt(value, state['mode'], state['prism'])}] + history
                bubble('user', value)
                response_md = bubble('assistant', 'Connecting…')
                command.value = ''
                state['runs'] += 1
                state['diagnostics'] = []
                diagnostics.controls = [text('Connecting…', 11)]
                set_busy(True)
                refresh_counters()
                update()
                page.run_thread(worker, messages, response_md, target_chat)
            except Exception as exc:
                set_busy(False)
                append_diagnostic(f'Local error: {type(exc).__name__}: {exc}')
                diag_panel.visible = True
                update()

    def new_chat(e):
        with lock:
            if state['busy']:
                return
            state['chat'] = store.new_chat(owner)
            chat.controls.clear()
            status.value = 'NEW SESSION  ·  READY'
            refresh_counters()
            update()

    search.on_change = category.on_change = on_filter
    modes.on_change = on_mode
    prism.on_change = on_prism
    new_session.on_click = new_chat
    command.on_submit = lambda e: submit(command.value)
    send.on_click = lambda e: submit(command.value)
    render_tools()

    quick_specs = [
        ('☀  Live Weather', 'Help me check the current weather. Ask me for my city and explain that you cannot access live conditions in this chat.'),
        ('अ  हिन्दी में पूछें', 'नमस्ते! कृपया मुझसे सरल हिंदी में बात करें। पूछें कि मुझे किस विषय में मदद चाहिए।'),
        ('♡  Emotional Support', 'I would like emotional support. Please listen kindly and ask what is on my mind.'),
        ('◷  Book Appointment', 'Help me prepare to book an appointment. Ask for the service, location and preferred time; do not claim you booked it.'),
    ]
    for caption, prompt in quick_specs:
        b = ft.Button(content=caption, bgcolor='#191827', color='#ddd7f3', elevation=0,
                      on_click=lambda e, p=prompt: submit(p))
        quick_buttons.append(b)

    sidebar = ft.Container(width=280, padding=ft.Padding.symmetric(horizontal=20, vertical=24), bgcolor='#0e0f17',
        border=ft.Border.only(right=ft.BorderSide(1, '#222331')),
        content=ft.Column(expand=True, spacing=16, controls=[
            ft.Row([ft.Container(ft.Icon(ft.Icons.AUTO_AWESOME, color=WHITE, size=20), bgcolor='#653ab3', border_radius=11, padding=9),
                    ft.Column([text('VOID', 19, WHITE, weight=ft.FontWeight.BOLD), text('MA  /  SOVEREIGN OS', 9, '#a89dbf')], spacing=0),
                    ft.Container(text('V9', 10, CYAN, weight=ft.FontWeight.BOLD), bgcolor='#18272a', border_radius=7, padding=6)]),
            ft.Divider(color=BORDER, height=1), label('COMMAND SEARCH'), search,
            label('DIMENSIONS'), category,
            ft.Container(content=modes, expand=True),
            new_session, ft.Row([prism], alignment=ft.MainAxisAlignment.START),
            ft.Divider(color=BORDER, height=1), label('LIVE TELEMETRY'),
            ft.Row([ft.Column([counter_msgs, text('Msgs', 10)], spacing=2, expand=True),
                    ft.Column([counter_chats, text('Chats', 10)], spacing=2, expand=True),
                    ft.Column([counter_runs, text('Runs', 10)], spacing=2, expand=True)]),
            text('GUEST SESSION  ·  LOCAL', 9, '#666b7f')]))
    stage = ft.Container(expand=True, padding=ft.Padding.symmetric(horizontal=32, vertical=25),
        content=ft.Column(expand=True, spacing=12, controls=[
            ft.Row([status, ft.Container(expand=True), text('◉  OPENROUTER', 10, CYAN)]),
            ft.Divider(color='#20212c', height=10),
            ft.Row([ft.Column([greeting, subtitle], spacing=5, expand=True),
                    ft.Container(text('✦  ADAPTIVE INTELLIGENCE', 10, '#c5a3ff'), bgcolor='#211a31', border_radius=30, padding=10)]),
            ft.Row(quick_buttons, wrap=True, spacing=8, run_spacing=8), mode_hint,
            chat, diag_panel,
            panel(ft.Row([command, send], spacing=5), padding=5),
            text('VOID can make mistakes. Verify important information.  ·  Enter to send / Shift+Enter for a new line', 10, '#717386')]))
    page.on_disconnect = lambda e: state.update(closed=True)
    page.add(ft.Row([sidebar, stage], spacing=0, expand=True))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    ft.run(main, host=os.getenv('FLET_HOST', '127.0.0.1'), port=int(os.getenv('FLET_PORT', '8550')),
           view=ft.AppView.WEB_BROWSER if os.getenv('VOID_WEB') == '1' else ft.AppView.FLET_APP) 
 
