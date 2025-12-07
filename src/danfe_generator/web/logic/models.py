"""Modelos de dados para criação de NF-e.

Este módulo define as dataclasses que representam a estrutura
de uma NF-e, usadas no formulário de criação.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Literal


# =============================================================================
# Enumerations
# =============================================================================


class UF(str, Enum):
    """Unidades Federativas do Brasil com códigos IBGE."""

    AC = "12"
    AL = "27"
    AP = "16"
    AM = "13"
    BA = "29"
    CE = "23"
    DF = "53"
    ES = "32"
    GO = "52"
    MA = "21"
    MT = "51"
    MS = "50"
    MG = "31"
    PA = "15"
    PB = "25"
    PR = "41"
    PE = "26"
    PI = "22"
    RJ = "33"
    RN = "24"
    RS = "43"
    RO = "11"
    RR = "14"
    SC = "42"
    SP = "35"
    SE = "28"
    TO = "17"


class TipoNF(str, Enum):
    """Tipo de Nota Fiscal."""

    ENTRADA = "0"
    SAIDA = "1"


class DestinoOperacao(str, Enum):
    """Destino da operação."""

    INTERNA = "1"
    INTERESTADUAL = "2"
    EXTERIOR = "3"


class TipoAmbiente(str, Enum):
    """Tipo de ambiente."""

    PRODUCAO = "1"
    HOMOLOGACAO = "2"


class FinalidadeNFe(str, Enum):
    """Finalidade de emissão da NF-e."""

    NORMAL = "1"
    COMPLEMENTAR = "2"
    AJUSTE = "3"
    DEVOLUCAO = "4"


class PresencaComprador(str, Enum):
    """Indicador de presença do comprador."""

    NAO_SE_APLICA = "0"
    PRESENCIAL = "1"
    INTERNET = "2"
    TELEMARKETING = "3"
    ENTREGA_DOMICILIO = "4"
    PRESENCIAL_FORA = "5"
    OUTROS = "9"


class RegimeTributario(str, Enum):
    """Código do Regime Tributário."""

    SIMPLES_NACIONAL = "1"
    SIMPLES_EXCESSO = "2"
    REGIME_NORMAL = "3"


class IndicadorIEDest(str, Enum):
    """Indicador IE do destinatário."""

    CONTRIBUINTE = "1"
    ISENTO = "2"
    NAO_CONTRIBUINTE = "9"


class ModalidadeFrete(str, Enum):
    """Modalidade de frete."""

    EMITENTE = "0"
    DESTINATARIO = "1"
    TERCEIROS = "2"
    PROPRIO_REMETENTE = "3"
    PROPRIO_DESTINATARIO = "4"
    SEM_FRETE = "9"


class FormaPagamento(str, Enum):
    """Formas de pagamento."""

    DINHEIRO = "01"
    CHEQUE = "02"
    CARTAO_CREDITO = "03"
    CARTAO_DEBITO = "04"
    LOJA = "05"
    ALIMENTACAO = "10"
    REFEICAO = "11"
    PRESENTE = "12"
    COMBUSTIVEL = "13"
    DUPLICATA = "14"
    BOLETO = "15"
    DEPOSITO = "16"
    PIX = "17"
    TRANSFERENCIA = "18"
    CASHBACK = "19"
    SEM_PAGAMENTO = "90"
    OUTROS = "99"


# =============================================================================
# Data Models
# =============================================================================


@dataclass
class Endereco:
    """Endereço genérico (emitente ou destinatário)."""

    logradouro: str = ""
    numero: str = ""
    complemento: str = ""
    bairro: str = ""
    codigo_municipio: str = ""  # IBGE
    nome_municipio: str = ""
    uf: str = ""  # Sigla UF
    cep: str = ""
    codigo_pais: str = "1058"
    nome_pais: str = "BRASIL"
    telefone: str = ""


@dataclass
class Identificacao:
    """Bloco <ide> - Identificação da NF-e."""

    codigo_uf: str = "35"  # SP padrão
    codigo_numerico: str = "00000001"
    natureza_operacao: str = "VENDA DE MERCADORIA"
    modelo: str = "55"
    serie: int = 1
    numero_nf: int = 1
    data_hora_emissao: datetime = field(default_factory=datetime.now)
    tipo_nf: TipoNF = TipoNF.SAIDA
    destino_operacao: DestinoOperacao = DestinoOperacao.INTERNA
    codigo_municipio_fg: str = ""
    tipo_impressao: str = "1"  # Retrato
    tipo_emissao: str = "1"  # Normal
    ambiente: TipoAmbiente = TipoAmbiente.HOMOLOGACAO
    finalidade: FinalidadeNFe = FinalidadeNFe.NORMAL
    consumidor_final: bool = True
    presenca_comprador: PresencaComprador = PresencaComprador.PRESENCIAL
    processo_emissao: str = "0"  # App contribuinte
    versao_processo: str = "1.0"


@dataclass
class Emitente:
    """Bloco <emit> - Dados do Emitente."""

    cnpj: str = ""
    razao_social: str = ""
    nome_fantasia: str = ""
    endereco: Endereco = field(default_factory=Endereco)
    inscricao_estadual: str = ""
    regime_tributario: RegimeTributario = RegimeTributario.REGIME_NORMAL


@dataclass
class Destinatario:
    """Bloco <dest> - Dados do Destinatário."""

    cnpj: str = ""  # Ou CPF
    cpf: str = ""
    razao_social: str = ""
    endereco: Endereco = field(default_factory=Endereco)
    indicador_ie: IndicadorIEDest = IndicadorIEDest.NAO_CONTRIBUINTE
    inscricao_estadual: str = ""


@dataclass
class ImpostosItem:
    """Impostos calculados para um item."""

    # ICMS
    origem: str = "0"  # Nacional
    cst_icms: str = "00"  # Tributação integral
    modalidade_bc: str = "3"  # Valor da operação
    base_calculo_icms: Decimal = Decimal("0.00")
    aliquota_icms: Decimal = Decimal("18.00")
    valor_icms: Decimal = Decimal("0.00")

    # PIS
    cst_pis: str = "01"  # Tributável
    base_calculo_pis: Decimal = Decimal("0.00")
    aliquota_pis: Decimal = Decimal("1.65")
    valor_pis: Decimal = Decimal("0.00")

    # COFINS
    cst_cofins: str = "01"  # Tributável
    base_calculo_cofins: Decimal = Decimal("0.00")
    aliquota_cofins: Decimal = Decimal("7.60")
    valor_cofins: Decimal = Decimal("0.00")


@dataclass
class Produto:
    """Bloco <det>/<prod> - Item da NF-e."""

    numero_item: int = 1
    codigo: str = ""
    ean: str = "SEM GTIN"
    descricao: str = ""
    ncm: str = ""
    cfop: str = "5102"
    unidade: str = "UN"
    quantidade: Decimal = Decimal("1.0000")
    valor_unitario: Decimal = Decimal("0.0000")
    valor_total: Decimal = Decimal("0.00")
    ean_tributavel: str = "SEM GTIN"
    unidade_tributavel: str = "UN"
    quantidade_tributavel: Decimal = Decimal("1.0000")
    valor_unitario_tributavel: Decimal = Decimal("0.0000")
    compoe_total: bool = True

    impostos: ImpostosItem = field(default_factory=ImpostosItem)


@dataclass
class Totais:
    """Bloco <total>/<ICMSTot> - Totais da NF-e."""

    base_calculo_icms: Decimal = Decimal("0.00")
    valor_icms: Decimal = Decimal("0.00")
    valor_icms_desonerado: Decimal = Decimal("0.00")
    valor_fcp: Decimal = Decimal("0.00")
    base_calculo_st: Decimal = Decimal("0.00")
    valor_st: Decimal = Decimal("0.00")
    valor_fcp_st: Decimal = Decimal("0.00")
    valor_fcp_st_ret: Decimal = Decimal("0.00")
    valor_produtos: Decimal = Decimal("0.00")
    valor_frete: Decimal = Decimal("0.00")
    valor_seguro: Decimal = Decimal("0.00")
    valor_desconto: Decimal = Decimal("0.00")
    valor_ii: Decimal = Decimal("0.00")
    valor_ipi: Decimal = Decimal("0.00")
    valor_ipi_devolvido: Decimal = Decimal("0.00")
    valor_pis: Decimal = Decimal("0.00")
    valor_cofins: Decimal = Decimal("0.00")
    valor_outros: Decimal = Decimal("0.00")
    valor_nota: Decimal = Decimal("0.00")


@dataclass
class Transporte:
    """Bloco <transp> - Transporte."""

    modalidade_frete: ModalidadeFrete = ModalidadeFrete.SEM_FRETE
    # Transportadora (opcional)
    cnpj_transportadora: str = ""
    nome_transportadora: str = ""
    ie_transportadora: str = ""
    endereco_transportadora: str = ""
    municipio_transportadora: str = ""
    uf_transportadora: str = ""
    # Volumes (opcional)
    quantidade_volumes: int = 0
    especie: str = ""
    marca: str = ""
    peso_liquido: Decimal = Decimal("0.000")
    peso_bruto: Decimal = Decimal("0.000")


@dataclass
class Cobranca:
    """Bloco <cobr> - Cobrança (opcional)."""

    numero_fatura: str = ""
    valor_original: Decimal = Decimal("0.00")
    valor_desconto: Decimal = Decimal("0.00")
    valor_liquido: Decimal = Decimal("0.00")


@dataclass
class Pagamento:
    """Bloco <pag>/<detPag> - Pagamento."""

    forma: FormaPagamento = FormaPagamento.DINHEIRO
    valor: Decimal = Decimal("0.00")
    troco: Decimal = Decimal("0.00")


@dataclass
class InformacoesAdicionais:
    """Bloco <infAdic> - Informações Adicionais."""

    informacoes_fisco: str = ""
    informacoes_complementares: str = ""


@dataclass
class ProtocoloAutorizacao:
    """Bloco <protNFe> - Protocolo de Autorização (opcional)."""

    incluir: bool = False
    ambiente: TipoAmbiente = TipoAmbiente.HOMOLOGACAO
    versao_aplicativo: str = ""
    chave_nfe: str = ""
    data_hora_recebimento: datetime = field(default_factory=datetime.now)
    numero_protocolo: str = ""
    digest_value: str = ""
    codigo_status: str = "100"
    motivo: str = "Autorizado o uso da NF-e"


@dataclass
class NFe:
    """Modelo completo de uma NF-e."""

    identificacao: Identificacao = field(default_factory=Identificacao)
    emitente: Emitente = field(default_factory=Emitente)
    destinatario: Destinatario = field(default_factory=Destinatario)
    produtos: list[Produto] = field(default_factory=list)
    totais: Totais = field(default_factory=Totais)
    transporte: Transporte = field(default_factory=Transporte)
    cobranca: Cobranca = field(default_factory=Cobranca)
    pagamentos: list[Pagamento] = field(default_factory=list)
    informacoes_adicionais: InformacoesAdicionais = field(
        default_factory=InformacoesAdicionais
    )
    protocolo: ProtocoloAutorizacao = field(default_factory=ProtocoloAutorizacao)

    def calcular_totais(self) -> None:
        """Calcula os totais da NF-e com base nos produtos."""
        if not self.produtos:
            return

        self.totais.base_calculo_icms = sum(
            p.impostos.base_calculo_icms for p in self.produtos
        )
        self.totais.valor_icms = sum(p.impostos.valor_icms for p in self.produtos)
        self.totais.valor_pis = sum(p.impostos.valor_pis for p in self.produtos)
        self.totais.valor_cofins = sum(p.impostos.valor_cofins for p in self.produtos)
        self.totais.valor_produtos = sum(
            p.valor_total for p in self.produtos if p.compoe_total
        )
        self.totais.valor_nota = (
            self.totais.valor_produtos
            + self.totais.valor_frete
            + self.totais.valor_seguro
            + self.totais.valor_outros
            - self.totais.valor_desconto
        )
