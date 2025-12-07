"""Módulo de utilitários para o DANFE Generator.

Este módulo reúne funções utilitárias reutilizáveis:

Manipulação de cores:
    - hex_to_rgb: Converte cor hexadecimal para RGB
    - rgb_to_hex: Converte cor RGB para hexadecimal

Manipulação de arquivos:
    - ensure_directory: Cria diretório se não existir
    - safe_write_file: Escrita atômica com backup opcional

Example:
    >>> from danfe_generator.utils import hex_to_rgb, ensure_directory
    >>> rgb = hex_to_rgb("#FF5500")  # (255, 85, 0)
    >>> ensure_directory("./output/pdfs")
"""

from danfe_generator.utils.colors import hex_to_rgb, rgb_to_hex
from danfe_generator.utils.file_handlers import ensure_directory, safe_write_file

__all__ = [
    "hex_to_rgb",
    "rgb_to_hex",
    "ensure_directory",
    "safe_write_file",
]
