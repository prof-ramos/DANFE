"""Componentes de layout e CSS para a aplicação Streamlit.

Este módulo contém o tema "Fiscal Dark" e funções de layout reutilizáveis.
"""

from __future__ import annotations

import streamlit as st

# =============================================================================
# DESIGN SYSTEM - "Fiscal Dark" Theme
# =============================================================================

THEME_CSS = """
<style>
    /* ========================================
       FONTS - Distinctive Typography
       ======================================== */
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;1,400&display=swap');

    /* ========================================
       CSS VARIABLES - Design Tokens
       ======================================== */
    :root {
        /* Primary Palette - Verde Bandeira */
        --fiscal-verde: #009739;
        --fiscal-verde-dark: #006B2B;
        --fiscal-verde-light: #00C04B;

        /* Secondary - Azul Petróleo */
        --fiscal-azul: #002654;
        --fiscal-azul-deep: #001A3A;
        --fiscal-azul-light: #003D7A;

        /* Accent - Dourado */
        --fiscal-gold: #FFCC00;
        --fiscal-gold-dim: #D4A800;
        --fiscal-gold-bright: #FFD633;

        /* Neutrals - Tons de Carbono */
        --carbon-900: #0D0D0F;
        --carbon-800: #151518;
        --carbon-700: #1C1C21;
        --carbon-600: #252529;
        --carbon-500: #35353C;
        --carbon-400: #52525E;
        --carbon-300: #79798A;
        --carbon-200: #A1A1B3;
        --carbon-100: #D4D4E0;
        --carbon-50: #F0F0F5;

        /* Semantic */
        --success: #00D26A;
        --error: #FF4757;
        --warning: #FFA502;
        --info: #00B4D8;

        /* Typography */
        --font-display: 'Sora', sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
        --font-body: 'Crimson Pro', serif;

        /* Spacing */
        --space-xs: 0.25rem;
        --space-sm: 0.5rem;
        --space-md: 1rem;
        --space-lg: 1.5rem;
        --space-xl: 2rem;
        --space-2xl: 3rem;

        /* Radii */
        --radius-sm: 4px;
        --radius-md: 8px;
        --radius-lg: 12px;
        --radius-xl: 20px;

        /* Shadows */
        --shadow-glow: 0 0 40px rgba(0, 151, 57, 0.15);
        --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.4);
        --shadow-hover: 0 8px 32px rgba(0, 151, 57, 0.2);
    }

    /* ========================================
       ANIMATIONS - High Impact Moments
       ======================================== */
    @keyframes fadeSlideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 151, 57, 0.3); }
        50% { box-shadow: 0 0 40px rgba(0, 151, 57, 0.5); }
    }

    @keyframes grid-move {
        0% { background-position: 0 0; }
        100% { background-position: 40px 40px; }
    }

    /* ========================================
       GLOBAL STYLES
       ======================================== */
    .stApp {
        background:
            linear-gradient(135deg, var(--carbon-900) 0%, var(--fiscal-azul-deep) 50%, var(--carbon-900) 100%),
            repeating-linear-gradient(
                0deg,
                transparent,
                transparent 39px,
                rgba(0, 151, 57, 0.03) 39px,
                rgba(0, 151, 57, 0.03) 40px
            ),
            repeating-linear-gradient(
                90deg,
                transparent,
                transparent 39px,
                rgba(0, 151, 57, 0.03) 39px,
                rgba(0, 151, 57, 0.03) 40px
            );
        background-attachment: fixed;
        animation: grid-move 60s linear infinite;
    }

    /* Main content area */
    .main .block-container {
        padding: var(--space-xl) var(--space-lg);
        max-width: 1200px;
    }

    /* ========================================
       TYPOGRAPHY
       ======================================== */
    h1, h2, h3, .main-title {
        font-family: var(--font-display) !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    h1 {
        font-size: 2.75rem !important;
        background: linear-gradient(135deg, var(--fiscal-verde-light) 0%, var(--fiscal-gold) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: fadeSlideUp 0.8s ease-out;
    }

    h2 {
        font-size: 1.5rem !important;
        color: var(--carbon-100) !important;
        animation: fadeSlideUp 0.8s ease-out 0.1s both;
    }

    h3 {
        font-size: 1.1rem !important;
        color: var(--fiscal-gold) !important;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        font-weight: 600 !important;
        animation: fadeSlideUp 0.8s ease-out 0.2s both;
    }

    p, .stMarkdown {
        font-family: var(--font-body) !important;
        font-size: 1.1rem;
        color: var(--carbon-200) !important;
        line-height: 1.7;
    }

    /* ========================================
       HERO SECTION
       ======================================== */
    .hero-container {
        background: linear-gradient(135deg,
            rgba(0, 151, 57, 0.1) 0%,
            rgba(0, 38, 84, 0.2) 50%,
            rgba(0, 0, 0, 0) 100%
        );
        border: 1px solid rgba(0, 151, 57, 0.2);
        border-radius: var(--radius-xl);
        padding: var(--space-2xl);
        margin-bottom: var(--space-xl);
        position: relative;
        overflow: hidden;
        animation: fadeSlideUp 0.6s ease-out;
    }

    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg,
            var(--fiscal-verde) 0%,
            var(--fiscal-gold) 50%,
            var(--fiscal-verde) 100%
        );
    }

    .hero-title {
        font-family: var(--font-display);
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg,
            var(--carbon-50) 0%,
            var(--fiscal-verde-light) 50%,
            var(--fiscal-gold) 100%
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: var(--space-md);
        letter-spacing: -0.03em;
    }

    .hero-subtitle {
        font-family: var(--font-body);
        font-size: 1.25rem;
        color: var(--carbon-300);
        font-style: italic;
        max-width: 600px;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: var(--space-sm);
        background: rgba(0, 151, 57, 0.15);
        border: 1px solid var(--fiscal-verde);
        border-radius: 100px;
        padding: var(--space-sm) var(--space-md);
        font-family: var(--font-mono);
        font-size: 0.75rem;
        color: var(--fiscal-verde-light);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: var(--space-lg);
    }

    /* ========================================
       SIDEBAR
       ======================================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg,
            var(--carbon-800) 0%,
            var(--fiscal-azul-deep) 100%
        ) !important;
        border-right: 1px solid rgba(0, 151, 57, 0.15);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        -webkit-text-fill-color: var(--carbon-100) !important;
        background: none !important;
    }

    .sidebar-section {
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 204, 0, 0.1);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
        margin-bottom: var(--space-md);
    }

    .sidebar-section-title {
        font-family: var(--font-display);
        font-size: 0.85rem;
        color: var(--fiscal-gold);
        text-transform: uppercase;
        letter-spacing: 0.2em;
        font-weight: 600;
        margin-bottom: var(--space-md);
        display: flex;
        align-items: center;
        gap: var(--space-sm);
    }

    /* ========================================
       FILE UPLOADER
       ======================================== */
    [data-testid="stFileUploader"] {
        animation: fadeSlideUp 0.8s ease-out 0.3s both;
    }

    [data-testid="stFileUploader"] > div {
        background: rgba(0, 151, 57, 0.05) !important;
        border: 2px dashed var(--fiscal-verde) !important;
        border-radius: var(--radius-xl) !important;
        transition: all 0.3s ease;
    }

    [data-testid="stFileUploader"] > div:hover {
        background: rgba(0, 151, 57, 0.1) !important;
        border-color: var(--fiscal-gold) !important;
        box-shadow: var(--shadow-glow);
    }

    [data-testid="stFileUploader"] label {
        font-family: var(--font-display) !important;
        color: var(--carbon-100) !important;
    }

    /* ========================================
       BUTTONS
       ======================================== */
    .stButton > button {
        font-family: var(--font-display) !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        border-radius: var(--radius-lg) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative;
        overflow: hidden;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg,
            var(--fiscal-verde) 0%,
            var(--fiscal-verde-dark) 100%
        ) !important;
        border: none !important;
        color: white !important;
        box-shadow: 0 4px 20px rgba(0, 151, 57, 0.3);
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 151, 57, 0.4);
        background: linear-gradient(135deg,
            var(--fiscal-verde-light) 0%,
            var(--fiscal-verde) 100%
        ) !important;
    }

    .stButton > button[kind="primary"]::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg,
            transparent,
            rgba(255, 255, 255, 0.2),
            transparent
        );
        transition: left 0.5s ease;
    }

    .stButton > button[kind="primary"]:hover::after {
        left: 100%;
    }

    /* Download button special styling */
    .stDownloadButton > button {
        background: transparent !important;
        border: 2px solid var(--fiscal-gold) !important;
        color: var(--fiscal-gold) !important;
        font-family: var(--font-mono) !important;
    }

    .stDownloadButton > button:hover {
        background: var(--fiscal-gold) !important;
        color: var(--carbon-900) !important;
    }

    /* ========================================
       INPUTS & FORM ELEMENTS
       ======================================== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background: var(--carbon-700) !important;
        border: 1px solid var(--carbon-500) !important;
        border-radius: var(--radius-md) !important;
        color: var(--carbon-100) !important;
        font-family: var(--font-mono) !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--fiscal-verde) !important;
        box-shadow: 0 0 0 2px rgba(0, 151, 57, 0.2) !important;
    }

    /* ========================================
       METRICS & STATS
       ======================================== */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg,
            rgba(0, 151, 57, 0.1) 0%,
            rgba(0, 38, 84, 0.15) 100%
        );
        border: 1px solid rgba(0, 151, 57, 0.2);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
        animation: fadeSlideUp 0.8s ease-out both;
    }

    [data-testid="stMetric"]:nth-child(1) { animation-delay: 0.1s; }
    [data-testid="stMetric"]:nth-child(2) { animation-delay: 0.2s; }
    [data-testid="stMetric"]:nth-child(3) { animation-delay: 0.3s; }

    [data-testid="stMetric"] label {
        font-family: var(--font-display) !important;
        color: var(--carbon-300) !important;
        text-transform: uppercase;
        font-size: 0.75rem !important;
        letter-spacing: 0.15em;
    }

    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-family: var(--font-mono) !important;
        font-size: 2.5rem !important;
        color: var(--fiscal-verde-light) !important;
        font-weight: 600;
    }

    /* ========================================
       ALERTS & FEEDBACK
       ======================================== */
    .stSuccess {
        background: linear-gradient(135deg,
            rgba(0, 210, 106, 0.1) 0%,
            rgba(0, 151, 57, 0.05) 100%
        ) !important;
        border-left: 4px solid var(--success) !important;
        border-radius: var(--radius-md) !important;
    }

    .stError {
        background: linear-gradient(135deg,
            rgba(255, 71, 87, 0.1) 0%,
            rgba(200, 0, 30, 0.05) 100%
        ) !important;
        border-left: 4px solid var(--error) !important;
        border-radius: var(--radius-md) !important;
    }

    .stInfo {
        background: linear-gradient(135deg,
            rgba(0, 180, 216, 0.1) 0%,
            rgba(0, 38, 84, 0.1) 100%
        ) !important;
        border-left: 4px solid var(--info) !important;
        border-radius: var(--radius-md) !important;
    }

    /* ========================================
       EXPANDER (Accordion sections)
       ======================================== */
    .streamlit-expanderHeader {
        background: rgba(0, 151, 57, 0.05) !important;
        border: 1px solid rgba(0, 151, 57, 0.2) !important;
        border-radius: var(--radius-md) !important;
        font-family: var(--font-display) !important;
        font-weight: 600 !important;
        color: var(--fiscal-gold) !important;
    }

    .streamlit-expanderHeader:hover {
        background: rgba(0, 151, 57, 0.1) !important;
        border-color: var(--fiscal-verde) !important;
    }

    .streamlit-expanderContent {
        border: 1px solid rgba(0, 151, 57, 0.1) !important;
        border-top: none !important;
        border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
        background: rgba(0, 0, 0, 0.2) !important;
    }

    /* ========================================
       DATA EDITOR / TABLE
       ======================================== */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(0, 151, 57, 0.2) !important;
        border-radius: var(--radius-md) !important;
    }

    /* ========================================
       RESULT CARD
       ======================================== */
    .result-card {
        background: linear-gradient(135deg,
            rgba(0, 0, 0, 0.3) 0%,
            rgba(0, 151, 57, 0.05) 100%
        );
        border: 1px solid rgba(0, 151, 57, 0.15);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
        margin: var(--space-md) 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        animation: fadeSlideUp 0.5s ease-out;
    }

    .result-card.success {
        border-left: 4px solid var(--success);
    }

    .result-card.error {
        border-left: 4px solid var(--error);
    }

    .result-filename {
        font-family: var(--font-mono);
        color: var(--carbon-100);
        font-size: 0.9rem;
    }

    /* ========================================
       PROGRESS BAR
       ======================================== */
    .stProgress > div > div > div {
        background: linear-gradient(90deg,
            var(--fiscal-verde) 0%,
            var(--fiscal-gold) 100%
        ) !important;
        border-radius: 100px !important;
        box-shadow: 0 0 20px rgba(0, 151, 57, 0.5);
    }

    .stProgress > div > div {
        background: var(--carbon-700) !important;
        border-radius: 100px !important;
    }

    /* ========================================
       DIVIDER
       ======================================== */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg,
            transparent 0%,
            var(--fiscal-verde) 50%,
            transparent 100%
        ) !important;
        margin: var(--space-xl) 0 !important;
    }

    /* ========================================
       TABS
       ======================================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: var(--space-sm);
        background: rgba(0, 0, 0, 0.2);
        border-radius: var(--radius-lg);
        padding: var(--space-xs);
    }

    .stTabs [data-baseweb="tab"] {
        font-family: var(--font-display) !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--carbon-300) !important;
        border-radius: var(--radius-md) !important;
        transition: all 0.3s ease !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--fiscal-gold) !important;
        background: rgba(0, 151, 57, 0.1) !important;
    }

    .stTabs [aria-selected="true"] {
        background: var(--fiscal-verde) !important;
        color: white !important;
    }

    /* ========================================
       FOOTER
       ======================================== */
    .footer {
        text-align: center;
        padding: var(--space-xl) 0;
        margin-top: var(--space-2xl);
        border-top: 1px solid rgba(0, 151, 57, 0.1);
    }

    .footer-text {
        font-family: var(--font-body);
        font-style: italic;
        color: var(--carbon-400);
        font-size: 0.95rem;
    }

    .footer-brand {
        font-family: var(--font-display);
        color: var(--fiscal-gold);
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        margin-top: var(--space-sm);
    }

    /* ========================================
       RESPONSIVE
       ======================================== */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        h1 {
            font-size: 2rem !important;
        }
    }
</style>
"""


