"""Configurações e modelos de dados para o DANFE Generator.


Este módulo define dataclasses imutáveis para configuração do gerador:

- MarginsConfig: Margens do documento em milímetros
- ColorsConfig: Cores RGB para personalização visual
- DANFEConfig: Configuração principal do gerador

Todas as classes possuem validação integrada e podem ser criadas
a partir de dicionários ou arquivos YAML.

Example:
    Configuração via código::

        from danfe_generator import DANFEConfig, MarginsConfig, ColorsConfig
        from pathlib import Path

        config = DANFEConfig(
            logo_path=Path("./logo.png"),
            margins=MarginsConfig(top=15, right=10, bottom=15, left=10),
            colors=ColorsConfig(primary=(41, 150, 161)),
        )

    Configuração via YAML::

        config = DANFEConfig.from_yaml("config.yaml")
"""

from dataclasses import dataclass, field
from pathlib import Path
import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

import yaml


@dataclass(frozen=True)
class MarginsConfig:
    """Configuração de margens do documento (em mm)."""

    top: int = 10
    right: int = 10
    bottom: int = 10
    left: int = 10

    def __post_init__(self) -> None:
        """Valida as margens."""
        for name in ("top", "right", "bottom", "left"):
            value = getattr(self, name)
            if not 0 <= value <= 50:
                raise ValueError(f"Margem {name} deve estar entre 0 e 50mm")

    @classmethod
    def from_dict(cls, data: dict[str, int]) -> Self:
        """Cria MarginsConfig a partir de dicionário."""
        return cls(
            top=data.get("top", 10),
            right=data.get("right", 10),
            bottom=data.get("bottom", 10),
            left=data.get("left", 10),
        )


@dataclass(frozen=True)
class ColorsConfig:
    """Configuração de cores RGB."""

    primary: tuple[int, int, int] = (41, 150, 161)
    secondary: tuple[int, int, int] = (94, 82, 64)
    accent: tuple[int, int, int] = (192, 21, 47)
    text: tuple[int, int, int] = (0, 0, 0)
    background: tuple[int, int, int] = (245, 245, 245)

    def __post_init__(self) -> None:
        """Valida os valores RGB."""
        for name in ("primary", "secondary", "accent", "text", "background"):
            color = getattr(self, name)
            if not isinstance(color, (tuple, list)) or len(color) != 3:
                raise ValueError(f"Cor {name} deve ter 3 componentes RGB")
            if not all(0 <= c <= 255 for c in color):
                raise ValueError(f"Cor {name} deve ter valores entre 0 e 255")

    @classmethod
    def from_dict(cls, data: dict[str, list[int]]) -> Self:
        """Cria ColorsConfig a partir de dicionário."""
        return cls(
            primary=tuple(data.get("primary", [41, 150, 161])),  # type: ignore
            secondary=tuple(data.get("secondary", [94, 82, 64])),  # type: ignore
            accent=tuple(data.get("accent", [192, 21, 47])),  # type: ignore
            text=tuple(data.get("text", [0, 0, 0])),  # type: ignore
            background=tuple(data.get("background", [245, 245, 245])),  # type: ignore
        )


@dataclass
class DANFEConfig:
    """Configuração principal do gerador DANFE."""

    logo_path: Path | None = None
    empresa_nome: str | None = None
    margins: MarginsConfig = field(default_factory=MarginsConfig)
    colors: ColorsConfig = field(default_factory=ColorsConfig)

    # Layout
    layout_type: str = "complete"
    show_logo: bool = True
    show_company_info: bool = True
    show_additional_info: bool = True

    def __post_init__(self) -> None:
        """Converte e valida campos."""
        if self.logo_path is not None and not isinstance(self.logo_path, Path):
            object.__setattr__(self, "logo_path", Path(self.logo_path))

        if self.layout_type not in ("complete", "simplified"):
            raise ValueError("layout_type deve ser 'complete' ou 'simplified'")

    @classmethod
    def from_yaml(cls, yaml_path: str | Path) -> Self:
        """Carrega configuração de arquivo YAML."""
        path = Path(yaml_path)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo de configuração não encontrado: {path}")

        with path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return cls(
            logo_path=Path(data.get("logo", {}).get("path", "")) or None,
            empresa_nome=data.get("issuer", {}).get("name"),
            margins=MarginsConfig.from_dict(data.get("margins", {})),
            colors=ColorsConfig.from_dict(data.get("colors", {})),
            layout_type=data.get("layout", {}).get("type", "complete"),
            show_logo=data.get("layout", {}).get("show_logo", True),
            show_company_info=data.get("layout", {}).get("show_company_info", True),
            show_additional_info=data.get("layout", {}).get("show_additional_info", True),
        )

    def to_dict(self) -> dict:
        """Converte configuração para dicionário."""
        return {
            "logo_path": str(self.logo_path) if self.logo_path else None,
            "empresa_nome": self.empresa_nome,
            "margins": {
                "top": self.margins.top,
                "right": self.margins.right,
                "bottom": self.margins.bottom,
                "left": self.margins.left,
            },
            "colors": {
                "primary": list(self.colors.primary),
                "secondary": list(self.colors.secondary),
                "accent": list(self.colors.accent),
            },
            "layout_type": self.layout_type,
        }
