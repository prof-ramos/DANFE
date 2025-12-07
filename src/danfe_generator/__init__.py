"""DANFE Generator - Gerador de DANFE personalizado.

Este pacote fornece ferramentas para gerar DANFEs (Documento Auxiliar
da Nota Fiscal Eletrônica) em formato PDF a partir de arquivos XML de NFe.

O pacote inclui:
    - DANFEGenerator: Classe principal para geração de PDFs
    - DANFEConfig: Configuração de margens, cores e logo
    - Interfaces CLI e Web (Streamlit)
    - Validadores de XML e logo
    - Exceções tipadas para tratamento de erros

Example:
    Uso básico::

        from danfe_generator import DANFEGenerator, DANFEConfig
        from pathlib import Path

        config = DANFEConfig(logo_path=Path("./logo.png"))
        generator = DANFEGenerator(config)
        result = generator.generate("nota.xml")

        if result.success:
            print(f"PDF gerado: {result.pdf_path}")

    Processamento em lote::

        batch = generator.generate_from_directory("./xmls", "./output")
        print(f"Taxa de sucesso: {batch.success_rate:.1f}%")

Attributes:
    __version__: Versão atual do pacote.
    __author__: Autor do pacote.
"""

from danfe_generator.core.config import ColorsConfig, DANFEConfig, MarginsConfig
from danfe_generator.core.generator import DANFEGenerator
from danfe_generator.exceptions import (
    DANFEError,
    DirectoryNotFoundError,
    GenerationError,
    InvalidLogoError,
    XMLNotFoundError,
)

__version__ = "0.2.0"
__author__ = "Gabriel Ramos"
__all__ = [
    "DANFEGenerator",
    "DANFEConfig",
    "MarginsConfig",
    "ColorsConfig",
    "DANFEError",
    "DirectoryNotFoundError",
    "XMLNotFoundError",
    "InvalidLogoError",
    "GenerationError",
]
