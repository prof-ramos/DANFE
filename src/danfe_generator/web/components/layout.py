"""Componentes de layout e CSS para a aplicação Streamlit.

Este módulo contém o tema "Fiscal Pro" e funções de layout reutilizáveis.
Design baseado em identidade fiscal brasileira com suporte a dark mode.
"""

from __future__ import annotations

import streamlit as st

from danfe_generator.web.components.icons import (
    icon_check_circle,
    icon_diamond,
    icon_folder,
    icon_image,
    icon_maximize,
    icon_navigation,
    icon_palette,
    icon_search,
    icon_zap,
)

# =============================================================================
# DESIGN SYSTEM - "Fiscal Pro" Theme
# =============================================================================

THEME_CSS = """
<style>
    /* ========================================
       FONTS - Modern Sans-serif with Preconnect
       ======================================== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ========================================
       CSS VARIABLES - Fiscal Pro Design Tokens
       ======================================== */
    :root {
        /* === LIGHT MODE (Default) === */
        /* Primary - Verde Fiscal (Brasil) */
        --color-primary: #009739;
        --color-primary-light: #00C04B;
        --color-primary-dark: #006B2B;

        /* Secondary - Azul Confiança */
        --color-secondary: #002776;
        --color-secondary-light: #0047AB;

        /* Accent - Dourado */
        --color-accent: #FFD700;
        --color-accent-muted: #E5C100;

        /* Neutrals */
        --color-background: #FFFFFF;
        --color-surface: #F8FAFC;
        --color-surface-elevated: #FFFFFF;
        --color-border: #E2E8F0;
        --color-border-hover: #CBD5E1;

        /* Text */
        --color-text-primary: #0F172A;
        --color-text-secondary: #475569;
        --color-text-muted: #94A3B8;

        /* Semantic */
        --color-success: #10B981;
        --color-success-bg: #ECFDF5;
        --color-error: #EF4444;
        --color-error-bg: #FEF2F2;
        --color-warning: #F59E0B;
        --color-warning-bg: #FFFBEB;
        --color-info: #3B82F6;
        --color-info-bg: #EFF6FF;

        /* Typography */
        --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        --font-mono: 'JetBrains Mono', 'Consolas', monospace;

        /* Spacing (8px grid) */
        --space-1: 4px;
        --space-2: 8px;
        --space-3: 12px;
        --space-4: 16px;
        --space-5: 20px;
        --space-6: 24px;
        --space-8: 32px;
        --space-10: 40px;
        --space-12: 48px;

        /* Radii */
        --radius-sm: 4px;
        --radius-md: 8px;
        --radius-lg: 12px;
        --radius-xl: 16px;
        --radius-full: 9999px;

        /* Shadows */
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);

        /* Transitions */
        --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* === DARK MODE === */
    /* Uses @media prefers-color-scheme for dark mode detection */
    @media (prefers-color-scheme: dark) {
        :root {
            /* Primary - Verde Fiscal (mais vibrante no dark) */
            --color-primary: #00C04B;
            --color-primary-light: #22D066;
            --color-primary-dark: #009739;

            /* Secondary - Azul Confiança */
            --color-secondary: #3B82F6;
            --color-secondary-light: #60A5FA;

            /* Accent - Dourado */
            --color-accent: #FBBF24;
            --color-accent-muted: #F59E0B;

            /* Neutrals - Dark */
            --color-background: #0F172A;
            --color-surface: #1E293B;
            --color-surface-elevated: #334155;
            --color-border: #334155;
            --color-border-hover: #475569;

            /* Text - Dark */
            --color-text-primary: #F1F5F9;
            --color-text-secondary: #CBD5E1;
            --color-text-muted: #64748B;

            /* Semantic - Dark */
            --color-success-bg: rgba(16, 185, 129, 0.15);
            --color-error-bg: rgba(239, 68, 68, 0.15);
            --color-warning-bg: rgba(245, 158, 11, 0.15);
            --color-info-bg: rgba(59, 130, 246, 0.15);
        }
    }

    /* ========================================
       GLOBAL STYLES
       ======================================== */
    .stApp {
        background-color: var(--color-background) !important;
        font-family: var(--font-sans) !important;
        color: var(--color-text-primary) !important;
    }

    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }

    /* Main content area */
    .main .block-container {
        padding: var(--space-8) var(--space-6) !important;
        max-width: 1100px !important;
    }

    /* ========================================
       TYPOGRAPHY
       ======================================== */
    h1, h2, h3, .main-title {
        font-family: var(--font-sans) !important;
        color: var(--color-text-primary) !important;
        letter-spacing: -0.025em;
    }

    h1 {
        font-size: 2.25rem !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
        margin-bottom: var(--space-6) !important;
    }

    h2 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        line-height: 1.3 !important;
        margin-top: var(--space-8) !important;
        margin-bottom: var(--space-4) !important;
    }

    h3 {
        font-size: 1.125rem !important;
        font-weight: 600 !important;
        color: var(--color-text-secondary) !important;
        margin-bottom: var(--space-3) !important;
    }

    p, .stMarkdown {
        font-family: var(--font-sans) !important;
        font-size: 1rem !important;
        font-weight: 400 !important;
        line-height: 1.6 !important;
        color: var(--color-text-secondary) !important;
    }

    label {
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        color: var(--color-text-primary) !important;
    }

    /* ========================================
       SIDEBAR
       ======================================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--color-surface) 0%, var(--color-background) 100%) !important;
        border-right: 1px solid var(--color-border) !important;
    }

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding: var(--space-4) !important;
    }

    [data-testid="stSidebar"] hr {
        margin: var(--space-5) 0 !important;
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, var(--color-border), transparent) !important;
    }

    .sidebar-section-title {
        font-family: var(--font-sans);
        font-size: 0.6875rem;
        color: var(--color-text-muted);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
        margin-bottom: var(--space-3);
        display: flex;
        align-items: center;
        gap: var(--space-2);
    }

    .sidebar-section-title svg {
        opacity: 0.7;
    }

    /* ========================================
       COMPONENTS - Buttons
       ======================================== */
    .stButton > button {
        font-family: var(--font-sans) !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        border-radius: var(--radius-md) !important;
        padding: var(--space-3) var(--space-5) !important;
        transition: all var(--transition-base) !important;
        border: 1px solid transparent !important;
        cursor: pointer !important;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%) !important;
        color: white !important;
        box-shadow: var(--shadow-md), 0 0 0 0 var(--color-primary) !important;
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg), 0 0 20px rgba(0, 151, 57, 0.3) !important;
    }

    .stButton > button[kind="primary"]:active {
        transform: translateY(0) !important;
    }

    .stButton > button[kind="secondary"],
    .stButton > button:not([kind="primary"]) {
        background-color: var(--color-surface) !important;
        border: 1px solid var(--color-border) !important;
        color: var(--color-text-primary) !important;
    }

    .stButton > button[kind="secondary"]:hover,
    .stButton > button:not([kind="primary"]):hover {
        background-color: var(--color-surface-elevated) !important;
        border-color: var(--color-border-hover) !important;
        transform: translateY(-1px) !important;
    }

    /* Download Button */
    .stDownloadButton > button {
        font-family: var(--font-sans) !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        border-radius: var(--radius-md) !important;
        padding: var(--space-3) var(--space-5) !important;
        transition: all var(--transition-base) !important;
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%) !important;
        color: white !important;
        border: none !important;
        cursor: pointer !important;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg), 0 0 20px rgba(0, 151, 57, 0.3) !important;
    }

    /* ========================================
       COMPONENTS - Inputs
       ======================================== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > div > textarea {
        background-color: var(--color-surface) !important;
        border: 1px solid var(--color-border) !important;
        border-radius: var(--radius-md) !important;
        color: var(--color-text-primary) !important;
        font-family: var(--font-sans) !important;
        transition: all var(--transition-fast) !important;
    }

    .stTextInput > div > div > input:hover,
    .stNumberInput > div > div > input:hover,
    .stSelectbox > div > div:hover,
    .stTextArea > div > div > textarea:hover {
        border-color: var(--color-border-hover) !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--color-primary) !important;
        box-shadow: 0 0 0 3px rgba(0, 151, 57, 0.15) !important;
        outline: none !important;
    }

    /* Placeholder */
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: var(--color-text-muted) !important;
    }

    /* ========================================
       COMPONENTS - File Uploader
       ======================================== */
    [data-testid="stFileUploader"] > div {
        background: linear-gradient(135deg, var(--color-surface) 0%, var(--color-background) 100%) !important;
        border: 2px dashed var(--color-border) !important;
        border-radius: var(--radius-lg) !important;
        transition: all var(--transition-base) !important;
    }

    [data-testid="stFileUploader"] > div:hover {
        background: var(--color-surface-elevated) !important;
        border-color: var(--color-primary) !important;
        box-shadow: 0 0 0 4px rgba(0, 151, 57, 0.1) !important;
    }

    /* ========================================
       COMPONENTS - Expander
       ======================================== */
    .streamlit-expanderHeader {
        font-family: var(--font-sans) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        color: var(--color-text-primary) !important;
        background-color: var(--color-surface) !important;
        border-radius: var(--radius-md) !important;
        padding: var(--space-4) !important;
        transition: all var(--transition-fast) !important;
    }

    .streamlit-expanderHeader:hover {
        background-color: var(--color-surface-elevated) !important;
    }

    [data-testid="stExpander"] {
        border: 1px solid var(--color-border) !important;
        border-radius: var(--radius-lg) !important;
        overflow: hidden !important;
        margin-bottom: var(--space-4) !important;
    }

    /* ========================================
       COMPONENTS - Metrics
       ======================================== */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, var(--color-surface) 0%, var(--color-surface-elevated) 100%) !important;
        border: 1px solid var(--color-border) !important;
        border-radius: var(--radius-lg) !important;
        padding: var(--space-4) !important;
        transition: all var(--transition-base) !important;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-md) !important;
    }

    [data-testid="stMetric"] label {
        color: var(--color-text-muted) !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--color-text-primary) !important;
        font-weight: 700 !important;
        font-family: var(--font-mono) !important;
    }

    /* ========================================
       COMPONENTS - Alerts
       ======================================== */
    .stSuccess, .stError, .stInfo, .stWarning {
        padding: var(--space-4) !important;
        border-radius: var(--radius-md) !important;
        border: none !important;
        font-family: var(--font-sans) !important;
    }

    .stSuccess {
        background-color: var(--color-success-bg) !important;
        color: var(--color-success) !important;
        border-left: 4px solid var(--color-success) !important;
    }

    .stError {
        background-color: var(--color-error-bg) !important;
        color: var(--color-error) !important;
        border-left: 4px solid var(--color-error) !important;
    }

    .stInfo {
        background-color: var(--color-info-bg) !important;
        color: var(--color-info) !important;
        border-left: 4px solid var(--color-info) !important;
    }

    .stWarning {
        background-color: var(--color-warning-bg) !important;
        color: var(--color-warning) !important;
        border-left: 4px solid var(--color-warning) !important;
    }

    /* ========================================
       COMPONENTS - Radio Buttons
       ======================================== */
    .stRadio > div {
        gap: var(--space-2) !important;
    }

    .stRadio > div > label {
        background-color: var(--color-surface) !important;
        border: 1px solid var(--color-border) !important;
        border-radius: var(--radius-md) !important;
        padding: var(--space-3) var(--space-4) !important;
        transition: all var(--transition-fast) !important;
        cursor: pointer !important;
    }

    .stRadio > div > label:hover {
        background-color: var(--color-surface-elevated) !important;
        border-color: var(--color-primary) !important;
    }

    .stRadio > div > label[data-checked="true"] {
        background-color: rgba(0, 151, 57, 0.1) !important;
        border-color: var(--color-primary) !important;
        color: var(--color-primary) !important;
    }

    /* ========================================
       CUSTOM COMPONENTS
       ======================================== */

    /* Hide Streamlit header/toolbar */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        backdrop-filter: none !important;
    }

    /* Hide hamburger menu decoration bar */
    [data-testid="stHeader"]::before,
    [data-testid="stHeader"]::after {
        display: none !important;
    }

    .hero-container {
        background: var(--color-background);
        padding: var(--space-8) 0;
        margin-bottom: var(--space-6);
        border-bottom: 1px solid var(--color-border);
        position: relative;
    }

    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--color-primary), var(--color-accent), var(--color-secondary));
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--color-text-primary);
        letter-spacing: -0.03em;
        margin-bottom: var(--space-3);
        display: flex;
        align-items: center;
        gap: var(--space-3);
    }

    .hero-title svg {
        color: var(--color-primary);
    }

    .hero-subtitle {
        font-size: 1.125rem;
        color: var(--color-text-secondary);
        max-width: 600px;
        line-height: 1.6;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: var(--space-2);
        background: linear-gradient(135deg, rgba(0, 151, 57, 0.1) 0%, rgba(0, 39, 118, 0.1) 100%);
        border: 1px solid rgba(0, 151, 57, 0.2);
        padding: var(--space-2) var(--space-4);
        border-radius: var(--radius-full);
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--color-primary);
        margin-top: var(--space-5);
        font-family: var(--font-mono);
    }

    .footer {
        text-align: center;
        padding: var(--space-10) 0;
        margin-top: var(--space-12);
        border-top: 1px solid var(--color-border);
        color: var(--color-text-muted);
        font-size: 0.875rem;
    }

    .footer-brand {
        font-family: var(--font-mono);
        font-weight: 600;
        color: var(--color-text-secondary);
        margin-top: var(--space-2);
    }

    /* File count badge */
    .file-count-badge {
        display: inline-flex;
        align-items: center;
        gap: var(--space-2);
        background: var(--color-success-bg);
        border: 1px solid var(--color-success);
        border-radius: var(--radius-full);
        padding: var(--space-2) var(--space-4);
        font-family: var(--font-mono);
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--color-success);
        margin: var(--space-4) 0;
    }

    .file-count-badge svg {
        color: var(--color-success);
    }

    /* Processing status */
    .processing-status {
        font-family: var(--font-mono);
        color: var(--color-accent);
        font-size: 0.875rem;
        display: flex;
        align-items: center;
        gap: var(--space-2);
    }

    .processing-status::before {
        content: '';
        width: 8px;
        height: 8px;
        background-color: var(--color-accent);
        border-radius: 50%;
        animation: pulse 1s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(0.8); }
    }

    /* Empty state */
    .empty-state {
        text-align: center;
        padding: var(--space-12);
        color: var(--color-text-muted);
    }

    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: var(--space-4);
        opacity: 0.5;
    }

    .empty-state-icon svg {
        width: 64px;
        height: 64px;
        color: var(--color-text-muted);
    }

    .empty-state-title {
        font-size: 1.125rem;
        font-weight: 500;
        color: var(--color-text-secondary);
        margin-bottom: var(--space-2);
    }

    .empty-state-subtitle {
        font-size: 0.875rem;
        color: var(--color-text-muted);
    }

    /* Sidebar Logo */
    .sidebar-logo {
        text-align: center;
        padding: var(--space-4) 0;
    }

    .sidebar-logo-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
        border-radius: var(--radius-lg);
        margin-bottom: var(--space-2);
    }

    .sidebar-logo-icon svg {
        color: white;
        width: 24px;
        height: 24px;
    }

    .sidebar-logo-text {
        font-family: var(--font-sans);
        font-size: 1rem;
        font-weight: 700;
        color: var(--color-text-primary);
    }

    .sidebar-logo-text span {
        color: var(--color-primary);
    }

    .sidebar-version {
        font-family: var(--font-mono);
        font-size: 0.625rem;
        color: var(--color-text-muted);
        background-color: var(--color-surface);
        padding: 2px 8px;
        border-radius: var(--radius-full);
        margin-top: var(--space-1);
        display: inline-block;
    }
</style>
"""


