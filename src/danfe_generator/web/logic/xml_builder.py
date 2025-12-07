"""Construtor de XML para NF-e.

Gera XML válido no padrão NF-e 4.00 a partir dos modelos de dados.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

from danfe_generator.web.logic.models import NFe


# =============================================================================
# Constants
# =============================================================================

NFE_NAMESPACE = "http://www.portalfiscal.inf.br/nfe"
NFE_VERSION = "4.00"


# =============================================================================
# Helper Functions
# =============================================================================


def _format_decimal(value: Decimal, casas: int = 2) -> str:
    """Formata um Decimal para string com casas decimais fixas."""
    return f"{value:.{casas}f}"


def _format_datetime(dt: datetime) -> str:
    """Formata datetime para o padrão NF-e."""
    return dt.strftime("%Y-%m-%dT%H:%M:%S-03:00")


def _format_date(dt: datetime) -> str:
    """Formata datetime para data apenas."""
    return dt.strftime("%Y-%m-%d")


def _calcular_digito_verificador(chave_sem_dv: str) -> str:
    """Calcula o dígito verificador da chave de acesso (módulo 11)."""
    pesos = [2, 3, 4, 5, 6, 7, 8, 9]
    soma = 0
    peso_idx = 0

    for digito in reversed(chave_sem_dv):
        soma += int(digito) * pesos[peso_idx]
        peso_idx = (peso_idx + 1) % 8

    resto = soma % 11
    if resto == 0 or resto == 1:
        return "0"
    return str(11 - resto)


def gerar_chave_acesso(nfe: NFe) -> str:
    """Gera a chave de acesso de 44 dígitos da NF-e.

    Formato: cUF + AAMM + CNPJ + mod + serie + nNF + tpEmis + cNF + cDV

    Args:
        nfe: Modelo da NF-e.

    Returns:
        Chave de acesso com 44 dígitos.
    """
    ide = nfe.identificacao
    emit = nfe.emitente

    # Componentes da chave
    cuf = ide.codigo_uf.zfill(2)
    aamm = ide.data_hora_emissao.strftime("%y%m")
    cnpj = emit.cnpj.zfill(14)
    mod = ide.modelo.zfill(2)
    serie = str(ide.serie).zfill(3)
    nnf = str(ide.numero_nf).zfill(9)
    tpemis = ide.tipo_emissao
    cnf = ide.codigo_numerico.zfill(8)

    # Monta a chave sem dígito verificador (43 dígitos)
    chave_sem_dv = f"{cuf}{aamm}{cnpj}{mod}{serie}{nnf}{tpemis}{cnf}"

    # Calcula e adiciona o dígito verificador
    cdv = _calcular_digito_verificador(chave_sem_dv)

    return chave_sem_dv + cdv


# =============================================================================
# XML Builder
# =============================================================================


def build_xml(nfe: NFe) -> str:
    """Constrói o XML completo da NF-e.

    Args:
        nfe: Modelo preenchido da NF-e.

    Returns:
        String XML formatada.
    """
    # Gera a chave de acesso
    chave = gerar_chave_acesso(nfe)
    id_nfe = f"NFe{chave}"

    # Elemento raiz (com ou sem protocolo)
    if nfe.protocolo.incluir:
        root = Element("nfeProc", {"versao": NFE_VERSION, "xmlns": NFE_NAMESPACE})
        nfe_elem = SubElement(root, "NFe", {"xmlns": NFE_NAMESPACE})
    else:
        root = Element("NFe", {"xmlns": NFE_NAMESPACE})
        nfe_elem = root

    # infNFe
    inf_nfe = SubElement(
        nfe_elem, "infNFe", {"versao": NFE_VERSION, "Id": id_nfe}
    )

    # Blocos da NF-e
    _build_ide(inf_nfe, nfe, chave)
    _build_emit(inf_nfe, nfe)
    _build_dest(inf_nfe, nfe)
    _build_det(inf_nfe, nfe)
    _build_total(inf_nfe, nfe)
    _build_transp(inf_nfe, nfe)

    if nfe.cobranca.numero_fatura:
        _build_cobr(inf_nfe, nfe)

    _build_pag(inf_nfe, nfe)

    if (
        nfe.informacoes_adicionais.informacoes_fisco
        or nfe.informacoes_adicionais.informacoes_complementares
    ):
        _build_inf_adic(inf_nfe, nfe)

    # Protocolo de autorização (se incluir)
    if nfe.protocolo.incluir:
        _build_prot_nfe(root, nfe, chave)

    # Formata o XML
    xml_str = tostring(root, encoding="unicode")
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ", encoding=None)

    # Remove a declaração XML duplicada do minidom
    lines = pretty_xml.split("\n")
    if lines[0].startswith("<?xml"):
        lines = lines[1:]

    # Adiciona declaração XML correta
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>'
    return xml_declaration + "\n" + "\n".join(lines)


def _build_ide(parent: Element, nfe: NFe, chave: str) -> None:
    """Constrói bloco <ide>."""
    ide = SubElement(parent, "ide")
    data = nfe.identificacao

    SubElement(ide, "cUF").text = data.codigo_uf
    SubElement(ide, "cNF").text = data.codigo_numerico.zfill(8)
    SubElement(ide, "natOp").text = data.natureza_operacao
    SubElement(ide, "mod").text = data.modelo
    SubElement(ide, "serie").text = str(data.serie)
    SubElement(ide, "nNF").text = str(data.numero_nf)
    SubElement(ide, "dhEmi").text = _format_datetime(data.data_hora_emissao)
    SubElement(ide, "tpNF").text = data.tipo_nf.value
    SubElement(ide, "idDest").text = data.destino_operacao.value
    SubElement(ide, "cMunFG").text = data.codigo_municipio_fg
    SubElement(ide, "tpImp").text = data.tipo_impressao
    SubElement(ide, "tpEmis").text = data.tipo_emissao
    SubElement(ide, "cDV").text = chave[-1]  # Último dígito da chave
    SubElement(ide, "tpAmb").text = data.ambiente.value
    SubElement(ide, "finNFe").text = data.finalidade.value
    SubElement(ide, "indFinal").text = "1" if data.consumidor_final else "0"
    SubElement(ide, "indPres").text = data.presenca_comprador.value
    SubElement(ide, "procEmi").text = data.processo_emissao
    SubElement(ide, "verProc").text = data.versao_processo


def _build_emit(parent: Element, nfe: NFe) -> None:
    """Constrói bloco <emit>."""
    emit = SubElement(parent, "emit")
    data = nfe.emitente

    SubElement(emit, "CNPJ").text = data.cnpj
    SubElement(emit, "xNome").text = data.razao_social
    if data.nome_fantasia:
        SubElement(emit, "xFant").text = data.nome_fantasia

    # Endereço
    ender = SubElement(emit, "enderEmit")
    end = data.endereco
    SubElement(ender, "xLgr").text = end.logradouro
    SubElement(ender, "nro").text = end.numero
    if end.complemento:
        SubElement(ender, "xCpl").text = end.complemento
    SubElement(ender, "xBairro").text = end.bairro
    SubElement(ender, "cMun").text = end.codigo_municipio
    SubElement(ender, "xMun").text = end.nome_municipio
    SubElement(ender, "UF").text = end.uf
    SubElement(ender, "CEP").text = end.cep
    SubElement(ender, "cPais").text = end.codigo_pais
    SubElement(ender, "xPais").text = end.nome_pais
    if end.telefone:
        SubElement(ender, "fone").text = end.telefone

    SubElement(emit, "IE").text = data.inscricao_estadual
    SubElement(emit, "CRT").text = data.regime_tributario.value


def _build_dest(parent: Element, nfe: NFe) -> None:
    """Constrói bloco <dest>."""
    dest = SubElement(parent, "dest")
    data = nfe.destinatario

    if data.cnpj:
        SubElement(dest, "CNPJ").text = data.cnpj
    elif data.cpf:
        SubElement(dest, "CPF").text = data.cpf

    SubElement(dest, "xNome").text = data.razao_social

    # Endereço
    ender = SubElement(dest, "enderDest")
    end = data.endereco
    SubElement(ender, "xLgr").text = end.logradouro
    SubElement(ender, "nro").text = end.numero
    if end.complemento:
        SubElement(ender, "xCpl").text = end.complemento
    SubElement(ender, "xBairro").text = end.bairro
    SubElement(ender, "cMun").text = end.codigo_municipio
    SubElement(ender, "xMun").text = end.nome_municipio
    SubElement(ender, "UF").text = end.uf
    SubElement(ender, "CEP").text = end.cep
    SubElement(ender, "cPais").text = end.codigo_pais
    SubElement(ender, "xPais").text = end.nome_pais
    if end.telefone:
        SubElement(ender, "fone").text = end.telefone

    SubElement(dest, "indIEDest").text = data.indicador_ie.value
    if data.inscricao_estadual and data.indicador_ie.value == "1":
        SubElement(dest, "IE").text = data.inscricao_estadual


def _build_det(parent: Element, nfe: NFe) -> None:
    """Constrói blocos <det> para cada produto."""
    for produto in nfe.produtos:
        det = SubElement(parent, "det", {"nItem": str(produto.numero_item)})

        # Produto
        prod = SubElement(det, "prod")
        SubElement(prod, "cProd").text = produto.codigo
        SubElement(prod, "cEAN").text = produto.ean
        SubElement(prod, "xProd").text = produto.descricao
        SubElement(prod, "NCM").text = produto.ncm
        SubElement(prod, "CFOP").text = produto.cfop
        SubElement(prod, "uCom").text = produto.unidade
        SubElement(prod, "qCom").text = _format_decimal(produto.quantidade, 4)
        SubElement(prod, "vUnCom").text = _format_decimal(produto.valor_unitario, 4)
        SubElement(prod, "vProd").text = _format_decimal(produto.valor_total, 2)
        SubElement(prod, "cEANTrib").text = produto.ean_tributavel
        SubElement(prod, "uTrib").text = produto.unidade_tributavel
        SubElement(prod, "qTrib").text = _format_decimal(
            produto.quantidade_tributavel, 4
        )
        SubElement(prod, "vUnTrib").text = _format_decimal(
            produto.valor_unitario_tributavel, 4
        )
        SubElement(prod, "indTot").text = "1" if produto.compoe_total else "0"

        # Impostos
        imposto = SubElement(det, "imposto")
        imp = produto.impostos

        # ICMS
        icms = SubElement(imposto, "ICMS")
        icms00 = SubElement(icms, "ICMS00")
        SubElement(icms00, "orig").text = imp.origem
        SubElement(icms00, "CST").text = imp.cst_icms
        SubElement(icms00, "modBC").text = imp.modalidade_bc
        SubElement(icms00, "vBC").text = _format_decimal(imp.base_calculo_icms, 2)
        SubElement(icms00, "pICMS").text = _format_decimal(imp.aliquota_icms, 2)
        SubElement(icms00, "vICMS").text = _format_decimal(imp.valor_icms, 2)

        # PIS
        pis = SubElement(imposto, "PIS")
        pis_aliq = SubElement(pis, "PISAliq")
        SubElement(pis_aliq, "CST").text = imp.cst_pis
        SubElement(pis_aliq, "vBC").text = _format_decimal(imp.base_calculo_pis, 2)
        SubElement(pis_aliq, "pPIS").text = _format_decimal(imp.aliquota_pis, 2)
        SubElement(pis_aliq, "vPIS").text = _format_decimal(imp.valor_pis, 2)

        # COFINS
        cofins = SubElement(imposto, "COFINS")
        cofins_aliq = SubElement(cofins, "COFINSAliq")
        SubElement(cofins_aliq, "CST").text = imp.cst_cofins
        SubElement(cofins_aliq, "vBC").text = _format_decimal(imp.base_calculo_cofins, 2)
        SubElement(cofins_aliq, "pCOFINS").text = _format_decimal(imp.aliquota_cofins, 2)
        SubElement(cofins_aliq, "vCOFINS").text = _format_decimal(imp.valor_cofins, 2)


def _build_total(parent: Element, nfe: NFe) -> None:
    """Constrói bloco <total>."""
    total = SubElement(parent, "total")
    icms_tot = SubElement(total, "ICMSTot")
    t = nfe.totais

    SubElement(icms_tot, "vBC").text = _format_decimal(t.base_calculo_icms, 2)
    SubElement(icms_tot, "vICMS").text = _format_decimal(t.valor_icms, 2)
    SubElement(icms_tot, "vICMSDeson").text = _format_decimal(t.valor_icms_desonerado, 2)
    SubElement(icms_tot, "vFCP").text = _format_decimal(t.valor_fcp, 2)
    SubElement(icms_tot, "vBCST").text = _format_decimal(t.base_calculo_st, 2)
    SubElement(icms_tot, "vST").text = _format_decimal(t.valor_st, 2)
    SubElement(icms_tot, "vFCPST").text = _format_decimal(t.valor_fcp_st, 2)
    SubElement(icms_tot, "vFCPSTRet").text = _format_decimal(t.valor_fcp_st_ret, 2)
    SubElement(icms_tot, "vProd").text = _format_decimal(t.valor_produtos, 2)
    SubElement(icms_tot, "vFrete").text = _format_decimal(t.valor_frete, 2)
    SubElement(icms_tot, "vSeg").text = _format_decimal(t.valor_seguro, 2)
    SubElement(icms_tot, "vDesc").text = _format_decimal(t.valor_desconto, 2)
    SubElement(icms_tot, "vII").text = _format_decimal(t.valor_ii, 2)
    SubElement(icms_tot, "vIPI").text = _format_decimal(t.valor_ipi, 2)
    SubElement(icms_tot, "vIPIDevol").text = _format_decimal(t.valor_ipi_devolvido, 2)
    SubElement(icms_tot, "vPIS").text = _format_decimal(t.valor_pis, 2)
    SubElement(icms_tot, "vCOFINS").text = _format_decimal(t.valor_cofins, 2)
    SubElement(icms_tot, "vOutro").text = _format_decimal(t.valor_outros, 2)
    SubElement(icms_tot, "vNF").text = _format_decimal(t.valor_nota, 2)


def _build_transp(parent: Element, nfe: NFe) -> None:
    """Constrói bloco <transp>."""
    transp = SubElement(parent, "transp")
    t = nfe.transporte

    SubElement(transp, "modFrete").text = t.modalidade_frete.value

    if t.cnpj_transportadora:
        transporta = SubElement(transp, "transporta")
        SubElement(transporta, "CNPJ").text = t.cnpj_transportadora
        SubElement(transporta, "xNome").text = t.nome_transportadora
        if t.ie_transportadora:
            SubElement(transporta, "IE").text = t.ie_transportadora
        SubElement(transporta, "xEnder").text = t.endereco_transportadora
        SubElement(transporta, "xMun").text = t.municipio_transportadora
        SubElement(transporta, "UF").text = t.uf_transportadora

    if t.quantidade_volumes > 0:
        vol = SubElement(transp, "vol")
        SubElement(vol, "qVol").text = str(t.quantidade_volumes)
        if t.especie:
            SubElement(vol, "esp").text = t.especie
        if t.marca:
            SubElement(vol, "marca").text = t.marca
        SubElement(vol, "pesoL").text = _format_decimal(t.peso_liquido, 3)
        SubElement(vol, "pesoB").text = _format_decimal(t.peso_bruto, 3)


def _build_cobr(parent: Element, nfe: NFe) -> None:
    """Constrói bloco <cobr>."""
    cobr = SubElement(parent, "cobr")
    c = nfe.cobranca

    fat = SubElement(cobr, "fat")
    SubElement(fat, "nFat").text = c.numero_fatura
    SubElement(fat, "vOrig").text = _format_decimal(c.valor_original, 2)
    SubElement(fat, "vDesc").text = _format_decimal(c.valor_desconto, 2)
    SubElement(fat, "vLiq").text = _format_decimal(c.valor_liquido, 2)


def _build_pag(parent: Element, nfe: NFe) -> None:
    """Constrói bloco <pag>."""
    pag = SubElement(parent, "pag")

    for pagamento in nfe.pagamentos:
        det_pag = SubElement(pag, "detPag")
        SubElement(det_pag, "tPag").text = pagamento.forma.value
        SubElement(det_pag, "vPag").text = _format_decimal(pagamento.valor, 2)

    # Se não houver pagamentos, adiciona um padrão
    if not nfe.pagamentos:
        det_pag = SubElement(pag, "detPag")
        SubElement(det_pag, "tPag").text = "90"  # Sem pagamento
        SubElement(det_pag, "vPag").text = "0.00"


def _build_inf_adic(parent: Element, nfe: NFe) -> None:
    """Constrói bloco <infAdic>."""
    inf_adic = SubElement(parent, "infAdic")
    info = nfe.informacoes_adicionais

    if info.informacoes_fisco:
        SubElement(inf_adic, "infAdFisco").text = info.informacoes_fisco
    if info.informacoes_complementares:
        SubElement(inf_adic, "infCpl").text = info.informacoes_complementares


def _build_prot_nfe(parent: Element, nfe: NFe, chave: str) -> None:
    """Constrói bloco <protNFe>."""
    prot = SubElement(parent, "protNFe", {"versao": NFE_VERSION})
    p = nfe.protocolo

    inf_prot = SubElement(prot, "infProt")
    SubElement(inf_prot, "tpAmb").text = p.ambiente.value
    SubElement(inf_prot, "verAplic").text = p.versao_aplicativo
    SubElement(inf_prot, "chNFe").text = chave
    SubElement(inf_prot, "dhRecbto").text = _format_datetime(p.data_hora_recebimento)
    SubElement(inf_prot, "nProt").text = p.numero_protocolo
    SubElement(inf_prot, "digVal").text = p.digest_value
    SubElement(inf_prot, "cStat").text = p.codigo_status
    SubElement(inf_prot, "xMotivo").text = p.motivo
