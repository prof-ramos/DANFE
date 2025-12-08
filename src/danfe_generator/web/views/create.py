"""View de criação de NF-e.

Este módulo implementa a interface de formulário para criar
uma NF-e do zero, gerando XML e PDF.
"""

from __future__ import annotations

import io
import tempfile
import zipfile
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import streamlit as st

from danfe_generator.core import ColorsConfig, DANFEConfig, DANFEGenerator, MarginsConfig
from danfe_generator.web.components.layout import render_hero
from danfe_generator.web.logic.models import (
    DestinoOperacao,
    Emitente,
    Endereco,
    Destinatario,
    FinalidadeNFe,
    FormaPagamento,
    Identificacao,
    ImpostosItem,
    IndicadorIEDest,
    ModalidadeFrete,
    NFe,
    Pagamento,
    PresencaComprador,
    Produto,
    ProtocoloAutorizacao,
    RegimeTributario,
    TipoAmbiente,
    TipoNF,
    Transporte,
    UF,
)
from danfe_generator.web.logic.validators import (
    format_cnpj,
    validate_cfop,
    validate_cnpj,
    validate_cpf,
    validate_ncm,
)
from danfe_generator.web.logic.xml_builder import build_xml, gerar_chave_acesso


# =============================================================================
# Session State Keys
# =============================================================================

STATE_NFE = "nfe_form_data"
STATE_PRODUTOS = "nfe_produtos"


def _init_session_state() -> None:
    """Inicializa o estado da sessão para o formulário."""
    if STATE_NFE not in st.session_state:
        st.session_state[STATE_NFE] = NFe()
    if STATE_PRODUTOS not in st.session_state:
        st.session_state[STATE_PRODUTOS] = []


def _get_nfe() -> NFe:
    """Obtém a NFe do session state."""
    return st.session_state[STATE_NFE]


def _update_nfe(nfe: NFe) -> None:
    """Atualiza a NFe no session state."""
    st.session_state[STATE_NFE] = nfe


# =============================================================================
# Form Sections
# =============================================================================