def setup_page(title: str = "DANFE Generator") -> None:
    """Configura a página Streamlit com tema Fiscal Pro.

    Args:
        title: Título da página.
    """
    st.set_page_config(
        page_title=title,
        page_icon="◆",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def render_hero(
    title: str = "DANFE Generator",
    subtitle: str = "Transforme seus XMLs de Nota Fiscal Eletrônica em documentos DANFE personalizados.",
    badge: str = "Sistema Fiscal Brasileiro • NF-e 4.00",
) -> None:
    """Renderiza seção hero com design impactante.

    Args:
        title: Título principal.
        subtitle: Subtítulo descritivo.
        badge: Texto do badge.
    """
    diamond_icon = icon_diamond(size=32, color="var(--color-primary)")
    st.markdown(
        f"""
        <div class="hero-container">
            <div class="hero-title">
                {diamond_icon}
                {title}
            </div>
            <div class="hero-subtitle">{subtitle}</div>
            <div class="hero-badge">
                {icon_zap(size=14)} {badge}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_logo() -> None:
    """Renderiza logo na sidebar com design moderno."""
    diamond_icon = icon_diamond(size=24, color="white")
    st.markdown(
        f"""
        <div class="sidebar-logo">
            <div class="sidebar-logo-icon">
                {diamond_icon}
            </div>
            <div class="sidebar-logo-text">
                DANFE<span>GEN</span>
            </div>
            <div class="sidebar-version">v0.2.0</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_title(title: str, icon_html: str = "") -> None:
    """Renderiza título de seção estilizado.

    Args:
        title: Texto do título.
        icon_html: HTML do ícone SVG (opcional).
    """
    # Map common section titles to icons
    icon_map = {
        "NAVEGAÇÃO": icon_navigation(size=14),
        "LOGOTIPO": icon_image(size=14),
        "CORES DO DANFE": icon_palette(size=14),
        "MARGENS (mm)": icon_maximize(size=14),
        "CONSULTA NCM": icon_search(size=14),
        "CONSULTA CFOP": icon_search(size=14),
    }
    icon = icon_map.get(title, icon_html)
    st.markdown(
        f'<div class="sidebar-section-title">{icon} {title}</div>',
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Renderiza footer com branding."""
    st.markdown(
        """
        <div class="footer">
            <div>Desenvolvido para o ecossistema fiscal brasileiro</div>
            <div class="footer-brand">DANFE GENERATOR • NF-e 4.00</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_file_count_badge(count: int) -> None:
    """Renderiza badge com contagem de arquivos.

    Args:
        count: Número de arquivos.
    """
    check_icon = icon_check_circle(size=16, color="var(--color-success)")
    st.markdown(
        f"""
        <div class="file-count-badge">
            {check_icon}
            {count} arquivo(s) carregado(s)
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_processing_status(filename: str) -> None:
    """Renderiza status de processamento.

    Args:
        filename: Nome do arquivo sendo processado.
    """
    st.markdown(
        f"""
        <div class="processing-status">
            Processando: {filename}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(
    icon: str = "",  # noqa: ARG001 - Kept for API compatibility, SVG used instead
    title: str = "Nenhum arquivo selecionado.",
    subtitle: str = "Faça upload de arquivos XML para começar.",
) -> None:
    """Renderiza estado vazio estilizado.

    Args:
        icon: Emoji/ícone (ignorado, usamos SVG - mantido para compatibilidade).
        title: Título do estado vazio.
        subtitle: Subtítulo/instrução.
    """
    folder_icon = icon_folder(size=64, color="var(--color-text-muted)")
    st.markdown(
        f"""
        <div class="empty-state">
            <div class="empty-state-icon">
                {folder_icon}
            </div>
            <div class="empty-state-title">{title}</div>
            <div class="empty-state-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
