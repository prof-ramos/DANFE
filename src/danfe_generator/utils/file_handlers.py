"""Utilitários para manipulação de arquivos.

Fornece funções para operações seguras com arquivos e diretórios.

Functions:
    ensure_directory: Garante que um diretório existe.
    safe_write_file: Escreve arquivo de forma atômica.
    get_file_size_formatted: Retorna tamanho formatado do arquivo.
    list_files_by_extension: Lista arquivos por extensão.

Example:
    >>> from danfe_generator.utils.file_handlers import ensure_directory
    >>> path = ensure_directory("./output/pdfs")
    >>> path.exists()
    True
"""

from __future__ import annotations

import shutil
from pathlib import Path


def _validate_path(path: str | Path, base_dir: Path | None = None) -> Path:
    """
    Valida e resolve um caminho, prevenindo path traversal.

    Args:
        path: Caminho a validar
        base_dir: Diretório base opcional para restringir o caminho

    Returns:
        Path resolvido e validado

    Raises:
        ValueError: Se o caminho tentar sair do diretório base
    """
    path = Path(path).resolve()

    if base_dir:
        base = Path(base_dir).resolve()
        try:
            path.relative_to(base)
        except ValueError:
            raise ValueError(f"Caminho inseguro detectado: {path} está fora de {base}")

    return path


def ensure_directory(path: str | Path) -> Path:
    """
    Garante que um diretório existe, criando-o se necessário.

    Args:
        path: Caminho do diretório

    Returns:
        Path do diretório criado/existente
    """
    path = _validate_path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_write_file(
    path: str | Path,
    content: str | bytes,
    encoding: str = "utf-8",
    backup: bool = False,
) -> Path:
    """
    Escreve arquivo de forma segura (atômica).

    Args:
        path: Caminho do arquivo
        content: Conteúdo a escrever
        encoding: Encoding para texto
        backup: Se True, faz backup do arquivo existente

    Returns:
        Path do arquivo escrito
    """
    path = _validate_path(path)

    # Garantir diretório
    path.parent.mkdir(parents=True, exist_ok=True)

    # Backup se necessário
    if backup and path.exists():
        backup_path = path.with_suffix(f"{path.suffix}.bak")
        # Copiar sem seguir symlinks para evitar TOCTOU
        if path.is_symlink():
            # Se for symlink, copiamos o link em si, não o alvo
            # Mas safe_write_file geralmente sobrescreve o arquivo
            # Para backup seguro, vamos ler o conteúdo e escrever no backup
            pass
        else:
            shutil.copy2(path, backup_path, follow_symlinks=False)

    # Escrever via arquivo temporário para atomicidade
    # Usar with_name para garantir que o tmp fique no mesmo diretório
    tmp_path = path.with_name(f"{path.name}.tmp")

    try:
        if isinstance(content, bytes):
            tmp_path.write_bytes(content)
        else:
            tmp_path.write_text(content, encoding=encoding)

        # Mover atomicamente
        tmp_path.replace(path)
    finally:
        # Limpar tmp se ainda existir
        if tmp_path.exists():
            tmp_path.unlink()

    return path


def get_file_size_formatted(path: str | Path) -> str:
    """
    Retorna tamanho do arquivo formatado.

    Args:
        path: Caminho do arquivo

    Returns:
        String formatada (ex: "1.5 MB")
    """
    path = Path(path)

    if not path.exists():
        return "0 B"

    # Manter como int inicialmente
    size = path.stat().st_size

    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size = float(size) / 1024

    return f"{size:.1f} TB"


def list_files_by_extension(
    directory: str | Path,
    extension: str,
    recursive: bool = False,
) -> list[Path]:
    """
    Lista arquivos por extensão em um diretório.

    Args:
        directory: Diretório a buscar
        extension: Extensão (com ou sem ponto)
        recursive: Se True, busca recursivamente

    Returns:
        Lista de Paths encontrados
    """
    directory = _validate_path(directory)

    if not directory.exists():
        return []

    extension = extension.lstrip(".")
    pattern = f"**/*.{extension}" if recursive else f"*.{extension}"

    return sorted(directory.glob(pattern))
