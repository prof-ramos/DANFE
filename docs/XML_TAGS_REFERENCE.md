# Documentação das tags do XML da NF-e (versão 4.00)

Este documento fornece uma referência completa e detalhada de todas as tags utilizadas no XML da Nota Fiscal Eletrônica (NFe) versão 4.00.

---

## 1. Estrutura geral

- `<?xml version="1.0" encoding="UTF-8"?>`
  - Declaração padrão XML: versão e codificação do arquivo.

- `<nfeProc versao="4.00" xmlns="http://www.portalfiscal.inf.br/nfe">`
  - Elemento raiz do "processo da NF-e", que agrupa a NF-e e o respectivo protocolo de autorização.
  - Atributos:
    - `versao`: versão do layout do nfeProc (4.00).
    - `xmlns`: namespace oficial da NF-e no Portal Fiscal.

- `<NFe>`
  - Contém os dados da Nota Fiscal Eletrônica em si (documento fiscal).

- `<infNFe Id="..." versao="4.00">`
  - Bloco principal de informações da NF-e.
  - Atributos:
    - `Id`: identificador único do documento, formado por "NFe" + chave de acesso de 44 dígitos.
    - `versao`: versão do layout da NF-e (4.00).

---

## 2. Bloco `ide` – Identificação da NF-e

`<ide>`: informações de cabeçalho que identificam a NF-e.

- `<cUF>`
  Código da UF do emitente segundo tabela do IBGE (35 = SP).

- `<cNF>`
  Código numérico (geralmente 8 dígitos), aleatório, usado para compor a chave de acesso.

- `<natOp>`
  Natureza da operação (descrição fiscal da operação: ex. "VENDA DE MERCADORIA").

- `<mod>`
  Modelo do documento fiscal.
  - `55` = NF-e (modelo 55).

- `<serie>`
  Série da NF-e (numeração paralela para organização fiscal).

- `<nNF>`
  Número da NF-e dentro da série.

- `<dhEmi>`
  Data e hora de emissão da NF-e, em formato UTC com fuso (AAAA-MM-DDThh:mm:ss-03:00).

- `<tpNF>`
  Tipo de operação:
  - `0` = entrada
  - `1` = saída

- `<idDest>`
  Identificador do local de destino da operação:
  - `1` = operação interna (dentro do próprio estado)
  - `2` = interestadual
  - `3` = exterior

- `<cMunFG>`
  Código do município de ocorrência do fato gerador do ICMS (IBGE).

- `<tpImp>`
  Formato de impressão do DANFE:
  - `1` = retrato
  - (outros valores no manual: paisagem, simplificado etc.)

- `<tpEmis>`
  Tipo de emissão da NF-e:
  - `1` = emissão normal
  - (outros códigos: contingência, FS-DA, SCAN etc.)

- `<cDV>`
  Dígito verificador da chave de acesso da NF-e (módulo 11).

- `<tpAmb>`
  Tipo de ambiente:
  - `1` = produção
  - `2` = homologação (teste, sem valor fiscal).

- `<finNFe>`
  Finalidade de emissão da NF-e:
  - `1` = NF-e normal
  - `2` = complementar
  - `3` = de ajuste
  - `4` = devolução

- `<indFinal>`
  Indicador de operação com consumidor final:
  - `0` = não
  - `1` = sim

- `<indPres>`
  Indicador de presença do comprador no estabelecimento:
  - `1` = operação presencial
  - (outros códigos: não presencial internet, teleatendimento etc.)

- `<procEmi>`
  Processo de emissão da NF-e:
  - `0` = emissão de aplicação do contribuinte
  - (outros códigos: avulsa Fisco, site da SEFAZ etc.)

- `<verProc>`
  Versão do aplicativo emissor utilizado pelo contribuinte (ex.: "1.0").

---

## 3. Bloco `emit` – Emitente

`<emit>`: dados cadastrais do emitente da NF-e.

- `<CNPJ>`
  CNPJ do emitente.

- `<xNome>`
  Razão social / nome completo do emitente.