def _render_section_identificacao(nfe: NFe) -> None:
    """Renderiza seção de identificação da NF-e."""
    with st.expander("1. IDENTIFICAÇÃO DA NF-e", expanded=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            uf_options = list(UF)
            uf_index = next(
                (i for i, uf in enumerate(uf_options) if uf.value == nfe.identificacao.codigo_uf),
                24,  # SP default
            )
            selected_uf = st.selectbox(
                "UF Emitente",
                options=uf_options,
                index=uf_index,
                format_func=lambda x: f"{x.name} ({x.value})",
                key="ide_uf",
            )
            nfe.identificacao.codigo_uf = selected_uf.value

        with col2:
            nfe.identificacao.serie = st.number_input(
                "Série",
                min_value=1,
                max_value=999,
                value=nfe.identificacao.serie,
                key="ide_serie",
            )

        with col3:
            nfe.identificacao.numero_nf = st.number_input(
                "Número da NF-e",
                min_value=1,
                value=nfe.identificacao.numero_nf,
                key="ide_numero",
            )

        nfe.identificacao.natureza_operacao = st.text_input(
            "Natureza da Operação",
            value=nfe.identificacao.natureza_operacao,
            placeholder="Ex: VENDA DE MERCADORIA",
            key="ide_natop",
        )

        col4, col5 = st.columns(2)
        with col4:
            tipo_options = list(TipoNF)
            tipo_index = tipo_options.index(nfe.identificacao.tipo_nf)
            selected_tipo = st.selectbox(
                "Tipo de Operação",
                options=tipo_options,
                index=tipo_index,
                format_func=lambda x: "Entrada" if x == TipoNF.ENTRADA else "Saída",
                key="ide_tipo",
            )
            nfe.identificacao.tipo_nf = selected_tipo

        with col5:
            dest_options = list(DestinoOperacao)
            dest_index = dest_options.index(nfe.identificacao.destino_operacao)
            selected_dest = st.selectbox(
                "Destino da Operação",
                options=dest_options,
                index=dest_index,
                format_func=lambda x: {
                    DestinoOperacao.INTERNA: "Interna (Mesmo Estado)",
                    DestinoOperacao.INTERESTADUAL: "Interestadual",
                    DestinoOperacao.EXTERIOR: "Exterior",
                }[x],
                key="ide_dest",
            )
            nfe.identificacao.destino_operacao = selected_dest

        col6, col7 = st.columns(2)
        with col6:
            amb_options = list(TipoAmbiente)
            amb_index = amb_options.index(nfe.identificacao.ambiente)
            selected_amb = st.selectbox(
                "Ambiente",
                options=amb_options,
                index=amb_index,
                format_func=lambda x: "Produção" if x == TipoAmbiente.PRODUCAO else "Homologação",
                key="ide_amb",
            )
            nfe.identificacao.ambiente = selected_amb

        with col7:
            fin_options = list(FinalidadeNFe)
            fin_index = fin_options.index(nfe.identificacao.finalidade)
            selected_fin = st.selectbox(
                "Finalidade",
                options=fin_options,
                index=fin_index,
                format_func=lambda x: {
                    FinalidadeNFe.NORMAL: "Normal",
                    FinalidadeNFe.COMPLEMENTAR: "Complementar",
                    FinalidadeNFe.AJUSTE: "Ajuste",
                    FinalidadeNFe.DEVOLUCAO: "Devolução",
                }[x],
                key="ide_fin",
            )
            nfe.identificacao.finalidade = selected_fin


def _render_section_emitente(nfe: NFe) -> None:
    """Renderiza seção do emitente."""
    with st.expander("2. EMITENTE", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            cnpj_input = st.text_input(
                "CNPJ *",
                value=nfe.emitente.cnpj,
                placeholder="00.000.000/0000-00",
                key="emit_cnpj",
            )
            nfe.emitente.cnpj = cnpj_input.replace(".", "").replace("/", "").replace("-", "")

            if cnpj_input:
                result = validate_cnpj(cnpj_input)
                if result.valid:
                    st.success("✓ CNPJ válido")
                else:
                    st.error(f"✕ {result.message}")

        with col2:
            crt_options = list(RegimeTributario)
            crt_index = crt_options.index(nfe.emitente.regime_tributario)
            selected_crt = st.selectbox(
                "Regime Tributário",
                options=crt_options,
                index=crt_index,
                format_func=lambda x: {
                    RegimeTributario.SIMPLES_NACIONAL: "Simples Nacional",
                    RegimeTributario.SIMPLES_EXCESSO: "Simples Nacional - Excesso",
                    RegimeTributario.REGIME_NORMAL: "Regime Normal",
                }[x],
                key="emit_crt",
            )
            nfe.emitente.regime_tributario = selected_crt

        nfe.emitente.razao_social = st.text_input(
            "Razão Social *",
            value=nfe.emitente.razao_social,
            max_chars=60,
            key="emit_razao",
        )

        nfe.emitente.nome_fantasia = st.text_input(
            "Nome Fantasia",
            value=nfe.emitente.nome_fantasia,
            max_chars=60,
            key="emit_fantasia",
        )

        nfe.emitente.inscricao_estadual = st.text_input(
            "Inscrição Estadual *",
            value=nfe.emitente.inscricao_estadual,
            key="emit_ie",
        )

        st.markdown("**Endereço**")
        col3, col4 = st.columns([3, 1])
        with col3:
            nfe.emitente.endereco.logradouro = st.text_input(
                "Logradouro *",
                value=nfe.emitente.endereco.logradouro,
                key="emit_logr",
            )
        with col4:
            nfe.emitente.endereco.numero = st.text_input(
                "Número *",
                value=nfe.emitente.endereco.numero,
                key="emit_nro",
            )

        col5, col6 = st.columns(2)
        with col5:
            nfe.emitente.endereco.bairro = st.text_input(
                "Bairro *",
                value=nfe.emitente.endereco.bairro,
                key="emit_bairro",
            )
        with col6:
            nfe.emitente.endereco.cep = st.text_input(
                "CEP *",
                value=nfe.emitente.endereco.cep,
                placeholder="00000-000",
                key="emit_cep",
            )

        col7, col8, col9 = st.columns([2, 2, 1])
        with col7:
            nfe.emitente.endereco.nome_municipio = st.text_input(
                "Município *",
                value=nfe.emitente.endereco.nome_municipio,
                key="emit_mun",
            )
        with col8:
            nfe.emitente.endereco.codigo_municipio = st.text_input(
                "Código IBGE *",
                value=nfe.emitente.endereco.codigo_municipio,
                placeholder="0000000",
                key="emit_cmun",
            )
        with col9:
            nfe.emitente.endereco.uf = st.text_input(
                "UF *",
                value=nfe.emitente.endereco.uf,
                max_chars=2,
                key="emit_uf",
            )


def _render_section_destinatario(nfe: NFe) -> None:
    """Renderiza seção do destinatário."""
    with st.expander("3. DESTINATÁRIO", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            doc_type = st.radio(
                "Tipo de Documento",
                options=["CNPJ", "CPF"],
                horizontal=True,
                key="dest_doc_type",
            )

        with col2:
            ie_options = list(IndicadorIEDest)
            ie_index = ie_options.index(nfe.destinatario.indicador_ie)
            selected_ie = st.selectbox(
                "Indicador IE",
                options=ie_options,
                index=ie_index,
                format_func=lambda x: {
                    IndicadorIEDest.CONTRIBUINTE: "Contribuinte ICMS",
                    IndicadorIEDest.ISENTO: "Contribuinte Isento",
                    IndicadorIEDest.NAO_CONTRIBUINTE: "Não Contribuinte",
                }[x],
                key="dest_ind_ie",
            )
            nfe.destinatario.indicador_ie = selected_ie

        if doc_type == "CNPJ":
            cnpj_input = st.text_input(
                "CNPJ *",
                value=nfe.destinatario.cnpj,
                placeholder="00.000.000/0000-00",
                key="dest_cnpj",
            )
            nfe.destinatario.cnpj = cnpj_input.replace(".", "").replace("/", "").replace("-", "")
            nfe.destinatario.cpf = ""
        else:
            cpf_input = st.text_input(
                "CPF *",
                value=nfe.destinatario.cpf,
                placeholder="000.000.000-00",
                key="dest_cpf",
            )
            nfe.destinatario.cpf = cpf_input.replace(".", "").replace("-", "")
            nfe.destinatario.cnpj = ""

        nfe.destinatario.razao_social = st.text_input(
            "Nome/Razão Social *",
            value=nfe.destinatario.razao_social,
            key="dest_nome",
        )

        if selected_ie == IndicadorIEDest.CONTRIBUINTE:
            nfe.destinatario.inscricao_estadual = st.text_input(
                "Inscrição Estadual *",
                value=nfe.destinatario.inscricao_estadual,
                key="dest_ie",
            )

        st.markdown("**Endereço**")
        col3, col4 = st.columns([3, 1])
        with col3:
            nfe.destinatario.endereco.logradouro = st.text_input(
                "Logradouro *",
                value=nfe.destinatario.endereco.logradouro,
                key="dest_logr",
            )
        with col4:
            nfe.destinatario.endereco.numero = st.text_input(
                "Número *",
                value=nfe.destinatario.endereco.numero,
                key="dest_nro",
            )

        col5, col6 = st.columns(2)
        with col5:
            nfe.destinatario.endereco.bairro = st.text_input(
                "Bairro *",
                value=nfe.destinatario.endereco.bairro,
                key="dest_bairro",
            )
        with col6:
            nfe.destinatario.endereco.cep = st.text_input(
                "CEP *",
                value=nfe.destinatario.endereco.cep,
                key="dest_cep",
            )

        col7, col8, col9 = st.columns([2, 2, 1])
        with col7:
            nfe.destinatario.endereco.nome_municipio = st.text_input(
                "Município *",
                value=nfe.destinatario.endereco.nome_municipio,
                key="dest_mun",
            )
        with col8:
            nfe.destinatario.endereco.codigo_municipio = st.text_input(
                "Código IBGE *",
                value=nfe.destinatario.endereco.codigo_municipio,
                key="dest_cmun",
            )
        with col9:
            nfe.destinatario.endereco.uf = st.text_input(
                "UF *",
                value=nfe.destinatario.endereco.uf,
                max_chars=2,
                key="dest_uf",
            )


def _render_section_produtos(nfe: NFe) -> None:
    """Renderiza seção de produtos."""
    with st.expander("4. PRODUTOS/SERVIÇOS", expanded=False):
        # Tabela de produtos usando st.data_editor
        st.markdown("**Lista de Produtos**")

        if st.button("➕ Adicionar Produto", key="btn_add_prod"):
            novo_produto = Produto(
                numero_item=len(nfe.produtos) + 1,
                codigo=f"PROD{len(nfe.produtos) + 1:03d}",
            )
            nfe.produtos.append(novo_produto)
            _update_nfe(nfe)

        if nfe.produtos:
            for idx, produto in enumerate(nfe.produtos):
                with st.container():
                    st.markdown(f"**Item {idx + 1}**")
                    col1, col2, col3 = st.columns([2, 3, 1])

                    with col1:
                        produto.codigo = st.text_input(
                            "Código",
                            value=produto.codigo,
                            key=f"prod_cod_{idx}",
                        )
                    with col2:
                        produto.descricao = st.text_input(
                            "Descrição *",
                            value=produto.descricao,
                            key=f"prod_desc_{idx}",
                        )
                    with col3:
                        produto.ncm = st.text_input(
                            "NCM",
                            value=produto.ncm,
                            key=f"prod_ncm_{idx}",
                        )

                    col4, col5, col6, col7 = st.columns(4)
                    with col4:
                        produto.cfop = st.text_input(
                            "CFOP",
                            value=produto.cfop,
                            key=f"prod_cfop_{idx}",
                        )
                    with col5:
                        produto.unidade = st.selectbox(
                            "Unidade",
                            options=["UN", "KG", "CX", "PCT", "M", "L"],
                            index=["UN", "KG", "CX", "PCT", "M", "L"].index(produto.unidade)
                            if produto.unidade in ["UN", "KG", "CX", "PCT", "M", "L"]
                            else 0,
                            key=f"prod_un_{idx}",
                        )
                    with col6:
                        qtd = st.number_input(
                            "Quantidade",
                            min_value=0.0001,
                            value=float(produto.quantidade),
                            format="%.4f",
                            key=f"prod_qtd_{idx}",
                        )
                        produto.quantidade = Decimal(str(qtd))
                    with col7:
                        vlr = st.number_input(
                            "Valor Unit.",
                            min_value=0.0001,
                            value=float(produto.valor_unitario),
                            format="%.4f",
                            key=f"prod_vlr_{idx}",
                        )
                        produto.valor_unitario = Decimal(str(vlr))

                    # Calcular valor total
                    produto.valor_total = produto.quantidade * produto.valor_unitario
                    produto.quantidade_tributavel = produto.quantidade
                    produto.valor_unitario_tributavel = produto.valor_unitario

                    # Calcular impostos simples
                    produto.impostos.base_calculo_icms = produto.valor_total
                    produto.impostos.valor_icms = produto.valor_total * produto.impostos.aliquota_icms / 100
                    produto.impostos.base_calculo_pis = produto.valor_total
                    produto.impostos.valor_pis = produto.valor_total * produto.impostos.aliquota_pis / 100
                    produto.impostos.base_calculo_cofins = produto.valor_total
                    produto.impostos.valor_cofins = produto.valor_total * produto.impostos.aliquota_cofins / 100

                    col8, col9, col10 = st.columns(3)
                    with col8:
                        st.metric("Valor Total", f"R$ {produto.valor_total:.2f}")
                    with col9:
                        st.metric("ICMS", f"R$ {produto.impostos.valor_icms:.2f}")
                    with col10:
                        if st.button("🗑️ Remover", key=f"btn_rm_prod_{idx}"):
                            nfe.produtos.pop(idx)
                            # Renumerar itens
                            for i, p in enumerate(nfe.produtos):
                                p.numero_item = i + 1
                            _update_nfe(nfe)
                            st.rerun()

                    st.markdown("---")
        else:
            st.info("Nenhum produto adicionado. Clique em '➕ Adicionar Produto' para começar.")


def _render_section_pagamento(nfe: NFe) -> None:
    """Renderiza seção de pagamento."""
    with st.expander("5. PAGAMENTO", expanded=False):
        forma_options = [
            FormaPagamento.DINHEIRO,
            FormaPagamento.PIX,
            FormaPagamento.CARTAO_CREDITO,
            FormaPagamento.CARTAO_DEBITO,
            FormaPagamento.BOLETO,
            FormaPagamento.TRANSFERENCIA,
        ]

        forma_labels = {
            FormaPagamento.DINHEIRO: "Dinheiro",
            FormaPagamento.PIX: "PIX",
            FormaPagamento.CARTAO_CREDITO: "Cartão de Crédito",
            FormaPagamento.CARTAO_DEBITO: "Cartão de Débito",
            FormaPagamento.BOLETO: "Boleto",
            FormaPagamento.TRANSFERENCIA: "Transferência",
        }

        selected_forma = st.selectbox(
            "Forma de Pagamento",
            options=forma_options,
            format_func=lambda x: forma_labels.get(x, x.value),
            key="pag_forma",
        )

        # Calcula total
        nfe.calcular_totais()
        total = float(nfe.totais.valor_nota)

        valor_pago = st.number_input(
            "Valor Pago",
            min_value=0.00,
            value=total,
            format="%.2f",
            key="pag_valor",
        )

        # Atualiza pagamento
        if nfe.pagamentos:
            nfe.pagamentos[0].forma = selected_forma
            nfe.pagamentos[0].valor = Decimal(str(valor_pago))
        else:
            nfe.pagamentos = [Pagamento(forma=selected_forma, valor=Decimal(str(valor_pago)))]


def _render_section_protocolo(nfe: NFe) -> None:
    """Renderiza seção de protocolo de autorização."""
    with st.expander("6. PROTOCOLO SEFAZ (Opcional)", expanded=False):
        nfe.protocolo.incluir = st.checkbox(
            "Incluir protocolo de autorização (protNFe)",
            value=nfe.protocolo.incluir,
            key="prot_incluir",
        )

        if nfe.protocolo.incluir:
            col1, col2 = st.columns(2)
            with col1:
                nfe.protocolo.numero_protocolo = st.text_input(
                    "Número do Protocolo",
                    value=nfe.protocolo.numero_protocolo,
                    key="prot_num",
                )
            with col2:
                nfe.protocolo.codigo_status = st.selectbox(
                    "Status",
                    options=["100", "101", "102"],
                    format_func=lambda x: {
                        "100": "100 - Autorizada",
                        "101": "101 - Cancelada",
                        "102": "102 - Inutilizada",
                    }.get(x, x),
                    key="prot_stat",
                )

            nfe.protocolo.versao_aplicativo = st.text_input(
                "Versão do Aplicativo SEFAZ",
                value=nfe.protocolo.versao_aplicativo or "SP_NFE_PL_008i2",
                key="prot_verap",
            )


def _render_totais(nfe: NFe) -> None:
    """Renderiza resumo dos totais."""
    from danfe_generator.web.components.icons import render_icon_text

    st.markdown(render_icon_text("diamond", "TOTAIS", header=True), unsafe_allow_html=True)

    nfe.calcular_totais()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Produtos", f"R$ {nfe.totais.valor_produtos:.2f}")
    with col2:
        st.metric("ICMS", f"R$ {nfe.totais.valor_icms:.2f}")
    with col3:
        st.metric("PIS + COFINS", f"R$ {nfe.totais.valor_pis + nfe.totais.valor_cofins:.2f}")
    with col4:
        st.metric("TOTAL NF-e", f"R$ {nfe.totais.valor_nota:.2f}")


def _generate_and_download(
    nfe: NFe,
    logo_path: Path | None,
    colors: ColorsConfig,
    margins: MarginsConfig,
) -> None:
    """Gera XML e PDF e oferece download."""
    # Gerar chave e atualizar campos derivados
    nfe.identificacao.data_hora_emissao = datetime.now()
    nfe.identificacao.codigo_municipio_fg = nfe.emitente.endereco.codigo_municipio
    nfe.calcular_totais()

    chave = gerar_chave_acesso(nfe)
    nfe.protocolo.chave_nfe = chave

    # Gerar XML
    xml_content = build_xml(nfe)
    xml_filename = f"nfe_{chave}.xml"

    # Gerar PDF usando o core existente
    config = DANFEConfig(
        logo_path=logo_path,
        margins=margins,
        colors=colors,
    )
    generator = DANFEGenerator(config)

    with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as xml_tmp:
        xml_tmp.write(xml_content.encode("utf-8"))
        xml_tmp_path = Path(xml_tmp.name)

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as pdf_tmp:
        pdf_tmp_path = Path(pdf_tmp.name)

    try:
        result = generator.generate(xml_tmp_path, pdf_tmp_path)

        if result.success:
            pdf_bytes = pdf_tmp_path.read_bytes()
            pdf_filename = f"nfe_{chave}.pdf"

            st.success(f"NF-e gerada com sucesso!")
            st.info(f"**Chave de Acesso:** {chave}")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.download_button(
                    label="⬇ Baixar XML",
                    data=xml_content,
                    file_name=xml_filename,
                    mime="application/xml",
                    key="dl_xml",
                )

            with col2:
                st.download_button(
                    label="⬇ Baixar PDF",
                    data=pdf_bytes,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    key="dl_pdf",
                )

            with col3:
                # ZIP com ambos
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                    zf.writestr(xml_filename, xml_content)
                    zf.writestr(pdf_filename, pdf_bytes)
                zip_buffer.seek(0)

                st.download_button(
                    label="⬇ Baixar ZIP",
                    data=zip_buffer.getvalue(),
                    file_name=f"nfe_{chave}.zip",
                    mime="application/zip",
                    key="dl_zip",
                )
        else:
            st.error(f"Erro ao gerar DANFE: {result.error_message}")

    finally:
        if xml_tmp_path.exists():
            xml_tmp_path.unlink()
        if pdf_tmp_path.exists():
            pdf_tmp_path.unlink()


# =============================================================================
# Main View
# =============================================================================


def render_create_view(
    logo_path: Path | None,
    colors: ColorsConfig,
    margins: MarginsConfig,
) -> None:
    """Renderiza view de criação de NF-e.

    Args:
        logo_path: Caminho para o logo (opcional).
        colors: Configuração de cores.
        margins: Configuração de margens.
    """
    _init_session_state()
    nfe = _get_nfe()

    render_hero(
        title="Criar NF-e",
        subtitle="Preencha os campos abaixo para gerar uma nova Nota Fiscal Eletrônica.",
        badge="Criação de NF-e • XML + PDF",
    )

    # Formulário em seções
    _render_section_identificacao(nfe)
    _render_section_emitente(nfe)
    _render_section_destinatario(nfe)
    _render_section_produtos(nfe)
    _render_section_pagamento(nfe)
    _render_section_protocolo(nfe)

    st.markdown("---")
    _render_totais(nfe)

    st.markdown("---")

    # Botão de geração
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button(
            "GERAR NF-e",
            type="primary",
            use_container_width=True,
            key="btn_generate_nfe",
        ):
            if not nfe.produtos:
                st.error("Adicione pelo menos um produto.")
            elif not nfe.emitente.cnpj:
                st.error("Preencha o CNPJ do emitente.")
            elif not nfe.emitente.razao_social:
                st.error("Preencha a razão social do emitente.")
            else:
                with st.spinner("Gerando NF-e..."):
                    _generate_and_download(nfe, logo_path, colors, margins)

    with col2:
        if st.button("🔄 Limpar", key="btn_clear"):
            st.session_state[STATE_NFE] = NFe()
            st.session_state[STATE_PRODUTOS] = []
            st.rerun()

    _update_nfe(nfe)
