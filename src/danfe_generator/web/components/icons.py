"""Ícones SVG para a aplicação Streamlit.

Este módulo contém ícones SVG inline no estilo Lucide (stroke-based).
Evita o uso de emojis, garantindo consistência visual entre plataformas.
"""

from __future__ import annotations

# =============================================================================
# SVG ICONS - Lucide Style (stroke-based, 24x24 default)
# =============================================================================

def _icon(paths: str, size: int = 20, color: str = "currentColor") -> str:
    """Gera um ícone SVG inline.

    Args:
        paths: Conteúdo SVG (paths, circles, etc).
        size: Tamanho em pixels.
        color: Cor do stroke.

    Returns:
        String HTML do ícone SVG.
    """
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display: inline-block; vertical-align: middle;">{paths}</svg>'


# =============================================================================
# NAVIGATION & UI ICONS
# =============================================================================


def icon_file_text(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de documento com texto (File Text)."""
    return _icon(
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
        '<polyline points="14 2 14 8 20 8"/>'
        '<line x1="16" y1="13" x2="8" y2="13"/>'
        '<line x1="16" y1="17" x2="8" y2="17"/>'
        '<polyline points="10 9 9 9 8 9"/>',
        size,
        color,
    )


def icon_upload(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de upload."""
    return _icon(
        '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
        '<polyline points="17 8 12 3 7 8"/>'
        '<line x1="12" y1="3" x2="12" y2="15"/>',
        size,
        color,
    )


def icon_folder(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de pasta."""
    return _icon(
        '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>',
        size,
        color,
    )


def icon_building(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de prédio/empresa."""
    return _icon(
        '<rect x="4" y="2" width="16" height="20" rx="2" ry="2"/>'
        '<line x1="9" y1="6" x2="9" y2="6.01"/>'
        '<line x1="15" y1="6" x2="15" y2="6.01"/>'
        '<line x1="9" y1="10" x2="9" y2="10.01"/>'
        '<line x1="15" y1="10" x2="15" y2="10.01"/>'
        '<line x1="9" y1="14" x2="9" y2="14.01"/>'
        '<line x1="15" y1="14" x2="15" y2="14.01"/>'
        '<line x1="9" y1="18" x2="15" y2="18"/>',
        size,
        color,
    )


def icon_user(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de usuário/pessoa."""
    return _icon(
        '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>'
        '<circle cx="12" cy="7" r="4"/>',
        size,
        color,
    )


def icon_package(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de pacote/produto."""
    return _icon(
        '<line x1="16.5" y1="9.4" x2="7.5" y2="4.21"/>'
        '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>'
        '<polyline points="3.27 6.96 12 12.01 20.73 6.96"/>'
        '<line x1="12" y1="22.08" x2="12" y2="12"/>',
        size,
        color,
    )


def icon_credit_card(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de cartão de crédito/pagamento."""
    return _icon(
        '<rect x="1" y="4" width="22" height="16" rx="2" ry="2"/>'
        '<line x1="1" y1="10" x2="23" y2="10"/>',
        size,
        color,
    )


def icon_file_check(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de documento com check (protocolo)."""
    return _icon(
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
        '<polyline points="14 2 14 8 20 8"/>'
        '<path d="M9 15l2 2 4-4"/>',
        size,
        color,
    )


def icon_plus(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de adicionar."""
    return _icon(
        '<line x1="12" y1="5" x2="12" y2="19"/>'
        '<line x1="5" y1="12" x2="19" y2="12"/>',
        size,
        color,
    )


def icon_trash(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de lixeira/remover."""
    return _icon(
        '<polyline points="3 6 5 6 21 6"/>'
        '<path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>'
        '<line x1="10" y1="11" x2="10" y2="17"/>'
        '<line x1="14" y1="11" x2="14" y2="17"/>',
        size,
        color,
    )


def icon_download(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de download."""
    return _icon(
        '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
        '<polyline points="7 10 12 15 17 10"/>'
        '<line x1="12" y1="15" x2="12" y2="3"/>',
        size,
        color,
    )


def icon_refresh(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de refresh/limpar."""
    return _icon(
        '<polyline points="23 4 23 10 17 10"/>'
        '<path d="M20.24 14a9 9 0 1 1-1.46-5.19L23 10"/>',
        size,
        color,
    )


def icon_check_circle(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de check dentro de círculo."""
    return _icon(
        '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>'
        '<polyline points="22 4 12 14.01 9 11.01"/>',
        size,
        color,
    )


def icon_x_circle(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de X dentro de círculo."""
    return _icon(
        '<circle cx="12" cy="12" r="10"/>'
        '<line x1="15" y1="9" x2="9" y2="15"/>'
        '<line x1="9" y1="9" x2="15" y2="15"/>',
        size,
        color,
    )


def icon_navigation(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de navegação/mapa."""
    return _icon(
        '<polygon points="3 11 22 2 13 21 11 13 3 11"/>',
        size,
        color,
    )


def icon_image(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de imagem/logo."""
    return _icon(
        '<rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>'
        '<circle cx="8.5" cy="8.5" r="1.5"/>'
        '<polyline points="21 15 16 10 5 21"/>',
        size,
        color,
    )


def icon_palette(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de paleta/cores."""
    return _icon(
        '<circle cx="13.5" cy="6.5" r=".5"/>'
        '<circle cx="17.5" cy="10.5" r=".5"/>'
        '<circle cx="8.5" cy="7.5" r=".5"/>'
        '<circle cx="6.5" cy="12.5" r=".5"/>'
        '<path d="M12 2a10 10 0 0 0 0 20c.73 0 1.4-.1 2.05-.28a1 1 0 0 0 .7-1.45l-1.31-2.63a1 1 0 0 1 .9-1.47h3.05a3 3 0 0 0 2.83-4A10 10 0 0 0 12 2z"/>',
        size,
        color,
    )


def icon_maximize(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de maximizar/margens."""
    return _icon(
        '<path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/>',
        size,
        color,
    )


def icon_search(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de busca."""
    return _icon(
        '<circle cx="11" cy="11" r="8"/>'
        '<line x1="21" y1="21" x2="16.65" y2="16.65"/>',
        size,
        color,
    )


def icon_info(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de informação."""
    return _icon(
        '<circle cx="12" cy="12" r="10"/>'
        '<line x1="12" y1="16" x2="12" y2="12"/>'
        '<line x1="12" y1="8" x2="12.01" y2="8"/>',
        size,
        color,
    )


def icon_diamond(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de diamante (marca)."""
    return _icon(
        '<path d="M2.7 10.3a2.41 2.41 0 0 0 0 3.41l7.59 7.59a2.41 2.41 0 0 0 3.41 0l7.59-7.59a2.41 2.41 0 0 0 0-3.41l-7.59-7.59a2.41 2.41 0 0 0-3.41 0Z"/>',
        size,
        color,
    )


def icon_edit(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de editar/criar."""
    return _icon(
        '<path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>'
        '<path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>',
        size,
        color,
    )


def icon_zap(size: int = 20, color: str = "currentColor") -> str:
    """Ícone de raio/energia."""
    return _icon(
        '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
        size,
        color,
    )
