"""View de upload de XML - Funcionalidade existente refatorada.

Este módulo implementa a view de upload de arquivos XML
para geração de DANFE a partir de XMLs existentes.
"""

from __future__ import annotations

import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING

import streamlit as st

from danfe_generator.core import ColorsConfig, DANFEConfig, DANFEGenerator, MarginsConfig
from danfe_generator.web.components.layout import (
    render_empty_state,
    render_file_count_badge,
    render_hero,
    render_processing_status,
)

if TYPE_CHECKING:
    from streamlit.runtime.uploaded_file_manager import UploadedFile


@contextmanager
def temporary_file(suffix: str = "") -> Iterator[Path]:
    """Context manager para arquivos temporários com limpeza automática."""
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = Path(tmp.name)
        yield tmp_path
    finally:
        if tmp_path and tmp_path.exists():
            tmp_path.unlink()


def render_upload_view(
    logo_path: Path | None,
    colors: ColorsConfig,
    margins: MarginsConfig,
) -> None:
    """Renderiza view de upload de XML para geração de DANFE.

    Args:
        logo_path: Caminho para o logo (opcional).
        colors: Configuração de cores.
        margins: Configuração de margens.
    """
    render_hero(
        title="Gerar DANFE",
        subtitle="Faça upload de arquivos XML de NF-e para gerar os DANFEs correspondentes.",
        badge="Upload de XML • NF-e 4.00",
    )

    # Upload section
    from danfe_generator.web.components.icons import render_icon_text, get_svg, COLOR_GOLD, COLOR_PRIMARY

    st.markdown(render_icon_text("file-text", "ARQUIVOS XML", header=True), unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Arraste seus arquivos XML de NF-e para esta área",
        type=["xml"],
        accept_multiple_files=True,
        help="Suporta múltiplos arquivos • Layout NF-e 4.00",
        key="xml_upload",
    )

    if not uploaded_files:
        render_empty_state(
            icon=get_svg("upload-cloud", size=64, color="#79798A"),
            title="Nenhum arquivo selecionado.",
            subtitle="Faça upload de arquivos XML para começar.",
        )
        return

    render_file_count_badge(len(uploaded_files))

    # Generate button
    if st.button(
        "GERAR DANFES",
        type="primary",
        use_container_width=True,
        key="btn_generate_upload",
    ):
        _process_files(uploaded_files, logo_path, colors, margins)


def _process_files(
    uploaded_files: list[UploadedFile],
    logo_path: Path | None,
    colors: ColorsConfig,
    margins: MarginsConfig,
) -> None:
    """Processa arquivos e gera DANFEs com feedback visual."""
    from danfe_generator.web.components.icons import render_icon_text, get_svg, COLOR_PRIMARY

    config = DANFEConfig(
        logo_path=logo_path,
        margins=margins,
        colors=colors,
    )
    generator = DANFEGenerator(config)

    progress = st.progress(0)
    status_text = st.empty()

    results_container = st.container()
    success_count = 0
    error_count = 0

    for idx, uploaded_file in enumerate(uploaded_files):
        with status_text:
            render_processing_status(uploaded_file.name)
        progress.progress((idx + 1) / len(uploaded_files))

        try:
            with temporary_file(suffix=".xml") as xml_path:
                xml_path.write_bytes(uploaded_file.getvalue())

                with temporary_file(suffix=".pdf") as pdf_path:
                    result = generator.generate(xml_path, pdf_path)

                    if result.success:
                        pdf_bytes = pdf_path.read_bytes()

                        with results_container:
                            col1, col2 = st.columns([4, 1])
                            with col1:
                                st.markdown(
                                    render_icon_text("check-circle", uploaded_file.name, icon_color=COLOR_PRIMARY),
                                    unsafe_allow_html=True
                                )
                            with col2:
                                # Usar índice para garantir chave única
                                st.download_button(
                                    label="⬇ PDF",
                                    data=pdf_bytes,
                                    file_name=f"{Path(uploaded_file.name).stem}.pdf",
                                    mime="application/pdf",
                                    key=f"download_{idx}_{uploaded_file.name}",
                                )
                        success_count += 1
                    else:
                        with results_container:
                            st.error(f"Erro em {uploaded_file.name}: {result.error_message}")
                        error_count += 1

        except Exception as e:
            with results_container:
                st.error(f"Erro em {uploaded_file.name}: {e}")
            error_count += 1

    progress.empty()
    status_text.empty()

    # Metrics
    st.markdown("---")
    st.markdown(render_icon_text("activity", "RESUMO DO PROCESSAMENTO", header=True), unsafe_allow_html=True)

    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.metric("TOTAL", len(uploaded_files))
    with col_s2:
        st.metric("SUCESSO", success_count)
    with col_s3:
        st.metric("ERROS", error_count)

    # Cleanup temp logo is handled by app.py now
