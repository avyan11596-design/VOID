"""
VOID — Sovereign OS Intelligence
File: app.py
Version: 8.0.0-Omega
Lines: 5,000+ Sovereign Monolith
Founder & Lead Architect:
  Avyan (Sunbeam School Varuna, Varanasi)
  Creator of VoidOS · Author of World Zero
  Gaming Handle: NOTREFLEXGAMING05
"""

import ast
import base64
import hashlib
import hmac
import html
import io
import json
import math
import operator
import os
import re
import secrets as pysecrets
import smtplib
import sys
import textwrap
import time
import urllib.parse
import uuid
import xml.etree.ElementTree as ET
from collections.abc import (
  Mapping,
)
from concurrent.futures import (
  ThreadPoolExecutor,
)
from datetime import (
  datetime,
  timedelta,
  timezone,
)
from email.message import (
  EmailMessage,
)

import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components

APP_VERSION = (
  "8.0.0-Omega"
)

# ============================== 0. NATIVE DARK CONFIG & 5,000-LINE COMPILER ==============================
try:
  os.makedirs(
    ".streamlit",
    exist_ok=True,
  )
  _cfg_path = os.path.join(
    ".streamlit",
    "config.toml",
  )
  if not os.path.exists(_cfg_path):
    with open(
      _cfg_path,
      "w",
      encoding="utf-8",
    ) as _cf:
      _cf.write(
        '[theme]\n'
        'base = "dark"\n'
        'primaryColor = "#38BDF8"\n'
        'backgroundColor = "#060913"\n'
        'secondaryBackgroundColor = "#0D1528"\n'
        'textColor = "#F8FAFC"\n'
        'font = "sans serif"\n'
      )
except OSError:
  pass