def setup_page(title: str = "DANFE Generator | Fiscal Dark") -> None:
    """Configura a página Streamlit com tema Fiscal Dark.

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
    st.markdown(
        f"""
        <div class="hero-container">
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
            <div class="hero-badge">
                <span>◆</span> {badge}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_logo() -> None:
    """Renderiza logo na sidebar."""
    st.markdown(
        """
        <div style="text-align: center; padding: 1rem 0;">
            <span style="font-size: 2.5rem;">◆</span>
            <div style="font-family: 'Sora', sans-serif; font-size: 1.1rem;
                 font-weight: 700; color: #D4D4E0; margin-top: 0.5rem;">
                DANFE<span style="color: #FFCC00;">GEN</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_title(title: str, icon: str = "◇") -> None:
    """Renderiza título de seção estilizado.

    Args:
        title: Texto do título.
        icon: Ícone opcional.
    """
    st.markdown(
        f'<div class="sidebar-section-title">{icon} {title}</div>',
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Renderiza footer com branding."""
    st.markdown(
        """
        <div class="footer">
            <div class="footer-text">
                Desenvolvido para o ecossistema fiscal brasileiro
            </div>
            <div class="footer-brand">
                DANFE GENERATOR • NF-e 4.00
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_file_count_badge(count: int) -> None:
    """Renderiza badge com contagem de arquivos.

    Args:
        count: Número de arquivos.
    """
    st.markdown(
        f"""
        <div style="display: inline-flex; align-items: center; gap: 0.5rem;
             background: rgba(0, 151, 57, 0.1); border: 1px solid rgba(0, 151, 57, 0.3);
             border-radius: 100px; padding: 0.5rem 1rem; margin: 1rem 0;
             font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; color: #00C04B;">
            <span>◆</span> {count} arquivo(s) carregado(s)
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
        <div style="font-family: 'JetBrains Mono', monospace; color: #FFCC00; font-size: 0.85rem;">
            ⟳ Processando: {filename}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(
    icon: str = "📁",
    title: str = "Nenhum arquivo selecionado.",
    subtitle: str = "Faça upload de arquivos XML para começar.",
) -> None:
    """Renderiza estado vazio estilizado.

    Args:
        icon: Emoji/ícone.
        title: Título do estado vazio.
        subtitle: Subtítulo/instrução.
    """
    st.markdown(
        f"""
        <div style="text-align: center; padding: 3rem; color: #79798A;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
            <div style="font-family: 'Crimson Pro', serif; font-size: 1.2rem; font-style: italic;">
                {title}<br/>{subtitle}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
