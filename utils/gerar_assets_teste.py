import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def criar_logo_teste(path: str):
    """Cria uma imagem PNG simples para servir de logo."""
    width, height = 300, 200
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Desenhar um retângulo e texto
    draw.rectangle([10, 10, width-10, height-10], outline=(33, 128, 141), width=5)

    # Tentar carregar fonte padrão, senão usar default
    try:
        font = ImageFont.truetype("Arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    text = "LOGO\nTESTE"

    # Calcular posição central (aproximada para fonte default)
    # bbox = draw.textbbox((0, 0), text, font=font)
    # text_width = bbox[2] - bbox[0]
    # text_height = bbox[3] - bbox[1]
    # position = ((width - text_width) / 2, (height - text_height) / 2)

    draw.text((70, 50), text, fill=(33, 128, 141), font=font)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    image.save(path)
    print(f"✓ Logo criada: {path}")

def criar_xml_teste(path: str):
    """Cria um XML de NFe mínimo válido para teste."""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<nfeProc versao="4.00" xmlns="http://www.portalfiscal.inf.br/nfe">
  <NFe xmlns="http://www.portalfiscal.inf.br/nfe">
    <infNFe versao="4.00" Id="NFe35231212345678000195550010000000011000000015">
      <ide>
        <cUF>35</cUF>
        <cNF>00000001</cNF>
        <natOp>VENDA DE MERCADORIA</natOp>
        <mod>55</mod>
        <serie>1</serie>
        <nNF>1</nNF>
        <dhEmi>2023-12-04T10:00:00-03:00</dhEmi>
        <tpNF>1</tpNF>
        <idDest>1</idDest>
        <cMunFG>3550308</cMunFG>
        <tpImp>1</tpImp>
        <tpEmis>1</tpEmis>
        <cDV>5</cDV>
        <tpAmb>2</tpAmb>
        <finNFe>1</finNFe>
        <indFinal>1</indFinal>
        <indPres>1</indPres>
        <procEmi>0</procEmi>
        <verProc>1.0</verProc>
      </ide>
      <emit>
        <CNPJ>12345678000195</CNPJ>
        <xNome>EMPRESA TESTE LTDA</xNome>
        <xFant>EMPRESA TESTE</xFant>
        <enderEmit>
          <xLgr>RUA TESTE</xLgr>
          <nro>123</nro>
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
        <CRT>3</CRT>
      </emit>
      <dest>
        <CNPJ>98765432000198</CNPJ>
        <xNome>CLIENTE TESTE LTDA</xNome>
        <enderDest>
          <xLgr>AVENIDA TESTE</xLgr>
          <nro>456</nro>
          <xBairro>BAIRRO TESTE</xBairro>
          <cMun>3550308</cMun>
          <xMun>SAO PAULO</xMun>
          <UF>SP</UF>
          <CEP>02002000</CEP>
          <cPais>1058</cPais>
          <xPais>BRASIL</xPais>
        </enderDest>
        <indIEDest>1</indIEDest>
        <IE>987654321098</IE>
      </dest>
      <det nItem="1">
        <prod>
          <cProd>001</cProd>
          <cEAN>SEM GTIN</cEAN>
          <xProd>PRODUTO TESTE 1</xProd>
          <NCM>85044021</NCM>
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
</nfeProc>
"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(xml_content.strip())
    print(f"✓ XML criado: {path}")

if __name__ == "__main__":
    criar_logo_teste("./logos/logo.png")
    criar_xml_teste("./xmls/nfe_teste.xml")