- `<xFant>`
  Nome fantasia do emitente.

- `<enderEmit>`
  Endereço completo do emitente.

  Dentro de `<enderEmit>`:

  - `<xLgr>`
    Logradouro (rua, avenida etc.).

  - `<nro>`
    Número do endereço.

  - `<xBairro>`
    Bairro/distrito.

  - `<cMun>`
    Código do município (IBGE).

  - `<xMun>`
    Nome do município.

  - `<UF>`
    Sigla da unidade federativa (estado).

  - `<CEP>`
    CEP do endereço.

  - `<cPais>`
    Código do país (1058 = Brasil, tabela oficial).

  - `<xPais>`
    Nome do país.

  - `<fone>`
    Telefone de contato (apenas números).

- `<IE>`
  Inscrição Estadual do emitente.

- `<CRT>`
  Código do Regime Tributário do emitente:
  - `1` = Simples Nacional
  - `2` = Simples Nacional – excesso sublimite
  - `3` = Regime Normal

---

## 4. Bloco `dest` – Destinatário/Remetente

`<dest>`: dados do destinatário da mercadoria.

- `<CNPJ>`
  CNPJ do destinatário (no caso de pessoa jurídica).

- `<xNome>`
  Razão social / nome do destinatário.

- `<enderDest>`
  Endereço completo do destinatário.

  Dentro de `<enderDest>` (mesmo significado das tags de endereço do emitente):

  - `<xLgr>` – logradouro.
  - `<nro>` – número.
  - `<xBairro>` – bairro.
  - `<cMun>` – código do município (IBGE).
  - `<xMun>` – nome do município.
  - `<UF>` – sigla do estado.
  - `<CEP>` – CEP.
  - `<cPais>` – código do país (1058 = Brasil).
  - `<xPais>` – nome do país.
  - `<fone>` – telefone do destinatário.

- `<IE>`
  Inscrição Estadual do destinatário (quando `indIEDest` = 1).

- `<indIEDest>`
  Indicador da inscrição estadual do destinatário:
  - `1` = contribuinte ICMS
  - `2` = contribuinte isento
  - `9` = não contribuinte

---

## 5. Bloco `det` – Detalhamento dos Itens

`<det nItem="1">`
Contém as informações de um item da NF-e.

- Atributo:
  - `nItem`: número sequencial do item na nota.

### 5.1. Sub-bloco `prod` – Dados do Produto/Serviço

`<prod>`: dados comerciais e fiscais do item.

- `<cProd>`
  Código interno ou do sistema para o produto.

- `<cEAN>`
  Código de barras EAN/GTIN da unidade comercial.
  - Valor "SEM GTIN" indica ausência de GTIN cadastrado.

- `<xProd>`
  Descrição do produto/serviço.

- `<NCM>`
  Código NCM (Nomenclatura Comum do Mercosul), usado para classificação fiscal.

- `<CFOP>`
  Código Fiscal de Operações e Prestações, que define a natureza fiscal da movimentação (ex.: 5102 = venda de mercadoria adquirida/recebida de terceiros dentro do estado).

- `<uCom>`
  Unidade de medida comercial (ex.: UN, KG, CX etc.).

- `<qCom>`
  Quantidade comercial do item.

- `<vUnCom>`
  Valor unitário de comercialização.

- `<vProd>`
  Valor total bruto do produto (qCom × vUnCom).

- `<cEANTrib>`
  Código de barras da unidade tributável (pode ser o mesmo do comercial).
  - "SEM GTIN" se não houver.

- `<uTrib>`
  Unidade de medida tributável (pode ser igual à unidade comercial).

- `<qTrib>`
  Quantidade na unidade tributável.

- `<vUnTrib>`
  Valor unitário na unidade tributável.

- `<indTot>`
  Indica se o valor do item compõe o total da NF-e:
  - `0` = não compõe
  - `1` = compõe (caso padrão para produtos faturados)

---

## 6. Bloco `imposto` – Tributos por Item

