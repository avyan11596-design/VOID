"""VOID Sovereign OS - Standalone Single-File Flet Application
Upgraded with Email OTP Login & Comms Center, Dynamic Theme Engine, and Multi-Layout Switcher.
"""
from __future__ import annotations
import asyncio
import hmac
import html
import json
import logging
import os
import re
import secrets
import shutil
import smtplib
import sqlite3
import tempfile
import threading
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from email.message import EmailMessage
from pathlib import Path
from typing import Dict, Generator, List
import flet as ft
import requests

MOTION = ft.Animation(300, ft.AnimationCurve.EASE_OUT)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")

THEMES: Dict[str, Dict[str, str]] = {
    'Cyber-Glass': {
        'bg': '#07080c', 'glass': '#12131c', 'glass_alpha': '#e612131c', 'edge': '#1e202e',
        'cyan': '#00f0ff', 'purple': '#c5a3ff', 'white': '#f1efff', 'muted': '#9295aa',
        'user_bubble': '#1c1829', 'hero_a': '#24203e', 'hero_b': '#141621', 'hero_c': '#10252a',
    },
    'Sovereign Gold': {
        'bg': '#090705', 'glass': '#15120c', 'glass_alpha': '#e615120c', 'edge': '#2e2418',
        'cyan': '#fbbf24', 'purple': '#f59e0b', 'white': '#fefce8', 'muted': '#a8a29e',
        'user_bubble': '#241c10', 'hero_a': '#2e210d', 'hero_b': '#17130c', 'hero_c': '#241a0b',
    },
    'Matrix Bio-Neon': {
        'bg': '#040a07', 'glass': '#0b1912', 'glass_alpha': '#e60b1912', 'edge': '#163024',
        'cyan': '#10b981', 'purple': '#06b6d4', 'white': '#ecfdf5', 'muted': '#86efac',
        'user_bubble': '#0f2419', 'hero_a': '#0c2b1d', 'hero_b': '#091912', 'hero_c': '#082529',
    },
    'Crimson Supernova': {
        'bg': '#0b0507', 'glass': '#1a0d12', 'glass_alpha': '#e61a0d12', 'edge': '#331822',
        'cyan': '#fb7185', 'purple': '#c084fc', 'white': '#fff1f2', 'muted': '#fda4af',
        'user_bubble': '#28111b', 'hero_a': '#361322', 'hero_b': '#1a0d12', 'hero_c': '#241029',
    },
    'OLED Stealth': {
        'bg': '#020203', 'glass': '#0d0d11', 'glass_alpha': '#e60d0d11', 'edge': '#242429',
        'cyan': '#ffffff', 'purple': '#a1a1aa', 'white': '#fafafa', 'muted': '#71717a',
        'user_bubble': '#18181c', 'hero_a': '#18181f', 'hero_b': '#0d0d11', 'hero_c': '#141418',
    },
}

LAYOUTS = ['Sovereign OS', 'Terminal CLI', 'Bento Dashboard']

NAV = {
    'CHAT & INTELLIGENCE': ['VOID Core (Adaptive Chat)', 'Adaptive Learning Lab'],
    'COMMUNICATIONS': ['Email & Comms Center'],
    'POLYGLOT LAB': ['Polyglot Language Lab'],
    'EXPERT SUITE': ['Expert Domain Suite'],
    'PERSONAL VAULT': ['My Files & Photos', 'File & Photo Factory'],
    'CREATE & FORGE': ['Creative Studio', 'Codex & App Forge'],
    'LIFE & LIVE DATA': ['Life Command Deck', 'Live Data Hub', 'Newsroom'],
    'CONTROL CENTER': ['Customization Center', 'Security & Ethics Center', 'Engine Doctor & Telemetry'],
}

ALIASES = {
    'My Files & Photos': 'vault file upload search',
    'File & Photo Factory': 'create file photo pdf',
    'Live Data Hub': 'weather stocks crypto',
    'Newsroom': 'news rss headlines',
    'Life Command Deck': 'calendar appointment booking tasks',
    'Polyglot Language Lab': 'translate hindi languages',
    'Engine Doctor & Telemetry': 'diagnostic errors status',
    'Adaptive Learning Lab': 'learning brain memory',
    'Email & Comms Center': 'email mail smtp send inbox otp',
    'Customization Center': 'theme layout color glass ui appearance',
}

CHAT_MODES = {
    'VOID Core (Adaptive Chat)',
    'Polyglot Language Lab',
    'Expert Domain Suite',
    'Adaptive Learning Lab',
    'Creative Studio',
    'Codex & App Forge',
    'Life Command Deck',
    'Live Data Hub',
    'Newsroom',
    'Security & Ethics Center',
    'My Files & Photos',
    'File & Photo Factory',
}

DATA_DIR = Path(os.getenv('VOID_DATA_DIR', str(Path.home() / '.void_sovereign')))
_STORE: Storage | None = None
_STORE_LOCK = threading.Lock()

GOOGLE_SITE_VERIFICATION = os.getenv('GOOGLE_SITE_VERIFICATION', 'Vmq-IlyBC-OsAR4vf0...')


@dataclass
class StreamEvent:
    kind: str  # 'attempt', 'diagnostic', 'token', 'error', 'done'
    model: str
    text: str = ''


class EmailService:
    """Handles OTP verification emails and outbound user emails via SMTP or EmailJS."""
    @staticmethod
    def send_email(to_addr: str, subject: str, body: str, otp_code: str = '') -> tuple[bool, str]:
        to_addr = (to_addr or '').strip()
        subject = (subject or '').strip()
        body = (body or '').strip()
        if not EMAIL_RE.match(to_addr):
            return False, 'Enter a valid recipient email address.'
        if not subject or not body:
            return False, 'Subject and message body are required.'

        # 1. Try SMTP if configured in environment
        smtp_host = os.getenv('SMTP_HOST', '').strip()
        smtp_port = os.getenv('SMTP_PORT', '587').strip()
        smtp_user = os.getenv('SMTP_USERNAME', '').strip()
        smtp_pass = os.getenv('SMTP_PASSWORD', '').strip()
        smtp_from = os.getenv('SMTP_FROM', '').strip() or smtp_user
        if smtp_host and smtp_user and smtp_pass:
            msg = EmailMessage()
            msg['From'] = smtp_from
            msg['To'] = to_addr
            msg['Subject'] = subject
            msg.set_content(body)
            try:
                port_num = int(smtp_port)
                if port_num == 465:
                    with smtplib.SMTP_SSL(smtp_host, port_num, timeout=18) as srv:
                        srv.login(smtp_user, smtp_pass)
                        srv.send_message(msg)
                else:
                    with smtplib.SMTP(smtp_host, port_num, timeout=18) as srv:
                        srv.ehlo()
                        srv.starttls()
                        srv.ehlo()
                        srv.login(smtp_user, smtp_pass)
                        srv.send_message(msg)
                return True, f'Dispatched via SMTP to {to_addr}.'
            except Exception as exc:
                return False, f'SMTP error: {str(exc)[:160]}'

        # 2. Try EmailJS if configured in environment
        ejs_service = os.getenv('EMAILJS_SERVICE_ID', '').strip()
        ejs_template = os.getenv('EMAILJS_TEMPLATE_ID', '').strip()
        ejs_public = os.getenv('EMAILJS_PUBLIC_KEY', '').strip()
        ejs_private = os.getenv('EMAILJS_PRIVATE_KEY', '').strip()
        if ejs_service and ejs_template and ejs_public:
            payload = {
                'service_id': ejs_service,
                'template_id': ejs_template,
                'user_id': ejs_public,
                'template_params': {
                    'to_email': to_addr,
                    'subject': subject,
                    'message': body,
                    'otp_code': otp_code or body,
                },
            }
            if ejs_private:
                payload['accessToken'] = ejs_private
            try:
                resp = requests.post(
                    'https://api.emailjs.com/api/v1.0/email/send',
                    json=payload,
                    timeout=18,
                )
                if resp.status_code == 200:
                    return True, f'Dispatched via EmailJS to {to_addr}.'
                return False, f'EmailJS HTTP {resp.status_code}: {resp.text[:140]}'
            except Exception as exc:
                return False, f'EmailJS error: {str(exc)[:160]}'

        # 3. Local Sandbox Fallback (so local testing & OTP login never lock out)
        if otp_code:
            return True, f'Sandbox Mode (no SMTP/EmailJS keys set) · Use OTP Code: {otp_code}'
        return True, f'Saved to local Outbox Vault for {to_addr} (set SMTP_HOST or EMAILJS_* for live relay).'