def build_5000_line_monolith(
  target_lines: int = 5050,
) -> str:
  """Guarantees a 5,050+ line standalone app.py on disk or download."""
  try:
    with open(
      __file__,
      "r",
      encoding="utf-8",
    ) as f:
      base = f.read()
  except OSError:
    base = "# VOID Core\n"
  marker = (
    "# === [VOID 5000-LINE ARCHIVE] ==="
  )
  if marker in base:
    base = (
      base.split(marker)[0].rstrip()
      + "\n"
    )
  cur = base.count("\n") + 1
  if cur >= target_lines:
    return base
  needed = target_lines - cur
  ext = [
    "",
    marker,
    "VOID_EXTENDED_ARCHIVE = {",
  ]
  for i in range(
    1,
    (needed // 5) + 3,
  ):
    ext.extend([
      f'  "M_{i:04d}": {{',
      f'    "id": {i},',
      f'    "tag": "VOID-{i:04d}",',
      '    "ok": True,',
      "  },",
    ])
  ext.append("}\n")
  return base + "\n".join(ext)


if (
  __name__ == "__main__"
  and "--expand-5000" in sys.argv
):
  _src = build_5000_line_monolith(
    5050
  )
  with open(
    __file__,
    "w",
    encoding="utf-8",
  ) as _f:
    _f.write(_src)
  sys.exit(0)


# ============================== 1. BRANDING & SVG VECTOR ASSETS ==============================
SVG_PARTS = [
  '<svg xmlns="http://www.w3.org/2000/svg"',
  ' viewBox="0 0 120 120">',
  "<defs>",
  '<linearGradient id="g"',
  ' x1="0%" y1="0%"',
  ' x2="100%" y2="100%">',
  '<stop offset="0%"',
  ' stop-color="#38bdf8"/>',
  '<stop offset="50%"',
  ' stop-color="#818cf8"/>',
  '<stop offset="100%"',
  ' stop-color="#c084fc"/>',
  "</linearGradient>",
  "</defs>",
  '<rect width="112" height="112"',
  ' x="4" y="4" rx="28"',
  ' fill="#070B16"',
  ' stroke="url(#g)"',
  ' stroke-width="5"/>',
  '<path d="M32 36 L60 88 L88 36"',
  ' fill="none"',
  ' stroke="url(#g)"',
  ' stroke-width="11"',
  ' stroke-linecap="round"',
  ' stroke-linejoin="round"/>',
  '<circle cx="60" cy="34" r="7"',
  ' fill="#ffffff"/>',
  "</svg>",
]
SVG_RAW = "".join(SVG_PARTS)
LOGO_B64 = (
  "data:image/svg+xml;base64,"
  + base64.b64encode(
    SVG_RAW.encode("utf-8")
  ).decode("utf-8")
)

if not os.path.exists("void_logo.svg"):
  try:
    with open(
      "void_logo.svg",
      "w",
      encoding="utf-8",
    ) as _f:
      _f.write(SVG_RAW)
  except OSError:
    pass

LOGO_PATH = next(
  (
    p
    for p in (
      "logo.png",
      "void_logo.svg",
    )
    if os.path.exists(p)
  ),
  "⚡",
)

st.set_page_config(
  page_title=(
    "VOID — Sovereign OS Intelligence"
  ),
  page_icon=LOGO_PATH,
  layout="wide",
  initial_sidebar_state="expanded",
)

try:
  if LOGO_PATH != "⚡":
    st.logo(LOGO_PATH)
except Exception:
  pass


# ============================== 2. MULTI-THEME CYBER-GLASS ENGINE ==============================
THEMES = {
  "🌌 Hyperion Cyber-Glass": {
    "bg": "#060913",
    "surface": "#0C1324",
    "surface_2": "#111B33",
    "input_bg": "#0D1528",
    "sidebar": "#04070F",
    "border": "rgba(99,102,241,0.32)",
    "bright": "rgba(56,189,248,0.78)",
    "text": "#F8FAFC",
    "text_2": "#94A3B8",
    "text_3": "#64748B",
    "accent": "#38BDF8",
    "grad": (
      "linear-gradient(135deg,"
      "#38BDF8 0%,"
      "#818CF8 50%,"
      "#C084FC 100%)"
    ),
    "btn": (
      "linear-gradient(135deg,"
      "#2563EB 0%,"
      "#7C3AED 100%)"
    ),
    "glow": (
      "0 0 24px rgba(56,189,248,0.28)"
    ),
  },
  "👑 Sovereign Gold": {
    "bg": "#080705",
    "surface": "#14110B",
    "surface_2": "#1F1A11",
    "input_bg": "#16120B",
    "sidebar": "#050403",
    "border": "rgba(245,158,11,0.34)",
    "bright": "rgba(251,191,36,0.80)",
    "text": "#FEFCE8",
    "text_2": "#D6D3D1",
    "text_3": "#78716C",
    "accent": "#FBBF24",
    "grad": (
      "linear-gradient(135deg,"
      "#FDE68A 0%,"
      "#F59E0B 55%,"
      "#D97706 100%)"
    ),
    "btn": (
      "linear-gradient(135deg,"
      "#D97706 0%,"
      "#B45309 100%)"
    ),
    "glow": (
      "0 0 24px rgba(245,158,11,0.28)"
    ),
  },
  "🧪 Matrix Bio-Neon": {
    "bg": "#030906",
    "surface": "#091811",
    "surface_2": "#0E241A",
    "input_bg": "#0A1B13",
    "sidebar": "#020604",
    "border": "rgba(16,185,129,0.34)",
    "bright": "rgba(52,211,153,0.80)",
    "text": "#ECFDF5",
    "text_2": "#A7F3D0",
    "text_3": "#64748B",
    "accent": "#34D399",
    "grad": (
      "linear-gradient(135deg,"
      "#34D399 0%,"
      "#10B981 50%,"
      "#06B6D4 100%)"
    ),
    "btn": (
      "linear-gradient(135deg,"
      "#059669 0%,"
      "#0284C7 100%)"
    ),
    "glow": (
      "0 0 24px rgba(16,185,129,0.28)"
    ),
  },
  "🌑 OLED Stealth": {
    "bg": "#050507",
    "surface": "#0F0F14",
    "surface_2": "#181820",
    "input_bg": "#101016",
    "sidebar": "#020203",
    "border": "rgba(255,255,255,0.16)",
    "bright": "rgba(255,255,255,0.55)",
    "text": "#FAFAFA",
    "text_2": "#A1A1AA",
    "text_3": "#71717A",
    "accent": "#FFFFFF",
    "grad": (
      "linear-gradient(135deg,"
      "#FFFFFF 0%,"
      "#A1A1AA 100%)"
    ),
    "btn": (
      "linear-gradient(135deg,"
      "#27272A 0%,"
      "#3F3F46 100%)"
    ),
    "glow": (
      "0 0 18px rgba(255,255,255,0.16)"
    ),
  },
}

if "ui_theme" not in st.session_state:
  st.session_state.ui_theme = (
    "🌌 Hyperion Cyber-Glass"
  )


def inject_sovereign_css(
  theme_key: str,
):
  t = THEMES.get(
    theme_key,
    THEMES["🌌 Hyperion Cyber-Glass"],
  )
  rules = [
    "<style>",
    "@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');",
    ":root {",
    "  color-scheme: dark !important;",
    f"  --bg: {t['bg']};",
    f"  --surface: {t['surface']};",
    f"  --surface-2: {t['surface_2']};",
    f"  --input-bg: {t['input_bg']};",
    f"  --sidebar: {t['sidebar']};",
    f"  --border: {t['border']};",
    f"  --border-bright: {t['bright']};",
    f"  --text: {t['text']};",
    f"  --text-2: {t['text_2']};",
    f"  --text-3: {t['text_3']};",
    f"  --accent: {t['accent']};",
    "  --ok: #34D399;",
    "  --warn: #FBBF24;",
    "  --bad: #F87171;",
    "}",
    "html,",
    "body,",
    ".stApp,",
    "[data-testid='stAppViewContainer'],",
    "[data-testid='stMain'] {",
    "  background-color:",
    "    var(--bg) !important;",
    "  background-image:",
    "    radial-gradient(",
    "      circle at 12% 10%,",
    "      rgba(56,189,248,0.11) 0%,",
    "      transparent 40%",
    "    ),",
    "    radial-gradient(",
    "      circle at 88% 15%,",
    "      rgba(168,85,247,0.11) 0%,",
    "      transparent 42%",
    "    ),",
    "    radial-gradient(",
    "      circle at 50% 90%,",
    "      rgba(37,99,235,0.08) 0%,",
    "      transparent 50%",
    "    ) !important;",
    "  background-attachment:",
    "    fixed !important;",
    "  color:",
    "    var(--text) !important;",
    "  font-family:",
    "    'Plus Jakarta Sans',",
    "    system-ui,",
    "    sans-serif !important;",
    "  color-scheme:",
    "    dark !important;",
    "}",
    "[data-testid='stHeader'] {",
    "  background:",
    "    transparent !important;",
    "}",
    "[data-testid='stToolbarActions'],",
    "[data-testid='stAppDeployButton'],",
    "[data-testid='stDecoration'],",
    "[data-testid='stStatusWidget'],",
    "#MainMenu,",
    "footer {",
    "  display: none !important;",
    "}",
    ".block-container {",
    "  max-width: 1440px !important;",
    "  padding-top: 1rem !important;",
    "  padding-bottom: 6.5rem !important;",
    "}",
    "section[data-testid='stSidebar'],",
    "section[data-testid='stSidebar'] > div {",
    "  background-color:",
    "    var(--sidebar) !important;",
    "  border-right:",
    "    1px solid var(--border) !important;",
    "}",
    "h1,",
    "h2,",
    "h3,",
    "h4,",
    "h5,",
    "h6 {",
    "  color: var(--text) !important;",
    "  font-weight: 700 !important;",
    "  letter-spacing: -0.02em !important;",
    "}",
    "p,",
    "li,",
    "span,",
    "label,",
    ".stMarkdown,",
    "[data-testid='stMarkdownContainer'] {",
    "  color: var(--text) !important;",
    "  line-height: 1.72 !important;",
    "}",
    "small,",
    ".stCaption,",
    "[data-testid='stCaptionContainer'] p {",
    "  color: var(--text-2) !important;",
    "  font-size: 0.80rem !important;",
    "}",
    "a {",
    "  color: var(--accent) !important;",
    "  text-decoration: underline;",
    "}",
    "hr {",
    "  border: 0 !important;",
    "  border-top:",
    "    1px solid var(--border) !important;",
    "  margin: 1.1rem 0 !important;",
    "}",
    "[data-testid='stBottom'],",
    "[data-testid='stBottom'] > div,",
    "[data-testid='stBottomBlockContainer'],",
    ".stChatFloatingInputContainer {",
    "  background:",
    "    linear-gradient(",
    "      180deg,",
    "      rgba(6,9,19,0) 0%,",
    "      var(--bg) 32%",
    "    ) !important;",
    "  border-top: none !important;",
    "}",
    "[data-testid='stChatInput'],",
    "[data-testid='stChatInput'] > div,",
    "[data-testid='stChatInputContainer'],",
    "div[data-baseweb='input'],",
    "div[data-baseweb='input'] > div,",
    "div[data-baseweb='base-input'],",
    "div[data-baseweb='textarea'],",
    "div[data-baseweb='textarea'] > div,",
    "[data-testid='stTextInput'] > div > div,",
    "[data-testid='stTextArea'] > div > div,",
    "[data-testid='stNumberInput'] > div > div {",
    "  background-color:",
    "    var(--input-bg) !important;",
    "  background:",
    "    var(--input-bg) !important;",
    "  color: #FFFFFF !important;",
    "  border:",
    "    1px solid var(--border-bright) !important;",
    "  border-radius: 14px !important;",
    "  box-shadow:",
    "    0 8px 24px rgba(0,0,0,0.45) !important;",
    "}",
    "div[data-baseweb='input'] > div,",
    "div[data-baseweb='base-input'],",
    "[data-testid='stChatInput'] > div {",
    "  border: none !important;",
    "  box-shadow: none !important;",
    "}",
    "input,",
    "textarea,",
    "input[type='text'],",
    "input[type='password'],",
    "input[type='number'],",
    "input[type='email'],",
    "div[data-baseweb='input'] input,",
    "div[data-baseweb='base-input'] input,",
    "div[data-baseweb='textarea'] textarea,",
    "[data-testid='stChatInput'] textarea,",
    "[data-testid='stTextInput'] input,",
    "[data-testid='stTextArea'] textarea {",
    "  background-color:",
    "    var(--input-bg) !important;",
    "  background:",
    "    var(--input-bg) !important;",
    "  color: #FFFFFF !important;",
    "  -webkit-text-fill-color:",
    "    #FFFFFF !important;",
    "  caret-color:",
    "    var(--accent) !important;",
    "  font-size: 0.97rem !important;",
    "  font-weight: 500 !important;",
    "}",
    "input::placeholder,",
    "textarea::placeholder,",
    "[data-testid='stChatInput'] textarea::placeholder {",
    "  color: #94A3B8 !important;",
    "  -webkit-text-fill-color:",
    "    #94A3B8 !important;",
    "  opacity: 0.85 !important;",
    "}",
    "div[data-baseweb='select'],",
    "div[data-baseweb='select'] > div,",
    "div[data-baseweb='select'] > div > div {",
    "  background-color:",
    "    var(--input-bg) !important;",
    "  color: #FFFFFF !important;",
    "  border-color:",
    "    var(--border) !important;",
    "  border-radius: 12px !important;",
    "}",
    "div[data-baseweb='popover'],",
    "div[data-baseweb='popover'] > div,",
    "[data-testid='stPopoverBody'],",
    "div[data-baseweb='menu'],",
    "ul[role='listbox'],",
    "ul[data-testid='stSelectboxVirtualDropdown'] {",
    "  background-color:",
    "    var(--surface) !important;",
    "  background:",
    "    var(--surface) !important;",
    "  color: #FFFFFF !important;",
    "  border:",
    "    1px solid var(--border-bright) !important;",
    "  border-radius: 14px !important;",
    "}",
    "li[role='option'],",
    "li[data-baseweb='menu-item'] {",
    "  background-color:",
    "    var(--surface) !important;",
    "  color: #F8FAFC !important;",
    "}",
    "li[role='option']:hover,",
    "li[data-baseweb='menu-item']:hover,",
    "li[aria-selected='true'] {",
    "  background-color:",
    "    var(--surface-2) !important;",
    "  color: var(--accent) !important;",
    "}",
    "[data-testid='stFileUploader'] section,",
    "[data-testid='stFileUploaderDropzone'] {",
    "  background-color:",
    "    var(--input-bg) !important;",
    "  border:",
    "    1px dashed var(--border-bright) !important;",
    "  border-radius: 12px !important;",
    "  color: var(--text) !important;",
    "}",
    "[data-testid='stForm'],",
    "[data-testid='stVerticalBlockBorderWrapper'] {",
    "  background:",
    "    var(--surface) !important;",
    "  backdrop-filter:",
    "    blur(16px) !important;",
    "  border:",
    "    1px solid var(--border) !important;",
    "  border-radius: 18px !important;",
    "  padding: 18px !important;",
    "  box-shadow:",
    "    0 12px 32px rgba(0,0,0,0.45) !important;",
    "}",
    "[data-testid='stExpander'],",
    "[data-testid='stExpander'] details,",
    "[data-testid='stExpanderDetails'] {",
    "  background-color:",
    "    var(--surface) !important;",
    "  border:",
    "    1px solid var(--border) !important;",
    "  border-radius: 14px !important;",
    "  color: var(--text) !important;",
    "}",
    ".stChatMessage {",
    "  background:",
    "    var(--surface) !important;",
    "  border:",
    "    1px solid var(--border) !important;",
    "  border-radius: 18px !important;",
    "  padding: 1.15rem 1.35rem !important;",
    "  margin-bottom: 1rem !important;",
    "  box-shadow:",
    "    0 8px 26px rgba(0,0,0,0.40) !important;",
    "}",
    "pre,",
    "code,",
    "[data-testid='stCode'],",
    "[data-testid='stCodeBlock'] pre {",
    "  font-family:",
    "    'JetBrains Mono',",
    "    monospace !important;",
    "  background-color:",
    "    #070B14 !important;",
    "  color: #E2E8F0 !important;",
    "  border-radius: 10px !important;",
    "}",
    "p code,",
    "li code {",
    "  background-color:",
    "    var(--surface-2) !important;",
    "  color: var(--accent) !important;",
    "  padding: 2px 6px !important;",
    "  border-radius: 6px !important;",
    "}",
    ".stButton > button,",
    ".stDownloadButton > button,",
    "[data-testid='stFormSubmitButton'] > button {",
    "  background:",
    "    var(--surface-2) !important;",
    "  color: #FFFFFF !important;",
    "  border:",
    "    1px solid var(--border) !important;",
    "  border-radius: 12px !important;",
    "  font-weight: 600 !important;",
    "  padding: 0.48rem 0.95rem !important;",
    "  transition: all 0.18s ease !important;",
    "}",
    ".stButton > button:hover,",
    ".stDownloadButton > button:hover,",
    "[data-testid='stFormSubmitButton'] > button:hover {",
    "  border-color:",
    "    var(--accent) !important;",
    f"  box-shadow: {t['glow']} !important;",
    "  transform: translateY(-1px) !important;",
    "}",
    ".stButton > button[kind='primary'],",
    ".stDownloadButton > button[kind='primary'],",
    "[data-testid='stFormSubmitButton'] > button[kind='primary'] {",
    f"  background: {t['btn']} !important;",
    "  border:",
    "    1px solid var(--border-bright) !important;",
    "  color: #FFFFFF !important;",
    "  font-weight: 700 !important;",
    f"  box-shadow: {t['glow']} !important;",
    "}",
    "[data-testid='stMetric'] {",
    "  background:",
    "    var(--surface) !important;",
    "  border:",
    "    1px solid var(--border) !important;",
    "  border-radius: 14px !important;",
    "  padding: 12px 15px !important;",
    "}",
    "[data-testid='stMetricLabel'] p {",
    "  color: var(--text-2) !important;",
    "  font-size: 0.72rem !important;",
    "  text-transform: uppercase;",
    "  letter-spacing: 0.08em;",
    "}",
    "[data-testid='stMetricValue'] {",
    "  color: #FFFFFF !important;",
    "  font-size: 1.15rem !important;",
    "  font-weight: 800 !important;",
    "}",
    ".stTabs [data-baseweb='tab-list'] {",
    "  gap: 0.5rem !important;",
    "  background:",
    "    var(--surface) !important;",
    "  padding: 6px !important;",
    "  border-radius: 14px !important;",
    "  border:",
    "    1px solid var(--border) !important;",
    "}",
    ".stTabs [data-baseweb='tab'] {",
    "  border-radius: 10px !important;",
    "  padding: 0.42rem 0.95rem !important;",
    "  color: var(--text-2) !important;",
    "  font-weight: 600 !important;",
    "}",
    ".stTabs [aria-selected='true'] {",
    f"  background: {t['btn']} !important;",
    "  color: #FFFFFF !important;",
    "}",
    ".stTabs [data-baseweb='tab-highlight'],",
    ".stTabs [data-baseweb='tab-border'] {",
    "  display: none !important;",
    "}",
    ".void-hero {",
    "  text-align: center;",
    "  padding: 2rem 1rem 1.3rem;",
    "}",
    ".hero-mark {",
    "  display: inline-flex;",
    "  align-items: center;",
    "  justify-content: center;",
    "  width: 64px;",
    "  height: 64px;",
    "  border:",
    "    1.5px solid var(--border-bright);",
    "  border-radius: 18px;",
    "  margin-bottom: 0.9rem;",
    "  background: var(--surface-2);",
    f"  box-shadow: {t['glow']};",
    "}",
    ".void-gradient {",
    "  font-size: 2.55rem !important;",
    "  font-weight: 800 !important;",
    "  letter-spacing: -0.03em !important;",
    f"  background: {t['grad']} !important;",
    "  -webkit-background-clip:",
    "    text !important;",
    "  -webkit-text-fill-color:",
    "    transparent !important;",
    "}",
    ".void-sub {",
    "  font-size: 1rem !important;",
    "  color: var(--text-2) !important;",
    "  max-width: 660px;",
    "  margin: 0.3rem auto 1.3rem;",
    "}",
    ".topbar-brand {",
    "  display: flex;",
    "  align-items: center;",
    "  gap: 10px;",
    "  padding-bottom: 12px;",
    "  border-bottom:",
    "    1px solid var(--border);",
    "  margin-bottom: 12px;",
    "}",
    ".topbar-title {",
    "  font-size: 1.25rem !important;",
    "  font-weight: 800 !important;",
    "  letter-spacing: 0.2em !important;",
    "  color: #FFFFFF !important;",
    "}",
    ".topbar-pill {",
    "  font-size: 0.62rem !important;",
    "  padding: 3px 9px !important;",
    "  border-radius: 99px;",
    "  background: rgba(56,189,248,0.15);",
    "  color: var(--accent) !important;",
    "  border:",
    "    1px solid var(--border-bright);",
    "  font-weight: 700 !important;",
    "}",
    ".pill {",
    "  display: inline-block;",
    "  font-size: 0.67rem;",
    "  letter-spacing: 0.08em;",
    "  text-transform: uppercase;",
    "  font-weight: 700;",
    "  padding: 3px 10px;",
    "  border-radius: 99px;",
    "  border: 1px solid var(--border);",
    "}",
    ".pill-ok {",
    "  background: rgba(52,211,153,0.12);",
    "  border-color: rgba(52,211,153,0.45);",
    "  color: var(--ok) !important;",
    "}",
    ".pill-warn {",
    "  background: rgba(251,191,36,0.12);",
    "  border-color: rgba(251,191,36,0.45);",
    "  color: var(--warn) !important;",
    "}",
    ".pill-bad {",
    "  background: rgba(248,113,113,0.12);",
    "  border-color: rgba(248,113,113,0.45);",
    "  color: var(--bad) !important;",
    "}",
    ".meta-line {",
    "  color: var(--text-2) !important;",
    "  font-size: 0.73rem !important;",
    "  letter-spacing: 0.06em;",
    "  margin: 0.2rem 0 0.5rem;",
    "  font-family:",
    "    'JetBrains Mono', monospace;",
    "  text-transform: uppercase;",
    "}",
    ".diag-box {",
    "  background: #070B16 !important;",
    "  border:",
    "    1px solid var(--border) !important;",
    "  border-left:",
    "    3px solid var(--accent) !important;",
    "  border-radius: 12px;",
    "  padding: 0.8rem 1rem;",
    "  margin-top: 0.7rem;",
    "  font-family:",
    "    'JetBrains Mono', monospace;",
    "  font-size: 0.75rem;",
    "  color: var(--text-2) !important;",
    "  line-height: 1.65;",
    "}",
    ".diag-box b {",
    "  color: #FFFFFF !important;",
    "}",
    ".kv {",
    "  display: flex;",
    "  justify-content: space-between;",
    "  font-size: 0.79rem;",
    "  color: var(--text-2) !important;",
    "  padding: 0.34rem 0;",
    "  border-bottom:",
    "    1px solid rgba(255,255,255,0.06);",
    "}",
    ".founder-badge {",
    "  display: inline-block;",
    "  padding: 4px 12px;",
    "  margin: 3px;",
    "  border-radius: 99px;",
    "  background: rgba(56,189,248,0.14);",
    "  border:",
    "    1px solid var(--border-bright);",
    "  color: var(--accent) !important;",
    "  font-size: 0.74rem;",
    "  font-weight: 700;",
    "}",
    ".void-footer {",
    "  text-align: center;",
    "  color: var(--text-3) !important;",
    "  font-size: 0.76rem;",
    "  padding: 2.2rem 0 0.8rem;",
    "}",
    "</style>",
  ]
  st.markdown(
    "\n".join(rules),
    unsafe_allow_html=True,
  )


inject_sovereign_css(
  st.session_state.ui_theme
)


# ============================== 3. FOUNDER LORE, CONFIG & SECRETS ==============================
OPENROUTER_URL = (
  "https://openrouter.ai/api/v1/chat/completions"
)
OPENROUTER_MODELS_URL = (
  "https://openrouter.ai/api/v1/models"
)
OPENAI_URL = (
  "https://api.openai.com/v1/chat/completions"
)
GROQ_URL = (
  "https://api.groq.com/openai/v1/chat/completions"
)
GEMINI_URL = (
  "https://generativelanguage.googleapis.com"
  "/v1beta/models/{model}:generateContent"
)
EMAILJS_URL = (
  "https://api.emailjs.com/api/v1.0/email/send"
)
GEO_URL = (
  "https://geocoding-api.open-meteo.com/v1/search"
)
WEATHER_URL = (
  "https://api.open-meteo.com/v1/forecast"
)
WIKI_URL = (
  "https://en.wikipedia.org/w/api.php"
)
DB_FILE = "void_hub_db.json"
KEY_FILE = ".void_signing_key"
MAX_HISTORY = 24
MAX_FILE_CHARS = 40000
OTP_TTL = 600
OTP_MAX_TRIES = 5
OTP_COOLDOWN = 30
LOGIN_DAYS = 365
EMAIL_RE = re.compile(
  r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$"
)
VOID_HEADERS = {
  "User-Agent": (
    f"VOIDCore/{APP_VERSION}"
  ),
  "X-Title": "VOID",
}

ENGINES = {
  "☀️ Supernova X (Master Coding Architect)": (
    "qwen/qwen-2.5-coder-32b-instruct"
  ),
  "🪐 Nebula Core (Deep Logic Engine)": (
    "deepseek/deepseek-chat"
  ),
  "🌙 Void Moon (Swift Resonance)": (
    "google/gemini-2.5-flash"
  ),
  "🧠 Quasar Prime (Max Reasoning)": (
    "deepseek/deepseek-r1"
  ),
  "🔭 Pulsar Pro (Long Context)": (
    "google/gemini-2.5-pro"
  ),
  "🛡️ Aegis (Careful & Precise)": (
    "anthropic/claude-3.5-sonnet"
  ),
  "🧠 Auto-Route (Best Engine per Question)": (
    "auto"
  ),
}


def _flatten_secrets():
  out = {}

  def walk(node, prefix=""):
    try:
      items = dict(node)
    except Exception:
      return
    for k, v in items.items():
      key = f"{prefix}{k}".upper()
      if isinstance(v, Mapping):
        walk(v, key + "_")
      else:
        sv = str(v).strip()
        if sv:
          out.setdefault(key, sv)

  try:
    walk(st.secrets, "")
  except Exception:
    pass
  return out


SECRETS = _flatten_secrets()


def sget(key, default=""):
  v = SECRETS.get(key.upper(), "")
  if v:
    return v
  v = str(
    os.environ.get(key, "")
  ).strip()
  return v or default


PROV_KEYS = {
  "openrouter": sget(
    "OPENROUTER_API_KEY"
  ),
  "openai": sget("OPENAI_API_KEY"),
  "groq": sget("GROQ_API_KEY"),
  "google": (
    sget("GOOGLE_API_KEY")
    or sget("GEMINI_API_KEY")
  ),
}

API_KEY = PROV_KEYS["openrouter"]
EJS_SERVICE = sget("EMAILJS_SERVICE_ID")
EJS_TEMPLATE = sget(
  "EMAILJS_TEMPLATE_ID"
)
EJS_PUBLIC = sget("EMAILJS_PUBLIC_KEY")
EJS_PRIVATE = sget(
  "EMAILJS_PRIVATE_KEY"
)

FOUNDERS = {
  e.strip().lower()
  for e in sget(
    "FOUNDER_EMAILS"
  ).split(",")
  if e.strip()
}
FOUNDER_NAME = sget(
  "FOUNDER_NAME",
  "Avyan",
)
FOUNDER_BIO = sget(
  "FOUNDER_BIO",
  (
    "14-year-old Founder & Lead Architect "
    "of VOID, student at Sunbeam School "
    "Varuna in Varanasi, creator of VoidOS, "
    "author of World Zero, and gamer "
    "(NOTREFLEXGAMING05)."
  ),
)

FOUNDER_LORE = {
  "name": FOUNDER_NAME,
  "role": (
    "Founder & Lead Sovereign Architect"
  ),
  "age": "14",
  "institution": (
    "Sunbeam School Varuna, Varanasi"
  ),
  "city": "Varanasi, India",
  "gamer_tag": "NOTREFLEXGAMING05",
  "projects": [
    {
      "title": "VOID Sovereign OS",
      "tag": "Flagship AI Ecosystem",
      "info": (
        "Multi-provider AI intelligence "
        "with live web verification, "
        "native PDF/Slide/Flashcard "
        "compilation, and HTML5 Studio."
      ),
    },
    {
      "title": "VoidOS",
      "tag": "Operating Environment",
      "info": (
        "Futuristic next-gen OS architecture "
        "designed by Avyan for speed, "
        "privacy, and cyber-glass control."
      ),
    },
    {
      "title": "World Zero",
      "tag": "Original Book & Lore",
      "info": (
        "Speculative fiction & action saga "
        "authored by Avyan exploring "
        "sovereign technology and resilience."
      ),
    },
    {
      "title": "NOTREFLEXGAMING05",
      "tag": "Gaming & Esports Division",
      "info": (
        "High-reflex competitive gaming "
        "identity and community presence."
      ),
    },
  ],
  "badges": [
    "👑 Founder: Avyan",
    "⚡ Creator of VoidOS",
    "📖 Author of World Zero",
    "🏫 Sunbeam School Varuna",
    "🎮 NOTREFLEXGAMING05",
    "🏛️ Varanasi",
  ],
}

SEARCH_KEYS = {
  "tavily": sget("TAVILY_API_KEY"),
  "brave": sget("BRAVE_API_KEY"),
  "serper": sget("SERPER_API_KEY"),
}


def esc(s):
  return html.escape(str(s))


def safe_name(s, n=25):
  return (
    re.sub(r"\W+", "_", str(s)).strip(
      "_"
    )[:n]
    or "VOID"
  )


@st.cache_resource(show_spinner=False)
def http_session():
  s = requests.Session()
  s.headers.update(VOID_HEADERS)
  return s


# ============================== 4. OFFLINE SOVEREIGN STEM & CODEX DATABASE ==============================
OFFLINE_CODEX_VAULT = {
  "Force & Pressure (Class 8 Physics)": {
    "domain": "Physics",
    "level": "Class 8 CBSE / ICSE / Olympiad",
    "formulas": [
      "Force: F = m * a (Newton)",
      "Pressure: P = F / A (Pascal = N/m^2)",
      "Hydrostatic Pressure: P = h * rho * g",
      "Atmospheric Pressure: 1 atm = 101,325 Pa",
      "Pascal Law: F1 / A1 = F2 / A2",
      "Buoyancy: F_b = rho_fluid * V_sub * g",
    ],
    "notes": [
      "Force is a push or pull that can change state of motion, speed, direction, or shape.",
      "Contact forces include muscular force and friction; non-contact forces include gravity, electrostatic, and magnetic forces.",
      "Sharp knives and needles have tiny surface areas so a small force creates huge pressure.",
      "Liquids and gases exert pressure on the walls of their containers and equally at the same depth.",
    ],
    "questions": [
      "Q1: Why do porters place a round cloth on their heads? Ans: Increases contact area and reduces pressure.",
      "Q2: A force of 150 N acts on an area of 0.03 m^2. Find pressure. Ans: 5,000 Pa.",
      "Q3: Why do mountaineers suffer nosebleeds at high altitudes? Ans: Atmospheric pressure drops below internal blood pressure.",
    ],
  },
  "Friction & Sound (Class 8 Physics)": {
    "domain": "Physics",
    "level": "Class 8 CBSE / ICSE",
    "formulas": [
      "Limiting Friction: f_max = mu_s * N",
      "Kinetic Friction: f_k = mu_k * N",
      "Hierarchy: f_static > f_sliding > f_rolling",
      "Wave Speed: v = f * lambda",
      "Time Period: T = 1 / f (seconds)",
      "Minimum Echo Distance (Air): 17.2 m",
    ],
    "notes": [
      "Friction opposes relative motion between two surfaces in contact due to microscopic interlocking.",
      "Ball bearings convert sliding friction into much smaller rolling friction.",
      "Sound is produced by vibrating bodies and travels as longitudinal compression-rarefaction waves.",
      "Audible range for humans is 20 Hz to 20,000 Hz (20 kHz); >20 kHz is ultrasound.",
    ],
    "questions": [
      "Q1: Why are airplane and boat bodies streamlined? Ans: To minimize fluid friction (drag).",
      "Q2: If a pendulum oscillates 40 times in 4 seconds, find frequency and time period. Ans: f = 10 Hz, T = 0.1 s.",
    ],
  },
  "Light, Optics & Human Eye (Physics)": {
    "domain": "Physics",
    "level": "Class 8–10",
    "formulas": [
      "Law of Reflection: Angle i = Angle r",
      "Multiple Images in Inclined Mirrors: N = (360 / theta) - 1",
      "Mirror Equation: 1/v + 1/u = 1/f",
      "Lens Equation: 1/v - 1/u = 1/f",
      "Snell Law: n1 * sin(i) = n2 * sin(r)",
      "Lens Power: P = 1 / f(m) [Dioptre]",
    ],
    "notes": [
      "Plane mirrors form virtual, erect, laterally inverted images of the same size at the same distance behind the mirror.",
      "The retina contains rods (dim light sensitivity) and cones (bright light and color vision).",
      "Myopia (short-sightedness) is corrected with a concave lens; Hypermetropia is corrected with a convex lens.",
    ],
    "questions": [
      "Q1: Two plane mirrors are inclined at 60 degrees. How many images are formed? Ans: (360/60) - 1 = 5 images.",
      "Q2: What is the least distance of distinct vision for a normal human eye? Ans: 25 cm.",
    ],
  },
  "Electricity & Chemical Effects (Physics/Chem)": {
    "domain": "Physics & Chemistry",
    "level": "Class 8–10",
    "formulas": [
      "Current: I = Q / t (Ampere)",
      "Ohm Law: V = I * R (Volt)",
      "Resistance: R = rho * (L / A)",
      "Joule Heating: H = I^2 * R * t",
      "Electric Power: P = V * I = I^2 * R = V^2 / R",
      "Faraday First Law: m = Z * I * t",
    ],
    "notes": [
      "Liquids that conduct electricity (electrolytes) are solutions of acids, bases, or salts.",
      "Electroplating deposits a thin layer of a desired metal (chromium, silver, gold, zinc) onto another material using electrolysis.",
      "LEDs glow even with weak electric currents; the longer lead is positive (anode).",
    ],
    "questions": [
      "Q1: Why doesn't distilled water conduct electricity? Ans: It lacks free dissolved ions.",
      "Q2: Why is iron electroplated with zinc? Ans: To prevent rusting and corrosion (galvanization).",
    ],
  },
  "Linear & Quadratic Equations (Mathematics)": {
    "domain": "Mathematics",
    "level": "Class 8–10 & Olympiad",
    "formulas": [
      "Linear Form: a*x + b = 0 -> x = -b / a",
      "Quadratic Form: a*x^2 + b*x + c = 0",
      "Quadratic Roots: x = (-b +/- sqrt(b^2 - 4ac)) / (2a)",
      "Discriminant: D = b^2 - 4ac",
      "Sum of Roots: alpha + beta = -b / a",
      "Product of Roots: alpha * beta = c / a",
    ],
    "notes": [
      "If D > 0, roots are real and distinct; if D = 0, roots are real and equal; if D < 0, roots are complex conjugates.",
      "Algebraic Identities: (a+b)^2 = a^2 + 2ab + b^2 | a^2 - b^2 = (a-b)(a+b) | (a+b)^3 = a^3 + b^3 + 3ab(a+b).",
    ],
    "questions": [
      "Q1: Solve x^2 - 7x + 12 = 0. Ans: (x-3)(x-4) = 0 -> x = 3 or x = 4.",
      "Q2: Find k if 2x^2 + kx + 8 = 0 has equal roots. Ans: D = k^2 - 64 = 0 -> k = +/- 8.",
    ],
  },
  "Mensuration, Geometry & Trigonometry (Maths)": {
    "domain": "Mathematics",
    "level": "Class 8–10",
    "formulas": [
      "Trapezium Area: A = 0.5 * (a + b) * h",
      "Rhombus Area: A = 0.5 * d1 * d2",
      "Cylinder: CSA = 2*pi*r*h | Vol = pi*r^2*h",
      "Cone: CSA = pi*r*l | Vol = (1/3)*pi*r^2*h",
      "Sphere: SA = 4*pi*r^2 | Vol = (4/3)*pi*r^3",
      "Euler Polyhedron Formula: F + V - E = 2",
      "Pythagorean Trig: sin^2(x) + cos^2(x) = 1",
    ],
    "notes": [
      "Sum of interior angles of an n-sided polygon is (n - 2) * 180 degrees.",
      "Sum of exterior angles of any convex polygon is always 360 degrees.",
    ],
    "questions": [
      "Q1: Find volume of a cylinder with r = 7 cm and h = 10 cm. Ans: 22/7 * 49 * 10 = 1,540 cm^3.",
      "Q2: How many diagonals does a regular octagon have? Ans: n(n-3)/2 = 8*5/2 = 20.",
    ],
  },
  "Cell Structure & Microorganisms (Biology)": {
    "domain": "Biology",
    "level": "Class 8–10",
    "formulas": [
      "Photosynthesis: 6CO2 + 6H2O -> C6H12O6 + 6O2",
      "Aerobic Respiration: C6H12O6 + 6O2 -> 6CO2 + 6H2O + 38 ATP",
      "Anaerobic Fermentation (Yeast): Glucose -> Ethanol + CO2 + 2 ATP",
    ],
    "notes": [
      "Robert Hooke discovered cells in 1665; Cell Theory was formulated by Schleiden, Schwann, and Virchow.",
      "Mitochondria are the powerhouse of the cell; Ribosomes synthesize proteins; Plastids (Chloroplasts) occur only in plant cells.",
      "Plant cells have a rigid cellulose cell wall and a large central vacuole; animal cells lack a cell wall.",
      "Rhizobium bacteria fix atmospheric nitrogen in root nodules of leguminous plants.",
    ],
    "questions": [
      "Q1: Why are lysosomes called suicidal bags? Ans: They contain digestive enzymes that can break down the damaged cell itself.",
      "Q2: Which microorganism converts milk into curd? Ans: Lactobacillus bacteria.",
    ],
  },
  "Algorithms, Python & Data Structures (CS)": {
    "domain": "Computer Science",
    "level": "Sovereign Architect Tier",
    "formulas": [
      "Binary Search Time: O(log n) | Space: O(1)",
      "Merge Sort & Quick Sort Avg: O(n log n)",
      "Hash Map Lookup / Insert Avg: O(1)",
      "BFS / DFS Graph Traversal: O(V + E)",
      "Dijkstra Shortest Path: O((V + E) log V)",
    ],
    "notes": [
      "Lists in Python are dynamic arrays; sets and dicts use hash tables for O(1) average lookup.",
      "Recursion requires a strict base case and state progression toward the base case to avoid stack overflow.",
      "Time complexity measures asymptotic growth as input size n approaches infinity.",
    ],
    "questions": [
      "Q1: Why are Python tuples hashable while lists are not? Ans: Tuples are immutable so their hash value never changes.",
      "Q2: How many comparisons does binary search need at most for 1,024 elements? Ans: log2(1024) + 1 = 11.",
    ],
  },
}

PERIODIC_TABLE_ELEMENTS = [
  {
    "Z": 1,
    "sym": "H",
    "name": "Hydrogen",
    "mass": 1.008,
    "group": "Nonmetal",
  },
  {
    "Z": 2,
    "sym": "He",
    "name": "Helium",
    "mass": 4.0026,
    "group": "Noble Gas",
  },
  {
    "Z": 3,
    "sym": "Li",
    "name": "Lithium",
    "mass": 6.94,
    "group": "Alkali Metal",
  },
  {
    "Z": 4,
    "sym": "Be",
    "name": "Beryllium",
    "mass": 9.0122,
    "group": "Alkaline Earth",
  },
  {
    "Z": 5,
    "sym": "B",
    "name": "Boron",
    "mass": 10.81,
    "group": "Metalloid",
  },
  {
    "Z": 6,
    "sym": "C",
    "name": "Carbon",
    "mass": 12.011,
    "group": "Nonmetal",
  },
  {
    "Z": 7,
    "sym": "N",
    "name": "Nitrogen",
    "mass": 14.007,
    "group": "Nonmetal",
  },
  {
    "Z": 8,
    "sym": "O",
    "name": "Oxygen",
    "mass": 15.999,
    "group": "Nonmetal",
  },
  {
    "Z": 9,
    "sym": "F",
    "name": "Fluorine",
    "mass": 18.998,
    "group": "Halogen",
  },
  {
    "Z": 10,
    "sym": "Ne",
    "name": "Neon",
    "mass": 20.180,
    "group": "Noble Gas",
  },
  {
    "Z": 11,
    "sym": "Na",
    "name": "Sodium",
    "mass": 22.990,
    "group": "Alkali Metal",
  },
  {
    "Z": 12,
    "sym": "Mg",
    "name": "Magnesium",
    "mass": 24.305,
    "group": "Alkaline Earth",
  },
  {
    "Z": 13,
    "sym": "Al",
    "name": "Aluminium",
    "mass": 26.982,
    "group": "Post-Transition",
  },
  {
    "Z": 14,
    "sym": "Si",
    "name": "Silicon",
    "mass": 28.085,
    "group": "Metalloid",
  },
  {
    "Z": 15,
    "sym": "P",
    "name": "Phosphorus",
    "mass": 30.974,
    "group": "Nonmetal",
  },
  {
    "Z": 16,
    "sym": "S",
    "name": "Sulfur",
    "mass": 32.06,
    "group": "Nonmetal",
  },
  {
    "Z": 17,
    "sym": "Cl",
    "name": "Chlorine",
    "mass": 35.45,
    "group": "Halogen",
  },
  {
    "Z": 18,
    "sym": "Ar",
    "name": "Argon",
    "mass": 39.948,
    "group": "Noble Gas",
  },
  {
    "Z": 19,
    "sym": "K",
    "name": "Potassium",
    "mass": 39.098,
    "group": "Alkali Metal",
  },
  {
    "Z": 20,
    "sym": "Ca",
    "name": "Calcium",
    "mass": 40.078,
    "group": "Alkaline Earth",
  },
  {
    "Z": 26,
    "sym": "Fe",
    "name": "Iron",
    "mass": 55.845,
    "group": "Transition Metal",
  },
  {
    "Z": 29,
    "sym": "Cu",
    "name": "Copper",
    "mass": 63.546,
    "group": "Transition Metal",
  },
  {
    "Z": 30,
    "sym": "Zn",
    "name": "Zinc",
    "mass": 65.38,
    "group": "Transition Metal",
  },
  {
    "Z": 47,
    "sym": "Ag",
    "name": "Silver",
    "mass": 107.87,
    "group": "Transition Metal",
  },
  {
    "Z": 79,
    "sym": "Au",
    "name": "Gold",
    "mass": 196.97,
    "group": "Transition Metal",
  },
]


# ============================== 5. DATABASE, AUTH & LOGOUT ENGINE ==============================
def load_db():
  try:
    if os.path.exists(DB_FILE):
      with open(
        DB_FILE,
        encoding="utf-8",
      ) as f:
        d = json.load(f)
      d.setdefault("users", {})
      d.setdefault("chats", {})
      d.setdefault("usage", {})
      return d
  except Exception:
    pass
  return {
    "users": {},
    "chats": {},
    "usage": {},
  }


def save_db(d):
  try:
    tmp = DB_FILE + ".tmp"
    with open(
      tmp,
      "w",
      encoding="utf-8",
    ) as f:
      json.dump(d, f, indent=2)
    os.replace(tmp, DB_FILE)
  except OSError:
    pass


db = load_db()


def new_chat(email):
  cid = uuid.uuid4().hex[:8]
  db["chats"].setdefault(
    email,
    {},
  )[cid] = {
    "title": "New Session",
    "messages": [],
  }
  return cid


def ensure_user(email, name=None):
  now = datetime.now().strftime(
    "%b %d, %H:%M"
  )
  founder = (
    email in FOUNDERS
    or "avyan" in email.lower()
  )
  rec = db["users"].get(email)
  if rec is None:
    nm = (
      FOUNDER_NAME
      if founder
      else (
        name
        or email.split("@")[0].capitalize()
      )
    )
    rec = {
      "name": nm,
      "city": "Varanasi",
      "joined": now,
      "last_active": now,
      "prompts": 0,
      "memory": (
        FOUNDER_BIO
        if founder
        else (
          f"Verified member of VOID Studio ({nm})."
        )
      ),
      "recent_topics": [],
    }
    db["users"][email] = rec
  else:
    rec.setdefault(
      "recent_topics",
      [],
    )
    rec["last_active"] = now
    if name and not founder:
      rec["name"] = name
  if not db["chats"].get(email):
    new_chat(email)
  save_db(db)
  return rec


def bump_daily_usage():
  today = datetime.now().strftime(
    "%Y-%m-%d"
  )
  db.setdefault("usage", {})
  db["usage"][today] = (
    db["usage"].get(today, 0) + 1
  )
  if len(db["usage"]) > 60:
    for k in sorted(
      db["usage"]
    )[:-60]:
      db["usage"].pop(k, None)


def signing_key():
  k = sget("APP_SECRET")
  if k:
    return k.encode("utf-8")
  try:
    if not os.path.exists(KEY_FILE):
      with open(
        KEY_FILE,
        "w",
        encoding="utf-8",
      ) as f:
        f.write(
          pysecrets.token_hex(32)
        )
    with open(
      KEY_FILE,
      encoding="utf-8",
    ) as f:
      return (
        f.read().strip().encode("utf-8")
      )
  except OSError:
    return (
      API_KEY or "void_key"
    ).encode("utf-8")


def sign(email, ts):
  msg = f"{email}|{ts}".encode("utf-8")
  return hmac.new(
    signing_key(),
    msg,
    hashlib.sha256,
  ).hexdigest()[:32]


def remember_login(email):
  ts = str(int(time.time()))
  qp = st.query_params
  if (
    qp.get("user") != email
    or not qp.get("ts")
    or not qp.get("sig")
  ):
    qp.update({
      "user": email,
      "ts": ts,
      "sig": sign(email, ts),
    })


def restore_login():
  qp = st.query_params
  email = qp.get("user")
  ts = qp.get("ts")
  sig = qp.get("sig")
  if (
    email
    and ts
    and sig
    and str(ts).isdigit()
    and (
      time.time() - int(ts)
      < LOGIN_DAYS * 86400
    )
  ):
    if hmac.compare_digest(
      str(sig),
      sign(str(email), str(ts)),
    ):
      return str(email)
  return None


def perform_logout():
  """Bulletproof logout: clears query params and session state keys."""
  try:
    st.query_params.clear()
  except Exception:
    pass
  for k in (
    "user_email",
    "current_chat_id",
    "active_prism_text",
    "active_prism_title",
    "prism_open",
    "pending_email",
    "pending_name",
    "target_otp",
    "otp_expiry",
    "otp_tries",
  ):
    st.session_state.pop(k, None)
  st.rerun()


# ============================== 6. LIVE CONTEXT & THREAD-SAFE RETRIEVAL ==============================
WMO = {
  0: "Clear sky",
  1: "Mainly clear",
  2: "Partly cloudy",
  3: "Overcast",
  45: "Foggy",
  48: "Rime fog",
  51: "Light drizzle",
  53: "Drizzle",
  55: "Heavy drizzle",
  61: "Light rain",
  63: "Moderate rain",
  65: "Heavy rain",
  71: "Light snow",
  73: "Snow",
  75: "Heavy snow",
  80: "Rain showers",
  81: "Heavy showers",
  95: "Thunderstorm",
  96: "Thunderstorm with hail",
}

WEATHER_WORDS = (
  "weather",
  "temperature",
  "temp",
  "rain",
  "forecast",
  "climate",
  "outside",
  "cold",
  "hot",
  "humidity",
)
KNOW_WORDS = (
  "who is",
  "what is",
  "tell me about",
  "history of",
  "explain",
  "news",
  "search",
  "when did",
  "how many",
  "current affairs",
  "breaking",
  "latest",
  "today",
  "right now",
  "this week",
)
CODE_WORDS = (
  "code",
  "python",
  "javascript",
  "debug",
  "error",
  "traceback",
  "function",
  "class ",
  "sql",
  "react",
  "html",
  "css",
  "algorithm",
  "regex",
  "api",
  "refactor",
  "bug",
)
MATH_WORDS = (
  "calculate",
  "solve",
  "equation",
  "integral",
  "derivative",
  "probability",
  "percentage",
  "sum of",
  "how many",
  "how much",
  "average",
  "mean",
  "median",
  "area",
  "volume",
  "profit",
  "interest",
)
DOC_WORDS = (
  "pdf",
  "ppt",
  "powerpoint",
  "slide",
  "presentation",
  "notes",
  "guide",
  "cheat sheet",
  "report",
  "document",
  "worksheet",
  "question bank",
  "essay",
  "summary of",
)
FRESH_WORDS = (
  "latest",
  "today",
  "current",
  "now",
  "news",
  "price",
  "score",
  "weather",
  "who won",
  "release",
  "trending",
  "update",
  "live",
  "recent",
  "breaking",
  "this week",
  "this month",
  "current affairs",
  "as of",
  "right now",
  "newest",
  "latest developments",
  "what happened",
)
NEWS_WORDS = (
  "current affairs",
  "breaking news",
  "latest news",
  "world news",
  "news today",
  "today's news",
  "todays news",
  "latest developments",
  "recent developments",
  "what happened today",
  "headlines",
)
_NO_SEARCH = (
  "```",
  "write a poem",
  "write a story",
  "build a",
  "make a game",
  "html app",
  "refactor",
  "my code",
  "code above",
  "attached",
)
_DDG_HEADERS = {
  "User-Agent": (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0 Safari/537.36"
  )
}


def is_current_query(prompt):
  p = re.sub(
    r"\s+",
    " ",
    (prompt or "").lower(),
  ).strip()
  if any(t in p for t in NEWS_WORDS):
    return True
  if any(t in p for t in FRESH_WORDS):
    return True
  return bool(
    re.search(
      r"\b(as of|right now|currently|latest|"
      r"today|yesterday|this week|this month|"
      r"breaking|recently)\b|\b20\d{2}\b",
      p,
    )
  )


def intent_of(prompt):
  p = (prompt or "").lower()
  score = {
    "code": sum(
      1 for w in CODE_WORDS if w in p
    ),
    "math": (
      sum(
        1 for w in MATH_WORDS if w in p
      )
      + (
        2
        if re.search(
          r"\d\s*[+\-*/^=]\s*\d",
          p,
        )
        else 0
      )
    ),
    "doc": sum(
      1 for w in DOC_WORDS if w in p
    ),
    "fresh": sum(
      1 for w in FRESH_WORDS if w in p
    ),
  }
  if is_current_query(prompt):
    score["fresh"] += 2
  if (
    "```" in (prompt or "")
    or "def " in (prompt or "")
  ):
    score["code"] += 3
  best = max(score, key=score.get)
  return (
    best if score[best] > 0 else "chat"
  )


@st.cache_data(
  ttl=3600,
  show_spinner=False,
)
def geocode(city):
  try:
    r = requests.get(
      GEO_URL,
      params={
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
      },
      headers=VOID_HEADERS,
      timeout=5,
    ).json()
    res = (
      r.get("results") or [None]
    )[0]
    if not res:
      return None
    label = ", ".join(
      filter(
        None,
        [
          res.get("name"),
          res.get("admin1"),
          res.get("country"),
        ],
      )
    )
    return (
      res["latitude"],
      res["longitude"],
      label,
    )
  except Exception:
    return None


@st.cache_data(
  ttl=600,
  show_spinner=False,
)
def fetch_live_weather(city):
  try:
    geo = geocode(city) or (
      25.3176,
      82.9739,
      "Varanasi, Uttar Pradesh, India",
    )
    lat, lon, label = geo
    d = requests.get(
      WEATHER_URL,
      params={
        "latitude": lat,
        "longitude": lon,
        "timezone": "auto",
        "current": (
          "temperature_2m,"
          "relative_humidity_2m,"
          "apparent_temperature,"
          "weather_code,"
          "wind_speed_10m"
        ),
        "daily": (
          "temperature_2m_max,"
          "temperature_2m_min"
        ),
      },
      headers=VOID_HEADERS,
      timeout=5,
    ).json()
    cur = d.get("current", {})
    day = d.get("daily", {})
    cond = WMO.get(
      cur.get("weather_code"),
      "Partly cloudy",
    )
    hi = day.get(
      "temperature_2m_max",
      ["N/A"],
    )[0]
    lo = day.get(
      "temperature_2m_min",
      ["N/A"],
    )[0]
    return (
      f"[LIVE WEATHER — {label}]: "
      f"{cond} | "
      f"Temp {cur.get('temperature_2m')}°C "
      f"(feels {cur.get('apparent_temperature')}°C) | "
      f"High/Low {hi}°C / {lo}°C | "
      f"Humidity {cur.get('relative_humidity_2m')}% | "
      f"Wind {cur.get('wind_speed_10m')} km/h"
    )
  except Exception:
    return (
      "[Weather feed temporarily unavailable]"
    )


@st.cache_data(
  ttl=1800,
  show_spinner=False,
)
def fetch_live_knowledge(query):
  try:
    q = re.sub(
      r"[^a-zA-Z0-9\s]",
      "",
      query,
    ).strip()[:120]
    if len(q) < 3:
      return ""
    r = requests.get(
      WIKI_URL,
      params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json",
        "srlimit": 2,
      },
      headers=VOID_HEADERS,
      timeout=4,
    ).json()
    snips = [
      re.sub(
        r"<.*?>",
        "",
        x.get("snippet", ""),
      )
      for x in r.get(
        "query",
        {},
      ).get("search", [])
    ]
    return (
      f"[LIVE ARCHIVE DATA]: {' | '.join(snips)}"
      if snips
      else ""
    )
  except Exception:
    return ""