`<imposto>`: agrupa os tributos incidentes sobre o item.

### 6.1. ICMS

- `<ICMS>`
  Bloco geral de ICMS.

- `<ICMS00>`
  Grupo de tributação do ICMS com CST 00 (tributação integral, sem benefícios).

  Dentro de `<ICMS00>`:

  - `<orig>`
    Origem da mercadoria:
    - `0` = nacional
    - (outros códigos: importado, nacional com conteúdo importado etc.)

  - `<CST>`
    Código de Situação Tributária do ICMS (00 = tributação integral).

  - `<modBC>`
    Modalidade de determinação da base de cálculo do ICMS.
    - `3` = valor da operação (mais comum em venda interna).

  - `<vBC>`
    Valor da base de cálculo do ICMS.

  - `<pICMS>`
    Alíquota do ICMS (percentual).

  - `<vICMS>`
    Valor do ICMS calculado (vBC × pICMS).

### 6.2. PIS

- `<PIS>`
  Agrupa informações de PIS.

- `<PISAliq>`
  Grupo para PIS calculado por alíquota sobre base de cálculo.

  Dentro de `<PISAliq>`:

  - `<CST>`
    Código de Situação Tributária do PIS (01 = operação tributável com alíquota).

  - `<vBC>`
    Base de cálculo do PIS.

  - `<pPIS>`
    Alíquota do PIS (percentual).

  - `<vPIS>`
    Valor do PIS (vBC × pPIS).

### 6.3. COFINS

- `<COFINS>`
  Agrupa informações de COFINS.

- `<COFINSAliq>`
  Grupo para COFINS calculado por alíquota sobre base de cálculo.

  Dentro de `<COFINSAliq>`:

  - `<CST>`
    Código de Situação Tributária do COFINS (01 = operação tributável com alíquota).

  - `<vBC>`
    Base de cálculo do COFINS.

  - `<pCOFINS>`
    Alíquota do COFINS (percentual).

  - `<vCOFINS>`
    Valor do COFINS (vBC × pCOFINS).

---

## 7. Bloco `total` – Totais da Nota

`<total>`: agrupa os valores totais da NF-e.

- `<ICMSTot>`
  Totais relacionados a ICMS e outros tributos.

  Dentro de `<ICMSTot>`:

  - `<vBC>`
    Soma das bases de cálculo do ICMS de todos os itens.

  - `<vICMS>`
    Soma dos valores de ICMS de todos os itens.

  - `<vICMSDeson>`
    Valor total de ICMS desonerado (isenções/benefícios). Aqui: 0,00.

  - `<vFCP>`
    Valor total do Fundo de Combate à Pobreza (FCP) na operação.

  - `<vBCST>`
    Base de cálculo do ICMS ST (substituição tributária).

  - `<vST>`
    Valor total do ICMS ST.

  - `<vFCPST>`
    Valor total de FCP retido por substituição tributária.

  - `<vFCPSTRet>`
    Valor total de FCP ST retido anteriormente.

  - `<vProd>`
    Soma dos valores dos produtos/serviços.

  - `<vFrete>`
    Valor total de frete na NF-e.

  - `<vSeg>`
    Valor total do seguro.

  - `<vDesc>`
    Valor total de descontos concedidos.

  - `<vII>`
    Valor total de Imposto de Importação.

  - `<vIPI>`
    Valor total de IPI.

  - `<vIPIDevol>`
    Valor de IPI devolvido (em devoluções de mercadoria).

  - `<vPIS>`
    Valor total de PIS da NF-e.

  - `<vCOFINS>`
    Valor total de COFINS da NF-e.

  - `<vOutro>`
    Outras despesas acessórias.

  - `<vNF>`
    Valor total da NF-e (total a pagar).

---

## 8. Bloco `transp` – Transporte

`<transp>`: informações sobre frete e transportador.

- `<modFrete>`
  Modalidade do frete: quem é o responsável pelo pagamento.
  Alguns valores comuns:
  - `0` = emitente
  - `1` = destinatário/remetente
  - `2` = terceiros
  - `9` = sem frete
  No XML: `9` = operação sem cobrança de frete.