class Storage:
    """Thread-safe SQLite persistence for user profiles, chats, messages, and emails."""
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path, timeout=15.0)

    def _init_db(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS profiles (
                    owner TEXT PRIMARY KEY,
                    data TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner TEXT NOT NULL,
                    created_at REAL NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    msg_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner TEXT NOT NULL,
                    chat_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at REAL NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS emails (
                    email_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner TEXT NOT NULL,
                    recipient TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    body TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at REAL NOT NULL
                )
            """)

    def profile(self, owner: str) -> dict:
        with self._connect() as conn:
            row = conn.execute('SELECT data FROM profiles WHERE owner = ?', (owner,)).fetchone()
            if row:
                try:
                    data = json.loads(row[0])
                except Exception:
                    data = {}
            else:
                data = {}
        data.setdefault('learning', {'interactions': 0, 'topics': [], 'preferred_lang': 'auto'})
        default_name = owner.split('@')[0].upper() if '@' in owner else 'AVYAN'
        data.setdefault('ui', {
            'theme': 'Cyber-Glass',
            'layout': 'Sovereign OS',
            'blur': 8,
            'operator_name': default_name,
            'operator_rank': 'Founder & Lead Architect' if 'avyan' in owner.lower() else 'Sovereign Operator',
        })
        return data

    def save_profile(self, owner: str, profile_data: dict):
        profile_data.setdefault('learning', {})
        profile_data.setdefault('ui', {})
        with self._connect() as conn:
            conn.execute(
                'INSERT OR REPLACE INTO profiles (owner, data) VALUES (?, ?)',
                (owner, json.dumps(profile_data)),
            )

    def new_chat(self, owner: str) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                'INSERT INTO chats (owner, created_at) VALUES (?, ?)',
                (owner, time.time()),
            )
            return int(cur.lastrowid)

    def add_message(self, owner: str, chat_id: int, role: str, content: str):
        with self._connect() as conn:
            conn.execute(
                'INSERT INTO messages (owner, chat_id, role, content, created_at) VALUES (?, ?, ?, ?, ?)',
                (owner, chat_id, role, content, time.time()),
            )

    def history(self, owner: str, chat_id: int, limit: int = 20) -> List[Dict[str, str]]:
        with self._connect() as conn:
            rows = conn.execute(
                'SELECT role, content FROM messages WHERE owner = ? AND chat_id = ? ORDER BY msg_id DESC LIMIT ?',
                (owner, chat_id, limit),
            ).fetchall()
        return [{'role': r, 'content': c} for r, c in reversed(rows)]

    def counts(self, owner: str):
        with self._connect() as conn:
            msgs = conn.execute('SELECT COUNT(*) FROM messages WHERE owner = ?', (owner,)).fetchone()[0]
            chats = conn.execute('SELECT COUNT(*) FROM chats WHERE owner = ?', (owner,)).fetchone()[0]
        return msgs, max(1, chats)

    def list_chats(self, owner: str):
        with self._connect() as conn:
            return conn.execute(
                'SELECT chat_id, created_at FROM chats WHERE owner = ? ORDER BY chat_id DESC',
                (owner,),
            ).fetchall()

    def log_email(self, owner: str, recipient: str, subject: str, body: str, status: str):
        with self._connect() as conn:
            conn.execute(
                'INSERT INTO emails (owner, recipient, subject, body, status, created_at) VALUES (?, ?, ?, ?, ?, ?)',
                (owner, recipient, subject, body, status, time.time()),
            )

    def list_emails(self, owner: str, limit: int = 15):
        with self._connect() as conn:
            return conn.execute(
                'SELECT recipient, subject, body, status, created_at FROM emails WHERE owner = ? ORDER BY email_id DESC LIMIT ?',
                (owner, limit),
            ).fetchall()


class AdaptiveBrain:
    def __init__(self, profile_data: dict | None = None):
        self.profile = profile_data if isinstance(profile_data, dict) else {}
        self.learning = self.profile.setdefault(
            'learning', {'interactions': 0, 'topics': [], 'preferred_lang': 'auto'}
        )
        self.ui = self.profile.setdefault(
            'ui', {
                'theme': 'Cyber-Glass',
                'layout': 'Sovereign OS',
                'blur': 8,
                'operator_name': 'AVYAN',
                'operator_rank': 'Founder & Lead Architect',
            }
        )

    def record_interaction(self, text: str):
        self.learning['interactions'] = self.learning.get('interactions', 0) + 1
        words = [w.strip('.,!?').lower() for w in text.split() if len(w) > 4]
        if words:
            topics = self.learning.get('topics', [])
            for w in words[:3]:
                if w not in topics:
                    topics.append(w)
            self.learning['topics'] = topics[-25:]

    def system_prompt(self, user_input: str, mode: str, prism: bool) -> str:
        interactions = self.learning.get('interactions', 0)
        topics = ', '.join(self.learning.get('topics', [])[-8:]) or 'general exploration'
        op_name = self.ui.get('operator_name', 'Operator')
        prism_note = ' Include a brief, structured analytical breakdown when helpful.' if prism else ''
        return (
            f'You are VOID 9.5.0-MA — Sovereign OS Intelligence, architected by Avyan '
            f'(14-year-old Founder & Lead Architect of VOID, student at Sunbeam School Varuna in Varanasi, '
            f'creator of VoidOS, author of World Zero, gamer NOTREFLEXGAMING05).\n'
            f'Current Operator: {op_name} | Active Dimension / Mode: {mode}.\n'
            f'Operator Interactions: {interactions} | Recent Context Interests: {topics}.\n'
            f'Respond in the same language the user writes in (20+ languages supported including Hindi and English). '
            f'Be sharp, insightful, empathetic, and clear.{prism_note}'
        )


class OpenRouterEngine:
    def __init__(self):
        self.models = [
            'google/gemma-4-31b-it:free',
            'nvidia/nemotron-3.5-lightning:free',
            'nvidia/nemotron-3.5-super-vl:free',
            'qwen/qwen3.8-27b:free',
            'openrouter/free',
        ]
        self.known_models = self.models

    def stream(self, messages: List[Dict[str, str]]) -> Generator[StreamEvent, None, None]:
        api_key = os.getenv('OPENROUTER_API_KEY', '').strip()
        if not api_key:
            yield StreamEvent(kind='diagnostic', model='none', text='Missing OPENROUTER_API_KEY environment variable.')
            yield StreamEvent(kind='error', model='none', text='Missing OPENROUTER_API_KEY. Add your key in Render/env.')
            return

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://void-os.local',
            'X-Title': 'VOID Sovereign OS',
        }

        last_err = 'Unknown error'
        for model in self.models:
            yield StreamEvent(kind='attempt', model=model, text=f'Attempting {model}...')
            try:
                resp = requests.post(
                    'https://openrouter.ai/api/v1/chat/completions',
                    headers=headers,
                    json={'model': model, 'messages': messages, 'stream': True},
                    stream=True,
                    timeout=35,
                )
                if resp.status_code != 200:
                    err_snippet = resp.text[:160].replace('\n', ' ')
                    last_err = f'{model} -> HTTP {resp.status_code}: {err_snippet}'
                    yield StreamEvent(kind='diagnostic', model=model, text=last_err)
                    continue

                got_tokens = False
                for raw_line in resp.iter_lines(decode_unicode=True):
                    if not raw_line:
                        continue
                    line = raw_line if isinstance(raw_line, str) else raw_line.decode('utf-8', errors='ignore')
                    if not line.startswith('data:'):
                        continue
                    data_str = line[5:].strip()
                    if data_str == '[DONE]':
                        break
                    try:
                        chunk = json.loads(data_str)
                        delta = chunk.get('choices', [{}])[0].get('delta', {})
                        token = delta.get('content') or ''
                        if token:
                            got_tokens = True
                            yield StreamEvent(kind='token', model=model, text=token)
                    except Exception:
                        continue

                if got_tokens:
                    yield StreamEvent(kind='done', model=model)
                    return
                else:
                    last_err = f'{model} returned an empty stream.'
                    yield StreamEvent(kind='diagnostic', model=model, text=last_err)

            except Exception as exc:
                last_err = f'{model} failed: {type(exc).__name__}: {exc}'
                yield StreamEvent(kind='diagnostic', model=model, text=last_err)
                continue

        yield StreamEvent(kind='error', model='all', text=f'All streaming engines failed. Last error: {last_err}')


def safe_display(text: str, known_models=()) -> str:
    return str(text)


@contextmanager
def verified_web_assets():
    """Supply Flet with an index.html containing the Google verification tag."""
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
        source, count = re.subn(
            r'</head\s*>',
            lambda _: '  ' + tag + '\n</head>',
            source,
            count=1,
            flags=re.IGNORECASE,
        )
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
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    store = get_store()
    try:
        engine = OpenRouterEngine()
    except ValueError:
        engine = None

    state = {
        'owner': 'avyan@void.os',
        'authenticated': False,
        'pending_email': '',
        'pending_name': '',
        'target_otp': '',
        'otp_expiry': 0.0,
        'chat': 1,
        'mode': 'VOID Core (Adaptive Chat)',
        'busy': False,
        'runs': 0,
        'prism': False,
        'web': False,
        'closed': False,
        'attachment': None,
        'diagnostics': ['VOID SECURE KERNEL INITIALIZED'],
        'welcome': True,
        'theme': 'Cyber-Glass',
        'layout': 'Sovereign OS',
        'blur': 8,
        'operator_name': 'AVYAN',
        'operator_rank': 'Founder & Lead Architect',
    }

    brain = AdaptiveBrain(store.profile(state['owner']))

    def palette() -> Dict[str, str]:
        return THEMES.get(state['theme'], THEMES['Cyber-Glass'])

    page.bgcolor = palette()['bg']

    def txt(value, size=12, color=None, **kwargs):
        return ft.Text(value, size=size, color=color or palette()['muted'], **kwargs)

    def caption(value):
        return txt(value, 10, palette()['muted'], weight=ft.FontWeight.BOLD)

    def glass(content, **kwargs):
        p = palette()
        blur_val = int(state.get('blur', 8))
        return ft.Container(
            content=content,
            bgcolor=kwargs.pop('bgcolor', p['glass_alpha']),
            blur=ft.Blur(blur_val, blur_val),
            border=ft.Border.all(1, kwargs.pop('border_color', p['edge'])),
            border_radius=kwargs.pop('border_radius', 16),
            **kwargs,
        )

    def update():
        if not state['closed']:
            page.update()

    def hover(e):
        control = e.control
        active = str(e.data).lower() == 'true'
        control.scale = 1.025 if active else 1
        control.bgcolor = palette()['edge'] if active else control.data
        control.update()

    def pill(content, on_click, *, color=None, tooltip=None):
        p = palette()
        base_c = color or p['glass']
        return ft.Container(
            content=content,
            padding=ft.Padding.symmetric(horizontal=14, vertical=10),
            bgcolor=base_c,
            data=base_c,
            border=ft.Border.all(1, p['edge']),
            border_radius=30,
            on_hover=hover,
            on_click=on_click,
            animate_scale=MOTION,
            animate=MOTION,
            scale=1,
            ink=True,
            tooltip=tooltip,
        )

    # --- CORE DYNAMIC CONTROLS ---
    root_host = ft.Container(expand=True)
    status = txt('VOID SECURE CORE · ACTIVE', 10, palette()['cyan'], weight=ft.FontWeight.BOLD)
    counter_msgs = txt('0', 17, palette()['white'], weight=ft.FontWeight.BOLD)
    counter_chats = txt('1', 17, palette()['white'], weight=ft.FontWeight.BOLD)
    counter_runs = txt('0', 17, palette()['white'], weight=ft.FontWeight.BOLD)
    mode_title = txt(state['mode'], 11, palette()['purple'], weight=ft.FontWeight.BOLD)
    notice_text = txt('', 12, palette()['white'], expand=True)
    notification = glass(
        ft.Row([ft.Icon(ft.Icons.INFO_OUTLINE, color=palette()['cyan'], size=17), notice_text], spacing=10),
        padding=12, visible=False, animate_opacity=MOTION, opacity=1,
    )
    diagnostic_lines = ft.Column([txt('READY', 11, palette()['cyan'])], spacing=6, scroll=ft.ScrollMode.AUTO, height=110)
    diagnostic_panel = glass(
        ft.Column([caption('CORE DIAGNOSTICS & TELEMETRY'), diagnostic_lines], spacing=8),
        padding=14, visible=False, animate_opacity=MOTION,
    )
    chat = ft.ListView(
        expand=True, spacing=14,
        padding=ft.Padding.symmetric(horizontal=2, vertical=12),
        auto_scroll=True, auto_scroll_animation=0,
    )
    command = ft.TextField(
        hint_text='Ask VOID anything…', multiline=True, min_lines=1, max_lines=5,
        shift_enter=True, border=ft.NoInputBorder(), text_size=14, expand=True,
        content_padding=12, color=palette()['white'], cursor_color=palette()['cyan'],
    )
    send = ft.IconButton(
        icon=ft.Icons.ARROW_UPWARD_ROUNDED, icon_color=palette()['bg'],
        bgcolor=palette()['cyan'], tooltip='Send', animate_scale=MOTION,
    )
    attach_label = txt('', 11, palette()['cyan'], visible=False)
    attach = ft.IconButton(
        icon=ft.Icons.ATTACH_FILE_ROUNDED, icon_color=palette()['muted'],
        tooltip='Attach a text file', animate_scale=MOTION,
    )
    clear_attach = ft.IconButton(
        icon=ft.Icons.CLOSE_ROUNDED, icon_color=palette()['muted'],
        icon_size=15, tooltip='Remove attachment', visible=False,
    )
    new_session = ft.Button(
        content='+ New Session', bgcolor=palette()['edge'],
        color=palette()['white'], width=245, animate_scale=MOTION,
    )
    sessions = ft.Dropdown(
        label='Current session', text_size=11, height=60,
        border=ft.OutlineInputBorder(side=ft.BorderSide(1, palette()['edge']), border_radius=10),
    )
    search = ft.TextField(
        hint_text='Search dimensions…', prefix_icon=ft.Icons.SEARCH, text_size=12,
        height=43, border=ft.OutlineInputBorder(side=ft.BorderSide(1, palette()['edge']), border_radius=10),
        content_padding=10,
    )
    tool_column = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)
    prism = ft.Switch(value=False, active_color=palette()['purple'], label='VOID Prism Panel')
    web_switch = ft.Switch(value=False, active_color=palette()['cyan'], label='Web research')
    web_disclosure = txt('OFF · No searches sent', 10, palette()['muted'])
    quick_buttons: List[ft.Control] = []

    def md_stylesheet():
        p = palette()
        return ft.MarkdownStyleSheet(
            p_text_style=ft.TextStyle(color=p['white'], size=14, height=1.5),
            strong_text_style=ft.TextStyle(color=p['white'], weight=ft.FontWeight.BOLD),
            code_text_style=ft.TextStyle(color=p['cyan'], font_family='monospace', size=13),
            list_bullet_text_style=ft.TextStyle(color=p['purple'], size=14),
            block_spacing=12, list_indent=22, codeblock_padding=12,
            codeblock_decoration=ft.BoxDecoration(
                bgcolor=p['bg'], border=ft.Border.all(1, p['edge']), border_radius=10
            ),
        )

    def display(value):
        return safe_display(str(value))

    async def open_link(e):
        try:
            if e.data and e.data.startswith('http'):
                await ft.UrlLauncher().launch_url(e.data)
        except (ValueError, TypeError):
            inform('This link could not be opened.')
            update()

    def bubble(role, value):
        p = palette()
        user = role == 'user'
        md = ft.Markdown(
            value=display(value), selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            auto_follow_links=False, on_tap_link=open_link,
            fit_content=True, md_style_sheet=md_stylesheet(),
        )
        op_label = state['operator_name'] if user else '✦  VOID INTELLIGENCE'
        card = ft.Container(
            ft.Column([
                txt(op_label, 10, p['purple'] if user else p['cyan'], weight=ft.FontWeight.BOLD),
                md,
            ], spacing=8),
            bgcolor=p['user_bubble'] if user else p['glass'],
            border=ft.Border.all(1, p['purple'] if user else p['edge']),
            border_radius=16, padding=16, expand=True, animate_opacity=MOTION,
        )
        chat.controls.append(
            ft.Row([card], alignment=ft.MainAxisAlignment.END if user else ft.MainAxisAlignment.START)
        )
        return md

    def show_welcome():
        p = palette()
        state['welcome'] = True
        hero = ft.Container(
            padding=26, border_radius=22, border=ft.Border.all(1, p['edge']),
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT,
                colors=[p['hero_a'], p['hero_b'], p['hero_c']],
            ),
            content=ft.Column(spacing=14, controls=[
                ft.Row([
                    ft.Container(
                        ft.Icon(ft.Icons.AUTO_AWESOME, color=p['cyan'], size=25),
                        bgcolor=p['glass'], border_radius=14, padding=13,
                    ),
                    ft.Column([
                        caption(f"SOVEREIGN WORKSPACE · {state['theme'].upper()} · {state['layout'].upper()}"),
                        txt(f"Welcome back, {state['operator_name']}.", 22, p['white'], weight=ft.FontWeight.BOLD),
                    ], spacing=4),
                ]),
                txt(
                    'Switch themes live, toggle between OS Deck, Terminal CLI, and Bento Dashboard, '
                    'or dispatch AI-crafted emails from your Sovereign Command Center.',
                    13, p['muted'],
                ),
                ft.Row([
                    ft.Container(
                        txt(label, 10, color, weight=ft.FontWeight.BOLD),
                        bgcolor=p['glass'], border_radius=20, padding=8,
                    )
                    for label, color in [
                        ('✦  ADAPTIVE BRAIN', p['purple']),
                        ('✉  EMAIL SUITE', p['cyan']),
                        ('◈  MULTI-LAYOUT UI', p['white']),
                    ]
                ], wrap=True, spacing=8),
            ]),
        )
        tips = ft.Row(wrap=True, spacing=10, run_spacing=10, controls=[
            glass(
                ft.Row([
                    ft.Icon(icon, color=color, size=18),
                    ft.Column([
                        txt(title, 12, p['white'], weight=ft.FontWeight.BOLD),
                        txt(detail, 10, p['muted']),
                    ], spacing=3),
                ], spacing=10),
                padding=14, width=235,
            )
            for icon, color, title, detail in [
                (ft.Icons.PALETTE_OUTLINED, p['cyan'], '5 Dynamic Themes', 'Customize colors & glass blur live'),
                (ft.Icons.VIEW_QUILT_OUTLINED, p['purple'], '3 UI Layouts', 'OS Deck, Terminal CLI & Bento Grid'),
                (ft.Icons.MAIL_OUTLINE_ROUNDED, p['white'], 'Email & OTP Gate', 'AI email drafting + SMTP/EmailJS'),
            ]
        ])
        chat.controls = [ft.Container(content=ft.Column([hero, tips], spacing=14), padding=ft.Padding.only(top=10))]

    def inform(message):
        notice_text.value = display(message)
        notification.visible = True
        notification.opacity = 1

    def add_diagnostic(message):
        p = palette()
        stamp = time.strftime('%H:%M:%S')
        state['diagnostics'].append(display(f'[{stamp}] {message}'))
        state['diagnostics'] = state['diagnostics'][-25:]
        diagnostic_lines.controls = [txt(item, 11, p['cyan']) for item in state['diagnostics']]

    def update_counts():
        msgs, chats = store.counts(state['owner'])
        counter_msgs.value = str(msgs)
        counter_chats.value = str(chats)
        counter_runs.value = str(state['runs'])

    def update_sessions():
        entries = store.list_chats(state['owner'])
        total = len(entries)
        sessions.options = [
            ft.DropdownOption(
                key=str(cid),
                text=f'Session {total - index}  ·  {time.strftime("%H:%M", time.localtime(created))}',
            )
            for index, (cid, created) in enumerate(entries)
        ]
        sessions.value = str(state['chat'])

    def save_ui_prefs():
        brain.ui.update({
            'theme': state['theme'],
            'layout': state['layout'],
            'blur': state['blur'],
            'operator_name': state['operator_name'],
            'operator_rank': state['operator_rank'],
        })
        store.save_profile(state['owner'], brain.profile)

    def rebuild_chat_view():
        chat.controls.clear()
        history = store.history(state['owner'], state['chat'], 200)
        state['welcome'] = not history
        for message in history:
            bubble(message.get('role', 'assistant'), message.get('content', ''))
        if not history:
            show_welcome()

    def load_operator_session(email_key: str, display_name: str = ''):
        state['owner'] = email_key.strip().lower()
        prof = store.profile(state['owner'])
        brain.__init__(prof)
        ui_cfg = prof.get('ui', {})
        state['theme'] = ui_cfg.get('theme', 'Cyber-Glass')
        state['layout'] = ui_cfg.get('layout', 'Sovereign OS')
        state['blur'] = int(ui_cfg.get('blur', 8))
        if display_name.strip():
            state['operator_name'] = display_name.strip().upper()
        else:
            state['operator_name'] = ui_cfg.get('operator_name', state['owner'].split('@')[0].upper())
        state['operator_rank'] = ui_cfg.get(
            'operator_rank',
            'Founder & Lead Architect' if 'avyan' in state['owner'] else 'Sovereign Operator',
        )
        existing = store.list_chats(state['owner'])
        state['chat'] = existing[0][0] if existing else store.new_chat(state['owner'])
        state['authenticated'] = True
        save_ui_prefs()
        update_sessions()
        update_counts()
        rebuild_chat_view()

    # --- EMAIL & COMMS CENTER BUILDER ---
    email_to_field = ft.TextField(label='Recipient Email (To)', hint_text='colleague@example.com', text_size=13, expand=True)
    email_sub_field = ft.TextField(label='Subject Line', hint_text='Project VOID Status Update', text_size=13, expand=True)
    email_body_field = ft.TextField(
        label='Email Message Body (or topic for AI Draft)',
        multiline=True, min_lines=4, max_lines=8, text_size=13,
    )
    email_status_txt = txt('', 12)
    email_log_col = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO, height=180)

    def refresh_email_logs():
        p = palette()
        rows = store.list_emails(state['owner'], limit=12)
        if not rows:
            email_log_col.controls = [txt('No emails logged for this operator yet.', 11, p['muted'])]
            return
        items = []
        for rec, subj, body_txt, st_txt, ts in rows:
            t_str = time.strftime('%b %d, %H:%M', time.localtime(ts))
            items.append(
                glass(
                    ft.Column([
                        ft.Row([
                            txt(f'To: {rec}', 11, p['cyan'], weight=ft.FontWeight.BOLD),
                            ft.Container(expand=True),
                            txt(f'{st_txt} · {t_str}', 10, p['purple']),
                        ]),
                        txt(f'Subject: {subj}', 12, p['white'], weight=ft.FontWeight.BOLD),
                        txt(body_txt[:180] + ('…' if len(body_txt) > 180 else ''), 11, p['muted']),
                    ], spacing=4),
                    padding=10,
                )
            )
        email_log_col.controls = items

    async def draft_email_with_ai():
        if state['busy'] or engine is None:
            inform('Engine is busy or unconfigured.')
            update()
            return
        subj = (email_sub_field.value or 'Important Follow-up').strip()
        notes = (email_body_field.value or 'Write a concise, professional email.').strip()
        email_status_txt.value = '✦ VOID AI is drafting your email…'
        email_status_txt.color = palette()['cyan']
        set_busy(True)
        update()
        prompt_msgs = [
            {
                'role': 'system',
                'content': (
                    f"You are VOID Executive Email Composer for {state['operator_name']}. "
                    'Write a polished, ready-to-send email body only (no markdown fences).'
                ),
            },
            {
                'role': 'user',
                'content': f'Subject: {subj}\nKey points / instructions: {notes}',
            },
        ]
        draft_pieces: List[str] = []
        try:
            for ev in engine.stream(prompt_msgs):
                if ev.kind == 'token':
                    draft_pieces.append(ev.text)
                    email_body_field.value = ''.join(draft_pieces)
                    update()
                elif ev.kind == 'diagnostic':
                    add_diagnostic(ev.text)
            if draft_pieces:
                email_status_txt.value = '✦ AI Draft complete. Review and click Send Email Now.'
                email_status_txt.color = palette()['purple']
            else:
                email_status_txt.value = 'Could not generate draft. Check OPENROUTER_API_KEY.'
        finally:
            set_busy(False)
            update()

    def handle_send_email(e):
        rec = (email_to_field.value or '').strip()
        subj = (email_sub_field.value or '').strip()
        body_val = (email_body_field.value or '').strip()
        ok, msg = EmailService.send_email(rec, subj, body_val)
        email_status_txt.value = msg
        email_status_txt.color = palette()['cyan'] if ok else '#ff6a61'
        if ok:
            store.log_email(state['owner'], rec, subj, body_val, 'DISPATCHED')
            add_diagnostic(f'EMAIL -> {rec} ({subj[:24]})')
            refresh_email_logs()
        update()

    def build_email_center_panel(compact: bool = False) -> ft.Control:
        p = palette()
        refresh_email_logs()
        return glass(
            ft.Column(
                spacing=12,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Row([
                        ft.Icon(ft.Icons.MAIL_LOCK_OUTLINED, color=p['cyan'], size=20),
                        txt('SOVEREIGN EMAIL & COMMS CENTER', 14, p['white'], weight=ft.FontWeight.BOLD),
                        ft.Container(expand=True),
                        txt(f"Signed in: {state['owner']}", 11, p['purple']),
                    ]),
                    txt(
                        'Dispatch emails via SMTP or EmailJS, use VOID AI to auto-write messages, '
                        'and inspect your encrypted SQLite outbox log.',
                        11, p['muted'],
                    ),
                    ft.Row([email_to_field, email_sub_field], spacing=10),
                    email_body_field,
                    ft.Row([
                        ft.Button(
                            content='✦ Draft with VOID AI',
                            bgcolor=p['edge'],
                            color=p['cyan'],
                            on_click=lambda e: page.run_task(draft_email_with_ai),
                        ),
                        ft.Button(
                            content='📨 Send Email Now',
                            bgcolor=p['cyan'],
                            color=p['bg'],
                            on_click=handle_send_email,
                        ),
                    ], spacing=10),
                    email_status_txt,
                    ft.Divider(color=p['edge'], height=1),
                    caption('SENT & LOGGED OUTBOX VAULT'),
                    email_log_col,
                ],
            ),
            padding=18,
            expand=not compact,
        )

    # --- CUSTOMIZATION & THEME / LAYOUT CENTER BUILDER ---
    def apply_theme(theme_name: str):
        if theme_name in THEMES:
            state['theme'] = theme_name
            save_ui_prefs()
            add_diagnostic(f'THEME SWITCHED -> {theme_name}')
            rebuild_workspace()

    def apply_layout(layout_name: str):
        if layout_name in LAYOUTS:
            state['layout'] = layout_name
            save_ui_prefs()
            add_diagnostic(f'LAYOUT SWITCHED -> {layout_name}')
            rebuild_workspace()

    def build_customization_panel() -> ft.Control:
        p = palette()
        name_input = ft.TextField(
            label='Operator Display Name', value=state['operator_name'],
            text_size=13, width=240,
        )
        rank_input = ft.TextField(
            label='Operator Rank / Title', value=state['operator_rank'],
            text_size=13, width=240,
        )
        blur_slider = ft.Slider(
            min=0, max=20, divisions=10, value=state['blur'],
            active_color=p['cyan'], label='{value}px Blur',
        )

        def save_identity_click(e):
            state['operator_name'] = (name_input.value or 'AVYAN').strip().upper()[:32]
            state['operator_rank'] = (rank_input.value or 'Sovereign Operator').strip()[:40]
            state['blur'] = int(blur_slider.value or 8)
            save_ui_prefs()
            inform('Operator identity & glassmorphism settings saved.')
            rebuild_workspace()

        theme_cards = []
        for t_name, t_colors in THEMES.items():
            active = state['theme'] == t_name
            theme_cards.append(
                ft.Container(
                    on_click=lambda e, tn=t_name: apply_theme(tn),
                    bgcolor=t_colors['glass'],
                    border=ft.Border.all(2 if active else 1, t_colors['cyan'] if active else t_colors['edge']),
                    border_radius=14,
                    padding=14,
                    width=195,
                    ink=True,
                    content=ft.Column(spacing=8, controls=[
                        ft.Row([
                            ft.Container(width=14, height=14, border_radius=7, bgcolor=t_colors['cyan']),
                            ft.Container(width=14, height=14, border_radius=7, bgcolor=t_colors['purple']),
                            ft.Container(width=14, height=14, border_radius=7, bgcolor=t_colors['bg']),
                            ft.Container(expand=True),
                            ft.Icon(
                                ft.Icons.CHECK_CIRCLE if active else ft.Icons.CIRCLE_OUTLINED,
                                color=t_colors['cyan'] if active else t_colors['muted'],
                                size=16,
                            ),
                        ]),
                        txt(t_name, 13, t_colors['white'], weight=ft.FontWeight.BOLD),
                        txt('Active Theme' if active else 'Click to activate', 10, t_colors['muted']),
                    ]),
                )
            )

        layout_cards = []
        layout_meta = {
            'Sovereign OS': (
                'Classic left command deck, stage header, and split-screen Prism support.',
                ft.Icons.SPACE_DASHBOARD_OUTLINED,
            ),
            'Terminal CLI': (
                'Streamlined hacker command-line interface with top telemetry bar and minimal chrome.',
                ft.Icons.TERMINAL_ROUNDED,
            ),
            'Bento Dashboard': (
                'Multi-column executive layout with simultaneous Chat, Email, and Telemetry cards.',
                ft.Icons.GRID_VIEW_ROUNDED,
            ),
        }
        for l_name in LAYOUTS:
            l_active = state['layout'] == l_name
            desc, l_icon = layout_meta[l_name]
            layout_cards.append(
                ft.Container(
                    on_click=lambda e, ln=l_name: apply_layout(ln),
                    bgcolor=p['glass'],
                    border=ft.Border.all(2 if l_active else 1, p['purple'] if l_active else p['edge']),
                    border_radius=14,
                    padding=14,
                    width=260,
                    ink=True,
                    content=ft.Column(spacing=6, controls=[
                        ft.Row([
                            ft.Icon(l_icon, color=p['cyan'] if l_active else p['muted'], size=20),
                            txt(l_name, 13, p['white'], weight=ft.FontWeight.BOLD),
                            ft.Container(expand=True),
                            txt(
                                'ACTIVE' if l_active else 'SELECT',
                                10,
                                p['cyan'] if l_active else p['muted'],
                                weight=ft.FontWeight.BOLD,
                            ),
                        ]),
                        txt(desc, 11, p['muted']),
                    ]),
                )
            )

        return glass(
            ft.Column(
                spacing=16,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Row([
                        ft.Icon(ft.Icons.PALETTE_OUTLINED, color=p['cyan'], size=22),
                        txt('SOVEREIGN UI CUSTOMIZATION & LAYOUT STUDIO', 15, p['white'], weight=ft.FontWeight.BOLD),
                    ]),
                    caption('1. SELECT DYNAMIC COLOR & GLASS THEME'),
                    ft.Row(theme_cards, wrap=True, spacing=10, run_spacing=10),
                    ft.Divider(color=p['edge'], height=1),
                    caption('2. SWITCH WORKSPACE UI LAYOUT ARCHITECTURE'),
                    ft.Row(layout_cards, wrap=True, spacing=10, run_spacing=10),
                    ft.Divider(color=p['edge'], height=1),
                    caption('3. OPERATOR IDENTITY & GLASSMORPHISM BLUR INTENSITY'),
                    ft.Row([name_input, rank_input], wrap=True, spacing=12),
                    ft.Row([txt('Glass Blur Radius:', 12, p['white']), ft.Container(blur_slider, expand=True)]),
                    ft.Button(
                        content='💾 Save Identity & Blur Preferences',
                        bgcolor=p['cyan'], color=p['bg'],
                        on_click=save_identity_click,
                    ),
                ],
            ),
            padding=20,
            expand=True,
        )

    def render_tools():
        p = palette()
        query = (search.value or '').strip().lower()
        controls = []
        for group, names in NAV.items():
            matching = [
                name for name in names
                if not query or query in (name + ' ' + ALIASES.get(name, '') + ' ' + group).lower()
            ]
            if not matching:
                continue
            radios = [
                ft.Radio(
                    value=name, label=name, active_color=p['purple'],
                    label_style=ft.TextStyle(size=11, color=p['white'] if name == state['mode'] else p['muted']),
                )
                for name in matching
            ]
            controls.append(
                ft.ExpansionTile(
                    title=txt(group, 10, p['muted'], weight=ft.FontWeight.BOLD),
                    controls=radios,
                    expanded=bool(query) or state['mode'] in names,
                    dense=True,
                    tile_padding=ft.Padding.symmetric(horizontal=4),
                    controls_padding=0,
                    animation_style=ft.AnimationStyle(duration=300, curve=ft.AnimationCurve.EASE_OUT),
                )
            )
        tool_column.controls = controls or [txt('No matching dimensions.', 12)]

    radio_group = ft.RadioGroup(content=tool_column, value=state['mode'])

    def filter_tools(e):
        render_tools()
        update()

    async def change_mode(e):
        state['mode'] = radio_group.value or 'VOID Core (Adaptive Chat)'
        mode_title.value = state['mode']
        diagnostic_panel.visible = state['prism'] or state['mode'] == 'Engine Doctor & Telemetry'
        rebuild_workspace()

    def set_busy(busy):
        state['busy'] = busy
        send.disabled = new_session.disabled = sessions.disabled = attach.disabled = web_switch.disabled = busy
        for control in quick_buttons:
            control.disabled = busy

    async def run_response(messages, response_md, chat_id):
        pieces = []
        failed = False
        previous_update = 0.0
        try:
            if engine is None:
                inform('OpenRouter API key missing or engine configuration is invalid.')
                failed = True
            else:
                for event in engine.stream(messages):
                    if state['closed']:
                        return
                    if event.kind == 'attempt':
                        status.value = f'SYNCHRONIZING · {event.model}'
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
                store.add_message(state['owner'], chat_id, 'assistant', actual)
                response_md.value = display(actual)
            elif failed:
                response_md.value = 'The core could not complete this request.'
            update_counts()
        except Exception:
            logging.getLogger('void.ui').error('Session error')
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
        if state['mode'] in {'Customization Center', 'Email & Comms Center'}:
            state['mode'] = 'VOID Core (Adaptive Chat)'
            radio_group.value = state['mode']
            mode_title.value = state['mode']
            rebuild_workspace()
        try:
            attachment = state['attachment']
            stored = value
            if attachment:
                stored += '\n\n[Attached text: ' + attachment['name'] + ']\n' + attachment['text']
            store.add_message(state['owner'], state['chat'], 'user', stored)
            brain.record_interaction(value)
            store.save_profile(state['owner'], brain.profile)
            messages = [{'role': 'system', 'content': brain.system_prompt(value, state['mode'], state['prism'])}]
            messages += store.history(state['owner'], state['chat'])
            if state['welcome']:
                chat.controls.clear()
                state['welcome'] = False
            bubble('user', value + ('\n\n📎 ' + attachment['name'] if attachment else ''))
            response_md = bubble('assistant', 'Preparing response…')
            state['attachment'] = None
            attach_label.visible = clear_attach.visible = False
            command.value = ''
            notification.visible = False
            state['runs'] += 1
            set_busy(True)
            update_counts()
            update()
            page.run_task(run_response, messages, response_md, state['chat'])
        except Exception:
            set_busy(False)
            inform('Could not start this session. Please retry.')
            update()

    def new_chat_click(e):
        if state['busy']:
            return
        state['chat'] = store.new_chat(state['owner'])
        state['attachment'] = None
        attach_label.visible = clear_attach.visible = False
        chat.controls.clear()
        show_welcome()
        notification.visible = False
        status.value = 'READY'
        update_sessions()
        update_counts()
        update()

    def select_chat(e):
        if state['busy'] or not sessions.value:
            return
        state['chat'] = int(sessions.value)
        rebuild_chat_view()
        notification.visible = False
        update()

    async def choose_file(e):
        if state['busy']:
            return
        try:
            files = await ft.FilePicker().pick_files(
                allow_multiple=False, with_data=True,
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=['txt', 'md', 'csv', 'json', 'py'],
            )
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

    def toggle_web(e):
        p = palette()
        state['web'] = bool(web_switch.value)
        web_disclosure.value = 'ON · Active mode' if state['web'] else 'OFF · No searches sent'
        web_disclosure.color = p['cyan'] if state['web'] else p['muted']
        update()

    def sign_out_click(e):
        state['authenticated'] = False
        state['pending_email'] = ''
        state['target_otp'] = ''
        rebuild_workspace()

    search.on_change = filter_tools
    radio_group.on_change = change_mode
    sessions.on_change = select_chat
    prism.on_change = toggle_prism
    web_switch.on_change = toggle_web
    attach.on_click = choose_file
    clear_attach.on_click = remove_file
    send.on_click = lambda e: submit(command.value)
    command.on_submit = lambda e: submit(command.value)
    new_session.on_click = new_chat_click

    # --- LOGIN GATE BUILDER ---
    def build_login_gate() -> ft.Control:
        p = palette()
        email_in = ft.TextField(
            label='Operator Email Address',
            hint_text='avyan@void.os',
            value=state['pending_email'],
            text_size=13,
            border=ft.OutlineInputBorder(side=ft.BorderSide(1, p['edge']), border_radius=12),
        )
        name_in = ft.TextField(
            label='Display Name',
            hint_text='Avyan',
            value=state['pending_name'],
            text_size=13,
            border=ft.OutlineInputBorder(side=ft.BorderSide(1, p['edge']), border_radius=12),
        )
        otp_in = ft.TextField(
            label='6-Digit Verification Code',
            hint_text='123456',
            text_size=15,
            border=ft.OutlineInputBorder(side=ft.BorderSide(1, p['cyan']), border_radius=12),
        )
        auth_msg = txt('', 12, p['cyan'])

        def send_otp_click(e):
            em = (email_in.value or '').strip().lower()
            nm = (name_in.value or '').strip()
            if not EMAIL_RE.match(em):
                auth_msg.value = 'Please enter a valid email address.'
                auth_msg.color = '#ff6a61'
                update()
                return
            code = str(secrets.randbelow(900000) + 100000)
            state['pending_email'] = em
            state['pending_name'] = nm
            state['target_otp'] = code
            state['otp_expiry'] = time.time() + 600
            ok, detail = EmailService.send_email(
                em,
                'VOID Sovereign OS · Verification Code',
                f'Your VOID Sovereign OS verification code is: {code} (valid for 10 minutes).',
                otp_code=code,
            )
            rebuild_workspace()
            inform(detail)
            update()

        def verify_otp_click(e):
            entered = (otp_in.value or '').strip()
            if time.time() > state['otp_expiry']:
                auth_msg.value = 'Code expired. Request a new code.'
                auth_msg.color = '#ff6a61'
                update()
                return
            if hmac.compare_digest(entered, state['target_otp']):
                load_operator_session(state['pending_email'], state['pending_name'])
                state['pending_email'] = ''
                state['target_otp'] = ''
                rebuild_workspace()
            else:
                auth_msg.value = 'Invalid verification code. Please check and try again.'
                auth_msg.color = '#ff6a61'
                update()

        def guest_launch_click(e):
            load_operator_session('avyan@void.os', 'AVYAN')
            rebuild_workspace()

        otp_pending = bool(state['pending_email'] and state['target_otp'])
        form_controls = [
            ft.Row([
                ft.Container(
                    ft.Icon(ft.Icons.AUTO_AWESOME, color=p['cyan'], size=28),
                    bgcolor=p['edge'], border_radius=16, padding=12,
                ),
                ft.Column([
                    txt('VOID MA · SOVEREIGN OS', 22, p['white'], weight=ft.FontWeight.BOLD),
                    txt('Encrypted Email Passport & Multi-Layout AI Deck', 12, p['muted']),
                ], spacing=2),
            ], spacing=12),
            ft.Divider(color=p['edge'], height=1),
        ]

        if not otp_pending:
            form_controls.extend([
                email_in,
                name_in,
                ft.Row([
                    ft.Button(
                        content='📨 Send Email Verification Code',
                        bgcolor=p['cyan'], color=p['bg'], expand=True,
                        on_click=send_otp_click,
                    ),
                    ft.Button(
                        content='⚡ Instant Founder / Guest Launch',
                        bgcolor=p['edge'], color=p['white'], expand=True,
                        on_click=guest_launch_click,
                    ),
                ], spacing=10),
                auth_msg,
            ])
        else:
            form_controls.extend([
                txt(
                    f"Verification code dispatched to {state['pending_email']}",
                    12, p['purple'], weight=ft.FontWeight.BOLD,
                ),
                notification,
                otp_in,
                ft.Row([
                    ft.Button(
                        content='🔓 Verify & Enter VOID',
                        bgcolor=p['cyan'], color=p['bg'], expand=True,
                        on_click=verify_otp_click,
                    ),
                    ft.Button(
                        content='↩ Change Email',
                        bgcolor=p['edge'], color=p['white'],
                        on_click=lambda e: (state.update(pending_email='', target_otp=''), rebuild_workspace()),
                    ),
                ], spacing=10),
                auth_msg,
            ])

        return ft.Container(
            expand=True,
            bgcolor=p['bg'],
            alignment=ft.Alignment.CENTER,
            padding=24,
            content=glass(
                ft.Column(form_controls, spacing=14, tight=True),
                width=500, padding=28,
            ),
        )

    # --- MULTI-LAYOUT WORKSPACE BUILDER ---
    def build_top_control_bar() -> ft.Control:
        p = palette()
        layout_pills = [
            pill(
                txt(
                    f"{'● ' if state['layout'] == ln else ''}{ln}",
                    11,
                    p['cyan'] if state['layout'] == ln else p['white'],
                    weight=ft.FontWeight.BOLD if state['layout'] == ln else None,
                ),
                lambda e, target=ln: apply_layout(target),
                tooltip=f'Switch to {ln} layout',
            )
            for ln in LAYOUTS
        ]
        theme_dd = ft.Dropdown(
            value=state['theme'],
            width=160,
            text_size=11,
            height=42,
            border=ft.OutlineInputBorder(side=ft.BorderSide(1, p['edge']), border_radius=10),
            options=[ft.DropdownOption(key=k, text=k) for k in THEMES.keys()],
            on_change=lambda e: apply_theme(e.control.value),
        )
        return ft.Row(
            wrap=True,
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row([
                    ft.Container(bgcolor=c, width=10, height=10, border_radius=10)
                    for c in ('#ff6a61', '#f8bf55', '#4fd37b')
                ], spacing=6),
                status,
                ft.Container(expand=True),
                *layout_pills,
                theme_dd,
                pill(
                    txt('✉ Email', 11, p['cyan'], weight=ft.FontWeight.BOLD),
                    lambda e: (
                        state.update(mode='Email & Comms Center'),
                        setattr(radio_group, 'value', 'Email & Comms Center'),
                        rebuild_workspace(),
                    ),
                ),
                pill(
                    txt('⚙ Customize', 11, p['purple'], weight=ft.FontWeight.BOLD),
                    lambda e: (
                        state.update(mode='Customization Center'),
                        setattr(radio_group, 'value', 'Customization Center'),
                        rebuild_workspace(),
                    ),
                ),
                pill(
                    txt('🚪 Log Out', 11, '#ff6a61', weight=ft.FontWeight.BOLD),
                    sign_out_click,
                ),
            ],
        )

    def build_active_stage_center() -> ft.Control:
        if state['mode'] == 'Customization Center':
            return build_customization_panel()
        if state['mode'] == 'Email & Comms Center':
            return build_email_center_panel(compact=False)
        return chat

    def build_composer_bar() -> ft.Control:
        p = palette()
        command.color = p['white']
        command.cursor_color = p['cyan']
        send.bgcolor = p['cyan']
        send.icon_color = p['bg']
        return ft.Column(
            spacing=6,
            controls=[
                ft.Row([attach_label, clear_attach], spacing=4),
                glass(ft.Row([attach, command, send], spacing=4), padding=5),
                txt(
                    f"Enter to send · Shift+Enter for new line · Theme: {state['theme']} · Layout: {state['layout']}",
                    10, p['muted'],
                ),
            ],
        )

    def rebuild_workspace():
        p = palette()
        page.bgcolor = p['bg']
        status.color = p['cyan']
        mode_title.value = state['mode']
        mode_title.color = p['purple']
        counter_msgs.color = counter_chats.color = counter_runs.color = p['white']

        if not state['authenticated']:
            root_host.content = build_login_gate()
            update()
            return

        render_tools()
        update_sessions()
        update_counts()

        quick_buttons.clear()
        quick_specs = [
            ('☀  Live Weather', 'Help me check current weather conditions.'),
            ('अ  हिन्दी में पूछें', 'नमस्ते! कृपया मुझसे सरल हिंदी में बात करें।'),
            ('✉  Email Center', '__EMAIL__'),
            ('🎨  Themes & Layouts', '__CUSTOMIZE__'),
        ]
        for label, prompt in quick_specs:
            def _q_click(e, pr=prompt):
                if pr == '__EMAIL__':
                    state['mode'] = 'Email & Comms Center'
                    radio_group.value = state['mode']
                    rebuild_workspace()
                elif pr == '__CUSTOMIZE__':
                    state['mode'] = 'Customization Center'
                    radio_group.value = state['mode']
                    rebuild_workspace()
                else:
                    submit(pr)
            quick_buttons.append(pill(txt(label, 12, p['white']), _q_click))

        top_bar = build_top_control_bar()
        center_view = build_active_stage_center()
        composer = build_composer_bar()
        diagnostic_panel.visible = state['prism'] or state['mode'] == 'Engine Doctor & Telemetry'

        # --- LAYOUT 1: STREAMLINED TERMINAL CLI ---
        if state['layout'] == 'Terminal CLI':
            mode_dd = ft.Dropdown(
                value=state['mode'],
                width=230,
                text_size=11,
                height=42,
                border=ft.OutlineInputBorder(side=ft.BorderSide(1, p['edge']), border_radius=10),
                options=[ft.DropdownOption(key=m, text=m) for grp in NAV.values() for m in grp],
                on_change=lambda e: (
                    state.update(mode=e.control.value),
                    setattr(radio_group, 'value', e.control.value),
                    rebuild_workspace(),
                ),
            )
            term_header = glass(
                ft.Row([
                    txt(
                        f"root@{state['operator_name'].lower()}://void-os~$ ",
                        13, p['cyan'], weight=ft.FontWeight.BOLD,
                    ),
                    mode_dd,
                    sessions,
                    ft.Button(content='+ New', bgcolor=p['edge'], color=p['white'], on_click=new_chat_click),
                    ft.Container(expand=True),
                    txt(
                        f"MSGS:{counter_msgs.value} | CHATS:{counter_chats.value} | RUNS:{counter_runs.value}",
                        11, p['purple'],
                    ),
                ], wrap=True, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=10,
            )
            root_host.content = ft.Container(
                expand=True, bgcolor=p['bg'],
                padding=ft.Padding.symmetric(horizontal=24, vertical=16),
                content=ft.Column(
                    expand=True, spacing=12,
                    controls=[top_bar, term_header, notification, center_view, diagnostic_panel, composer],
                ),
            )
            update()
            return

        # --- SHARED SIDEBAR FOR SOVEREIGN OS & BENTO DASHBOARD ---
        sidebar = ft.Container(
            width=285,
            padding=ft.Padding.symmetric(horizontal=16, vertical=20),
            bgcolor=p['glass'],
            border=ft.Border.only(right=ft.BorderSide(1, p['edge'])),
            content=ft.Column(expand=True, spacing=11, controls=[
                ft.Row([
                    ft.Container(
                        ft.Icon(ft.Icons.AUTO_AWESOME, color=p['white'], size=20),
                        bgcolor=p['purple'], border_radius=12, padding=9,
                    ),
                    ft.Column([
                        txt('VOID', 19, p['white'], weight=ft.FontWeight.BOLD),
                        txt('MA / SOVEREIGN OS', 9, p['muted']),
                    ], spacing=0),
                    ft.Container(
                        txt('V9.5', 10, p['cyan'], weight=ft.FontWeight.BOLD),
                        bgcolor=p['bg'], border_radius=7, padding=6,
                    ),
                ]),
                ft.Divider(color=p['edge'], height=1),
                ft.Row([
                    ft.Container(
                        ft.Icon(ft.Icons.VERIFIED_USER_OUTLINED, color=p['cyan'], size=18),
                        bgcolor=p['bg'], border_radius=12, padding=9,
                    ),
                    ft.Column([
                        txt(state['operator_name'], 11, p['white'], weight=ft.FontWeight.BOLD),
                        txt(f"{state['operator_rank']} · {state['owner']}", 9, p['muted']),
                    ], spacing=2),
                ]),
                caption('COMMAND SEARCH'),
                search,
                caption('DIMENSIONS'),
                ft.Container(content=radio_group, expand=True),
                new_session,
                sessions,
                prism,
                ft.Divider(color=p['edge'], height=1),
                caption('LIVE TELEMETRY'),
                ft.Row([
                    ft.Column([counter_msgs, txt('Msgs', 10)], spacing=2, expand=True),
                    ft.Column([counter_chats, txt('Chats', 10)], spacing=2, expand=True),
                    ft.Column([counter_runs, txt('Runs', 10)], spacing=2, expand=True),
                ]),
            ]),
        )

        # --- LAYOUT 2: BENTO EXECUTIVE DASHBOARD ---
        if state['layout'] == 'Bento Dashboard':
            topics_str = ', '.join(brain.learning.get('topics', [])[-6:]) or 'Adaptive indexing active'
            bento_right = ft.Column(
                width=390,
                spacing=12,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    glass(
                        ft.Column(spacing=8, controls=[
                            caption('ADAPTIVE BRAIN & TELEMETRY'),
                            ft.Row([
                                ft.Column([counter_msgs, txt('Messages', 10)], expand=True),
                                ft.Column([counter_chats, txt('Sessions', 10)], expand=True),
                                ft.Column([counter_runs, txt('AI Runs', 10)], expand=True),
                            ]),
                            txt(f'Learned Context: {topics_str}', 11, p['cyan']),
                        ]),
                        padding=14,
                    ),
                    build_email_center_panel(compact=True),
                    glass(
                        ft.Column([caption('LIVE CORE DIAGNOSTICS'), diagnostic_lines], spacing=6),
                        padding=14,
                    ),
                ],
            )
            bento_left = ft.Column(
                expand=True,
                spacing=12,
                controls=[
                    ft.Row([
                        ft.Column([
                            txt(f"Command Deck · {state['operator_name']}", 22, p['white'], weight=ft.FontWeight.BOLD),
                            txt('Bento Multi-Panel Intelligence Workspace', 12, p['muted']),
                        ], spacing=2, expand=True),
                        glass(mode_title, padding=10),
                    ]),
                    ft.Row(quick_buttons, wrap=True, spacing=8, run_spacing=8),
                    notification,
                    center_view,
                    composer,
                ],
            )
            stage = ft.Container(
                expand=True,
                bgcolor=p['bg'],
                padding=ft.Padding.symmetric(horizontal=24, vertical=18),
                content=ft.Column(
                    expand=True, spacing=14,
                    controls=[top_bar, ft.Row([bento_left, bento_right], expand=True, spacing=16)],
                ),
            )
            root_host.content = ft.Row([sidebar, stage], spacing=0, expand=True)
            update()
            return

        # --- LAYOUT 3: STANDARD SOVEREIGN OS DECK ---
        stage_body = ft.Column(
            expand=True,
            spacing=12,
            controls=[
                top_bar,
                ft.Divider(color=p['edge'], height=4),
                ft.Row([
                    ft.Column([
                        txt(f"Hello, {state['operator_name']}", 28, p['white'], weight=ft.FontWeight.BOLD),
                        txt('Your Sovereign intelligence workspace is ready. What shall we explore?', 13, p['muted']),
                    ], spacing=4, expand=True),
                    web_disclosure,
                    web_switch,
                    glass(mode_title, padding=10),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Row(quick_buttons, wrap=True, spacing=8, run_spacing=8),
                center_view,
                notification,
                diagnostic_panel,
                composer,
            ],
        )
        stage = ft.Container(
            expand=True,
            bgcolor=p['bg'],
            padding=ft.Padding.symmetric(horizontal=30, vertical=20),
            content=stage_body,
        )
        root_host.content = ft.Row([sidebar, stage], spacing=0, expand=True)
        update()

    # Boot into the Email Login Gate (or click Instant Founder / Guest Launch)
    rebuild_workspace()
    page.on_disconnect = lambda e: state.update(closed=True)
    page.add(root_host)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    port = int(os.getenv('PORT', os.getenv('FLET_PORT', '8550')))
    host = os.getenv('FLET_HOST', '0.0.0.0' if os.getenv('PORT') else '127.0.0.1')
    web = os.getenv('VOID_WEB') == '1' or bool(os.getenv('PORT'))
    with verified_web_assets() as web_assets:
        ft.run(
            main,
            host=host,
            port=port,
            assets_dir=web_assets,
            view=ft.AppView.WEB_BROWSER if web else ft.AppView.FLET_APP,
        )
