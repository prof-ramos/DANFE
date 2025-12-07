"""Testes para o módulo de modelos de dados."""

from __future__ import annotations

from decimal import Decimal

from danfe_generator.web.logic.models import (
    Destinatario,
    Emitente,
    Endereco,
    FinalidadeNFe,
    FormaPagamento,
    Identificacao,
    ImpostosItem,
    ModalidadeFrete,
    NFe,
    Pagamento,
    Produto,
    RegimeTributario,
    TipoAmbiente,
    TipoNF,
    Totais,
    Transporte,
    UF,
)


class TestEnums:
    """Testes para enumerações."""

    def test_uf_codigo_sp(self) -> None:
        """Testa código IBGE de SP."""
        assert UF.SP.value == "35"

    def test_uf_codigo_rj(self) -> None:
        """Testa código IBGE de RJ."""
        assert UF.RJ.value == "33"

    def test_tipo_nf_saida(self) -> None:
        """Testa tipo NF saída."""
        assert TipoNF.SAIDA.value == "1"

    def test_tipo_ambiente(self) -> None:
        """Testa tipos de ambiente."""
        assert TipoAmbiente.PRODUCAO.value == "1"
        assert TipoAmbiente.HOMOLOGACAO.value == "2"

    def test_forma_pagamento(self) -> None:
        """Testa formas de pagamento."""
        assert FormaPagamento.DINHEIRO.value == "01"
        assert FormaPagamento.PIX.value == "17"

    def test_modalidade_frete(self) -> None:
        """Testa modalidades de frete."""
        assert ModalidadeFrete.SEM_FRETE.value == "9"
        assert ModalidadeFrete.EMITENTE.value == "0"


class TestEndereco:
    """Testes para modelo Endereço."""

    def test_endereco_default(self) -> None:
        """Testa criação de endereço com valores padrão."""
        end = Endereco()
        assert end.logradouro == ""
        assert end.codigo_pais == "1058"
        assert end.nome_pais == "BRASIL"

    def test_endereco_completo(self) -> None:
        """Testa criação de endereço completo."""
        end = Endereco(
            logradouro="Rua das Flores",
            numero="100",
            bairro="Centro",
            codigo_municipio="3550308",
            nome_municipio="São Paulo",
            uf="SP",
            cep="01001000",
        )
        assert end.logradouro == "Rua das Flores"
        assert end.uf == "SP"


class TestProduto:
    """Testes para modelo Produto."""

    def test_produto_default(self) -> None:
        """Testa criação de produto com valores padrão."""
        prod = Produto()
        assert prod.numero_item == 1
        assert prod.ean == "SEM GTIN"
        assert prod.cfop == "5102"
        assert prod.unidade == "UN"

    def test_produto_com_valores(self) -> None:
        """Testa criação de produto com valores."""
        prod = Produto(
            numero_item=1,
            codigo="PROD001",
            descricao="Notebook Dell",
            ncm="84713012",
            quantidade=Decimal("2.0000"),
            valor_unitario=Decimal("3500.0000"),
            valor_total=Decimal("7000.00"),
        )
        assert prod.codigo == "PROD001"
        assert prod.valor_total == Decimal("7000.00")

    def test_produto_impostos(self) -> None:
        """Testa impostos do produto."""
        impostos = ImpostosItem(
            base_calculo_icms=Decimal("1000.00"),
            aliquota_icms=Decimal("18.00"),
            valor_icms=Decimal("180.00"),
        )
        prod = Produto(impostos=impostos)
        assert prod.impostos.valor_icms == Decimal("180.00")


