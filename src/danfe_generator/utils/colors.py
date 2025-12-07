"""Utilitários para manipulação de cores.

Fornece funções para conversão entre formatos de cor e
manipulação de luminosidade.

Functions:
    hex_to_rgb: Converte cor hexadecimal (#RRGGBB) para tupla RGB.
    rgb_to_hex: Converte tupla RGB para hexadecimal.
    lighten_color: Clareia uma cor RGB.
    darken_color: Escurece uma cor RGB.

Example:
    >>> from danfe_generator.utils.colors import hex_to_rgb, rgb_to_hex
    >>> rgb = hex_to_rgb("#FF5500")
    >>> rgb
    (255, 85, 0)
    >>> rgb_to_hex(255, 85, 0)
    '#FF5500'
"""


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """
    Converte cor hexadecimal para RGB.

    Args:
        hex_color: Cor em formato hex (#RRGGBB ou RRGGBB)

    Returns:
        Tupla (R, G, B) com valores 0-255

    Examples:
        >>> hex_to_rgb("#FF0000")
        (255, 0, 0)
        >>> hex_to_rgb("00FF00")
        (0, 255, 0)
    """
    hex_color = hex_color.lstrip("#")

    if len(hex_color) != 6:
        raise ValueError(f"Cor hex inválida: {hex_color}")

    try:
        return (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
        )
    except ValueError as e:
        raise ValueError(f"Cor hex inválida: {hex_color}") from e


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """
    Converte cor RGB para hexadecimal.

    Args:
        r: Componente vermelho (0-255)
        g: Componente verde (0-255)
        b: Componente azul (0-255)

    Returns:
        String hex no formato #RRGGBB

    Examples:
        >>> rgb_to_hex(255, 0, 0)
        '#FF0000'
        >>> rgb_to_hex(0, 255, 0)
        '#00FF00'
    """
    for name, value in [("r", r), ("g", g), ("b", b)]:
        if not 0 <= value <= 255:
            raise ValueError(f"Componente {name} fora do intervalo 0-255: {value}")

    return f"#{r:02X}{g:02X}{b:02X}"


def _validate_color_args(rgb: tuple[int, int, int], factor: float) -> None:
    """Valida argumentos de cor e fator."""
    if not (0.0 <= factor <= 1.0):
        raise ValueError(f"Fator deve estar entre 0.0 e 1.0: {factor}")

    if len(rgb) != 3:
        raise ValueError(f"Tupla RGB deve ter 3 elementos: {rgb}")

    for val in rgb:
        if not isinstance(val, int) or not (0 <= val <= 255):
            raise ValueError(f"Componentes RGB devem ser inteiros entre 0 e 255: {rgb}")


def lighten_color(rgb: tuple[int, int, int], factor: float = 0.2) -> tuple[int, int, int]:
    """
    Clareia uma cor RGB.

    Args:
        rgb: Tupla (R, G, B)
        factor: Fator de clareamento (0-1)

    Returns:
        Cor clareada
    """
    _validate_color_args(rgb, factor)

    r, g, b = rgb
    return (
        min(255, int(r + (255 - r) * factor)),
        min(255, int(g + (255 - g) * factor)),
        min(255, int(b + (255 - b) * factor)),
    )


def darken_color(rgb: tuple[int, int, int], factor: float = 0.2) -> tuple[int, int, int]:
    """
    Escurece uma cor RGB.

    Args:
        rgb: Tupla (R, G, B)
        factor: Fator de escurecimento (0-1)

    Returns:
        Cor escurecida
    """
    _validate_color_args(rgb, factor)

    r, g, b = rgb
    return (
        max(0, int(r * (1 - factor))),
        max(0, int(g * (1 - factor))),
        max(0, int(b * (1 - factor))),
    )
