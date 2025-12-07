#!/usr/bin/env python3
"""Script para gerar DANFE com logo personalizado."""

import sys
from pathlib import Path
from danfe_gerador import DANFEPersonalizado

def main():
    # Cores da empresa (ASOF)
    cores_asof = {
        'primary': [41, 150, 161],      # Teal ASOF
        'secondary': [94, 82, 64],      # Marrom neutro
        'accent': [192, 21, 47],        # Vermelho
    }

    # Margens padrão
    margens = {
        'top': 10,
        'right': 10,
        'bottom': 10,
        'left': 10
    }

    # Criar gerador
    print("🔧 Inicializando gerador DANFE...")
    gerador = DANFEPersonalizado(
        logo_path='./logos/logo.png',
        empresa_nome='ASOF',
        cores_personalizadas=cores_asof,
        margens=margens
    )

    # Opções
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg == '--lote':
            # Processar lote
            pasta_xmls = Path('./xmls')
            pasta_saida = Path('./danfes_saida')

            if not pasta_xmls.exists():
                print(f"✗ Pasta não encontrada: {pasta_xmls}")
                return 1

            gerador.gerar_lote(str(pasta_xmls), str(pasta_saida))

        elif arg.endswith('.xml'):
            # Gerar single
            xml_path = arg
            output = Path(xml_path).stem + '.pdf'

            gerador.gerar_danfe(xml_path, output)
        else:
            print(f"✗ Argumento inválido: {arg}")
            print("\nUso:")
            print("  python main.py --lote")
            print("  python main.py nfe.xml")
            return 1
    else:
        # Modo interativo
        print("\n📁 Arquivos disponíveis:")

        pasta_xmls = Path('./xmls')
        xmls = list(pasta_xmls.glob('*.xml'))

        if not xmls:
            print("✗ Nenhum XML encontrado em ./xmls")
            return 1

        for i, xml in enumerate(xmls, 1):
            print(f"  {i}. {xml.name}")

        print(f"\n  0. Processar todos ({len(xmls)} arquivos)")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == '0':
            gerador.gerar_lote(str(pasta_xmls), './danfes_saida')
        else:
            try:
                idx = int(opcao) - 1
                xml_selecionado = xmls[idx]
                gerador.gerar_danfe(str(xml_selecionado))
            except (ValueError, IndexError):
                print("✗ Opção inválida")
                return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
