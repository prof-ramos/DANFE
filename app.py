import streamlit as st
from pathlib import Path
import tempfile
import os
from danfe_gerador import DANFEPersonalizado

# Configuração da página
st.set_page_config(page_title="Gerador de DANFE", page_icon="📄", layout="wide")

# Título e Descrição
st.title("📄 Gerador de DANFE Personalizado")
st.markdown("""
Gere DANFEs (Documento Auxiliar da Nota Fiscal Eletrônica) personalizados a partir de arquivos XML.
Configure cores, margens e logo na barra lateral.
""")

# Sidebar - Configurações
with st.sidebar:
    st.header("⚙️ Configurações")

    # Logo
    st.subheader("Logo")
    uploaded_logo = st.file_uploader(
        "Upload da Logo (PNG/JPG)", type=["png", "jpg", "jpeg"]
    )

    # Verificar se logo padrão existe
    default_logo = "./logos/logo.png"
    logo_path = default_logo if Path(default_logo).exists() else None

    if uploaded_logo:
        # Salvar logo temporária
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=Path(uploaded_logo.name).suffix
        ) as tmp_logo:
            tmp_logo.write(uploaded_logo.getvalue())
            logo_path = tmp_logo.name

    # Cores
    st.subheader("Cores")
    default_primary = "#2996A1"
    default_secondary = "#5E5240"
    default_accent = "#C0152F"

    col1, col2, col3 = st.columns(3)
    with col1:
        c_primary = st.color_picker("Primária", default_primary)
    with col2:
        c_secondary = st.color_picker("Secundária", default_secondary)
    with col3:
        c_accent = st.color_picker("Destaque", default_accent)

    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    cores_personalizadas = {
        "primary": list(hex_to_rgb(c_primary)),
        "secondary": list(hex_to_rgb(c_secondary)),
        "accent": list(hex_to_rgb(c_accent)),
    }

    # Margens
    st.subheader("Margens (mm)")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        m_top = st.number_input("Topo", value=10, min_value=0, max_value=50)
        m_bottom = st.number_input("Base", value=10, min_value=0, max_value=50)
    with col_m2:
        m_left = st.number_input("Esquerda", value=10, min_value=0, max_value=50)
        m_right = st.number_input("Direita", value=10, min_value=0, max_value=50)

    margens = {"top": m_top, "right": m_right, "bottom": m_bottom, "left": m_left}

# Área Principal
st.header("📤 Upload de XMLs")

uploaded_files = st.file_uploader(
    "Arraste e solte arquivos XML aqui", type=["xml"], accept_multiple_files=True
)

if uploaded_files:
    if st.button("🚀 Gerar DANFEs", type="primary"):
        # Container para resultados
        results_container = st.container()

        # Inicializar gerador
        gerador = DANFEPersonalizado(
            logo_path=logo_path,
            empresa_nome="Empresa",  # Opcional, pode ser extraído do XML ou input
            cores_personalizadas=cores_personalizadas,
            margens=margens,
        )

        # Processar arquivos
        with st.spinner(f"Processando {len(uploaded_files)} arquivos..."):
            for uploaded_file in uploaded_files:
                tmp_xml_path = None
                output_pdf_path = None

                try:
                    # Criar arquivo temporário para o XML
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".xml"
                    ) as tmp_xml:
                        tmp_xml.write(uploaded_file.getvalue())
                        tmp_xml_path = tmp_xml.name

                    # Definir path de saída temporário
                    output_pdf_path = tmp_xml_path.replace(".xml", ".pdf")

                    # Gerar DANFE
                    success = gerador.gerar_danfe(tmp_xml_path, output_pdf_path)

                    if success:
                        with open(output_pdf_path, "rb") as pdf_file:
                            pdf_bytes = pdf_file.read()

                        col_res1, col_res2 = results_container.columns([3, 1])
                        with col_res1:
                            st.success(f"✅ {uploaded_file.name} gerado com sucesso!")
                        with col_res2:
                            st.download_button(
                                label="⬇️ Baixar PDF",
                                data=pdf_bytes,
                                file_name=f"{Path(uploaded_file.name).stem}.pdf",
                                mime="application/pdf",
                                key=uploaded_file.name,
                            )
                    else:
                        st.error(f"❌ Erro ao processar {uploaded_file.name}")

                finally:
                    # Limpar arquivos temporários independente de sucesso/erro
                    if tmp_xml_path and os.path.exists(tmp_xml_path):
                        os.unlink(tmp_xml_path)
                    if output_pdf_path and os.path.exists(output_pdf_path):
                        os.unlink(output_pdf_path)

        # Limpar logo temp se foi upload
        if uploaded_logo and logo_path and os.path.exists(logo_path):
            os.unlink(logo_path)

# Footer
st.markdown("---")
st.markdown("Desenvolvido com Streamlit e BrazilFiscalReport")