---

## 9. Bloco `protNFe` – Protocolo de Autorização

`<protNFe versao="4.00">`
Contém o protocolo de autorização emitido pela SEFAZ para a NF-e.

- Atributo `versao`: versão do layout do protocolo.

- `<infProt>`
  Dados do protocolo.

  Dentro de `<infProt>`:

  - `<tpAmb>`
    Ambiente da autorização (mesmo conceito de `ide/tpAmb`):
    - `1` = produção
    - `2` = homologação

  - `<verAplic>`
    Versão do aplicativo da SEFAZ que processou/autorizou a NF-e.

  - `<chNFe>`
    Chave de acesso da NF-e (44 dígitos).

  - `<dhRecbto>`
    Data e hora em que a NF-e foi recebida e processada pela SEFAZ.

  - `<nProt>`
    Número do protocolo de autorização de uso da NF-e.

  - `<digVal>`
    Hash (digest value) do XML da NF-e, usado para validação de integridade.

  - `<cStat>`
    Código do status de retorno da SEFAZ para a NF-e.
    - `100` = Autorizado o uso da NF-e.

  - `<xMotivo>`
    Descrição textual do status (`cStat`), por exemplo "Autorizado o uso da NF-e".

---

## 10. Exemplo Completo de XML com `protNFe`