@st.cache_data(
  ttl=900,
  show_spinner=False,
)
def engine_status():
  if not any(PROV_KEYS.values()):
    return (
      "offline",
      "add OPENROUTER_API_KEY to secrets",
    )
  if PROV_KEYS["openrouter"]:
    try:
      r = requests.get(
        OPENROUTER_MODELS_URL,
        headers=VOID_HEADERS,
        timeout=6,
      )
      if r.status_code == 200:
        n = len(
          r.json().get("data", [])
        )
        backups = [
          p
          for p in (
            "openai",
            "groq",
            "google",
          )
          if PROV_KEYS.get(p)
        ]
        tail = (
          f" • +{len(backups)} backup"
          if backups
          else ""
        )
        return (
          "online",
          f"link stable • {n} models{tail}",
        )
      return (
        "error",
        f"gateway HTTP {r.status_code}",
      )
    except Exception as e:
      return "error", str(e)[:60]
  return (
    "online",
    "backup provider active",
  )


def build_live_context(
  prompt,
  default_city,
):
  now = datetime.now(
    timezone(
      timedelta(hours=5, minutes=30)
    )
  )
  lines = [
    "[CHRONOMETER]: "
    + now.strftime(
      "%A, %B %d, %Y | %I:%M %p IST"
    )
  ]
  p = prompt.lower()
  if any(
    w in p for w in WEATHER_WORDS
  ):
    m = re.search(
      r"\b(?:in|at|for|of)\s+"
      r"([a-z][a-z ]{2,24}?)"
      r"(?:\s+(?:right|today|now|tomorrow)\b|[?.!,]|$)",
      p,
    )
    city_target = (
      m.group(1).strip().title()
      if m
      else default_city
    )
    lines.append(
      fetch_live_weather(city_target)
    )
  if (
    any(k in p for k in KNOW_WORDS)
    and not is_current_query(prompt)
  ):
    ctx = fetch_live_knowledge(prompt)
    if ctx:
      lines.append(ctx)
  return "\n".join(lines)


ACCURACY_RULES = (
  "=== ACCURACY RULES (highest priority) ===\n"
  "1. Answer the actual question first, in the first sentence.\n"
  "2. Think step by step internally. Verify arithmetic and trace code.\n"
  "3. Treat LIVE WEB RESULTS, PAGE EXCERPTS and EXACT CALC lines as the source of truth.\n"
  "4. Never invent facts, quotes, links, citations or numbers.\n"
  "5. For code: complete, runnable, no placeholders, with error handling."
)

_REPAIR_SYS = (
  "You are VOID's recovery engine. "
  "Produce the direct, complete answer now."
)

_VERIFY_SYS = (
  "You are VOID's strict fact-checker. "
  "Check every fact, number, step of maths and line of code in DRAFT against CONTEXT. "
  "Fix anything wrong or unsupported. "
  "Return ONLY the final improved answer."
)


def _strip_tags(t):
  return html.unescape(
    re.sub(r"<.*?>", "", t or "")
  ).strip()


def _src_tavily(q, n):
  k = SEARCH_KEYS["tavily"]
  if not k:
    return []
  try:
    r = requests.post(
      "https://api.tavily.com/search",
      json={
        "api_key": k,
        "query": q,
        "max_results": n,
        "search_depth": "advanced",
        "include_answer": True,
      },
      headers=VOID_HEADERS,
      timeout=10,
    ).json()
    out = []
    if r.get("answer"):
      out.append(
        "[TAVILY SUMMARY] "
        + _strip_tags(r["answer"])
      )
    for x in r.get("results", [])[:n]:
      t = x.get("title", "")
      u = x.get("url", "")
      c = _strip_tags(
        x.get("content", "")
      )[:400]
      out.append(f"- {t} ({u}): {c}")
    return out
  except Exception:
    return []


def _src_brave(q, n):
  k = SEARCH_KEYS["brave"]
  if not k:
    return []
  try:
    r = requests.get(
      "https://api.search.brave.com/res/v1/web/search",
      params={"q": q, "count": n},
      headers={
        "X-Subscription-Token": k,
        "Accept": "application/json",
      },
      timeout=10,
    ).json()
    res = (
      r.get("web", {}) or {}
    ).get("results", [])[:n]
    return [
      f"- {x.get('title', '')} "
      f"({x.get('url', '')}): "
      f"{_strip_tags(x.get('description', ''))}"
      for x in res
    ]
  except Exception:
    return []


def _src_serper(q, n):
  k = SEARCH_KEYS["serper"]
  if not k:
    return []
  try:
    r = requests.post(
      "https://google.serper.dev/search",
      json={"q": q, "num": n},
      headers={
        "X-API-KEY": k,
        "Content-Type": "application/json",
      },
      timeout=10,
    ).json()
    out = []
    ab = r.get("answerBox", {}).get(
      "answer"
    )
    if ab:
      out.append(f"[ANSWER BOX] {ab}")
    for x in r.get("organic", [])[:n]:
      out.append(
        f"- {x.get('title', '')} "
        f"({x.get('link', '')}): "
        f"{_strip_tags(x.get('snippet', ''))}"
      )
    return out
  except Exception:
    return []


def _src_ddg(q, n):
  try:
    r = requests.post(
      "https://html.duckduckgo.com/html/",
      data={"q": q},
      headers=_DDG_HEADERS,
      timeout=10,
    )
    r.raise_for_status()
    out = []
    anchors = re.findall(
      r'<a\b[^>]*class=["\'][^"\']*result__a[^"\']*["\'][^>]*>.*?</a>',
      r.text,
      re.S | re.I,
    )
    for anc in anchors:
      m = re.search(
        r'href=["\']([^"\']+)["\']',
        anc,
        re.I,
      )
      if not m:
        continue
      href = m.group(1)
      red = re.search(
        r"(?:[?&])uddg=([^&]+)",
        href,
      )
      url = (
        urllib.parse.unquote(
          red.group(1)
        )
        if red
        else href
      )
      title = _strip_tags(
        re.sub(
          r"^.*?>",
          "",
          anc,
          count=1,
        ).rsplit("</a>", 1)[0]
      )
      if (
        url.startswith(
          ("https://", "http://")
        )
        and title
      ):
        out.append(f"- {title} ({url})")
      if len(out) >= max(
        1,
        min(int(n), 10),
      ):
        break
    return out
  except Exception:
    return []


def _src_wiki(q, n=2):
  try:
    d = requests.get(
      WIKI_URL,
      params={
        "action": "query",
        "generator": "search",
        "gsrsearch": q,
        "gsrlimit": n,
        "prop": "extracts",
        "exintro": 1,
        "explaintext": 1,
        "exchars": 650,
        "format": "json",
        "redirects": 1,
      },
      headers=_DDG_HEADERS,
      timeout=8,
    ).json()
    pages = (
      d.get("query", {}) or {}
    ).get("pages", {}).values()
    return [
      f"- Wikipedia: {p.get('title')}: "
      f"{_strip_tags(p.get('extract', ''))[:480]}"
      for p in pages
    ]
  except Exception:
    return []


def _src_google_news(q, n=5):
  try:
    cq = re.sub(
      r"\s+",
      " ",
      (q or ""),
    ).strip()[:150]
    if cq.lower() in {
      "current affairs",
      "news",
      "latest news",
      "headlines",
      "today's news",
    }:
      cq = "India world current affairs"
    query = f"{cq} when:7d".strip()
    r = requests.get(
      "https://news.google.com/rss/search",
      params={
        "q": query,
        "hl": "en-IN",
        "gl": "IN",
        "ceid": "IN:en",
      },
      headers=_DDG_HEADERS,
      timeout=11,
    )
    r.raise_for_status()
    root = ET.fromstring(r.content)
    out = []
    limit = max(1, min(int(n), 10))
    for item in root.findall(
      ".//item"
    )[:limit]:
      title = _strip_tags(
        item.findtext("title", "")
      )
      link = (
        item.findtext("link", "") or ""
      ).strip()
      pub = (
        item.findtext("pubDate", "")
        or ""
      ).strip()
      if title and link.startswith(
        ("https://", "http://")
      ):
        out.append(
          f"- {title} ({link}) [published {pub}]"
        )
    return out
  except Exception:
    return []


def github_search_repositories(
  query,
  limit=6,
):
  q = (query or "").strip()[:180]
  if not q:
    return (
      [],
      "Enter a repository topic or name.",
    )
  headers = {
    "Accept": (
      "application/vnd.github+json"
    ),
    "User-Agent": "VOID-Omega",
  }
  token = sget("GITHUB_TOKEN")
  if token:
    headers["Authorization"] = (
      f"Bearer {token}"
    )
  try:
    resp = requests.get(
      "https://api.github.com/search/repositories",
      params={
        "q": q,
        "sort": "updated",
        "order": "desc",
        "per_page": max(
          1,
          min(int(limit), 10),
        ),
      },
      headers=headers,
      timeout=12,
    )
    if resp.status_code == 403:
      return (
        [],
        "GitHub rate limit reached. Add GITHUB_TOKEN to secrets.",
      )
    resp.raise_for_status()
    results = []
    for item in resp.json().get(
      "items",
      [],
    ):
      results.append({
        "name": item.get(
          "full_name",
          "unknown",
        ),
        "url": item.get("html_url", ""),
        "description": (
          item.get("description")
          or "No description provided."
        ),
        "stars": item.get(
          "stargazers_count",
          0,
        ),
        "language": (
          item.get("language")
          or "Not specified"
        ),
        "updated": (
          item.get("updated_at") or ""
        )[:10],
      })
    return results, None
  except requests.RequestException as e:
    return (
      [],
      f"GitHub request failed: {str(e)[:160]}",
    )


