# 📋 Estrutura do XML de NFe


Este documento descreve a estrutura do XML de Nota Fiscal Eletrônica (NFe) utilizado pelo DANFE Generator.

---

## Visão Geral

O arquivo XML de NFe segue o padrão definido pelo Portal da Nota Fiscal Eletrônica do Brasil. A estrutura básica é:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<nfeProc versao="4.00" xmlns="http://www.portalfiscal.inf.br/nfe">
    <NFe>
        <infNFe Id="NFe..." versao="4.00">
            <!-- Conteúdo da NFe -->
        </infNFe>
    </NFe>
    <protNFe versao="4.00">
        <!-- Protocolo de autorização -->
    </protNFe>
</nfeProc>
```

---

## Elementos Principais

### 1. `<nfeProc>` - Raiz do Documento

Elemento raiz que contém a NFe e seu protocolo de autorização.

| Atributo | Descrição |
|----------|-----------|
| `versao` | Versão do layout (ex: "4.00") |
| `xmlns` | Namespace XML |

---

### 2. `<NFe>` - Nota Fiscal Eletrônica

Contém o elemento `<infNFe>` com todos os dados da nota.

---

### 3. `<infNFe>` - Informações da NFe

| Atributo | Descrição | Exemplo |
|----------|-----------|---------|
| `Id` | Identificador único (chave de acesso) | `NFe35231200000000000000550010000000011000000000` |
| `versao` | Versão do layout | `4.00` |

---

## Grupos de Informações

### `<ide>` - Identificação da NFe

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `cUF` | Código da UF do emitente | `35` (SP) |
| `cNF` | Código numérico da NFe | `00000001` |
| `natOp` | Natureza da operação | `VENDA DE MERCADORIA` |
| `mod` | Modelo do documento | `55` (NFe) |
| `serie` | Série do documento | `1` |
| `nNF` | Número da NFe | `1` |
| `dhEmi` | Data/hora de emissão | `2023-12-04T12:00:00-03:00` |
| `tpNF` | Tipo da NFe | `1` (Saída) |
| `idDest` | Destino da operação | `1` (Interna) |
| `cMunFG` | Código do município | `3550308` (São Paulo) |
| `tpImp` | Tipo de impressão | `1` (Retrato) |
| `tpEmis` | Tipo de emissão | `1` (Normal) |
| `cDV` | Dígito verificador | `0` |
| `tpAmb` | Ambiente | `1` (Produção), `2` (Homologação) |
| `finNFe` | Finalidade | `1` (Normal) |
| `indFinal` | Consumidor final | `1` (Sim) |
| `indPres` | Presença do comprador | `1` (Presencial) |
| `procEmi` | Processo de emissão | `0` (Aplicativo próprio) |
| `verProc` | Versão do aplicativo | `1.0` |

---

### `<emit>` - Emitente

| Campo | Descrição |
|-------|-----------|
| `CNPJ` | CNPJ do emitente |
| `xNome` | Razão social |
| `xFant` | Nome fantasia |
| `IE` | Inscrição estadual |
| `CRT` | Código de regime tributário |

#### `<enderEmit>` - Endereço do Emitente

| Campo | Descrição |
|-------|-----------|
| `xLgr` | Logradouro |
| `nro` | Número |
| `xBairro` | Bairro |
| `cMun` | Código do município (IBGE) |
| `xMun` | Nome do município |
| `UF` | Sigla do estado |
| `CEP` | CEP |
| `cPais` | Código do país |
| `xPais` | Nome do país |
| `fone` | Telefone |

---

### `<dest>` - Destinatário

| Campo | Descrição |
|-------|-----------|
| `CNPJ` ou `CPF` | Documento do destinatário |
| `xNome` | Nome/Razão social |
| `indIEDest` | Indicador de IE: `1` (Contribuinte), `2` (Isento), `9` (Não contribuinte) |

#### `<enderDest>` - Endereço do Destinatário

Mesma estrutura de `<enderEmit>`.

---

### `<det>` - Detalhes dos Produtos/Serviços

Pode haver múltiplos elementos `<det>`, um para cada item.

| Atributo | Descrição |
|----------|-----------|
| `nItem` | Número sequencial do item |

#### `<prod>` - Dados do Produto

| Campo | Descrição |
|-------|-----------|
| `cProd` | Código do produto |
| `cEAN` | Código de barras (GTIN) |
| `xProd` | Descrição do produto |
| `NCM` | Código NCM |
| `CFOP` | Código fiscal da operação |
| `uCom` | Unidade comercial |
| `qCom` | Quantidade comercial |
| `vUnCom` | Valor unitário |
| `vProd` | Valor total do produto |
| `indTot` | Indica se compõe o total |

#### `<imposto>` - Impostos

Contém grupos de tributação: `<ICMS>`, `<PIS>`, `<COFINS>`, `<IPI>`, etc.

---

### `<total>` - Totais da NFe

#### `<ICMSTot>` - Totais de ICMS

| Campo | Descrição |
|-------|-----------|
| `vBC` | Base de cálculo do ICMS |
| `vICMS` | Valor do ICMS |
| `vProd` | Valor total dos produtos |
| `vFrete` | Valor do frete |
| `vSeg` | Valor do seguro |
| `vDesc` | Valor do desconto |
| `vPIS` | Valor do PIS |
| `vCOFINS` | Valor da COFINS |
| `vNF` | Valor total da NFe |

---

### `<transp>` - Transporte

| Campo | Descrição |
|-------|-----------|
| `modFrete` | Modalidade do frete: `0` (Emitente), `1` (Destinatário), `9` (Sem frete) |

---

### `<protNFe>` - Protocolo de Autorização

| Campo | Descrição |
|-------|-----------|
| `tpAmb` | Ambiente |
| `verAplic` | Versão do aplicativo SEFAZ |
| `chNFe` | Chave de acesso (44 dígitos) |
| `dhRecbto` | Data/hora do recebimento |
| `nProt` | Número do protocolo |
| `digVal` | Digest value da assinatura |
| `cStat` | Código do status (100 = autorizado) |
| `xMotivo` | Descrição do status |

---

## XML de Exemplo Completo

```xml
<?xml version="1.0" encoding="UTF-8"?>
<nfeProc versao="4.00" xmlns="http://www.portalfiscal.inf.br/nfe">
    <NFe>
        <infNFe Id="NFe35231200000000000000550010000000011000000000" versao="4.00">
            <ide>
                <cUF>35</cUF>
                <cNF>00000001</cNF>
                <natOp>VENDA DE MERCADORIA</natOp>
                <mod>55</mod>
                <serie>1</serie>
                <nNF>1</nNF>
                <dhEmi>2023-12-04T12:00:00-03:00</dhEmi>
                <tpNF>1</tpNF>
                <idDest>1</idDest>
                <cMunFG>3550308</cMunFG>
                <tpImp>1</tpImp>
                <tpEmis>1</tpEmis>
                <cDV>0</cDV>
                <tpAmb>2</tpAmb>
                <finNFe>1</finNFe>
                <indFinal>1</indFinal>
                <indPres>1</indPres>
                <procEmi>0</procEmi>
                <verProc>1.0</verProc>
            </ide>
            <emit>
                <CNPJ>00000000000000</CNPJ>
                <xNome>EMPRESA EMITENTE LTDA</xNome>
                <xFant>EMPRESA TESTE</xFant>
                <enderEmit>
                    <xLgr>RUA DE TESTE</xLgr>
                    <nro>123</nro>
                    <xBairro>BAIRRO TESTE</xBairro>
                    <cMun>3550308</cMun>
                    <xMun>SAO PAULO</xMun>
                    <UF>SP</UF>
                    <CEP>00000000</CEP>
                    <cPais>1058</cPais>
                    <xPais>BRASIL</xPais>
                    <fone>1100000000</fone>
                </enderEmit>
                <IE>000000000000</IE>
                <CRT>3</CRT>
            </emit>
            <dest>
                <CNPJ>11111111111111</CNPJ>
                <xNome>CLIENTE DESTINATARIO TESTE</xNome>
                <enderDest>
                    <xLgr>RUA DO CLIENTE</xLgr>
                    <nro>456</nro>
                    <xBairro>BAIRRO CLIENTE</xBairro>
                    <cMun>3550308</cMun>
                    <xMun>SAO PAULO</xMun>
                    <UF>SP</UF>
                    <CEP>11111111</CEP>
                    <cPais>1058</cPais>
                    <xPais>BRASIL</xPais>
                    <fone>1111111111</fone>
                </enderDest>
                <indIEDest>9</indIEDest>
            </dest>
            <det nItem="1">
                <prod>
                    <cProd>001</cProd>
                    <cEAN>SEM GTIN</cEAN>
                    <xProd>PRODUTO TESTE 01</xProd>
                    <NCM>00000000</NCM>
                    <CFOP>5102</CFOP>
                    <uCom>UN</uCom>
                    <qCom>1.0000</qCom>
                    <vUnCom>100.0000</vUnCom>
                    <vProd>100.00</vProd>
                    <cEANTrib>SEM GTIN</cEANTrib>
                    <uTrib>UN</uTrib>
                    <qTrib>1.0000</qTrib>
                    <vUnTrib>100.0000</vUnTrib>
                    <indTot>1</indTot>
                </prod>
                <imposto>
                    <ICMS>
                        <ICMS00>
                            <orig>0</orig>
                            <CST>00</CST>
                            <modBC>3</modBC>
                            <vBC>100.00</vBC>
                            <pICMS>18.00</pICMS>
                            <vICMS>18.00</vICMS>
                        </ICMS00>
                    </ICMS>
                    <PIS>
                        <PISAliq>
                            <CST>01</CST>
                            <vBC>100.00</vBC>
                            <pPIS>1.65</pPIS>
                            <vPIS>1.65</vPIS>
                        </PISAliq>
                    </PIS>
                    <COFINS>
                        <COFINSAliq>
                            <CST>01</CST>
                            <vBC>100.00</vBC>
                            <pCOFINS>7.60</pCOFINS>
                            <vCOFINS>7.60</vCOFINS>
                        </COFINSAliq>
                    </COFINS>
                </imposto>
            </det>
            <total>
                <ICMSTot>
                    <vBC>100.00</vBC>
                    <vICMS>18.00</vICMS>
                    <vICMSDeson>0.00</vICMSDeson>
                    <vFCP>0.00</vFCP>
                    <vBCST>0.00</vBCST>
                    <vST>0.00</vST>
                    <vFCPST>0.00</vFCPST>
                    <vFCPSTRet>0.00</vFCPSTRet>
                    <vProd>100.00</vProd>
                    <vFrete>0.00</vFrete>
                    <vSeg>0.00</vSeg>
                    <vDesc>0.00</vDesc>
                    <vII>0.00</vII>
                    <vIPI>0.00</vIPI>
                    <vIPIDevol>0.00</vIPIDevol>
                    <vPIS>1.65</vPIS>
                    <vCOFINS>7.60</vCOFINS>
                    <vOutro>0.00</vOutro>
                    <vNF>100.00</vNF>
                </ICMSTot>
            </total>
            <transp>
                <modFrete>9</modFrete>
            </transp>
        </infNFe>
    </NFe>
    <protNFe versao="4.00">
        <infProt>
            <tpAmb>2</tpAmb>
            <verAplic>1.0</verAplic>
            <chNFe>35231200000000000000550010000000011000000000</chNFe>
            <dhRecbto>2023-12-04T12:00:00-03:00</dhRecbto>
            <nProt>135230000000000</nProt>
            <digVal>...</digVal>
            <cStat>100</cStat>
            <xMotivo>Autorizado o uso da NF-e</xMotivo>
        </infProt>
    </protNFe>
</nfeProc>
```

---

## Referências

- [Portal Nacional da NFe](https://www.nfe.fazenda.gov.br/)
- [Manual de Orientação do Contribuinte - MOC](https://www.nfe.fazenda.gov.br/portal/listaConteudo.aspx?tipoConteudo=BMPFMBoln3w=)
- [Schemas XML da NFe](https://www.nfe.fazenda.gov.br/portal/listaConteudo.aspx?tipoConteudo=SDSDxDtxjzw=)

---

**DANFE Generator** - Documentação da Estrutura XML