O exemplo abaixo mostra um XML completo de NF-e autorizada, incluindo o protocolo de autorização da SEFAZ:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<nfeProc versao="4.00" xmlns="http://www.portalfiscal.inf.br/nfe">
  <NFe xmlns="http://www.portalfiscal.inf.br/nfe">
    <infNFe versao="4.00" Id="NFe35231212345678000195550010000000011000000015">
      <!-- ========================================== -->
      <!-- BLOCO IDE - Identificação da NF-e         -->
      <!-- ========================================== -->
      <ide>
        <cUF>35</cUF>                                    <!-- SP -->
        <cNF>00000001</cNF>                              <!-- Código numérico -->
        <natOp>VENDA DE MERCADORIA</natOp>               <!-- Natureza da operação -->
        <mod>55</mod>                                    <!-- Modelo NF-e -->
        <serie>1</serie>                                 <!-- Série -->
        <nNF>1</nNF>                                     <!-- Número -->
        <dhEmi>2023-12-04T10:00:00-03:00</dhEmi>         <!-- Data/hora emissão -->
        <tpNF>1</tpNF>                                   <!-- 1 = Saída -->
        <idDest>1</idDest>                               <!-- 1 = Operação interna -->
        <cMunFG>3550308</cMunFG>                         <!-- São Paulo (IBGE) -->
        <tpImp>1</tpImp>                                 <!-- 1 = Retrato -->
        <tpEmis>1</tpEmis>                               <!-- 1 = Normal -->
        <cDV>5</cDV>                                     <!-- Dígito verificador -->
        <tpAmb>1</tpAmb>                                 <!-- 1 = PRODUÇÃO -->
        <finNFe>1</finNFe>                               <!-- 1 = Normal -->
        <indFinal>1</indFinal>                           <!-- 1 = Consumidor final -->
        <indPres>1</indPres>                             <!-- 1 = Presencial -->
        <procEmi>0</procEmi>                             <!-- 0 = App contribuinte -->
        <verProc>1.0</verProc>                           <!-- Versão app -->
      </ide>

      <!-- ========================================== -->
      <!-- BLOCO EMIT - Dados do Emitente            -->
      <!-- ========================================== -->
      <emit>
        <CNPJ>12345678000195</CNPJ>
        <xNome>EMPRESA EMITENTE LTDA</xNome>
        <xFant>LOJA EXEMPLO</xFant>
        <enderEmit>
          <xLgr>RUA DAS FLORES</xLgr>
          <nro>1000</nro>
          <xBairro>CENTRO</xBairro>
          <cMun>3550308</cMun>
          <xMun>SAO PAULO</xMun>
          <UF>SP</UF>
          <CEP>01001000</CEP>
          <cPais>1058</cPais>
          <xPais>BRASIL</xPais>
          <fone>1133334444</fone>
        </enderEmit>
        <IE>123456789012</IE>
        <CRT>3</CRT>                                     <!-- 3 = Regime Normal -->
      </emit>

      <!-- ========================================== -->
      <!-- BLOCO DEST - Dados do Destinatário        -->
      <!-- ========================================== -->
      <dest>
        <CNPJ>98765432000198</CNPJ>
        <xNome>CLIENTE DESTINATARIO LTDA</xNome>
        <enderDest>
          <xLgr>AVENIDA PAULISTA</xLgr>
          <nro>2000</nro>
          <xBairro>BELA VISTA</xBairro>
          <cMun>3550308</cMun>
          <xMun>SAO PAULO</xMun>
          <UF>SP</UF>
          <CEP>01310100</CEP>
          <cPais>1058</cPais>
          <xPais>BRASIL</xPais>
          <fone>1199998888</fone>
        </enderDest>
        <indIEDest>1</indIEDest>                         <!-- 1 = Contribuinte ICMS -->
        <IE>987654321098</IE>
      </dest>

      <!-- ========================================== -->
      <!-- BLOCO DET - Detalhamento dos Itens        -->
      <!-- ========================================== -->
      <det nItem="1">
        <prod>
          <cProd>PROD001</cProd>
          <cEAN>7891234567890</cEAN>                     <!-- Código de barras -->
          <xProd>NOTEBOOK DELL INSPIRON 15</xProd>
          <NCM>84713012</NCM>                            <!-- NCM para notebooks -->
          <CFOP>5102</CFOP>                              <!-- Venda merc. adquirida -->
          <uCom>UN</uCom>
          <qCom>2.0000</qCom>
          <vUnCom>3500.0000</vUnCom>
          <vProd>7000.00</vProd>
          <cEANTrib>7891234567890</cEANTrib>
          <uTrib>UN</uTrib>
          <qTrib>2.0000</qTrib>
          <vUnTrib>3500.0000</vUnTrib>
          <indTot>1</indTot>                             <!-- 1 = Compõe total -->
        </prod>
        <imposto>
          <ICMS>
            <ICMS00>
              <orig>0</orig>                             <!-- 0 = Nacional -->
              <CST>00</CST>                              <!-- 00 = Trib. integral -->
              <modBC>3</modBC>                           <!-- 3 = Valor operação -->
              <vBC>7000.00</vBC>
              <pICMS>18.00</pICMS>
              <vICMS>1260.00</vICMS>
            </ICMS00>
          </ICMS>
          <PIS>
            <PISAliq>
              <CST>01</CST>                              <!-- 01 = Tributável -->
              <vBC>7000.00</vBC>
              <pPIS>1.65</pPIS>
              <vPIS>115.50</vPIS>
            </PISAliq>
          </PIS>
          <COFINS>
            <COFINSAliq>
              <CST>01</CST>                              <!-- 01 = Tributável -->
              <vBC>7000.00</vBC>
              <pCOFINS>7.60</pCOFINS>
              <vCOFINS>532.00</vCOFINS>
            </COFINSAliq>
          </COFINS>
        </imposto>
      </det>

      <det nItem="2">
        <prod>
          <cProd>PROD002</cProd>
          <cEAN>SEM GTIN</cEAN>
          <xProd>MOUSE WIRELESS LOGITECH</xProd>
          <NCM>84716052</NCM>
          <CFOP>5102</CFOP>
          <uCom>UN</uCom>
          <qCom>5.0000</qCom>
          <vUnCom>150.0000</vUnCom>
          <vProd>750.00</vProd>
          <cEANTrib>SEM GTIN</cEANTrib>
          <uTrib>UN</uTrib>
          <qTrib>5.0000</qTrib>
          <vUnTrib>150.0000</vUnTrib>
          <indTot>1</indTot>
        </prod>
        <imposto>
          <ICMS>
            <ICMS00>
              <orig>0</orig>
              <CST>00</CST>
              <modBC>3</modBC>
              <vBC>750.00</vBC>
              <pICMS>18.00</pICMS>
              <vICMS>135.00</vICMS>
            </ICMS00>
          </ICMS>
          <PIS>
            <PISAliq>
              <CST>01</CST>
              <vBC>750.00</vBC>
              <pPIS>1.65</pPIS>
              <vPIS>12.38</vPIS>
            </PISAliq>
          </PIS>
          <COFINS>
            <COFINSAliq>
              <CST>01</CST>
              <vBC>750.00</vBC>
              <pCOFINS>7.60</pCOFINS>
              <vCOFINS>57.00</vCOFINS>
            </COFINSAliq>
          </COFINS>
        </imposto>
      </det>

      <!-- ========================================== -->
      <!-- BLOCO TOTAL - Totais da NF-e              -->
      <!-- ========================================== -->
      <total>
        <ICMSTot>
          <vBC>7750.00</vBC>                             <!-- Base ICMS total -->
          <vICMS>1395.00</vICMS>                         <!-- ICMS total -->
          <vICMSDeson>0.00</vICMSDeson>
          <vFCP>0.00</vFCP>
          <vBCST>0.00</vBCST>
          <vST>0.00</vST>
          <vFCPST>0.00</vFCPST>
          <vFCPSTRet>0.00</vFCPSTRet>
          <vProd>7750.00</vProd>                         <!-- Total produtos -->
          <vFrete>0.00</vFrete>
          <vSeg>0.00</vSeg>
          <vDesc>0.00</vDesc>
          <vII>0.00</vII>
          <vIPI>0.00</vIPI>
          <vIPIDevol>0.00</vIPIDevol>
          <vPIS>127.88</vPIS>                            <!-- PIS total -->
          <vCOFINS>589.00</vCOFINS>                      <!-- COFINS total -->
          <vOutro>0.00</vOutro>
          <vNF>7750.00</vNF>                             <!-- VALOR TOTAL NF-e -->
        </ICMSTot>
      </total>

      <!-- ========================================== -->
      <!-- BLOCO TRANSP - Transporte                 -->
      <!-- ========================================== -->
      <transp>
        <modFrete>0</modFrete>                           <!-- 0 = Por conta emitente -->
        <transporta>
          <CNPJ>11222333000144</CNPJ>
          <xNome>TRANSPORTADORA RAPIDA LTDA</xNome>
          <IE>111222333444</IE>
          <xEnder>ROD. DOS BANDEIRANTES KM 50</xEnder>
          <xMun>CAMPINAS</xMun>
          <UF>SP</UF>
        </transporta>
        <vol>
          <qVol>2</qVol>                                 <!-- Quantidade volumes -->
          <esp>CAIXA</esp>                               <!-- Espécie -->
          <marca>DELL</marca>
          <pesoL>5.500</pesoL>                           <!-- Peso líquido (kg) -->
          <pesoB>6.200</pesoB>                           <!-- Peso bruto (kg) -->
        </vol>
      </transp>

      <!-- ========================================== -->
      <!-- BLOCO COBR - Cobrança (opcional)          -->
      <!-- ========================================== -->
      <cobr>
        <fat>
          <nFat>000001</nFat>                            <!-- Número da fatura -->
          <vOrig>7750.00</vOrig>                         <!-- Valor original -->
          <vDesc>0.00</vDesc>
          <vLiq>7750.00</vLiq>                           <!-- Valor líquido -->
        </fat>
        <dup>
          <nDup>001</nDup>                               <!-- Número duplicata -->
          <dVenc>2024-01-04</dVenc>                      <!-- Data vencimento -->
          <vDup>7750.00</vDup>                           <!-- Valor -->
        </dup>
      </cobr>

      <!-- ========================================== -->
      <!-- BLOCO PAG - Pagamento                     -->
      <!-- ========================================== -->
      <pag>
        <detPag>
          <tPag>01</tPag>                                <!-- 01 = Dinheiro -->
          <vPag>7750.00</vPag>
        </detPag>
      </pag>

      <!-- ========================================== -->
      <!-- BLOCO INFADIC - Informações Adicionais    -->
      <!-- ========================================== -->
      <infAdic>
        <infCpl>Venda realizada conforme pedido 12345. Garantia de 12 meses.</infCpl>
      </infAdic>

    </infNFe>

    <!-- ========================================== -->
    <!-- ASSINATURA DIGITAL (obrigatória)          -->
    <!-- ========================================== -->
    <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
      <SignedInfo>
        <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
        <SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
        <Reference URI="#NFe35231212345678000195550010000000011000000015">
          <Transforms>
            <Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
            <Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
          </Transforms>
          <DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
          <DigestValue>kH5B3sLz9mT2vNpYq...</DigestValue>
        </Reference>
      </SignedInfo>
      <SignatureValue>XyZ123AbC456...</SignatureValue>
      <KeyInfo>
        <X509Data>
          <X509Certificate>MIIGwDCCBaigAwIBAgIQ...</X509Certificate>
        </X509Data>
      </KeyInfo>
    </Signature>

  </NFe>

  <!-- ============================================================ -->
  <!-- BLOCO PROTNFE - Protocolo de Autorização da SEFAZ           -->
  <!-- Este bloco é ADICIONADO pela SEFAZ após autorização         -->
  <!-- ============================================================ -->
  <protNFe versao="4.00">
    <infProt Id="ID135231212345678901234567890123456789012345">
      <tpAmb>1</tpAmb>                                   <!-- 1 = Produção -->
      <verAplic>SP_NFE_PL_008i2</verAplic>               <!-- Versão SEFAZ -->
      <chNFe>35231212345678000195550010000000011000000015</chNFe>
      <dhRecbto>2023-12-04T10:01:15-03:00</dhRecbto>     <!-- Data/hora recebimento -->
      <nProt>135231234567890</nProt>                     <!-- Número protocolo -->
      <digVal>kH5B3sLz9mT2vNpYqRxWz1a2b3c=</digVal>      <!-- Digest XML -->
      <cStat>100</cStat>                                 <!-- 100 = AUTORIZADA -->
      <xMotivo>Autorizado o uso da NF-e</xMotivo>        <!-- Descrição status -->
    </infProt>
  </protNFe>