class TestNFe:
    """Testes para modelo NFe completo."""

    def test_nfe_default(self) -> None:
        """Testa criação de NFe com valores padrão."""
        nfe = NFe()
        assert nfe.identificacao is not None
        assert nfe.emitente is not None
        assert nfe.destinatario is not None
        assert nfe.produtos == []
        assert nfe.pagamentos == []

    def test_nfe_calcular_totais_vazia(self) -> None:
        """Testa cálculo de totais sem produtos."""
        nfe = NFe()
        nfe.calcular_totais()
        assert nfe.totais.valor_nota == Decimal("0.00")

    def test_nfe_calcular_totais_com_produtos(self) -> None:
        """Testa cálculo de totais com produtos."""
        nfe = NFe()

        # Adiciona produtos
        prod1 = Produto(
            numero_item=1,
            valor_total=Decimal("1000.00"),
            impostos=ImpostosItem(
                base_calculo_icms=Decimal("1000.00"),
                valor_icms=Decimal("180.00"),
                base_calculo_pis=Decimal("1000.00"),
                valor_pis=Decimal("16.50"),
                base_calculo_cofins=Decimal("1000.00"),
                valor_cofins=Decimal("76.00"),
            ),
        )
        prod2 = Produto(
            numero_item=2,
            valor_total=Decimal("500.00"),
            impostos=ImpostosItem(
                base_calculo_icms=Decimal("500.00"),
                valor_icms=Decimal("90.00"),
                base_calculo_pis=Decimal("500.00"),
                valor_pis=Decimal("8.25"),
                base_calculo_cofins=Decimal("500.00"),
                valor_cofins=Decimal("38.00"),
            ),
        )

        nfe.produtos = [prod1, prod2]
        nfe.calcular_totais()

        assert nfe.totais.base_calculo_icms == Decimal("1500.00")
        assert nfe.totais.valor_icms == Decimal("270.00")
        assert nfe.totais.valor_pis == Decimal("24.75")
        assert nfe.totais.valor_cofins == Decimal("114.00")
        assert nfe.totais.valor_produtos == Decimal("1500.00")
        assert nfe.totais.valor_nota == Decimal("1500.00")

    def test_nfe_calcular_totais_com_frete(self) -> None:
        """Testa cálculo de totais com frete e desconto."""
        nfe = NFe()

        prod = Produto(
            numero_item=1,
            valor_total=Decimal("1000.00"),
            impostos=ImpostosItem(
                base_calculo_icms=Decimal("1000.00"),
                valor_icms=Decimal("180.00"),
            ),
        )

        nfe.produtos = [prod]
        nfe.totais.valor_frete = Decimal("50.00")
        nfe.totais.valor_desconto = Decimal("30.00")
        nfe.calcular_totais()

        # valor_nota = produtos + frete + seg + outros - desconto
        assert nfe.totais.valor_nota == Decimal("1020.00")


class TestIdentificacao:
    """Testes para modelo Identificação."""

    def test_identificacao_default(self) -> None:
        """Testa valores padrão de identificação."""
        ide = Identificacao()
        assert ide.modelo == "55"
        assert ide.serie == 1
        assert ide.tipo_nf == TipoNF.SAIDA
        assert ide.ambiente == TipoAmbiente.HOMOLOGACAO
        assert ide.finalidade == FinalidadeNFe.NORMAL


class TestEmitente:
    """Testes para modelo Emitente."""

    def test_emitente_default(self) -> None:
        """Testa valores padrão de emitente."""
        emit = Emitente()
        assert emit.regime_tributario == RegimeTributario.REGIME_NORMAL


class TestTransporte:
    """Testes para modelo Transporte."""

    def test_transporte_default(self) -> None:
        """Testa valores padrão de transporte."""
        transp = Transporte()
        assert transp.modalidade_frete == ModalidadeFrete.SEM_FRETE


class TestPagamento:
    """Testes para modelo Pagamento."""

    def test_pagamento_default(self) -> None:
        """Testa valores padrão de pagamento."""
        pag = Pagamento()
        assert pag.forma == FormaPagamento.DINHEIRO

    def test_pagamento_pix(self) -> None:
        """Testa pagamento via PIX."""
        pag = Pagamento(forma=FormaPagamento.PIX, valor=Decimal("100.00"))
        assert pag.forma == FormaPagamento.PIX
        assert pag.valor == Decimal("100.00")
