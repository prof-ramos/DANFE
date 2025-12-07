#!/usr/bin/env python3
"""Interface de linha de comando para o DANFE Generator.

Este módulo fornece uma CLI completa para geração de DANFEs,
suportando modos interativo, único e em lote.

Comandos:
    danfe              - Modo interativo com menu de seleção
    danfe arquivo.xml  - Gera DANFE para um arquivo específico
    danfe --batch DIR  - Processa todos XMLs de um diretório

Opções:
    -o, --output PATH    Caminho de saída do PDF
    -l, --logo PATH      Caminho da logo da empresa
    -c, --config FILE    Arquivo de configuração YAML
    -v, --verbose        Modo verboso (debug)
    --format TYPE        Formato de saída: simple, detailed, json

Example:
    Linha de comando::

        $ danfe nota.xml -o ./output/nota.pdf --logo ./logo.png
        $ danfe --batch ./xmls -o ./output
        $ danfe --config config.yaml nota.xml
"""

from __future__ import annotations

import argparse
import logging
import sys
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

from danfe_generator.core import DANFEConfig, DANFEGenerator

if TYPE_CHECKING:
    from danfe_generator.core.generator import GenerationResult


class OutputFormat(str, Enum):
    """Formatos de saída suportados."""

    SIMPLE = "simple"
    DETAILED = "detailed"
    JSON = "json"


def setup_logging(verbose: bool = False) -> None:
    """Configura logging."""
    level = logging.DEBUG if verbose else logging.INFO
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove handlers existentes para evitar duplicação
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)


def print_banner() -> None:
    """Imprime banner do aplicativo."""
    print(
        """
╔══════════════════════════════════════════════════════════════╗
║                    📄 DANFE Generator                        ║
║              Gerador de DANFE Personalizado                  ║
╚══════════════════════════════════════════════════════════════╝
"""
    )


def print_result(result: GenerationResult, format_type: OutputFormat = OutputFormat.SIMPLE) -> None:
    """Imprime resultado da geração."""

    if format_type == OutputFormat.JSON:
        import json

        print(
            json.dumps(
                {
                    "xml": str(result.xml_path),
                    "pdf": str(result.pdf_path) if result.pdf_path else None,
                    "success": result.success,
                    "error": result.error_message,
                    "size_kb": result.file_size_kb,
                },
                indent=2,
            )
        )
    elif format_type == OutputFormat.DETAILED:
        status = "✓" if result.success else "✗"
        print(f"\n{status} {result.xml_path.name}")
        if result.success:
            print(f"   PDF: {result.pdf_path}")
            print(f"   Tamanho: {result.file_size_kb:.2f} KB")
        else:
            print(f"   Erro: {result.error_message}")
    else:
        status = "✓" if result.success else "✗"
        print(f"{status} {result.xml_path.name}")


def cmd_generate(
    xml_path: str,
    output: str | None = None,
    logo: str | None = None,
    config_file: str | None = None,
    verbose: bool = False,
    format_type: OutputFormat = OutputFormat.SIMPLE,
) -> int:
    """
    Gera DANFE para um único arquivo XML.

    Args:
        xml_path: Caminho do arquivo XML
        output: Caminho de saída do PDF
        logo: Caminho da logo
        config_file: Arquivo de configuração YAML
        verbose: Modo verboso
        format: Formato de saída

    Returns:
        Código de saída (0 = sucesso)
    """
    setup_logging(verbose)

    # Carregar configuração
    if config_file:
        config = DANFEConfig.from_yaml(config_file)
    else:
        config = DANFEConfig(logo_path=Path(logo) if logo else None)

    generator = DANFEGenerator(config)

    try:
        result = generator.generate(xml_path, output)
        print_result(result, format_type)
        return 0 if result.success else 1
    except OSError as e:
        print(f"✗ Erro de E/S: {e}")
        return 1
    except Exception as e:
        print(f"✗ Erro inesperado: {e}")
        return 1


def cmd_batch(
    input_dir: str,
    output_dir: str | None = None,
    logo: str | None = None,
    config_file: str | None = None,
    verbose: bool = False,
    _format_type: OutputFormat = OutputFormat.SIMPLE,  # noqa: ARG001
) -> int:
    """
    Processa múltiplos XMLs de um diretório.

    Args:
        input_dir: Diretório contendo XMLs
        output_dir: Diretório de saída
        logo: Caminho da logo
        config_file: Arquivo de configuração
        verbose: Modo verboso
        format: Formato de saída

    Returns:
        Código de saída
    """
    setup_logging(verbose)

    # Carregar configuração
    if config_file:
        config = DANFEConfig.from_yaml(config_file)
    else:
        config = DANFEConfig(logo_path=Path(logo) if logo else None)

    generator = DANFEGenerator(config)

    try:
        result = generator.generate_from_directory(input_dir, output_dir)

        print("\n📊 Resumo:")
        print(f"   Total:   {result.total}")
        print(f"   Sucesso: {result.successful} ✓")
        print(f"   Erro:    {result.failed} ✗")
        print(f"   Taxa:    {result.success_rate:.1f}%")

        return 0 if result.failed == 0 else 1
    except OSError as e:
        print(f"✗ Erro de E/S ao processar diretório: {e}")
        return 1
    except Exception as e:
        print(f"✗ Erro inesperado: {e}")
        return 1