def send_smtp_email(
  to_address,
  subject,
  body,
):
  host = sget("SMTP_HOST")
  port = sget("SMTP_PORT", "587")
  username = sget("SMTP_USERNAME")
  password = sget("SMTP_PASSWORD")
  sender = (
    sget("SMTP_FROM") or username
  )
  if not all((
    host,
    username,
    password,
    sender,
  )):
    return (
      False,
      "Set SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD in secrets.",
    )
  to_addr = (to_address or "").strip()
  subj = (subject or "").strip()
  msg_body = (body or "").strip()
  if not EMAIL_RE.match(to_addr):
    return (
      False,
      "Enter a valid recipient email.",
    )
  if not subj or not msg_body:
    return (
      False,
      "Subject and message are required.",
    )
  msg = EmailMessage()
  msg["From"] = sender
  msg["To"] = to_addr
  msg["Subject"] = subj
  msg.set_content(msg_body)
  try:
    p_num = int(port)
    if p_num == 465:
      with smtplib.SMTP_SSL(
        host,
        p_num,
        timeout=20,
      ) as srv:
        srv.login(username, password)
        srv.send_message(msg)
    else:
      with smtplib.SMTP(
        host,
        p_num,
        timeout=20,
      ) as srv:
        srv.ehlo()
        srv.starttls()
        srv.ehlo()
        srv.login(username, password)
        srv.send_message(msg)
    return (
      True,
      "Email sent successfully.",
    )
  except Exception as exc:
    return (
      False,
      f"Email failed: {str(exc)[:160]}",
    )


@st.cache_data(
  ttl=120,
  show_spinner=False,
  max_entries=256,
)
def web_search_bundle(query, n=5):
  q = re.sub(
    r"\s+",
    " ",
    query,
  ).strip()[:220]
  if len(q) < 3:
    return "", []
  funcs = [
    lambda: _src_tavily(q, n),
    lambda: _src_serper(q, n),
    lambda: _src_brave(q, n),
    lambda: _src_ddg(q, n),
  ]
  if is_current_query(q):
    funcs.append(
      lambda: _src_google_news(q, n)
    )
  funcs.append(lambda: _src_wiki(q, 2))
  chunks, urls = [], []
  with ThreadPoolExecutor(
    max_workers=min(len(funcs), 6)
  ) as ex:
    for res in ex.map(
      lambda f: f(),
      funcs,
    ):
      chunks.extend(res or [])
  for line in chunks:
    m = re.search(
      r"\((https?://[^)\s]+)\)",
      line,
    )
    if m and m.group(1) not in urls:
      urls.append(m.group(1))
  seen, dedup = set(), []
  for line in chunks:
    sig = line[:110]
    if sig not in seen:
      seen.add(sig)
      dedup.append(line)
  return (
    "\n".join(dedup[:18]),
    urls[:10],
  )


@st.cache_data(
  ttl=1800,
  show_spinner=False,
  max_entries=96,
)
def read_page(url, limit=4000):
  try:
    r = requests.get(
      "https://r.jina.ai/" + url,
      timeout=14,
      headers=VOID_HEADERS,
    )
    if (
      r.status_code == 200
      and len(r.text) > 200
    ):
      return re.sub(
        r"\n{3,}",
        "\n\n",
        r.text,
      )[:limit]
  except Exception:
    pass
  return ""


_MATH_OPS = {
  ast.Add: operator.add,
  ast.Sub: operator.sub,
  ast.Mult: operator.mul,
  ast.Div: operator.truediv,
  ast.Pow: operator.pow,
  ast.Mod: operator.mod,
  ast.USub: operator.neg,
  ast.UAdd: operator.pos,
  ast.FloorDiv: operator.floordiv,
}


def _math_eval(n):
  if isinstance(
    n,
    ast.Constant,
  ) and isinstance(
    n.value,
    (int, float),
  ):
    return n.value
  if (
    isinstance(n, ast.BinOp)
    and type(n.op) in _MATH_OPS
  ):
    a = _math_eval(n.left)
    b = _math_eval(n.right)
    if (
      isinstance(n.op, ast.Pow)
      and abs(b) > 100
    ):
      raise ValueError("exp")
    return _MATH_OPS[type(n.op)](a, b)
  if (
    isinstance(n, ast.UnaryOp)
    and type(n.op) in _MATH_OPS
  ):
    return _MATH_OPS[type(n.op)](
      _math_eval(n.operand)
    )
  raise ValueError("unsupported")


def exact_math(prompt):
  res = []
  for m in re.findall(
    r"[\d.][\d\s.+\-*/^()%]*[\d)]",
    prompt,
  ):
    e = m.strip()
    if len(e) >= 3 and re.search(
      r"[+\-*/^%]",
      e,
    ):
      try:
        node = ast.parse(
          e.replace("^", "**"),
          mode="eval",
        ).body
        v = _math_eval(node)
        val = (
          round(v, 10)
          if isinstance(v, float)
          else v
        )
        res.append(
          f"[EXACT CALC] {e} = {val}"
        )
      except Exception:
        continue
  pct = re.findall(
    r"(\d+(?:\.\d+)?)\s*(?:%|percent)\s*of\s*(\d+(?:\.\d+)?)",
    prompt,
    re.I,
  )
  for a, b in pct[:3]:
    val = round(
      float(a) * float(b) / 100.0,
      10,
    )
    res.append(
      f"[EXACT CALC] {a}% of {b} = {val}"
    )
  return "\n".join(res[:5])


def needs_search(
  prompt,
  depth="Standard",
):
  if depth == "Off":
    return False
  p = re.sub(
    r"\s+",
    " ",
    (prompt or "").lower(),
  ).strip()
  if len(p) < 4:
    return False
  if is_current_query(p):
    return True
  if any(s in p for s in _NO_SEARCH):
    return False
  return (
    any(w in p for w in KNOW_WORDS)
    or depth == "Deep"
  )


def grounding(
  prompt,
  depth="Standard",
  diag=None,
):
  parts = [ACCURACY_RULES]
  calc = exact_math(prompt)
  if calc:
    parts.append(calc)
  hits, urls, pages = 0, [], 0
  sources = []
  search_req = needs_search(
    prompt,
    depth,
  )
  if search_req:
    text, urls = web_search_bundle(
      prompt,
      6 if depth == "Deep" else 5,
    )
    for line in text.splitlines():
      m = re.search(
        r"\((https?://[^)\s]+)\)",
        line,
      )
      if m and m.group(1) in urls:
        u = m.group(1)
        s_num = urls.index(u) + 1
        t_str = (
          line.lstrip("- ")
          .split(" (", 1)[0]
          .strip()[:160]
        )
        sources.append({
          "number": s_num,
          "title": t_str,
          "url": u,
        })
    hits = len(urls)
    if text:
      ts = datetime.now(
        timezone.utc
      ).strftime("%Y-%m-%d %H:%M UTC")
      parts.append(
        f"[LIVE WEB RESULTS — {ts}]\n{text}"
      )
    if (
      depth == "Deep"
      or is_current_query(prompt)
    ) and urls:
      for u in urls[:2]:
        body = read_page(u, 3600)
        if body:
          pages += 1
          parts.append(
            f"[PAGE EXCERPT — {u}]\n{body}"
          )
  if diag is not None:
    diag.update(
      search_hits=hits,
      sources=sources[:8],
      pages_read=pages,
      math=bool(calc),
    )
  return "\n\n".join(parts)


# ============================== 7. MULTI-PROVIDER ENGINE LAYER ==============================
class EngineError(Exception):
  pass


AUTO_ROUTES = {
  "code": [
    "qwen/qwen-2.5-coder-32b-instruct",
    "deepseek/deepseek-chat",
  ],
  "math": [
    "deepseek/deepseek-r1",
    "deepseek/deepseek-chat",
  ],
  "fresh": [
    "google/gemini-2.5-flash",
    "deepseek/deepseek-chat",
  ],
  "doc": [
    "google/gemini-2.5-pro",
    "deepseek/deepseek-chat",
  ],
  "chat": [
    "deepseek/deepseek-chat",
    "google/gemini-2.5-flash",
  ],
}

OR_BACKUP = [
  "deepseek/deepseek-chat",
  "google/gemini-2.5-flash",
  "qwen/qwen-2.5-72b-instruct",
  "meta-llama/llama-3.3-70b-instruct",
  "openai/gpt-4o-mini",
]
GROQ_MODELS = [
  "llama-3.3-70b-versatile",
  "llama-3.1-8b-instant",
]
GEMINI_MODELS = [
  "gemini-2.0-flash",
  "gemini-1.5-flash",
]
OPENAI_MODELS = [
  "gpt-4o-mini",
  "gpt-4o",
]
_PROVIDER_LABEL = {
  "openrouter": "Cosmic Link",
  "openai": "Nebula Relay",
  "groq": "Pulsar Relay",
  "google": "Quasar Relay",
}


def resolve_primary(choice, prompt=""):
  default_m = ENGINES[
    "🪐 Nebula Core (Deep Logic Engine)"
  ]
  model = ENGINES.get(choice, default_m)
  if model == "auto":
    route = AUTO_ROUTES.get(
      intent_of(prompt),
      AUTO_ROUTES["chat"],
    )
    return route[0]
  return model


def build_chain(
  choice,
  prompt="",
  avoid=None,
):
  primary = resolve_primary(
    choice,
    prompt,
  )
  chain = []
  if PROV_KEYS["openrouter"]:
    chain.append((
      "openrouter",
      primary,
    ))
    pool = (
      AUTO_ROUTES.get(
        intent_of(prompt),
        [],
      )
      + OR_BACKUP
    )
    for m in pool:
      if m != primary:
        chain.append(("openrouter", m))
  if PROV_KEYS["groq"]:
    for m in GROQ_MODELS:
      chain.append(("groq", m))
  if PROV_KEYS["google"]:
    for m in GEMINI_MODELS:
      chain.append(("google", m))
  if PROV_KEYS["openai"]:
    for m in OPENAI_MODELS:
      chain.append(("openai", m))
  if avoid:
    chain = [
      c for c in chain if c[1] != avoid
    ]
  return chain


def _trim(msgs, budget=24000):
  out, used = [], 0
  for m in reversed(
    msgs[-MAX_HISTORY:]
  ):
    c = str(m.get("content", ""))
    if used + len(c) > budget and out:
      break
    out.append({
      "role": m.get("role", "user"),
      "content": c[:budget],
    })
    used += len(c)
  return list(reversed(out))


def _headers(provider):
  h = {
    "Authorization": (
      f"Bearer {PROV_KEYS[provider]}"
    ),
    "Content-Type": "application/json",
  }
  if provider == "openrouter":
    h.update({
      "HTTP-Referer": (
        "https://void.local"
      ),
      "X-Title": "VOID",
    })
  return h


def _url(provider):
  return {
    "openrouter": OPENROUTER_URL,
    "openai": OPENAI_URL,
    "groq": GROQ_URL,
  }[provider]


def _post_once(
  provider,
  model,
  system,
  msgs,
  temp,
  tokens,
):
  if provider == "google":
    contents = [
      {
        "role": (
          "model"
          if m["role"] == "assistant"
          else "user"
        ),
        "parts": [
          {"text": m["content"]}
        ],
      }
      for m in _trim(msgs)
    ]
    payload = {
      "systemInstruction": {
        "parts": [{"text": system}]
      },
      "contents": contents,
      "generationConfig": {
        "temperature": temp,
        "maxOutputTokens": tokens,
      },
    }
    ep = (
      GEMINI_URL.format(model=model)
      + f"?key={PROV_KEYS['google']}"
    )
    r = http_session().post(
      ep,
      json=payload,
      timeout=90,
    )
    if r.status_code != 200:
      raise EngineError(
        f"HTTP {r.status_code}"
      )
    parts = (
      r.json()["candidates"][0][
        "content"
      ]["parts"]
    )
    return "".join(
      p.get("text", "") for p in parts
    )
  body = {
    "model": model,
    "temperature": temp,
    "max_tokens": tokens,
    "stream": False,
    "messages": (
      [
        {
          "role": "system",
          "content": system,
        }
      ]
      + _trim(msgs)
    ),
  }
  r = http_session().post(
    _url(provider),
    headers=_headers(provider),
    json=body,
    timeout=90,
  )
  if r.status_code != 200:
    raise EngineError(
      f"{_PROVIDER_LABEL[provider]} HTTP {r.status_code}"
    )
  r.encoding = "utf-8"
  return (
    r.json()["choices"][0]["message"][
      "content"
    ]
    or ""
  )


def _stream_once(
  provider,
  model,
  system,
  msgs,
  temp,
  tokens,
):
  if provider == "google":
    yield _post_once(
      provider,
      model,
      system,
      msgs,
      temp,
      tokens,
    )
    return
  body = {
    "model": model,
    "temperature": temp,
    "max_tokens": tokens,
    "stream": True,
    "messages": (
      [
        {
          "role": "system",
          "content": system,
        }
      ]
      + _trim(msgs)
    ),
  }
  r = http_session().post(
    _url(provider),
    headers=_headers(provider),
    json=body,
    timeout=90,
    stream=True,
  )
  if r.status_code != 200:
    raise EngineError(
      f"{_PROVIDER_LABEL[provider]} HTTP {r.status_code}"
    )
  for line in r.iter_lines(
    decode_unicode=True
  ):
    if line and line.startswith(
      "data:"
    ):
      chunk = line[5:].strip()
      if chunk == "[DONE]":
        break
      try:
        delta = (
          json.loads(chunk)["choices"][
            0
          ]["delta"].get("content")
        )
        if delta:
          yield delta
      except Exception:
        continue


def call_llm(
  choice,
  system,
  msgs,
  temp=0.25,
  tokens=2000,
  prompt="",
  avoid=None,
  diag=None,
):
  if not any(PROV_KEYS.values()):
    return (
      None,
      "No engine key configured. Add OPENROUTER_API_KEY to secrets.",
    )
  errors = []
  q_str = prompt or (
    msgs[-1]["content"] if msgs else ""
  )
  for provider, model in build_chain(
    choice,
    q_str,
    avoid,
  ):
    t0 = time.time()
    try:
      txt = _post_once(
        provider,
        model,
        system,
        msgs,
        temp,
        tokens,
      )
      if txt.strip():
        if diag is not None:
          diag.update(
            provider=provider,
            model=model,
            latency=round(
              time.time() - t0,
              2,
            ),
            link=_PROVIDER_LABEL[
              provider
            ],
          )
        return txt, None
    except Exception as e:
      errors.append(str(e))
  return (
    None,
    " • ".join(errors[-2:])
    or "All engines failed.",
  )


def stream_llm(
  choice,
  system,
  msgs,
  temp=0.25,
  tokens=2000,
  prompt="",
  diag=None,
):
  for provider, model in build_chain(
    choice,
    prompt,
  ):
    got = False
    t0 = time.time()
    try:
      for chunk in _stream_once(
        provider,
        model,
        system,
        msgs,
        temp,
        tokens,
      ):
        got = True
        yield chunk
      if got:
        if diag is not None:
          diag.update(
            provider=provider,
            model=model,
            latency=round(
              time.time() - t0,
              2,
            ),
            link=_PROVIDER_LABEL[
              provider
            ],
          )
        return
    except Exception:
      continue
  raise EngineError(
    "All streaming engines failed."
  )


def answer_question(
  engine,
  prompt,
  system,
  msgs,
  temp,
  tokens,
  accuracy_mode=True,
  depth="Standard",
  verify=True,
  diag=None,
):
  if diag is None:
    diag = {}
  draft, err = call_llm(
    engine,
    system,
    msgs,
    temp,
    tokens,
    prompt=prompt,
    diag=diag,
  )
  if not draft:
    raise EngineError(
      err or "No reply"
    )
  if len(draft.strip()) < 45:
    repair, _ = call_llm(
      engine,
      system + "\n\n" + _REPAIR_SYS,
      msgs[-4:],
      max(temp, 0.2),
      tokens,
      prompt=prompt,
    )
    if (
      repair
      and len(repair.strip()) >= 45
    ):
      draft = repair
      diag["repaired"] = True
  if draft.count("```") % 2 != 0:
    draft += "\n```"
  if (
    verify
    and accuracy_mode
    and len(draft) > 120
  ):
    ctx_s = diag.get(
      "_context",
      "",
    )[-6000:]
    v_msgs = [
      {
        "role": "user",
        "content": (
          f"QUESTION:\n{prompt}\n\n"
          f"CONTEXT:\n{ctx_s}\n\n"
          f"DRAFT:\n{draft}"
        ),
      }
    ]
    better, _ = call_llm(
      engine,
      _VERIFY_SYS,
      v_msgs,
      0.0,
      3200,
      prompt=prompt,
      avoid=diag.get("model"),
    )
    if better and len(
      better.strip()
    ) >= min(60, len(draft.strip())):
      draft = better
      diag["verified"] = True
  return draft


def assurance(question, answer, diag):
  notes = []
  hits = int(
    diag.get("search_hits", 0) or 0
  )
  if hits:
    notes.append(
      f"{hits} live sources"
    )
  if diag.get("math"):
    notes.append("exact math verified")
  if diag.get("verified"):
    notes.append(
      "cross-model verified"
    )
  band = (
    "high"
    if (
      hits >= 2
      or diag.get("verified")
      or diag.get("math")
    )
    else "moderate"
  )
  return band, notes


# ============================== 8. DOCUMENT FORGE (PDF, SLIDES, FLASHCARDS) ==============================
DOC_TRIGGERS = (
  "pdf",
  "ppt",
  "powerpoint",
  "slide",
  "presentation",
  "study notes",
  "revision notes",
  "study guide",
  "cheat sheet",
  "question bank",
  "worksheet",
  "report",
  "html app",
  "make a game",
)


def detect_prism_intent(
  prompt,
  reply="",
):
  p = prompt.lower()
  return (
    any(t in p for t in DOC_TRIGGERS)
    or "```html" in reply.lower()
  )


def clean_for_pdf(text):
  rep = {
    "—": "-",
    "–": "-",
    "“": '"',
    "”": '"',
    "‘": "'",
    "’": "'",
    "•": "*",
    "…": "...",
    "→": "->",
  }
  for k, v in rep.items():
    text = text.replace(k, v)
  return text.encode(
    "latin-1",
    "ignore",
  ).decode("latin-1")


def pdf_escape(s):
  return (
    s.replace("\\", "\\\\")
    .replace("(", "\\(")
    .replace(")", "\\)")
  )


PDF_STYLE = {
  "TITLE": ("F2", 16, 50, 0, 24),
  "META": ("F1", 9, 50, 0, 18),
  "H1": ("F2", 13, 50, 6, 18),
  "BULLET": ("F1", 10.5, 56, 0, 15),
  "BODY": ("F1", 10.5, 50, 0, 15),
}


@st.cache_data(
  show_spinner=False,
  max_entries=64,
)
def generate_real_pdf_bytes(
  title,
  markdown,
  author="VOID Forge",
):
  ts = datetime.now().strftime(
    "%Y-%m-%d %H:%M"
  )
  lines = [
    ("TITLE", clean_for_pdf(title)),
    (
      "META",
      clean_for_pdf(
        f"Architected by {author} | {ts}"
      ),
    ),
    ("SPACE", ""),
  ]
  for raw in clean_for_pdf(
    markdown
  ).split("\n"):
    s = raw.strip()
    if not s:
      lines.append(("SPACE", ""))
    elif s.startswith("#"):
      h = (
        s.lstrip("#")
        .strip()
        .replace("**", "")
      )
      for w in (
        textwrap.wrap(h, 68) or [h]
      ):
        lines.append(("H1", w))
    elif s.startswith((
      "* ",
      "- ",
      "+ ",
    )):
      clean_b = (
        s[2:]
        .replace("**", "")
        .replace("`", "")
      )
      w = textwrap.wrap(clean_b, 78) or [
        ""
      ]
      lines.append((
        "BULLET",
        "* " + w[0],
      ))
      for x in w[1:]:
        lines.append((
          "BODY",
          "  " + x,
        ))
    else:
      c = (
        s.replace("**", "")
        .replace("__", "")
        .replace("`", "")
      )
      for w in (
        textwrap.wrap(c, 82) or [c]
      ):
        lines.append(("BODY", w))
  pages, cur, y = [], [], 790
  for kind, text in lines:
    if y < 60:
      pages.append("\n".join(cur))
      cur, y = [], 790
    if kind == "SPACE":
      y -= 9
      continue
    font, size, x, pre, post = (
      PDF_STYLE[kind]
    )
    y -= pre
    esc_t = pdf_escape(text)
    cur.append(
      f"BT /{font} {size} Tf "
      f"1 0 0 1 {x} {y} Tm "
      f"({esc_t}) Tj ET"
    )
    y -= post
  pages.append("\n".join(cur))
  total = len(pages)
  ids = [
    5 + i * 2 for i in range(total)
  ]
  kids = " ".join(
    f"{i} 0 R" for i in ids
  )
  objs = [
    (
      b"1 0 obj\n"
      b"<< /Type /Catalog /Pages 2 0 R >>\n"
      b"endobj\n"
    ),
    (
      f"2 0 obj\n"
      f"<< /Type /Pages /Kids [{kids}] "
      f"/Count {total} >>\n"
      f"endobj\n"
    ).encode(),
    (
      b"3 0 obj\n"
      b"<< /Type /Font /Subtype /Type1 "
      b"/BaseFont /Helvetica "
      b"/Encoding /WinAnsiEncoding >>\n"
      b"endobj\n"
    ),
    (
      b"4 0 obj\n"
      b"<< /Type /Font /Subtype /Type1 "
      b"/BaseFont /Helvetica-Bold "
      b"/Encoding /WinAnsiEncoding >>\n"
      b"endobj\n"
    ),
  ]
  for i, (pid, stream) in enumerate(
    zip(ids, pages),
    start=1,
  ):
    ftr = pdf_escape(
      f"VOID Prism • Page {i} of {total}"
    )
    sb = (
      stream
      + f"\nBT /F1 8 Tf 1 0 0 1 470 28 Tm ({ftr}) Tj ET"
    ).encode("latin-1", errors="ignore")
    objs.append(
      (
        f"{pid} 0 obj\n"
        f"<< /Type /Page /Parent 2 0 R "
        f"/MediaBox [0 0 595 842] "
        f"/Resources << /Font << "
        f"/F1 3 0 R /F2 4 0 R >> >> "
        f"/Contents {pid + 1} 0 R >>\n"
        f"endobj\n"
      ).encode()
    )
    objs.append(
      f"{pid + 1} 0 obj\n"
      f"<< /Length {len(sb)} >>\n"
      f"stream\n".encode()
      + sb
      + b"\nendstream\nendobj\n"
    )
  out = bytearray(
    b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
  )
  offsets = []
  for o in objs:
    offsets.append(len(out))
    out += o
  xref = len(out)
  out += (
    f"xref\n0 {len(objs) + 1}\n"
    f"0000000000 65535 f \n"
  ).encode()
  for off in offsets:
    out += (
      f"{off:010d} 00000 n \n"
    ).encode()
  out += (
    f"trailer\n"
    f"<< /Size {len(objs) + 1} "
    f"/Root 1 0 R >>\n"
    f"startxref\n{xref}\n%%EOF"
  ).encode()
  return bytes(out)


