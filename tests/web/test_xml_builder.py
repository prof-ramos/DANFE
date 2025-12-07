"""Testes para o módulo de construção de XML."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

import pytest

from danfe_generator.web.logic.models import (
    Emitente,
    Endereco,
    Identificacao,
    ImpostosItem,
    NFe,
    Pagamento,
    Produto,
    TipoAmbiente,
)
from danfe_generator.web.logic.xml_builder import (
    build_xml,
    gerar_chave_acesso,
)


class TestGerarChaveAcesso:
    """Testes para geração de chave de acesso."""

    def test_chave_tem_44_digitos(self) -> None:
        """Testa que a chave tem 44 dígitos."""
        nfe = NFe()
        nfe.identificacao.codigo_uf = "35"
        nfe.identificacao.data_hora_emissao = datetime(2023, 12, 4, 10, 0, 0)
        nfe.identificacao.modelo = "55"
        nfe.identificacao.serie = 1
        nfe.identificacao.numero_nf = 1
        nfe.identificacao.tipo_emissao = "1"
        nfe.identificacao.codigo_numerico = "00000001"
        nfe.emitente.cnpj = "12345678000195"

        chave = gerar_chave_acesso(nfe)

        assert len(chave) == 44
        assert chave.isdigit()

    def test_chave_componentes_corretos(self) -> None:
        """Testa os componentes da chave de acesso."""
        nfe = NFe()
        nfe.identificacao.codigo_uf = "35"
        nfe.identificacao.data_hora_emissao = datetime(2023, 12, 4, 10, 0, 0)
        nfe.identificacao.modelo = "55"
        nfe.identificacao.serie = 1
        nfe.identificacao.numero_nf = 1
        nfe.identificacao.tipo_emissao = "1"
        nfe.identificacao.codigo_numerico = "00000001"
        nfe.emitente.cnpj = "12345678000195"

        chave = gerar_chave_acesso(nfe)

        # Verifica componentes
        assert chave[:2] == "35"  # cUF
        assert chave[2:6] == "2312"  # AAMM (dezembro 2023)
        assert chave[6:20] == "12345678000195"  # CNPJ
        assert chave[20:22] == "55"  # mod
        assert chave[22:25] == "001"  # serie
        assert chave[25:34] == "000000001"  # nNF


class TestBuildXML:
    """Testes para construção de XML."""

    @pytest.fixture
    def nfe_completa(self) -> NFe:
        """Cria uma NFe completa para testes."""
        nfe = NFe()

        # Identificação
        nfe.identificacao.codigo_uf = "35"
        nfe.identificacao.codigo_numerico = "00000001"
        nfe.identificacao.natureza_operacao = "VENDA DE MERCADORIA"
        nfe.identificacao.serie = 1
        nfe.identificacao.numero_nf = 1
        nfe.identificacao.data_hora_emissao = datetime(2023, 12, 4, 10, 0, 0)
        nfe.identificacao.codigo_municipio_fg = "3550308"
        nfe.identificacao.ambiente = TipoAmbiente.HOMOLOGACAO

        # Emitente
        nfe.emitente.cnpj = "12345678000195"
        nfe.emitente.razao_social = "EMPRESA TESTE LTDA"
        nfe.emitente.nome_fantasia = "TESTE"
        nfe.emitente.inscricao_estadual = "123456789012"
        nfe.emitente.endereco = Endereco(
            logradouro="RUA TESTE",
            numero="100",
            bairro="CENTRO",
            codigo_municipio="3550308",
            nome_municipio="SAO PAULO",
            uf="SP",
            cep="01001000",
        )

        # Destinatário
        nfe.destinatario.cnpj = "98765432000198"
        nfe.destinatario.razao_social = "CLIENTE TESTE LTDA"
        nfe.destinatario.endereco = Endereco(
            logradouro="AV PAULISTA",
            numero="1000",
            bairro="BELA VISTA",
            codigo_municipio="3550308",
            nome_municipio="SAO PAULO",
            uf="SP",
            cep="01310100",
        )

        # Produto
        produto = Produto(
            numero_item=1,
            codigo="PROD001",
            descricao="PRODUTO TESTE",
            ncm="84713012",
            cfop="5102",
            quantidade=Decimal("1.0000"),
            valor_unitario=Decimal("100.0000"),
            valor_total=Decimal("100.00"),
            impostos=ImpostosItem(
                base_calculo_icms=Decimal("100.00"),
                aliquota_icms=Decimal("18.00"),
                valor_icms=Decimal("18.00"),
                base_calculo_pis=Decimal("100.00"),
                aliquota_pis=Decimal("1.65"),
                valor_pis=Decimal("1.65"),
                base_calculo_cofins=Decimal("100.00"),
                aliquota_cofins=Decimal("7.60"),
                valor_cofins=Decimal("7.60"),
            ),
        )
        nfe.produtos = [produto]

        # Pagamento
        nfe.pagamentos = [Pagamento(valor=Decimal("100.00"))]

        # Calcula totais
        nfe.calcular_totais()

        return nfe

    def test_xml_contem_declaracao(self, nfe_completa: NFe) -> None:
        """Testa que o XML contém declaração correta."""
        xml = build_xml(nfe_completa)
        assert '<?xml version="1.0" encoding="UTF-8"?>' in xml

    def test_xml_contem_namespace(self, nfe_completa: NFe) -> None:
        """Testa que o XML contém namespace correto."""
        xml = build_xml(nfe_completa)
        assert "http://www.portalfiscal.inf.br/nfe" in xml

    def test_xml_contem_versao(self, nfe_completa: NFe) -> None:
        """Testa que o XML contém versão correta."""
        xml = build_xml(nfe_completa)
        assert 'versao="4.00"' in xml

    def test_xml_contem_ide(self, nfe_completa: NFe) -> None:
        """Testa que o XML contém bloco ide."""
        xml = build_xml(nfe_completa)
        assert "<ide>" in xml
        assert "<cUF>35</cUF>" in xml
        assert "<natOp>VENDA DE MERCADORIA</natOp>" in xml

    def test_xml_contem_emit(self, nfe_completa: NFe) -> None:
        """Testa que o XML contém bloco emit."""
        xml = build_xml(nfe_completa)
        assert "<emit>" in xml
        assert "<CNPJ>12345678000195</CNPJ>" in xml
        assert "<xNome>EMPRESA TESTE LTDA</xNome>" in xml

    def test_xml_contem_dest(self, nfe_completa: NFe) -> None:
        """Testa que o XML contém bloco dest."""
        xml = build_xml(nfe_completa)
        assert "<dest>" in xml
        assert "<CNPJ>98765432000198</CNPJ>" in xml

    def test_xml_contem_det(self, nfe_completa: NFe) -> None:
        """Testa que o XML contém bloco det."""
        xml = build_xml(nfe_completa)
        assert '<det nItem="1">' in xml
        assert "<prod>" in xml
        assert "<cProd>PROD001</cProd>" in xml
        assert "<xProd>PRODUTO TESTE</xProd>" in xml

    def test_xml_contem_impostos(self, nfe_completa: NFe) -> None:
        """Testa que o XML contém impostos."""
        xml = build_xml(nfe_completa)
        assert "<imposto>" in xml
        assert "<ICMS>" in xml
        assert "<ICMS00>" in xml
        assert "<PIS>" in xml
        assert "<COFINS>" in xml

    def test_xml_contem_total(self, nfe_completa: NFe) -> None:
        """Testa que o XML contém bloco total."""
        xml = build_xml(nfe_completa)
        assert "<total>" in xml
        assert "<ICMSTot>" in xml
        assert "<vNF>" in xml

    def test_xml_contem_transp(self, nfe_completa: NFe) -> None:
        """Testa que o XML contém bloco transp."""
        xml = build_xml(nfe_completa)
        assert "<transp>" in xml
        assert "<modFrete>9</modFrete>" in xml  # Sem frete

    def test_xml_contem_pag(self, nfe_completa: NFe) -> None:
        """Testa que o XML contém bloco pag."""
        xml = build_xml(nfe_completa)
        assert "<pag>" in xml
        assert "<detPag>" in xml
        assert "<tPag>01</tPag>" in xml  # Dinheiro

    def test_xml_com_protocolo(self, nfe_completa: NFe) -> None:
        """Testa XML com protocolo de autorização."""
        nfe_completa.protocolo.incluir = True
        nfe_completa.protocolo.numero_protocolo = "135231234567890"
        nfe_completa.protocolo.versao_aplicativo = "SP_NFE_PL_008i2"
        nfe_completa.protocolo.data_hora_recebimento = datetime(2023, 12, 4, 10, 1, 15)

        xml = build_xml(nfe_completa)

        assert "<nfeProc" in xml
        assert "<protNFe" in xml
        assert "<nProt>135231234567890</nProt>" in xml
        assert "<cStat>100</cStat>" in xml

    def test_xml_sem_protocolo(self, nfe_completa: NFe) -> None:
        """Testa XML sem protocolo de autorização."""
        nfe_completa.protocolo.incluir = False

        xml = build_xml(nfe_completa)

        assert "<nfeProc" not in xml
        assert "<protNFe" not in xml