</nfeProc>
```

### Observações sobre o exemplo

1. **Ambiente de Produção**: O XML acima usa `tpAmb = 1` (produção), diferente do XML de teste que usa homologação.

2. **Múltiplos Itens**: O exemplo inclui 2 produtos (`det nItem="1"` e `det nItem="2"`) para demonstrar como são listados múltiplos itens.

3. **Bloco `transp` Completo**: Inclui dados do transportador e volumes, não apenas a modalidade de frete.

4. **Blocos Adicionais**: Demonstra blocos opcionais como:
   - `<cobr>` - Dados de cobrança/fatura
   - `<pag>` - Forma de pagamento
   - `<infAdic>` - Informações complementares
   - `<Signature>` - Assinatura digital (obrigatória)

5. **Protocolo SEFAZ**: O bloco `<protNFe>` com `cStat = 100` confirma que a NF-e foi autorizada.

6. **Valores Coerentes**: Os totais (vBC, vICMS, vPIS, vCOFINS, vNF) refletem a soma dos itens.

---

## Referências

- [Portal Nacional da NFe](https://www.nfe.fazenda.gov.br/)
- [Manual de Orientação do Contribuinte - MOC](https://www.nfe.fazenda.gov.br/portal/listaConteudo.aspx?tipoConteudo=BMPFMBoln3w=)
- [Schemas XML da NFe](https://www.nfe.fazenda.gov.br/portal/listaConteudo.aspx?tipoConteudo=SDSDxDtxjzw=)

---

**DANFE Generator** - Referência Completa das Tags XML