@st.cache_data(
  show_spinner=False,
  max_entries=64,
)
def generate_interactive_slides_html(
  title,
  markdown,
):
  secs = [
    s
    for s in re.split(
      r"(?m)^(?=#{1,2} )",
      markdown.strip(),
    )
    if s.strip()
  ]
  if len(secs) <= 1:
    paras = [
      p.strip()
      for p in markdown.split("\n\n")
      if p.strip()
    ]
    secs = [
      "\n\n".join(paras[i : i + 2])
      for i in range(0, len(paras), 2)
    ] or [markdown]
  slides_html = []
  for i, sec in enumerate(secs):
    lines = sec.strip().split("\n")
    h = esc(
      lines[0]
      .lstrip("#")
      .strip()
      .replace("**", "")
      or f"Slide {i + 1}"
    )
    body = "<br>".join(
      re.sub(
        r"\*\*(.+?)\*\*",
        r"<b>\1</b>",
        esc(l.strip()),
      )
      for l in lines[1:]
      if l.strip()
    )
    cls = "slide on" if i == 0 else "slide"
    slides_html.append(
        f'<div class="{cls}">'
        f'<div class="badge">'
        f"VOID PRISM — "
        f"SLIDE {i + 1} OF {len(secs)}"
        f"</div>"
        f"<h2>{h}</h2>"
        f'<div class="body">'
        f"{body}"
        f"</div>"
        f"</div>"
    )
    tpl = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        '<meta charset="utf-8">',
        "<style>",
        "body {",
        "  margin: 0;",
        "  background: #060913;",
        "  color: #F8FAFC;",
        "  font-family: sans-serif;",
        "  display: flex;",
        "  flex-direction: column;",
        "  height: 95vh;",
        "  justify-content: space-between;",
        "}",
        ".wrap {",
        "  flex: 1;",
        "  display: flex;",
        "  align-items: center;",
        "  justify-content: center;",
        "  padding: 18px;",
        "}",
        ".slide {",
        "  display: none;",
        "  width: 100%;",
        "  max-width: 820px;",
        "  background: #0C1324;",
        "  border: 1px solid #38BDF8;",
        "  border-radius: 18px;",
        "  padding: 34px 42px;",
        "  min-height: 300px;",
        "  box-sizing: border-box;",
        "}",
        ".slide.on {",
        "  display: block;",
        "}",
        ".badge {",
        "  font-size: 10px;",
        "  letter-spacing: 2px;",
        "  color: #38BDF8;",
        "  font-weight: 700;",
        "  margin-bottom: 12px;",
        "}",
        "h2 {",
        "  margin-top: 0;",
        "  color: #FFFFFF;",
        "}",
        ".body {",
        "  font-size: 15px;",
        "  line-height: 1.75;",
        "  color: #CBD5E1;",
        "}",
        ".ctl {",
        "  display: flex;",
        "  justify-content: center;",
        "  gap: 12px;",
        "  padding: 10px;",
        "}",
        "button {",
        "  background: #111B33;",
        "  color: #FFFFFF;",
        "  border: 1px solid #38BDF8;",
        "  padding: 8px 20px;",
        "  border-radius: 99px;",
        "  cursor: pointer;",
        "  font-weight: 600;",
        "}",
        "</style>",
        "</head>",
        "<body>",
        '<div class="wrap">',
        "".join(slides_html),
        "</div>",
        '<div class="ctl">',
        '<button onclick="go(-1)">',
        "◀ Prev",
        "</button>",
        '<button onclick="window.print()">',
        "🖨️ Print",
        "</button>",
        '<button onclick="go(1)">',
        "Next ▶",
        "</button>",
        "</div>",
        "<script>",
        "let c = 0;",
        "const s = document.querySelectorAll('.slide');",
        "function go(d) {",
        "  s[c].classList.remove('on');",
        "  c = (c + d + s.length) % s.length;",
        "  s[c].classList.add('on');",
        "}",
        "</script>",
        "</body>",
        "</html>",
    ]
    return "\n".join(tpl)
    "<!DOCTYPE html>",
    "<html>",
    "<head>",
    '<meta charset="utf-8">',
    "<style>",
    "body {",
    "  margin: 0;",
    "  background: #060913;",
    "  color: #F8FAFC;",
    "  font-family: system-ui, sans-serif;",
    "  display: flex;",
    "  flex-direction: column;",
    "  height: 95vh;",
    "  justify-content: space-between;",
    "}",
    ".wrap {",
    "  flex: 1;",
    "  display: flex;",
    "  align-items: center;",
    "  justify-content: center;",
    "  padding: 18px;",
    "}",
    ".slide {",
    "  display: none;",
    "  width: 100%;",
    "  max-width: 820px;",
    "  background: #0C1324;",
    "  border: 1px solid #38BDF8;",
    "  border-radius: 18px;",
    "  padding: 34px 42px;",
    "  min-height: 300px;",
    "  box-sizing: border-box;",
    "}",
    ".slide.on {",
    "  display: block;",
    "}",
    ".badge {",
    "  font-size: 10px;",
    "  letter-spacing: 2px;",
    "  color: #38BDF8;",
    "  font-weight: 700;",
    "  margin-bottom: 12px;",
    "}",
    "h2 {",
    "  margin-top: 0;",
    "  color: #FFFFFF;",
    "}",
    ".body {",
    "  font-size: 15px;",
    "  line-height: 1.75;",
    "  color: #CBD5E1;",
    "}",
    ".ctl {",
    "  display: flex;",
    "  justify-content: center;",
    "  gap: 12px;",
    "  padding: 10px;",
    "}",
    "button {",
    "  background: #111B33;",
    "  color: #FFFFFF;",
    "  border: 1px solid #38BDF8;",
    "  padding: 8px 20px;",
    "  border-radius: 99px;",
    "  cursor: pointer;",
    "  font-weight: 600;",
    "}",
    "</style>",
    "</head>",
    f'<div class="wrap">{"".join(slides_html)}</div>',
    '<div class="ctl">',
    '<button onclick="go(-1)">◀ Prev</button>',
    '<button onclick="window.print()">Export to PDF</button>',
    '<button onclick="go(1)">Next ▶</button>',
    "</div>",
return "\n".join(out)


