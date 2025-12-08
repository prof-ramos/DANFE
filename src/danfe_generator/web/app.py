"""Interface Web Streamlit para o DANFE Generator.

Este módulo implementa a aplicação web principal com design "Fiscal Dark",
servindo como ponto de entrada que roteia entre as diferentes views.

Views disponíveis:
    - Upload XML: Upload de arquivos XML existentes para geração de DANFE
    - Criar NF-e: Formulário completo para criar NF-e do zero

Para executar:
    $ streamlit run src/danfe_generator/web/app.py
    # ou
    $ ./run_app.sh

A aplicação estará disponível em http://localhost:8501 por padrão.
Para configurar outra porta, use: streamlit run ... --server.port 8080
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st

from danfe_generator.core import ColorsConfig, MarginsConfig
from danfe_generator.utils.colors import hex_to_rgb
from danfe_generator.web.components.layout import (
    render_footer,
    render_section_title,
    render_sidebar_logo,
    setup_page,
)
from danfe_generator.web.views.create import render_create_view
from danfe_generator.web.views.upload import render_upload_view

# ============================================================================
# Constants
# ============================================================================

VIEW_UPLOAD = "upload"
VIEW_CREATE = "create"

DEFAULT_PRIMARY_COLOR = "#009739"
DEFAULT_SECONDARY_COLOR = "#002654"
DEFAULT_ACCENT_COLOR = "#FFCC00"


# ============================================================================
# Sidebar Configuration
# ============================================================================


def _render_sidebar() -> tuple[Path | None, ColorsConfig, MarginsConfig, str]:
    """Renderiza sidebar com configurações.

    Returns:
        Tupla com (logo_path, colors, margins, selected_view).
    """
    with st.sidebar:
        render_sidebar_logo()

        # Navegação
        st.markdown("---")
        render_section_title("NAVEGAÇÃO", "compass")

        view_options = {
            VIEW_UPLOAD: "Upload XML",
            VIEW_CREATE: "Criar NF-e",
        }

        selected_view = st.radio(
            "Selecione a funcionalidade",
            options=list(view_options.keys()),
            format_func=lambda x: view_options[x],
            key="view_selector",
            label_visibility="collapsed",
        )

        # Logo upload
        st.markdown("---")
        render_section_title("LOGOTIPO", "image")

        logo_path = None
        logo_file = st.file_uploader(
            "Logo da empresa (PNG/JPG)",
            type=["png", "jpg", "jpeg"],
            help="Recomendado: 150x150px • Fundo transparente",
            key="logo_uploader",
        )

        if logo_file:
            # Gerenciamento de arquivo temporário com limpeza
            # Verifica se já existe um arquivo anterior na sessão e remove
            if "logo_tmp_path" in st.session_state:
                old_path = Path(st.session_state["logo_tmp_path"])
                if old_path.exists():
                    try:
                        old_path.unlink()
                    except OSError:
                        pass  # Ignora erro se não conseguir remover

            # Cria novo arquivo temporário
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=Path(logo_file.name).suffix,
            ) as tmp:
                tmp.write(logo_file.getvalue())
                logo_path = Path(tmp.name)
                st.session_state["logo_tmp_path"] = str(logo_path)

        # Cores
        st.markdown("---")
        render_section_title("CORES DO DANFE", "palette")

        col1, col2 = st.columns(2)
        with col1:
            primary_color = st.color_picker(
                "Primária",
                DEFAULT_PRIMARY_COLOR,
                key="color_primary",
            )
        with col2:
            secondary_color = st.color_picker(
                "Secundária",
                DEFAULT_SECONDARY_COLOR,
                key="color_secondary",
            )

        accent_color = st.color_picker(
            "Acento",
            DEFAULT_ACCENT_COLOR,
            key="color_accent",
        )

        colors = ColorsConfig(
            primary=hex_to_rgb(primary_color),
            secondary=hex_to_rgb(secondary_color),
            accent=hex_to_rgb(accent_color),
        )

        # Margens
        st.markdown("---")
        render_section_title("MARGENS (mm)", "layout")

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            margin_top = st.number_input("Superior", 5, 30, 10, key="margin_top")
            margin_left = st.number_input("Esquerda", 5, 30, 10, key="margin_left")
        with col_m2:
            margin_bottom = st.number_input("Inferior", 5, 30, 10, key="margin_bottom")
            margin_right = st.number_input("Direita", 5, 30, 10, key="margin_right")

        margins = MarginsConfig(
            top=margin_top,
            bottom=margin_bottom,
            left=margin_left,
            right=margin_right,
        )

        # Sobre
        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center; padding: 1rem 0; font-size: 0.75rem; color: #79798A;">
                <div style="font-family: 'JetBrains Mono', monospace;">v0.2.0</div>
                <div style="margin-top: 0.5rem;">NF-e 4.00 Compliant</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return logo_path, colors, margins, selected_view


# ============================================================================
# Main Application
# ============================================================================


def main() -> None:
    """Ponto de entrada principal da aplicação Streamlit."""
    setup_page(title="DANFE Generator | Fiscal Dark")

    try:
        # Configurações da sidebar
        logo_path, colors, margins, selected_view = _render_sidebar()

        # Roteamento de views
        if selected_view == VIEW_UPLOAD:
            render_upload_view(logo_path, colors, margins)
        elif selected_view == VIEW_CREATE:
            render_create_view(logo_path, colors, margins)

        # Footer
        render_footer()

    finally:
        # Limpeza final de arquivos temporários ao encerrar sessão/script
        # Nota: Streamlit roda o script inteiro a cada interação, então isso
        # só limpa se ocorrer uma exceção não tratada ou fim de execução.
        # A limpeza principal do logo está no _render_sidebar.
        pass


if __name__ == "__main__":
    main()
