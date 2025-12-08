"""Módulo de ícones SVG (Lucide) para a interface web.

Substitui o uso de emojis por ícones vetoriais consistentes e estilizados.
"""

from typing import Literal

# Cores do tema (referência cruzada com layout.py)
COLOR_PRIMARY = "#009739"
COLOR_VERDE_LIGHT = "#00C04B"
COLOR_GOLD = "#FFCC00"
COLOR_TEXT = "#D4D4E0"
COLOR_MUTED = "#79798A"


def get_svg(
    name: str,
    color: str = "currentColor",
    size: int = 24,
    stroke_width: float = 2,
) -> str:
    """Retorna o código SVG para um ícone específico.

    Args:
        name: Nome do ícone.
        color: Cor do stroke (hex ou var).
        size: Tamanho em pixels.
        stroke_width: Espessura da linha.
    """
    icons = {
        "upload-cloud": f"""<path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/><path d="M12 12v9"/><path d="m16 16-4-4-4 4"/>""",
        "file-plus": f"""<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M9 15h6"/><path d="M12 18v-6"/>""",
        "file-text": f"""<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>""",
        "building": f"""<rect width="16" height="20" x="4" y="2" rx="2" ry="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M8 10h.01"/><path d="M8 14h.01"/>""",
        "user": f"""<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>""",
        "package": f"""<path d="m16.5 9.4-9-5.19"/><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" x2="12" y1="22.08" y2="12"/>""",
        "credit-card": f"""<rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/>""",
        "shield-check": f"""<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>""",
        "check-circle": f"""<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>""",
        "alert-circle": f"""<circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/>""",
        "download": f"""<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/>""",
        "trash": f"""<path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>""",
        "refresh-cw": f"""<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>""",
        "diamond": f"""<path d="M2.7 10.3a2.41 2.41 0 0 0 0 3.41l7.59 7.59a2.41 2.41 0 0 0 3.41 0l7.59-7.59a2.41 2.41 0 0 0 0-3.41l-7.59-7.59a2.41 2.41 0 0 0-3.41 0Z"/>""",
        "compass": f"""<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>""",
        "image": f"""<rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>""",
        "palette": f"""<circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/>""",
        "layout": f"""<rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><line x1="3" x2="21" y1="9" y2="9"/><line x1="9" x2="9" y1="21" y2="9"/>""",
        "activity": f"""<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>""",
    }

    path = icons.get(name, icons["alert-circle"])

    return f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         width="{size}" height="{size}"
         viewBox="0 0 24 24"
         fill="none"
         stroke="{color}"
         stroke-width="{stroke_width}"
         stroke-linecap="round"
         stroke-linejoin="round"
         style="vertical-align: middle; margin-right: 8px; display: inline-block;">
        {path}
    </svg>
    """.strip()


def render_icon_text(
    icon_name: str,
    text: str,
    color: str = COLOR_TEXT,
    icon_color: str = COLOR_GOLD,
    size: int = 20,
    header: bool = False
) -> str:
    """Helper para renderizar ícone + texto alinhados."""

    style = ""
    if header:
        style = "font-family: var(--font-display); font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em;"

    svg = get_svg(icon_name, color=icon_color, size=size)

    return f"""
    <div style="display: flex; align-items: center; {style} color: {color};">
        {svg}
        <span>{text}</span>
    </div>
    """