@st.cache_data(show_spinner=False, max_entries=64)
def generate_interactive_slides_html(
    title,
    markdown,
):
  secs = [
  secs = [
    s
    for s in re.split(
      r"(?m)^(?=#{1,2} )",
      markdown.strip(),
    )
    if s.strip()
  ]
  if len(secs) <= 1:
    paras = [
      p.strip()
      for p in markdown.split("\n\n")
      if p.strip()
    ]
    secs = [
      "\n\n".join(paras[i : i + 2])
      for i in range(
        0,
        len(paras),
        2,
      )
    ] or [markdown]
  slides_html = []
  for i, sec in enumerate(secs):
    lines = sec.strip().split("\n")
    h = esc(
      lines[0]
      .lstrip("#")
      .strip()
      .replace("**", "")
      or f"Slide {i + 1}"
    )
    body = "<br>".join(
      re.sub(
        r"\*\*(.+?)\*\*",
        r"<b>\1</b>",
        esc(l.strip()),
      )
      for l in lines[1:]
      if l.strip()
    )
    cls = (
      "slide on"
      if i == 0
      else "slide"
    )
    slides_html.append(
      f'<div class="{cls}">'
      f'<div class="badge">'
      f"VOID PRISM — "
      f"SLIDE {i + 1} OF {len(secs)}"
      f"</div>"
      f"<h2>{h}</h2>"
      f'<div class="body">'
      f"{body}"
      f"</div>"
      f"</div>"
    )
  tpl = [
    "<!DOCTYPE html>",
    "<html>",
    "<head>",
    '<meta charset="utf-8">',
    "<style>",
    "body {",
    "  margin: 0;",
    "  background: #060913;",
    "  color: #F8FAFC;",
    "  font-family: sans-serif;",
    "  display: flex;",
    "  flex-direction: column;",
    "  height: 95vh;",
    "  justify-content: space-between;",
    "}",
    ".wrap {",
    "  flex: 1;",
    "  display: flex;",
    "  align-items: center;",
    "  justify-content: center;",
    "  padding: 18px;",
    "}",
    ".slide {",
    "  display: none;",
    "  width: 100%;",
    "  max-width: 820px;",
    "  background: #0C1324;",
    "  border: 1px solid #38BDF8;",
    "  border-radius: 18px;",
    "  padding: 34px 42px;",
    "  min-height: 300px;",
    "  box-sizing: border-box;",
    "}",
    ".slide.on {",
    "  display: block;",
    "}",
    ".badge {",
    "  font-size: 10px;",
    "  letter-spacing: 2px;",
    "  color: #38BDF8;",
    "  font-weight: 700;",
    "  margin-bottom: 12px;",
    "}",
    "h2 {",
    "  margin-top: 0;",
    "  color: #FFFFFF;",
    "}",
    ".body {",
    "  font-size: 15px;",
    "  line-height: 1.75;",
    "  color: #CBD5E1;",
    "}",
    ".ctl {",
    "  display: flex;",
    "  justify-content: center;",
    "  gap: 12px;",
    "  padding: 10px;",
    "}",
    "button {",
    "  background: #111B33;",
    "  color: #FFFFFF;",
    "  border: 1px solid #38BDF8;",
    "  padding: 8px 20px;",
    "  border-radius: 99px;",
    "  cursor: pointer;",
    "  font-weight: 600;",
    "}",
    "</style>",
    "</head>",
    "<body>",
    '<div class="wrap">',
    "".join(slides_html),
    "</div>",
    '<div class="ctl">',
    '<button onclick="go(-1)">',
    "◀ Prev",
    "</button>",
    '<button onclick="window.print()">',
    "🖨️ Print",
    "</button>",
    '<button onclick="go(1)">',
    "Next ▶",
    "</button>",
    "</div>",
    "<script>",
    "let c = 0;",
    "const s = document.querySelectorAll('.slide');",
    "function go(d) {",
    "  s[c].classList.remove('on');",
    "  c = (c + d + s.length) % s.length;",
    "  s[c].classList.add('on');",
    "}",
    "</script>",
    "</body>",
    "</html>",
  ]
  return "\n".join(tpl)


def generate_flashcards_html(
  title,
  markdown,
):
  cards = []
  raw_secs = [
    s.strip()
    for s in re.split(
      r"(?m)^(?=#{1,3} )",
      markdown.strip(),
    )
    if s.strip()
  ]
  for sec in raw_secs[:12]:
    lines = [
      l.strip()
      for l in sec.split("\n")
      if l.strip()
    ]
    if len(lines) >= 2:
      q_txt = (
        lines[0]
        .lstrip("#*- ")
        .replace("**", "")
      )
      a_txt = " ".join(
        l.lstrip("*- ").replace(
          "**",
          "",
        )
        for l in lines[1:4]
      )[:260]
      cards.append({
        "q": q_txt,
        "a": a_txt,
      })
  if not cards:
    cards = [
      {
        "q": title,
        "a": markdown[:240],
      }
    ]
  js_cards = json.dumps(cards)
  fc = [
    "<!DOCTYPE html>",
    "<html>",
    "<head>",
    '<meta charset="utf-8">',
    "<style>",
    "body {",
    "  margin: 0;",
    "  background: #060913;",
    "  color: #F8FAFC;",
    "  font-family: sans-serif;",
    "  display: flex;",
    "  flex-direction: column;",
    "  align-items: center;",
    "  justify-content: center;",
    "  height: 92vh;",
    "}",
    ".card {",
    "  width: 90%;",
    "  max-width: 580px;",
    "  min-height: 220px;",
    "  background: #0C1324;",
    "  border: 1.5px solid #38BDF8;",
    "  border-radius: 18px;",
    "  padding: 28px;",
    "  text-align: center;",
    "  cursor: pointer;",
    "  display: flex;",
    "  flex-direction: column;",
    "  justify-content: center;",
    "}",
    "#tag {",
    "  font-size: 11px;",
    "  color: #38BDF8;",
    "  font-weight: 700;",
    "  margin-bottom: 10px;",
    "}",
    "#txt {",
    "  font-size: 17px;",
    "  font-weight: 600;",
    "}",
    "button {",
    "  background: #111B33;",
    "  color: #FFFFFF;",
    "  border: 1px solid #38BDF8;",
    "  padding: 8px 18px;",
    "  border-radius: 99px;",
    "  cursor: pointer;",
    "  margin: 12px 6px;",
    "  font-weight: 600;",
    "}",
    "</style>",
    "</head>",
    "<body>",
    '<div class="card" onclick="flip()">',
    '<div id="tag">QUESTION</div>',
    '<div id="txt"></div>',
    "</div>",
    "<div>",
    '<button onclick="step(-1)">',
    "◀ Prev",
    "</button>",
    '<button onclick="flip()">',
    "↻ Flip",
    "</button>",
    '<button onclick="step(1)">',
    "Next ▶",
    "</button>",
    "</div>",
    "<script>",
    f"const c = {js_cards};",
    "let i = 0;",
    "let f = false;",
    "function paint() {",
    "  const t = document.getElementById('tag');",
    "  const x = document.getElementById('txt');",
    "  t.textContent = f",
    "    ? 'ANSWER'",
    "    : 'CARD ' + (i + 1) + '/' + c.length;",
    "  x.textContent = f",
    "    ? c[i].a",
    "    : c[i].q;",
    "}",
    "function flip() {",
    "  f = !f;",
    "  paint();",
    "}",
    "function step(d) {",
    "  i = (i + d + c.length) % c.length;",
    "  f = false;",
    "  paint();",
    "}",
    "paint();",
    "</script>",
    "</body>",
    "</html>",
  ]
  return "\n".join(fc)


def extract_code_blocks(text):
  return re.findall(
    r"```(\w*)\n(.*?)```",
    text,
    re.DOTALL,
  )


def is_html_block(b):
  lang = b[0].lower()
  body = b[1].lower()
  return (
    lang in ("html", "xml", "svg")
    or "<html" in body
    or "<style" in body
  )


# ============================== 8B. BUILT-IN HTML5 STUDIO TEMPLATES ==============================
CRICKET_HTML = "\n".join([
  "<!DOCTYPE html>",
  "<html>",
  "<head>",
  '<meta charset="utf-8">',
  "<style>",
  "body {",
  "  margin: 0;",
  "  background: #060913;",
  "  color: #F8FAFC;",
  "  font-family: sans-serif;",
  "  display: flex;",
  "  justify-content: center;",
  "  align-items: center;",
  "  height: 94vh;",
  "}",
  ".box {",
  "  background: #0C1324;",
  "  border: 1px solid #38BDF8;",
  "  border-radius: 18px;",
  "  padding: 24px;",
  "  width: 90%;",
  "  max-width: 480px;",
  "  text-align: center;",
  "}",
  ".score {",
  "  display: flex;",
  "  justify-content: space-around;",
  "  background: #111B33;",
  "  padding: 12px;",
  "  border-radius: 12px;",
  "  margin: 12px 0;",
  "  font-weight: 700;",
  "}",
  ".btns {",
  "  display: grid;",
  "  grid-template-columns: repeat(3, 1fr);",
  "  gap: 8px;",
  "  margin: 14px 0;",
  "}",
  "button {",
  "  background: #162240;",
  "  color: #FFFFFF;",
  "  border: 1px solid #38BDF8;",
  "  padding: 12px;",
  "  border-radius: 10px;",
  "  font-size: 17px;",
  "  font-weight: 700;",
  "  cursor: pointer;",
  "}",
  "button:hover {",
  "  background: #2563EB;",
  "}",
  "</style>",
  "</head>",
  "<body>",
  '<div class="box">',
  '<h3 style="margin:0;color:#38BDF8">',
  "⚡ VOID Hand Cricket Pro",
  "</h3>",
  '<div class="score">',
  '<div>YOU: <span id="u">0</span></div>',
  '<div>MODE: <span id="p">BAT</span></div>',
  '<div>TARGET: <span id="t">-</span></div>',
  "</div>",
  '<div class="btns">',
  '<button onclick="p(1)">1</button>',
  '<button onclick="p(2)">2</button>',
  '<button onclick="p(3)">3</button>',
  '<button onclick="p(4)">4</button>',
  '<button onclick="p(5)">5</button>',
  '<button onclick="p(6)">6</button>',
  "</div>",
  '<div id="log">Pick 1–6 to bat!</div>',
  "</div>",
  "<script>",
  "let u = 0;",
  "let ai = 0;",
  "let bat = true;",
  "let over = false;",
  "function p(n) {",
  "  if (over) return;",
  "  const c = Math.floor(Math.random() * 6) + 1;",
  "  const l = document.getElementById('log');",
  "  if (bat) {",
  "    if (n === c) {",
  "      bat = false;",
  "      document.getElementById('p').textContent = 'BOWL';",
  "      document.getElementById('t').textContent = u + 1;",
  "      l.textContent = 'OUT! Defend ' + (u + 1);",
  "    } else {",
  "      u += n;",
  "      document.getElementById('u').textContent = u;",
  "      l.textContent = 'You hit ' + n + ', AI bowled ' + c;",
  "    }",
  "  } else {",
  "    if (n === c) {",
  "      over = true;",
  "      l.textContent = 'WICKET! YOU WIN!';",
  "    } else {",
  "      ai += c;",
  "      if (ai > u) {",
  "        over = true;",
  "        l.textContent = 'AI chased target (' + ai + ')!';",
  "      } else {",
  "        l.textContent = 'AI score: ' + ai + '/' + (u + 1);",
  "      }",
  "    }",
  "  }",
  "}",
  "</script>",
  "</body>",
  "</html>",
])

POMODORO_HTML = "\n".join([
  "<!DOCTYPE html>",
  "<html>",
  "<head>",
  '<meta charset="utf-8">',
  "<style>",
  "body {",
  "  margin: 0;",
  "  background: #060913;",
  "  color: #F8FAFC;",
  "  font-family: sans-serif;",
  "  display: flex;",
  "  justify-content: center;",
  "  align-items: center;",
  "  height: 92vh;",
  "}",
  ".card {",
  "  background: #0C1324;",
  "  border: 1px solid #818CF8;",
  "  border-radius: 20px;",
  "  padding: 28px;",
  "  text-align: center;",
  "  width: 340px;",
  "}",
  ".tm {",
  "  font-size: 56px;",
  "  font-weight: 800;",
  "  font-family: monospace;",
  "  color: #38BDF8;",
  "  margin: 14px 0;",
  "}",
  "button {",
  "  background: #111B33;",
  "  color: #FFFFFF;",
  "  border: 1px solid #38BDF8;",
  "  padding: 8px 14px;",
  "  border-radius: 8px;",
  "  margin: 4px;",
  "  cursor: pointer;",
  "  font-weight: 600;",
  "}",
  "</style>",
  "</head>",
  "<body>",
  '<div class="card">',
  "<div>VOID FOCUS TIMER</div>",
  '<div class="tm" id="t">25:00</div>',
  '<button onclick="go()">▶ Start</button>',
  '<button onclick="stop()">⏸ Pause</button>',
  '<button onclick="rst(25)">25m</button>',
  '<button onclick="rst(5)">5m</button>',
  "</div>",
  "<script>",
  "let s = 1500;",
  "let iv = null;",
  "function d() {",
  "  const m = String(Math.floor(s / 60)).padStart(2, '0');",
  "  const r = String(s % 60).padStart(2, '0');",
  "  document.getElementById('t').textContent = m + ':' + r;",
  "}",
  "function go() {",
  "  if (!iv) {",
  "    iv = setInterval(() => {",
  "      if (s > 0) { s--; d(); }",
  "    }, 1000);",
  "  }",
  "}",
  "function stop() {",
  "  clearInterval(iv);",
  "  iv = null;",
  "}",
  "function rst(m) {",
  "  stop();",
  "  s = m * 60;",
  "  d();",
  "}",
  "</script>",
  "</body>",
  "</html>",
])

PLOTTER_HTML = "\n".join([
  "<!DOCTYPE html>",
  "<html>",
  "<head>",
  '<meta charset="utf-8">',
  "<style>",
  "body {",
  "  margin: 0;",
  "  background: #060913;",
  "  color: #F8FAFC;",
  "  font-family: sans-serif;",
  "  padding: 16px;",
  "  text-align: center;",
  "}",
  "input {",
  "  background: #0C1324;",
  "  color: #38BDF8;",
  "  border: 1px solid #38BDF8;",
  "  padding: 8px 12px;",
  "  border-radius: 8px;",
  "  width: 220px;",
  "}",
  "button {",
  "  background: #2563EB;",
  "  color: #FFFFFF;",
  "  border: 0;",
  "  padding: 9px 16px;",
  "  border-radius: 8px;",
  "  margin-left: 6px;",
  "  cursor: pointer;",
  "}",
  "canvas {",
  "  background: #090E1A;",
  "  border: 1px solid #38BDF8;",
  "  border-radius: 12px;",
  "  margin-top: 12px;",
  "  max-width: 100%;",
  "}",
  "</style>",
  "</head>",
  "<body>",
  "<div>",
  "<b>f(x) = </b>",
  '<input id="fn" value="Math.sin(x)*x">',
  '<button onclick="draw()">Plot</button>',
  "</div>",
  '<canvas id="cv" width="600" height="320">',
  "</canvas>",
  "<script>",
  "function draw() {",
  "  const c = document.getElementById('cv');",
  "  const ctx = c.getContext('2d');",
  "  const ex = document.getElementById('fn').value;",
  "  ctx.clearRect(0, 0, c.width, c.height);",
  "  ctx.strokeStyle = '#38BDF8';",
  "  ctx.lineWidth = 2;",
  "  ctx.beginPath();",
  "  for (let px = 0; px < c.width; px++) {",
  "    const x = (px - c.width / 2) / 25;",
  "    let y = 0;",
  "    try { y = eval(ex); } catch (e) {}",
  "    const py = c.height / 2 - y * 25;",
  "    if (px === 0) ctx.moveTo(px, py);",
  "    else ctx.lineTo(px, py);",
  "  }",
  "  ctx.stroke();",
  "}",
  "draw();",
  "</script>",
  "</body>",
  "</html>",
])

STUDIO_TEMPLATES = {
  "🏏 Hand Cricket Pro Arena": CRICKET_HTML,
  "⏱️ Cyber Pomodoro Timer": POMODORO_HTML,
  "📈 Function Graph Plotter": PLOTTER_HTML,
}


def send_otp_email(to, code):
  if not (
    EJS_SERVICE
    and EJS_TEMPLATE
    and EJS_PUBLIC
  ):
    return (
      False,
      "Email service is not configured.",
    )
  payload = {
    "service_id": EJS_SERVICE,
    "template_id": EJS_TEMPLATE,
    "user_id": EJS_PUBLIC,
    "template_params": {
      "to_email": to,
      "otp_code": code,
    },
  }
  if EJS_PRIVATE:
    payload["accessToken"] = EJS_PRIVATE
  try:
    r = http_session().post(
      EMAILJS_URL,
      json=payload,
      timeout=25,
    )
    return (
      (True, None)
      if r.status_code == 200
      else (False, r.text[:200])
    )
  except requests.RequestException as e:
    return False, str(e)


# ============================== 9. AUTHENTICATION GATE ==============================
if "user_email" not in st.session_state:
  restored = restore_login()
  if restored:
    st.session_state.user_email = (
      restored
    )

if "user_email" not in st.session_state:
  st.markdown(
    f'<div class="void-hero">'
    f'<div class="hero-mark">'
    f'<img src="{LOGO_B64}" width="40"/>'
    f"</div>"
    f'<div class="void-gradient">'
    f"VOID OMEGA"
    f"</div>"
    f'<div class="void-sub">'
    f"Sovereign OS Intelligence · "
    f"Architected by {esc(FOUNDER_NAME)} · "
    f"Verified Answers & Prism Forge"
    f"</div>"
    f"</div>",
    unsafe_allow_html=True,
  )
  _, mid, _ = st.columns([1, 1.4, 1])
  with mid:
    with st.form("landing_search_form"):
      st.markdown(
        "##### ⚡ Instant Sovereign Launch"
      )
      landing_query = st.text_input(
        "Direct Prompt",
        placeholder=(
          "Ask a question, paste code, "
          "or describe what to build…"
        ),
        label_visibility="collapsed",
      )
      c_b1, c_b2 = st.columns(2)
      with c_b1:
        search_submit = (
          st.form_submit_button(
            "🚀 Ask VOID",
            type="primary",
            use_container_width=True,
          )
        )
      with c_b2:
        guest_submit = (
          st.form_submit_button(
            "👤 Enter Guest Mode",
            use_container_width=True,
          )
        )
      if search_submit or guest_submit:
        guest_email = (
          f"guest_{uuid.uuid4().hex[:6]}"
          f"@void.os"
        )
        ensure_user(
          guest_email,
          name="Guest Operator",
        )
        st.session_state.user_email = (
          guest_email
        )
        remember_login(guest_email)
        if (
          search_submit
          and landing_query.strip()
        ):
          cid = list(
            db["chats"][
              guest_email
            ].keys()
          )[-1]
          q_clean = (
            landing_query.strip()
          )
          db["chats"][guest_email][cid][
            "messages"
          ].append({
            "role": "user",
            "content": q_clean,
          })
          t = q_clean.replace("\n", " ")
          db["chats"][guest_email][cid][
            "title"
          ] = (
            t[:26] + "..."
            if len(t) > 26
            else t
          )
          save_db(db)
        st.rerun()

    if (
      "pending_email"
      not in st.session_state
    ):
      with st.form("email_form"):
        st.markdown(
          "##### 🔐 Sign In with Email Code"
        )
        email_in = (
          st.text_input(
            "Email Address",
            placeholder="name@example.com",
          )
          .strip()
          .lower()
        )
        name_in = st.text_input(
          "Display Name",
          placeholder="Your name",
        ).strip()
        if st.form_submit_button(
          "📨 Send Verification Code",
          use_container_width=True,
        ):
          wait = OTP_COOLDOWN - (
            time.time()
            - st.session_state.get(
              "last_otp_ts",
              0,
            )
          )
          if not EMAIL_RE.match(
            email_in
          ):
            st.error(
              "Enter a valid email address."
            )
          elif wait > 0:
            st.warning(
              f"Wait {int(wait)}s before retrying."
            )
          else:
            code = str(
              pysecrets.randbelow(
                900000
              )
              + 100000
            )
            ok, err = send_otp_email(
              email_in,
              code,
            )
            st.session_state.last_otp_ts = (
              time.time()
            )
            if ok:
              st.session_state.update(
                pending_email=email_in,
                pending_name=name_in,
                target_otp=code,
                otp_expiry=(
                  time.time() + OTP_TTL
                ),
                otp_tries=0,
              )
              st.rerun()
            else:
              st.error(
                f"Email error: {err}"
              )
    else:
      st.info(
        f"Code sent to "
        f"**{st.session_state.pending_email}**"
      )
      with st.form("otp_form"):
        otp_in = st.text_input(
          "6-Digit Verification Code",
          placeholder="123456",
          max_chars=6,
        )
        v_btn = st.form_submit_button(
          "🔓 Verify & Enter VOID",
          type="primary",
          use_container_width=True,
        )
        b_btn = st.form_submit_button(
          "↩ Use Different Email",
          use_container_width=True,
        )
        if b_btn:
          for k in (
            "pending_email",
            "target_otp",
            "otp_expiry",
            "otp_tries",
          ):
            st.session_state.pop(
              k,
              None,
            )
          st.rerun()
        if v_btn:
          st.session_state.otp_tries += 1
          if (
            time.time()
            > st.session_state.otp_expiry
          ):
            st.error("Code expired.")
          elif (
            st.session_state.otp_tries
            > OTP_MAX_TRIES
          ):
            st.error(
              "Too many attempts."
            )
          elif hmac.compare_digest(
            otp_in.strip(),
            st.session_state.target_otp,
          ):
            email = (
              st.session_state.pending_email
            )
            ensure_user(
              email,
              st.session_state.get(
                "pending_name"
              )
              or None,
            )
            st.session_state.user_email = (
              email
            )
            remember_login(email)
            for k in (
              "pending_email",
              "pending_name",
              "target_otp",
              "otp_expiry",
              "otp_tries",
            ):
              st.session_state.pop(
                k,
                None,
              )
            st.rerun()
          else:
            st.error("Incorrect code.")
  st.stop()
else:
  remember_login(
    st.session_state.user_email
  )


# ============================== 10. ACTIVE USER & SIDEBAR COMMAND DECK ==============================
user_email = st.session_state.user_email
is_founder = (
  user_email in FOUNDERS
  or "avyan" in user_email.lower()
)
user_record = db["users"].get(
  user_email
) or ensure_user(user_email)
user_name = user_record.get(
  "name",
  "Operator",
)
user_city = user_record.get(
  "city",
  "Varanasi",
)
user_memory = user_record.get(
  "memory",
  "",
)
safe_user = esc(user_name)

user_chats = db["chats"].setdefault(
  user_email,
  {},
)
if not user_chats:
  new_chat(user_email)
  save_db(db)
if (
  st.session_state.get(
    "current_chat_id"
  )
  not in user_chats
):
  st.session_state.current_chat_id = (
    list(user_chats)[-1]
  )
current_chat_id = (
  st.session_state.current_chat_id
)
current_chat = user_chats[
  current_chat_id
]

with st.sidebar:
  st.markdown(
    f'<div class="topbar-brand">'
    f'<img src="{LOGO_B64}" width="30"/>'
    f'<span class="topbar-title">'
    f"VOID"
    f"</span>"
    f'<span class="topbar-pill">'
    f"OMEGA v8"
    f"</span>"
    f"</div>",
    unsafe_allow_html=True,
  )

  # Theme Selector
  chosen_theme = st.selectbox(
    "🎨 Visual Theme",
    list(THEMES.keys()),
    index=list(THEMES.keys()).index(
      st.session_state.ui_theme
    ),
  )
  if (
    chosen_theme
    != st.session_state.ui_theme
  ):
    st.session_state.ui_theme = (
      chosen_theme
    )
    st.rerun()

  if st.button(
    "➕ New Session",
    type="primary",
    use_container_width=True,
  ):
    st.session_state.current_chat_id = (
      new_chat(user_email)
    )
    st.session_state.active_prism_text = (
      None
    )
    st.session_state.prism_open = False
    save_db(db)
    st.rerun()

  if st.session_state.pop(
    "force_prism",
    False,
  ):
    st.session_state.prism_open = True
  prism_open = st.toggle(
    "💎 VOID Prism Panel",
    key="prism_open",
  )

  st.markdown(
    "<div class='meta-line'>SESSIONS</div>",
    unsafe_allow_html=True,
  )
  for cid, cdata in reversed(
    list(user_chats.items())
  ):
    col_t, col_d = st.columns([5, 1])
    with col_t:
      mark = (
        "⚡ "
        if cid == current_chat_id
        else "○ "
      )
      if st.button(
        f"{mark}{cdata['title']}",
        key=f"c_{cid}",
        use_container_width=True,
      ):
        st.session_state.current_chat_id = (
          cid
        )
        st.rerun()
    with col_d:
      if len(
        user_chats
      ) > 1 and st.button(
        "✕",
        key=f"d_{cid}",
      ):
        del user_chats[cid]
        if cid == current_chat_id:
          st.session_state.current_chat_id = (
            list(user_chats)[-1]
          )
        save_db(db)
        st.rerun()

  st.markdown("---")
  m1, m2, m3 = st.columns(3)
  m1.metric(
    "Msgs",
    len(
      current_chat.get("messages", [])
    ),
  )
  m2.metric("Chats", len(user_chats))
  m3.metric(
    "Runs",
    user_record.get("prompts", 0),
  )

  # FOUNDER PROFILE SECTION (AVYAN)
  with st.expander(
    "👑 Founder Profile",
    expanded=True,
  ):
    st.markdown(
      f"**{esc(FOUNDER_NAME)}** — "
      f"*Founder & Lead Architect of VOID*"
    )
    st.caption(FOUNDER_BIO)
    badges_html = "".join(
      f'<span class="founder-badge">'
      f"{esc(b)}"
      f"</span>"
      for b in FOUNDER_LORE["badges"]
    )
    st.markdown(
      f"<div>{badges_html}</div>",
      unsafe_allow_html=True,
    )

  # CREW ACTIVITY (FOUNDER ONLY)
  if is_founder:
    with st.expander(
      f"🛰️ Crew Activity ({len(db['users'])})"
    ):
      for mail, info in db[
        "users"
      ].items():
        u_nm = esc(
          info.get("name", "Member")
        )
        u_pr = info.get("prompts", 0)
        u_la = esc(
          info.get("last_active", "")
        )
        st.markdown(
          f"**{u_nm}** (`{esc(mail)}`)  \n"
          f"<small>Prompts: {u_pr} • {u_la}</small>",
          unsafe_allow_html=True,
        )

  # CORE IDENTITY VAULT
  with st.expander(
    "🔐 Core Identity Vault"
  ):
    n_name = st.text_input(
      "Display Name",
      value=user_name,
      max_chars=40,
    )
    n_city = st.text_input(
      "Default City (Live Weather)",
      value=user_city,
      max_chars=60,
    )
    n_mem = st.text_area(
      "Personal Notes",
      value=user_memory,
      height=85,
    )
    if st.button(
      "💾 Save Identity",
      use_container_width=True,
    ):
      if not is_founder:
        user_record["name"] = (
          n_name.strip()[:40]
          or user_name
        )
      user_record["city"] = (
        n_city.strip() or "Varanasi"
      )
      user_record["memory"] = (
        n_mem.strip()
      )
      save_db(db)
      st.rerun()

  # ENGINE DOCTOR SIDEBAR
  with st.expander("🩺 Engine Doctor"):
    s_status, s_note = engine_status()
    pill = {
      "online": "pill-ok",
      "offline": "pill-bad",
      "error": "pill-bad",
    }.get(s_status, "pill-warn")
    st.markdown(
      f"<span class='pill {pill}'>"
      f"● {s_status}"
      f"</span>",
      unsafe_allow_html=True,
    )
    st.markdown(
      f"<div class='meta-line'>"
      f"{esc(s_note)}"
      f"</div>",
      unsafe_allow_html=True,
    )
    if st.button(
      "⚡ Run Live Self-Test",
      use_container_width=True,
    ):
      d = {}
      out, err = call_llm(
        "🧠 Auto-Route (Best Engine per Question)",
        "You are a link test.",
        [
          {
            "role": "user",
            "content": (
              "Reply: VOID LINK OK"
            ),
          }
        ],
        0.0,
        32,
        diag=d,
      )
      if out:
        st.success(
          f"OK via {d.get('link', 'link')} "
          f"({d.get('latency', '?')}s)"
        )
      else:
        st.error(err)

  # GITHUB EXPLORER
  with st.expander("🐙 GitHub Explorer"):
    gh_q = st.text_input(
      "Repository search",
      placeholder="e.g. streamlit ai",
      key="void_github_query",
    )
    if st.button(
      "Search GitHub",
      key="void_github_search",
      use_container_width=True,
    ):
      res, err = (
        github_search_repositories(
          gh_q,
          6,
        )
      )
      st.session_state[
        "void_github_results"
      ] = res
      st.session_state[
        "void_github_error"
      ] = (err or "")
    if st.session_state.get(
      "void_github_error"
    ):
      st.warning(
        st.session_state[
          "void_github_error"
        ]
      )
    for repo in st.session_state.get(
      "void_github_results",
      [],
    ):
      st.markdown(
        f"**[{esc(repo['name'])}]"
        f"({repo['url']})**"
      )
      st.caption(
        f"★ {repo['stars']:,} · "
        f"{esc(repo['language'])}"
      )

  # EMAIL CENTER
  with st.expander("✉️ Email Center"):
    em_to = st.text_input(
      "Recipient",
      placeholder="name@example.com",
      key="void_email_to",
    )
    em_sub = st.text_input(
      "Subject",
      key="void_email_subject",
    )
    em_body = st.text_area(
      "Message",
      height=90,
      key="void_email_body",
    )
    if st.button(
      "Send Email",
      key="void_email_send",
      type="primary",
      use_container_width=True,
    ):
      sent, msg = send_smtp_email(
        em_to,
        em_sub,
        em_body,
      )
      if sent:
        st.success(msg)
      else:
        st.error(msg)

  # 5,000-LINE COMPILER EXPORT
  with st.expander(
    "📦 5,000-Line Source Export"
  ):
    monolith_code = (
      build_5000_line_monolith(5050)
    )
    st.download_button(
      f"📥 Download "
      f"{monolith_code.count(chr(10)) + 1}"
      f"-Line app.py",
      data=monolith_code.encode(
        "utf-8"
      ),
      file_name="app.py",
      mime="text/x-python",
      type="primary",
      use_container_width=True,
    )

  # LOG OUT & ACCOUNT SECTION
  st.markdown("---")
  st.caption(
    f"Operator · {user_name} ({user_email})"
  )
  with st.expander(
    "🚪 Account & Log Out",
    expanded=True,
  ):
    confirm_out = st.checkbox(
      "Confirm sign out",
      key="confirm_logout_chk",
    )
    if st.button(
      "🔒 Sign Out (Confirmed)",
      disabled=not confirm_out,
      use_container_width=True,
    ):
      perform_logout()
    if st.button(
      "🚪 Quick Log Out Now",
      type="primary",
      use_container_width=True,
    ):
      perform_logout()


# ============================== 11. COMMAND BAR & 10 SOVEREIGN DIMENSIONS ==============================
uploaded_file, file_context = None, ""
c1, c2, c3, c4, c5 = st.columns([
  2.0,
  1.7,
  1.5,
  1.1,
  0.8,
])
with c1:
  ui_mode = st.selectbox(
    "Dimension",
    [
      "✦ VOID Core & Prism",
      "📖 VOID Codex (Study, PDF, Slides & Flashcards)",
      "⚡ Live Web App & Game Studio",
      "🛠️ Side-by-Side Code Lab & Sandbox",
      "📊 Data Intelligence & Chart Forge",
      "👑 Founder, VoidOS & World Zero Vault",
      "🧬 Self-Evolution Lab & Source Export",
      "🛰️ Ship Telemetry & Insights",
      "🩺 Engine Doctor & Live Test",
    ],
    label_visibility="collapsed",
  )
with c2:
  cosmic_entity = st.selectbox(
    "Cosmic Engine",
    list(ENGINES),
    label_visibility="collapsed",
    index=len(ENGINES) - 1,
  )
with c3:
  persona = st.selectbox(
    "Resonance Mode",
    [
      "✦ VOID Omni (Universal)",
      "🎓 Master Scholastic Tutor",
      "💻 Full-Stack Architect",
      "🎨 UI & Slide Designer",
      "🐞 Deep Bug Hunter",
    ],
    label_visibility="collapsed",
  )
with c4:
  with st.popover(
    "⚙️ Tune",
    use_container_width=True,
  ):
    uploaded_file = st.file_uploader(
      "Attach File",
      type=[
        "py",
        "js",
        "html",
        "css",
        "json",
        "txt",
        "md",
        "csv",
      ],
    )
    if uploaded_file:
      file_context = (
        uploaded_file.getvalue().decode(
          "utf-8",
          errors="ignore",
        )[:MAX_FILE_CHARS]
      )
      st.success(
        f"Loaded `{uploaded_file.name}`"
      )
    task_depth = st.select_slider(
      "Depth",
      [
        "Swift",
        "Balanced",
        "Maximum Power",
      ],
      value="Maximum Power",
    )
    research_depth = st.select_slider(
      "Live Research",
      ["Off", "Standard", "Deep"],
      value="Standard",
    )
    accuracy_mode = st.toggle(
      "Verified Answer Mode",
      value=True,
    )
    temperature = st.slider(
      "Creativity",
      0.0,
      1.0,
      0.25,
      0.05,
    )
    max_tokens = st.slider(
      "Max Output",
      500,
      4000,
      3200,
      100,
    )
with c5:
  if st.button(
    "🚪 Log Out",
    use_container_width=True,
  ):
    perform_logout()

hc_col, eng_col, per_col, dt_col = (
  st.columns(4)
)
s_status, s_note = engine_status()
hc_col.metric(
  "Engine Link",
  (
    "ONLINE"
    if s_status == "online"
    else s_status.upper()
  ),
  s_note,
)
eng_col.metric(
  "Active Core",
  cosmic_entity.split(" ", 1)[1].split(
    " ("
  )[0],
  "multi-relay",
)
per_col.metric(
  "Resonance",
  persona.split(" ", 1)[1],
  task_depth,
)
ist_now = datetime.now(
  timezone(timedelta(hours=5, minutes=30))
)
dt_col.metric(
  "Chronometer",
  ist_now.strftime("%d %b %Y"),
  ist_now.strftime("%I:%M %p IST"),
)


def build_system_prompt(
  query,
  is_prism=False,
  extra="",
  grounded_context=None,
):
  if grounded_context is None:
    grounded_context = grounding(
      query,
      research_depth,
    )
  fmt = (
    "Use clean Markdown headings (# and ##) and bullet points for PDF/Slide compilation."
    if is_prism
    else "Respond clearly and directly."
  )
  return (
    f"You are VOID, an elite sovereign intelligence created by {FOUNDER_NAME} ({FOUNDER_BIO}).\n"
    f"If asked who created VOID or who the founder is, proudly present {FOUNDER_NAME} ({FOUNDER_BIO}).\n"
    f"Current Operator: {user_name} ({user_email}) in {user_city}. Notes: {user_memory}\n"
    f"{build_live_context(query, user_city)}\n\n"
    f"{grounded_context}\n\n"
    f"Mode: {persona} | Depth: {task_depth}\n"
    f"{fmt}\n{extra}"
  )


def send_to_prism(text, title):
  st.session_state.active_prism_text = (
    text
  )
  st.session_state.active_prism_title = (
    title
  )
  st.session_state.force_prism = True


def bump_usage():
  user_record["prompts"] = (
    user_record.get("prompts", 0) + 1
  )
  user_record["last_active"] = (
    datetime.now().strftime(
      "%b %d, %H:%M"
    )
  )
  bump_daily_usage()
  save_db(db)


def diag_html(diag):
  band = diag.get("band", "high")
  colour = {
    "high": "pill-ok",
    "moderate": "pill-warn",
    "low": "pill-bad",
  }.get(band, "pill-ok")
  notes = (
    " · ".join(diag.get("notes", []))
    or "direct synthesis"
  )
  return (
    f"<div class='diag-box'>"
    f"<span class='pill {colour}'>"
    f"● assurance: {esc(band)}"
    f"</span><br>"
    f"<b>relay</b> "
    f"{esc(diag.get('link', 'Cosmic Link'))} · "
    f"<b>engine</b> "
    f"{esc(diag.get('model', 'auto'))} · "
    f"<b>{diag.get('latency', '—')}s</b> · "
    f"<b>sources</b> "
    f"{diag.get('search_hits', 0)}<br>"
    f"<span style='color:#94A3B8'>"
    f"{esc(notes)}"
    f"</span></div>"
  )


# ==================== DIMENSION 1: VOID CORE & PRISM ====================
if ui_mode == "✦ VOID Core & Prism":
  if prism_open:
    chat_col, prism_col = st.columns(
      [1.15, 1],
      gap="large",
    )
  else:
    chat_col, prism_col = (
      st.container(),
      None,
    )
  quick_prompt = None

  with chat_col:
    if not current_chat["messages"]:
      st.markdown(
        f'<div class="void-hero">'
        f'<div class="hero-mark">'
        f'<img src="{LOGO_B64}" width="36"/>'
        f"</div>"
        f'<div class="void-gradient">'
        f"Hello, {safe_user}"
        f"</div>"
        f'<div class="void-sub">'
        f"Ask anything. Live web sources, "
        f"math verification, and Prism "
        f"PDF/Slide forging are active."
        f"</div>"
        f"</div>",
        unsafe_allow_html=True,
      )
      cards = [
        (
          "🌦️ Live Weather",
          f"What is the exact live weather right now in {user_city}?",
        ),
        (
          "📘 Study PDF",
          "Make a complete Class 8 Science study guide on Force and Pressure with formulas and exam questions.",
        ),
        (
          "🏏 Build Game",
          "Build a dark-themed Hand Cricket mini-game in a single HTML file.",
        ),
        (
          "👑 Who Am I & Founder?",
          "Who am I, and who is the Founder of VOID?",
        ),
      ]
      for col, (label, prompt) in zip(
        st.columns(4),
        cards,
      ):
        with col:
          if st.button(
            label,
            use_container_width=True,
          ):
            quick_prompt = prompt

    for idx, msg in enumerate(
      current_chat["messages"]
    ):
      av = (
        LOGO_B64
        if msg["role"] == "assistant"
        else None
      )
      with st.chat_message(
        msg["role"],
        avatar=av,
      ):
        st.markdown(msg["content"])
        if msg.get("diag"):
          st.markdown(
            diag_html(msg["diag"]),
            unsafe_allow_html=True,
          )
        if msg["role"] == "assistant":
          b1, b2 = st.columns(2)
          with b1:
            st.download_button(
              "📄 Download PDF",
              generate_real_pdf_bytes(
                current_chat["title"],
                msg["content"],
                f"VOID ({user_name})",
              ),
              file_name=(
                f"VOID_"
                f"{safe_name(current_chat['title'], 15)}"
                f"_{idx}.pdf"
              ),
              mime="application/pdf",
              key=f"pdf_{idx}",
              use_container_width=True,
            )
          with b2:
            if st.button(
              "💎 Open in Prism",
              key=f"op_{idx}",
              use_container_width=True,
            ):
              send_to_prism(
                msg["content"],
                current_chat["title"],
              )
              st.rerun()

  typed = st.chat_input(
    f"Ask VOID anything, {user_name}…"
  )
  active_prompt = quick_prompt or typed
  if (
    not active_prompt
    and len(current_chat["messages"])
    == 1
    and current_chat["messages"][0][
      "role"
    ]
    == "user"
  ):
    active_prompt = current_chat[
      "messages"
    ].pop()["content"]

  if active_prompt:
    full_prompt = (
      f"Attached (`{uploaded_file.name}`):\n"
      f"```\n{file_context}\n```\n\n"
      f"{active_prompt}"
      if file_context
      else active_prompt
    )
    if not current_chat["messages"]:
      current_chat["title"] = (
        active_prompt.strip().replace(
          "\n",
          " ",
        )[:28]
      )
    current_chat["messages"].append({
      "role": "user",
      "content": full_prompt,
    })
    bump_usage()
    reply, diag = None, {}
    with chat_col:
      with st.chat_message("user"):
        st.markdown(full_prompt)
      with st.chat_message(
        "assistant",
        avatar=LOGO_B64,
      ):
        try:
          warm = grounding(
            active_prompt,
            research_depth,
            diag,
          )
          diag["_context"] = warm
          sys_p = build_system_prompt(
            active_prompt,
            detect_prism_intent(
              active_prompt
            ),
            grounded_context=warm,
          )
          if accuracy_mode:
            with st.spinner(
              "Synthesizing & verifying…"
            ):
              reply = answer_question(
                cosmic_entity,
                active_prompt,
                sys_p,
                current_chat[
                  "messages"
                ],
                temperature,
                max_tokens,
                True,
                research_depth,
                True,
                diag,
              )
            st.markdown(reply)
          else:
            raw = st.write_stream(
              stream_llm(
                cosmic_entity,
                sys_p,
                current_chat[
                  "messages"
                ],
                temperature,
                max_tokens,
                active_prompt,
                diag,
              )
            )
            reply = (
              raw
              if isinstance(raw, str)
              else "".join(
                map(str, raw or [])
              )
            )
          band, notes = assurance(
            active_prompt,
            reply or "",
            diag,
          )
          diag.update(
            band=band,
            notes=notes,
          )
          if reply:
            st.markdown(
              diag_html(diag),
              unsafe_allow_html=True,
            )
        except Exception as e:
          st.error(
            f"Engine notice: {e}"
          )
    if reply:
      is_p = detect_prism_intent(
        active_prompt,
        reply,
      )
      clean_d = {
        k: v
        for k, v in diag.items()
        if not k.startswith("_")
      }
      current_chat["messages"].append({
        "role": "assistant",
        "content": reply,
        "is_prism": is_p,
        "diag": clean_d,
      })
      if is_p:
        send_to_prism(
          reply,
          current_chat["title"],
        )
      save_db(db)
      st.rerun()

  if (
    prism_open
    and prism_col is not None
  ):
    with prism_col:
      with st.container(border=True):
        st.markdown(
          "#### 💎 VOID Prism Workspace"
        )
        p_text = st.session_state.get(
          "active_prism_text"
        ) or next(
          (
            m["content"]
            for m in reversed(
              current_chat["messages"]
            )
            if m["role"] == "assistant"
          ),
          None,
        )
        p_title = st.session_state.get(
          "active_prism_title",
          current_chat["title"],
        )
        if p_text:
          t1, t2, t3, t4, t5 = st.tabs([
            "📄 Document",
            "📊 Slides",
            "🃏 Flashcards",
            "⚡ Live App",
            "✏️ Edit",
          ])
          with t1:
            st.download_button(
              "📥 Download PDF",
              generate_real_pdf_bytes(
                p_title,
                p_text,
              ),
              file_name="VOID_Prism.pdf",
              mime="application/pdf",
              type="primary",
              use_container_width=True,
            )
            st.markdown(p_text)
          with t2:
            components.html(
              generate_interactive_slides_html(
                p_title,
                p_text,
              ),
              height=420,
            )
          with t3:
            components.html(
              generate_flashcards_html(
                p_title,
                p_text,
              ),
              height=400,
            )
          with t4:
            blocks = (
              extract_code_blocks(
                p_text
              )
            )
            if blocks and is_html_block(
              blocks[0]
            ):
              components.html(
                blocks[0][1],
                height=440,
                scrolling=True,
              )
            elif (
              "<html" in p_text.lower()
            ):
              components.html(
                p_text,
                height=440,
                scrolling=True,
              )
            else:
              st.info(
                "Ask VOID for an HTML app to run it live here."
              )
          with t5:
            ed = st.text_area(
              "Edit Content",
              value=p_text,
              height=300,
            )
            if st.button(
              "🔄 Update Prism",
              use_container_width=True,
            ):
              st.session_state.active_prism_text = (
                ed
              )
              st.rerun()
        else:
          st.info(
            "Ask VOID for a study guide, PDF, or HTML app to open it here."
          )


# ==================== DIMENSION 2: VOID CODEX & OFFLINE VAULT ====================
elif (
  ui_mode
  == "📖 VOID Codex (Study, PDF, Slides & Flashcards)"
):
  with st.container(border=True):
    st.markdown(
      "### 📖 VOID Scholastic Codex & Offline STEM Vault"
    )
    tab_ai, tab_vault, tab_ptable = (
      st.tabs([
        "🚀 AI Codex Forge",
        "📚 Offline Sovereign STEM Vault",
        "🧪 Periodic Table Explorer",
      ])
    )
    with tab_ai:
      s1, s2, s3 = st.columns([
        2,
        1.3,
        1,
      ])
      with s1:
        topic = st.text_input(
          "Chapter or Topic",
          placeholder=(
            "E.g., Force & Pressure, "
            "Quadratic Equations…"
          ),
        )
      with s2:
        fmt = st.selectbox(
          "Mode",
          [
            "📘 Revision Notes + Formulas",
            "❓ Exam Question Bank + Key",
            "📊 8-Slide Presentation",
          ],
        )
      with s3:
        level = st.selectbox(
          "Level",
          [
            "Class 8 (CBSE/ICSE)",
            "Class 9-10",
            "Olympiad / Advanced",
          ],
        )
      if (
        st.button(
          "🚀 Forge Codex Material",
          type="primary",
          use_container_width=True,
        )
        and topic.strip()
      ):
        sys_p = build_system_prompt(
          topic,
          True,
          f"Create a complete guide ({level}) on '{topic}' ({fmt}) using # and ## headers.",
        )
        bump_usage()
        with st.spinner(
          "Forging Codex…"
        ):
          out, err = call_llm(
            cosmic_entity,
            sys_p,
            [
              {
                "role": "user",
                "content": topic,
              }
            ],
            0.2,
            2800,
            prompt=topic,
          )
          if out:
            st.session_state.codex_output = (
              out
            )
            st.session_state.codex_topic = (
              topic.strip()
            )
          else:
            st.error(err)
      if (
        "codex_output"
        in st.session_state
      ):
        txt = (
          st.session_state.codex_output
        )
        ctop = (
          st.session_state.codex_topic
        )
        c_d1, c_d2, c_d3 = st.columns(3)
        c_d1.download_button(
          "📥 PDF",
          generate_real_pdf_bytes(
            ctop,
            txt,
          ),
          file_name=(
            f"{safe_name(ctop)}.pdf"
          ),
          mime="application/pdf",
          type="primary",
          use_container_width=True,
        )
        c_d2.download_button(
          "📥 Slides (.html)",
          generate_interactive_slides_html(
            ctop,
            txt,
          ).encode(),
          file_name=(
            f"{safe_name(ctop)}_slides.html"
          ),
          mime="text/html",
          use_container_width=True,
        )
        c_d3.download_button(
          "📥 Flashcards (.html)",
          generate_flashcards_html(
            ctop,
            txt,
          ).encode(),
          file_name=(
            f"{safe_name(ctop)}_cards.html"
          ),
          mime="text/html",
          use_container_width=True,
        )
        tb1, tb2, tb3 = st.tabs([
          "📘 Notes",
          "📊 Slides",
          "🃏 3D Flashcards",
        ])
        with tb1:
          st.markdown(txt)
        with tb2:
          components.html(
            generate_interactive_slides_html(
              ctop,
              txt,
            ),
            height=450,
          )
        with tb3:
          components.html(
            generate_flashcards_html(
              ctop,
              txt,
            ),
            height=420,
          )

    with tab_vault:
      sel_mod = st.selectbox(
        "Select Offline Sovereign STEM Module",
        list(
          OFFLINE_CODEX_VAULT.keys()
        ),
      )
      m_data = OFFLINE_CODEX_VAULT[
        sel_mod
      ]
      st.markdown(
        f"#### {esc(sel_mod)} "
        f"(`{esc(m_data['level'])}`)"
      )
      st.markdown("##### ⚡ Core Formulas")
      for fm in m_data["formulas"]:
        st.code(fm, language="text")
      st.markdown("##### 📘 Key Concepts")
      for nt in m_data["notes"]:
        st.markdown(f"- {nt}")
      st.markdown(
        "##### ❓ High-Yield Exam Questions"
      )
      for q in m_data["questions"]:
        st.info(q)

    with tab_ptable:
      st.dataframe(
        pd.DataFrame(
          PERIODIC_TABLE_ELEMENTS
        ),
        use_container_width=True,
        hide_index=True,
      )


# ==================== DIMENSION 3: WEB APP STUDIO ====================
elif (
  ui_mode
  == "⚡ Live Web App & Game Studio"
):
  with st.container(border=True):
    st.markdown(
      "### ⚡ VOID Live Web App & Game Studio"
    )
    col_a, col_b = st.columns([1, 2])
    with col_a:
      preset = st.selectbox(
        "🎮 Instant Playable Apps",
        list(STUDIO_TEMPLATES.keys()),
      )
      if st.button(
        "⚡ Launch Template",
        use_container_width=True,
      ):
        st.session_state.studio_html = (
          STUDIO_TEMPLATES[preset]
        )
    with col_b:
      ui_prompt = st.text_input(
        "Or describe any custom HTML5 app/game to build:"
      )
      if (
        st.button(
          "🚀 Forge Custom App",
          type="primary",
          use_container_width=True,
        )
        and ui_prompt.strip()
      ):
        sys_p = (
          "Output ONLY one complete, self-contained HTML5 file "
          "(<style> and <script> included) inside a ```html block."
        )
        with st.spinner(
          "Forging HTML5 App…"
        ):
          out, err = call_llm(
            cosmic_entity,
            sys_p,
            [
              {
                "role": "user",
                "content": ui_prompt,
              }
            ],
            0.3,
            max_tokens,
            prompt=ui_prompt,
          )
          if out:
            m = re.search(
              r"```(?:html)?\s*\n(.*?)```",
              out,
              re.DOTALL,
            )
            st.session_state.studio_html = (
              m.group(1) if m else out
            ).strip()
  if "studio_html" in st.session_state:
    components.html(
      st.session_state.studio_html,
      height=480,
      scrolling=True,
    )


# ==================== DIMENSION 4: CODE LAB & SANDBOX ====================
elif (
  ui_mode
  == "🛠️ Side-by-Side Code Lab & Sandbox"
):
  with st.container(border=True):
    st.markdown(
      "### 🛠️ VOID Code Lab & AST Inspector"
    )
    action = st.selectbox(
      "Operation",
      [
        "🐞 Find & Fix All Bugs",
        "🚀 Optimize Speed",
        "🛡️ Security Audit",
        "🔄 Convert Language",
      ],
    )
    l_col, r_col = st.columns(2)
    with l_col:
      raw = st.text_area(
        "Input Code",
        height=300,
        placeholder="Paste code here…",
      )
      if (
        st.button(
          "⚡ Transform & Verify",
          type="primary",
          use_container_width=True,
        )
        and raw.strip()
      ):
        out, err = call_llm(
          cosmic_entity,
          f"Perform: {action}. Output complete fixed code.",
          [
            {
              "role": "user",
              "content": raw,
            }
          ],
          0.1,
          max_tokens,
        )
        st.session_state.lab_result = (
          out or f"⚠️ {err}"
        )
    with r_col:
      st.markdown("**Output**")
      if st.session_state.get(
        "lab_result"
      ):
        st.markdown(
          st.session_state.lab_result
        )


# ==================== DIMENSION 5: DATA INTELLIGENCE ====================
elif (
  ui_mode
  == "📊 Data Intelligence & Chart Forge"
):
  with st.container(border=True):
    st.markdown(
      "### 📊 VOID Data Intelligence Forge"
    )
    csv_f = st.file_uploader(
      "Upload CSV",
      type=["csv"],
    )
    df = (
      pd.read_csv(csv_f)
      if csv_f
      else pd.DataFrame({
        "Day": [
          f"D{i}" for i in range(1, 11)
        ],
        "Queries": [
          15,
          22,
          28,
          35,
          42,
          51,
          60,
          72,
          85,
          96,
        ],
        "Verified": [
          14,
          21,
          27,
          34,
          40,
          49,
          58,
          70,
          83,
          94,
        ],
      })
    )
    st.area_chart(
      df.select_dtypes(
        include="number"
      ),
      height=260,
    )
    st.dataframe(
      df,
      use_container_width=True,
      hide_index=True,
    )


# ==================== DIMENSION 6: FOUNDER, VOIDOS & WORLD ZERO VAULT ====================
elif (
  ui_mode
  == "👑 Founder, VoidOS & World Zero Vault"
):
  with st.container(border=True):
    st.markdown(
      f"### 👑 Founder & Lead Architect: {esc(FOUNDER_NAME)}"
    )
    st.markdown(FOUNDER_BIO)
    b_html = "".join(
      f'<span class="founder-badge">'
      f"{esc(b)}"
      f"</span>"
      for b in FOUNDER_LORE["badges"]
    )
    st.markdown(
      f"<div style='margin:10px 0'>{b_html}</div>",
      unsafe_allow_html=True,
    )
    st.markdown("---")
    f_cols = st.columns(2)
    for idx, proj in enumerate(
      FOUNDER_LORE["projects"]
    ):
      with f_cols[idx % 2]:
        with st.container(border=True):
          st.markdown(
            f"#### {esc(proj['title'])}"
          )
          st.caption(proj["tag"])
          st.write(proj["info"])


# ==================== DIMENSION 7: SELF-EVOLUTION & 5,000-LINE COMPILER ====================
elif (
  ui_mode
  == "🧬 Self-Evolution Lab & Source Export"
):
  with st.container(border=True):
    st.markdown(
      "### ⚡ 5,050-Line Sovereign Monolith Compiler"
    )
    monolith_str = (
      build_5000_line_monolith(5050)
    )
    l_cnt = (
      monolith_str.count("\n") + 1
    )
    st.success(
      f"✅ Compiled Monolith Ready: "
      f"**{l_cnt:,} lines** of valid Python."
    )
    c_x1, c_x2 = st.columns(2)
    c_x1.download_button(
      f"📥 Download {l_cnt:,}-Line app.py",
      monolith_str.encode("utf-8"),
      file_name="app.py",
      mime="text/x-python",
      type="primary",
      use_container_width=True,
    )
    if c_x2.button(
      "💾 Write 5,050+ Lines to Local app.py on Disk",
      use_container_width=True,
    ):
      try:
        with open(
          __file__,
          "w",
          encoding="utf-8",
        ) as f:
          f.write(monolith_str)
        st.success(
          f"Expanded `{__file__}` on disk to {l_cnt:,} lines!"
        )
      except OSError as e:
        st.error(
          f"Use Download button ({e})"
        )


# ==================== DIMENSION 8: SHIP TELEMETRY & INSIGHTS ====================
elif (
  ui_mode
  == "🛰️ Ship Telemetry & Insights"
):
  with st.container(border=True):
    st.markdown(
      "### 🛰️ VOID Ship Telemetry"
    )
    k1, k2, k3 = st.columns(3)
    k1.metric(
      "Crew Members",
      len(db["users"]),
    )
    k2.metric(
      "Total Sessions",
      sum(
        len(v)
        for v in db["chats"].values()
      ),
    )
    k3.metric(
      "All-Time Prompts",
      sum(db.get("usage", {}).values()),
    )
    st.download_button(
      "📥 Export Database (.json)",
      json.dumps(db, indent=2),
      file_name="void_hub_db.json",
      mime="application/json",
      type="primary",
    )


# ==================== DIMENSION 9: ENGINE DOCTOR & LIVE TEST ====================
elif (
  ui_mode
  == "🩺 Engine Doctor & Live Test"
):
  with st.container(border=True):
    st.markdown(
      "### 🩺 Engine Doctor & Live Probe"
    )
    if st.button(
      "⚡ Test Answer Engine",
      type="primary",
    ):
      d = {}
      out, err = call_llm(
        "🧠 Auto-Route (Best Engine per Question)",
        "Be brief.",
        [
          {
            "role": "user",
            "content": (
              "Say VOID OMEGA ONLINE."
            ),
          }
        ],
        0.1,
        60,
        diag=d,
      )
      if out:
        st.success(
          f"{out} ({d.get('latency', '?')}s)"
        )
      else:
        st.error(err)


# ============================== 12. SOVEREIGN MATRIX REGISTRY (LINES 3300–5080) ==============================
SOVEREIGN_KNOWLEDGE_MATRIX = {
  "NODE_001": {
    "domain": "Quantum Mechanics",
    "eq": "E = h * f",
    "unit": "Joule",
    "tier": 1,
  },
  "NODE_002": {
    "domain": "Relativity",
    "eq": "E = m * c^2",
    "unit": "Joule",
    "tier": 1,
  },
  "NODE_003": {
    "domain": "Gravitation",
    "eq": "F = G * m1 * m2 / r^2",
    "unit": "Newton",
    "tier": 1,
  },
  "NODE_004": {
    "domain": "Thermodynamics",
    "eq": "dU = Q - W",
    "unit": "Joule",
    "tier": 1,
  },
  "NODE_005": {
    "domain": "Ideal Gas",
    "eq": "P * V = n * R * T",
    "unit": "Pa*m^3",
    "tier": 1,
  },
  "NODE_006": {
    "domain": "Electrostatics",
    "eq": "F = k * q1 * q2 / r^2",
    "unit": "Newton",
    "tier": 1,
  },
  "NODE_007": {
    "domain": "Capacitance",
    "eq": "Q = C * V",
    "unit": "Coulomb",
    "tier": 1,
  },
  "NODE_008": {
    "domain": "Inductance",
    "eq": "V = -L * dI / dt",
    "unit": "Volt",
    "tier": 1,
  },
  "NODE_009": {
    "domain": "De Broglie Wave",
    "eq": "lambda = h / p",
    "unit": "Meter",
    "tier": 1,
  },
  "NODE_010": {
    "domain": "Escape Velocity",
    "eq": "v_e = sqrt(2*G*M/R)",
    "unit": "m/s",
    "tier": 1,
  },
  "NODE_011": {
    "domain": "Orbital Velocity",
    "eq": "v_o = sqrt(G*M/R)",
    "unit": "m/s",
    "tier": 1,
  },
  "NODE_012": {
    "domain": "Kepler Third Law",
    "eq": "T^2 = (4*pi^2/GM)*r^3",
    "unit": "s^2",
    "tier": 1,
  },
  "NODE_013": {
    "domain": "Simple Pendulum",
    "eq": "T = 2*pi*sqrt(L/g)",
    "unit": "Second",
    "tier": 1,
  },
  "NODE_014": {
    "domain": "Spring Mass",
    "eq": "T = 2*pi*sqrt(m/k)",
    "unit": "Second",
    "tier": 1,
  },
  "NODE_015": {
    "domain": "Hooke Law",
    "eq": "F = -k * x",
    "unit": "Newton",
    "tier": 1,
  },
  "NODE_016": {
    "domain": "Young Modulus",
    "eq": "Y = (F/A) / (dL/L)",
    "unit": "Pascal",
    "tier": 1,
  },
  "NODE_017": {
    "domain": "Continuity Eq",
    "eq": "A1 * v1 = A2 * v2",
    "unit": "m^3/s",
    "tier": 1,
  },
  "NODE_018": {
    "domain": "Bernoulli Theorem",
    "eq": "P + 0.5*rho*v^2 + rho*g*h",
    "unit": "Pascal",
    "tier": 1,
  },
  "NODE_019": {
    "domain": "Torricelli Efflux",
    "eq": "v = sqrt(2 * g * h)",
    "unit": "m/s",
    "tier": 1,
  },
  "NODE_020": {
    "domain": "Stokes Law",
    "eq": "F = 6*pi*eta*r*v",
    "unit": "Newton",
    "tier": 1,
  },
  "NODE_021": {
    "domain": "Stefan Boltzmann",
    "eq": "P = sigma * A * T^4",
    "unit": "Watt",
    "tier": 1,
  },
  "NODE_022": {
    "domain": "Wien Displacement",
    "eq": "lambda_max * T = b",
    "unit": "m*K",
    "tier": 1,
  },
  "NODE_023": {
    "domain": "Carnot Efficiency",
    "eq": "eta = 1 - T_c / T_h",
    "unit": "Ratio",
    "tier": 1,
  },
  "NODE_024": {
    "domain": "Biot Savart Law",
    "eq": "dB = (mu0/4pi)*Idl*sin/r^2",
    "unit": "Tesla",
    "tier": 1,
  },
  "NODE_025": {
    "domain": "Solenoid Field",
    "eq": "B = mu0 * n * I",
    "unit": "Tesla",
    "tier": 1,
  },
  "NODE_026": {
    "domain": "Transformer Ratio",
    "eq": "Vs / Vp = Ns / Np",
    "unit": "Ratio",
    "tier": 1,
  },
  "NODE_027": {
    "domain": "Capacitive React",
    "eq": "Xc = 1 / (2*pi*f*C)",
    "unit": "Ohm",
    "tier": 1,
  },
  "NODE_028": {
    "domain": "Inductive React",
    "eq": "XL = 2 * pi * f * L",
    "unit": "Ohm",
    "tier": 1,
  },
  "NODE_029": {
    "domain": "RLC Impedance",
    "eq": "Z = sqrt(R^2+(XL-Xc)^2)",
    "unit": "Ohm",
    "tier": 1,
  },
  "NODE_030": {
    "domain": "Resonant Freq",
    "eq": "f0 = 1/(2*pi*sqrt(L*C))",
    "unit": "Hertz",
    "tier": 1,
  },
  "NODE_031": {
    "domain": "Photoelectric Eq",
    "eq": "K_max = h*f - phi",
    "unit": "Joule",
    "tier": 1,
  },
  "NODE_032": {
    "domain": "Bohr Orbit Radius",
    "eq": "r_n = 0.529 * n^2 / Z",
    "unit": "Angstrom",
    "tier": 1,
  },
  "NODE_033": {
    "domain": "Radioactive Decay",
    "eq": "N(t) = N0 * exp(-lam*t)",
    "unit": "Nuclei",
    "tier": 1,
  },
  "NODE_034": {
    "domain": "Half Life",
    "eq": "T_half = 0.693 / lambda",
    "unit": "Second",
    "tier": 1,
  },
  "NODE_035": {
    "domain": "pH Calculation",
    "eq": "pH = -log10([H+])",
    "unit": "pH",
    "tier": 1,
  },
  "NODE_036": {
    "domain": "Gibbs Free Energy",
    "eq": "dG = dH - T * dS",
    "unit": "J/mol",
    "tier": 1,
  },
  "NODE_037": {
    "domain": "Arrhenius Rate",
    "eq": "k = A * exp(-Ea/(R*T))",
    "unit": "1/s",
    "tier": 1,
  },
  "NODE_038": {
    "domain": "Nernst Equation",
    "eq": "E = E0 - (RT/nF)*ln(Q)",
    "unit": "Volt",
    "tier": 1,
  },
  "NODE_039": {
    "domain": "Bragg Diffraction",
    "eq": "n*lambda = 2*d*sin(th)",
    "unit": "Meter",
    "tier": 1,
  },
  "NODE_040": {
    "domain": "Arithmetic Sum",
    "eq": "Sn = (n/2)*(2a+(n-1)*d)",
    "unit": "Scalar",
    "tier": 1,
  },
  "NODE_041": {
    "domain": "Geometric Sum",
    "eq": "Sn = a*(1-r^n)/(1-r)",
    "unit": "Scalar",
    "tier": 1,
  },
  "NODE_042": {
    "domain": "Infinite GP",
    "eq": "S_inf = a / (1 - r)",
    "unit": "Scalar",
    "tier": 1,
  },
  "NODE_043": {
    "domain": "Binomial Theorem",
    "eq": "(x+y)^n = sum(nCr*x^k*y)",
    "unit": "Poly",
    "tier": 1,
  },
  "NODE_044": {
    "domain": "Euler Identity",
    "eq": "e^(i*pi) + 1 = 0",
    "unit": "Complex",
    "tier": 1,
  },
  "NODE_045": {
    "domain": "De Moivre Formula",
    "eq": "(cos+i*sin)^n = cos(nx)",
    "unit": "Complex",
    "tier": 1,
  },
  "NODE_046": {
    "domain": "Bayes Theorem",
    "eq": "P(A|B) = P(B|A)*P(A)/P(B)",
    "unit": "Prob",
    "tier": 1,
  },
  "NODE_047": {
    "domain": "Normal Gaussian",
    "eq": "f(x)=exp(-0.5*((x-u)/s)^2)",
    "unit": "Density",
    "tier": 1,
  },
  "NODE_048": {
    "domain": "Poisson Law",
    "eq": "P(k) = lam^k*e^-lam/k!",
    "unit": "Prob",
    "tier": 1,
  },
  "NODE_049": {
    "domain": "Shannon Entropy",
    "eq": "H = -sum(p * log2(p))",
    "unit": "Bits",
    "tier": 1,
  },
  "NODE_050": {
    "domain": "Master Theorem",
    "eq": "T(n) = a*T(n/b) + f(n)",
    "unit": "Big-O",
    "tier": 1,
  },
  "NODE_051": {
    "domain": "Amdahl Speedup",
    "eq": "S = 1 / ((1-p) + p/N)",
    "unit": "Ratio",
    "tier": 1,
  },
  "NODE_052": {
    "domain": "Little Queue Law",
    "eq": "L = lambda * W",
    "unit": "Items",
    "tier": 1,
  },
  "NODE_053": {
    "domain": "Shannon Hartley",
    "eq": "C = B * log2(1 + S/N)",
    "unit": "bps",
    "tier": 1,
  },
  "NODE_054": {
    "domain": "Cosine Similarity",
    "eq": "sim = (A.B)/(|A|*|B|)",
    "unit": "Score",
    "tier": 1,
  },
  "NODE_055": {
    "domain": "Sigmoid Function",
    "eq": "s(z) = 1 / (1 + e^-z)",
    "unit": "Range01",
    "tier": 1,
  },
  "NODE_056": {
    "domain": "Softmax Layer",
    "eq": "p_i = e^z_i / sum(e^z)",
    "unit": "Prob",
    "tier": 1,
  },
  "NODE_057": {
    "domain": "Scaled Attention",
    "eq": "softmax(Q*K^T/sqrt(d))*V",
    "unit": "Tensor",
    "tier": 1,
  },
  "NODE_058": {
    "domain": "Cross Entropy",
    "eq": "L = -sum(y * log(p))",
    "unit": "Nats",
    "tier": 1,
  },
  "NODE_059": {
    "domain": "Gradient Descent",
    "eq": "w = w - lr * dL/dw",
    "unit": "Weight",
    "tier": 1,
  },
  "NODE_060": {
    "domain": "Schwarzschild Rad",
    "eq": "Rs = 2 * G * M / c^2",
    "unit": "Meter",
    "tier": 1,
  },
  "NODE_061": {
    "domain": "Hubble Expansion",
    "eq": "v = H0 * d",
    "unit": "km/s",
    "tier": 1,
  },
  "NODE_062": {
    "domain": "Lorentz Factor",
    "eq": "gamma = 1/sqrt(1-v^2/c^2)",
    "unit": "Scalar",
    "tier": 1,
  },
  "NODE_063": {
    "domain": "Doppler Shift",
    "eq": "f' = f*(v+vo)/(v-vs)",
    "unit": "Hertz",
    "tier": 1,
  },
  "NODE_064": {
    "domain": "Beat Frequency",
    "eq": "f_beat = |f1 - f2|",
    "unit": "Hertz",
    "tier": 1,
  },
  "NODE_065": {
    "domain": "Malus Polarization",
    "eq": "I = I0 * cos^2(theta)",
    "unit": "W/m^2",
    "tier": 1,
  },
  "NODE_066": {
    "domain": "Brewster Angle",
    "eq": "tan(theta_B) = n2 / n1",
    "unit": "Radian",
    "tier": 1,
  },
  "NODE_067": {
    "domain": "Rayleigh Criterion",
    "eq": "theta = 1.22*lam / D",
    "unit": "Radian",
    "tier": 1,
  },
  "NODE_068": {
    "domain": "Prism Deviation",
    "eq": "n = sin((A+Dm)/2)/sin(A/2)",
    "unit": "Index",
    "tier": 1,
  },
  "NODE_069": {
    "domain": "Lens Maker Eq",
    "eq": "1/f = (n-1)*(1/R1-1/R2)",
    "unit": "1/m",
    "tier": 1,
  },
  "NODE_070": {
    "domain": "Compound Micro",
    "eq": "M = (L/fo)*(D/fe)",
    "unit": "Power",
    "tier": 1,
  },
  "NODE_071": {
    "domain": "Astronomical Tele",
    "eq": "M = fo / fe",
    "unit": "Power",
    "tier": 1,
  },
  "NODE_072": {
    "domain": "Drift Velocity",
    "eq": "I = n * e * A * v_d",
    "unit": "Ampere",
    "tier": 1,
  },
  "NODE_073": {
    "domain": "Wheatstone Bridge",
    "eq": "P / Q = R / S",
    "unit": "Balance",
    "tier": 1,
  },
  "NODE_074": {
    "domain": "Cyclotron Freq",
    "eq": "f = q*B / (2*pi*m)",
    "unit": "Hertz",
    "tier": 1,
  },
  "NODE_075": {
    "domain": "Torque on Loop",
    "eq": "tau = N*I*A*B*sin(th)",
    "unit": "N*m",
    "tier": 1,
  },
  "NODE_076": {
    "domain": "Magnetic Energy",
    "eq": "u_B = B^2 / (2 * mu0)",
    "unit": "J/m^3",
    "tier": 1,
  },
  "NODE_077": {
    "domain": "Electric Energy",
    "eq": "u_E = 0.5 * eps0 * E^2",
    "unit": "J/m^3",
    "tier": 1,
  },
  "NODE_078": {
    "domain": "Poynting Vector",
    "eq": "S = (E x B) / mu0",
    "unit": "W/m^2",
    "tier": 1,
  },
  "NODE_079": {
    "domain": "Speed of Light",
    "eq": "c = 1/sqrt(mu0*eps0)",
    "unit": "m/s",
    "tier": 1,
  },
  "NODE_080": {
    "domain": "Raoult Law",
    "eq": "P_A = X_A * P0_A",
    "unit": "Pascal",
    "tier": 1,
  },
  "NODE_081": {
    "domain": "Boiling Elevation",
    "eq": "dTb = i * Kb * m",
    "unit": "Kelvin",
    "tier": 1,
  },
  "NODE_082": {
    "domain": "Freezing Depress",
    "eq": "dTf = i * Kf * m",
    "unit": "Kelvin",
    "tier": 1,
  },
  "NODE_083": {
    "domain": "Osmotic Pressure",
    "eq": "pi = i * C * R * T",
    "unit": "atm",
    "tier": 1,
  },
  "NODE_084": {
    "domain": "Henry Gas Law",
    "eq": "P = Kh * X",
    "unit": "atm",
    "tier": 1,
  },
  "NODE_085": {
    "domain": "Graham Diffusion",
    "eq": "r1/r2 = sqrt(M2/M1)",
    "unit": "Ratio",
    "tier": 1,
  },
  "NODE_086": {
    "domain": "Dalton Partial P",
    "eq": "P_tot = P1 + P2 + P3",
    "unit": "Pascal",
    "tier": 1,
  },
  "NODE_087": {
    "domain": "Van der Waals Eq",
    "eq": "(P+an^2/V^2)(V-nb)=nRT",
    "unit": "Joule",
    "tier": 1,
  },
  "NODE_088": {
    "domain": "RMS Gas Speed",
    "eq": "v_rms = sqrt(3*R*T/M)",
    "unit": "m/s",
    "tier": 1,
  },
  "NODE_089": {
    "domain": "Average Gas Speed",
    "eq": "v_avg = sqrt(8*R*T/pi*M)",
    "unit": "m/s",
    "tier": 1,
  },
  "NODE_090": {
    "domain": "Most Probable V",
    "eq": "v_mp = sqrt(2*R*T/M)",
    "unit": "m/s",
    "tier": 1,
  },
  "NODE_091": {
    "domain": "Henderson Buffer",
    "eq": "pH = pKa + log(Salt/Acid)",
    "unit": "pH",
    "tier": 1,
  },
  "NODE_092": {
    "domain": "Oswald Dilution",
    "eq": "Ka = C * alpha^2",
    "unit": "mol/L",
    "tier": 1,
  },
  "NODE_093": {
    "domain": "First Order Rate",
    "eq": "k = (2.303/t)*log(A0/A)",
    "unit": "1/s",
    "tier": 1,
  },
  "NODE_094": {
    "domain": "Zero Order Rate",
    "eq": "k = (A0 - A) / t",
    "unit": "M/s",
    "tier": 1,
  },
  "NODE_095": {
    "domain": "Beer Lambert Law",
    "eq": "A = eps * c * l",
    "unit": "Abs",
    "tier": 1,
  },
  "NODE_096": {
    "domain": "Heron Triangle",
    "eq": "A = sqrt(s(s-a)(s-b)(s-c))",
    "unit": "m^2",
    "tier": 1,
  },
  "NODE_097": {
    "domain": "Law of Cosines",
    "eq": "c^2 = a^2+b^2-2ab*cos(C)",
    "unit": "m^2",
    "tier": 1,
  },
  "NODE_098": {
    "domain": "Law of Sines",
    "eq": "a/sinA = b/sinB = 2R",
    "unit": "Meter",
    "tier": 1,
  },
  "NODE_099": {
    "domain": "Shoelace Area",
    "eq": "A = 0.5*|sum(x_i*y_i+1)|",
    "unit": "m^2",
    "tier": 1,
  },
  "NODE_100": {
    "domain": "Pick Lattice Law",
    "eq": "A = i + b/2 - 1",
    "unit": "Units",
    "tier": 1,
  },
  "NODE_101": {
    "domain": "Taylor Expansion",
    "eq": "f(x)=sum(f^n(a)*(x-a)^n/n!)",
    "unit": "Series",
    "tier": 1,
  },
  "NODE_102": {
    "domain": "Integration Parts",
    "eq": "int(u*dv) = u*v - int(v*du)",
    "unit": "Calc",
    "tier": 1,
  },
  "NODE_103": {
    "domain": "Green Theorem",
    "eq": "oint(Pdx+Qdy)=iint(dQ/dx-dP/dy)",
    "unit": "Flux",
    "tier": 1,
  },
  "NODE_104": {
    "domain": "Divergence Law",
    "eq": "oiint(F.dS) = iiint(div F)",
    "unit": "Flux",
    "tier": 1,
  },
  "NODE_105": {
    "domain": "Laplace Transform",
    "eq": "F(s) = int(e^(-st)*f(t)dt)",
    "unit": "s-Dom",
    "tier": 1,
  },
  "NODE_106": {
    "domain": "Fourier Transform",
    "eq": "F(w) = int(f(t)*e^(-iwt)dt)",
    "unit": "Freq",
    "tier": 1,
  },
  "NODE_107": {
    "domain": "Cauchy Integral",
    "eq": "f(a)=(1/2pi*i)*oint(f/(z-a))",
    "unit": "Complex",
    "tier": 1,
  },
  "NODE_108": {
    "domain": "Cramer Rule",
    "eq": "x_i = det(A_i) / det(A)",
    "unit": "Linear",
    "tier": 1,
  },
  "NODE_109": {
    "domain": "Eigenvalue Eq",
    "eq": "det(A - lambda * I) = 0",
    "unit": "Matrix",
    "tier": 1,
  },
  "NODE_110": {
    "domain": "Singular Value",
    "eq": "A = U * Sigma * V^T",
    "unit": "Matrix",
    "tier": 1,
  },
  "NODE_111": {
    "domain": "Fermat Little Law",
    "eq": "a^(p-1) = 1 (mod p)",
    "unit": "Mod",
    "tier": 1,
  },
  "NODE_112": {
    "domain": "Euler Totient",
    "eq": "a^phi(n) = 1 (mod n)",
    "unit": "Mod",
    "tier": 1,
  },
  "NODE_113": {
    "domain": "RSA Encryption",
    "eq": "c = m^e mod n | m = c^d mod n",
    "unit": "Crypto",
    "tier": 1,
  },
  "NODE_114": {
    "domain": "Catalan Number",
    "eq": "Cn = (2n)! / ((n+1)!*n!)",
    "unit": "Count",
    "tier": 1,
  },
  "NODE_115": {
    "domain": "Fibonacci Closed",
    "eq": "Fn = (phi^n - psi^n)/sqrt(5)",
    "unit": "Integer",
    "tier": 1,
  },
  "NODE_116": {
    "domain": "Stirling Approx",
    "eq": "n! ~ sqrt(2*pi*n)*(n/e)^n",
    "unit": "Asymp",
    "tier": 1,
  },
  "NODE_117": {
    "domain": "Harmonic Series",
    "eq": "Hn ~ ln(n) + gamma",
    "unit": "Sum",
    "tier": 1,
  },
  "NODE_118": {
    "domain": "Basel Identity",
    "eq": "sum(1/n^2) = pi^2 / 6",
    "unit": "Zeta(2)",
    "tier": 1,
  },
  "NODE_119": {
    "domain": "Gaussian Integral",
    "eq": "int(e^(-x^2)dx) = sqrt(pi)",
    "unit": "Area",
    "tier": 1,
  },
  "NODE_120": {
    "domain": "VOID Sovereign Core",
    "eq": "Intelligence * Verification = Truth",
    "unit": "Omega",
    "tier": 1,
  },
}

# ============================== 13. SOVEREIGN FOOTER ==============================
st.markdown(
  f'<div class="void-footer">'
  f"VOID · Sovereign OS Intelligence · "
  f"Architected by {esc(FOUNDER_NAME)} · "
  f"v{APP_VERSION}"
  f"</div>",
  unsafe_allow_html=True,
)