def cmd_interactive(
    logo: str | None = None,
    config_file: str | None = None,
) -> int:
    """
    Modo interativo - seleciona arquivos do diretório.

    Args:
        logo: Caminho da logo
        config_file: Arquivo de configuração

    Returns:
        Código de saída
    """
    print_banner()

    xml_dir = Path("./xmls")
    output_dir = Path("./danfes_saida")

    if not xml_dir.exists():
        print(f"✗ Diretório não encontrado: {xml_dir}")
        return 1

    xml_files = list(xml_dir.glob("*.xml"))

    if not xml_files:
        print(f"✗ Nenhum XML encontrado em {xml_dir}")
        return 1

    print("📁 Arquivos disponíveis:\n")
    for i, xml in enumerate(xml_files, 1):
        print(f"  {i}. {xml.name}")

    print(f"\n  0. Processar todos ({len(xml_files)} arquivos)\n")

    try:
        opcao = input("Escolha uma opção: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n\nOperação cancelada.")
        return 0

    # Carregar configuração
    if config_file:
        config = DANFEConfig.from_yaml(config_file)
    else:
        config = DANFEConfig(logo_path=Path(logo) if logo else None)

    generator = DANFEGenerator(config)

    if opcao == "0":
        batch_result = generator.generate_from_directory(xml_dir, output_dir)
        print(f"\n📊 Processados: {batch_result.successful}/{batch_result.total}")
        return 0 if batch_result.failed == 0 else 1

    try:
        idx = int(opcao) - 1
        if idx < 0 or idx >= len(xml_files):
            raise IndexError(f"Índice inválido: {opcao}")

        xml_file = xml_files[idx]
        output_file = output_dir / f"{xml_file.stem}.pdf"

        single_result = generator.generate(xml_file, output_file)
        print_result(single_result, OutputFormat.DETAILED)
        return 0 if single_result.success else 1

    except ValueError:
        print("✗ Opção inválida: digite um número")
        return 1
    except IndexError as e:
        print(f"✗ {e}")
        return 1


def cli_app() -> int:
    """
    Ponto de entrada principal da CLI.

    Processa argumentos e executa comando apropriado.
    """
    parser = argparse.ArgumentParser(
        description="DANFE Generator - Gerador de DANFE Personalizado",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  danfe nota.xml -o ./output/nota.pdf
  danfe --batch ./xmls -o ./output
  danfe --config config.yaml nota.xml
""",
    )

    parser.add_argument(
        "input_path",
        nargs="?",
        help="Arquivo XML de entrada ou diretório (se --batch)",
    )

    parser.add_argument(
        "-o", "--output",
        help="Caminho de saída do PDF ou diretório de saída",
    )

    parser.add_argument(
        "-l", "--logo",
        help="Caminho da logo da empresa",
    )

    parser.add_argument(
        "-c", "--config",
        dest="config_file",
        help="Arquivo de configuração YAML",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Modo verboso (debug)",
    )

    parser.add_argument(
        "--format",
        type=OutputFormat,
        choices=list(OutputFormat),
        default=OutputFormat.SIMPLE,
        help="Formato de saída",
    )

    parser.add_argument(
        "--batch",
        action="store_true",
        help="Processa todos XMLs de um diretório",
    )

    # Se nenhum argumento for passado, sys.argv terá apenas o nome do script
    if len(sys.argv) == 1:
        return cmd_interactive()

    try:
        args = parser.parse_args()
    except Exception as e:
        print(f"Erro nos argumentos: {e}")
        return 1

    # Lógica de despacho
    if args.batch:
        input_dir = args.input_path or "./xmls"
        return cmd_batch(
            input_dir,
            args.output,
            args.logo,
            args.config_file,
            args.verbose,
            args.format,
        )

    if args.input_path:
        # Modo arquivo único
        return cmd_generate(
            args.input_path,
            args.output,
            args.logo,
            args.config_file,
            args.verbose,
            args.format,
        )

    # Fallback para interativo se tiver flags mas sem input path?
    # O comportamento original era: se não tem args, interativo.
    # Se tem args mas não input path, argparse vai reclamar ou input_path será None.
    # Se input_path for None e não for batch, podemos ir para interativo
    # passando as configs.
    return cmd_interactive(args.logo, args.config_file)


def main() -> int:
    """Wrapper para cli_app."""
    try:
        return cli_app()
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
        return 130
    except SystemExit as e:
        return e.code


if __name__ == "__main__":
    sys.exit(main())
