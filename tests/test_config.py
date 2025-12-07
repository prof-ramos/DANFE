"""Testes para o módulo de configuração."""

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from danfe_generator.core.config import ColorsConfig, DANFEConfig, MarginsConfig


class TestMarginsConfig:
    """Testes para MarginsConfig."""

    def test_default_values(self):
        """Testa valores padrão."""
        margins = MarginsConfig()
        assert margins.top == 10
        assert margins.right == 10
        assert margins.bottom == 10
        assert margins.left == 10

    def test_custom_values(self):
        """Testa valores customizados."""
        margins = MarginsConfig(top=5, right=15, bottom=20, left=25)
        assert margins.top == 5
        assert margins.right == 15
        assert margins.bottom == 20
        assert margins.left == 25

    def test_validation_negative(self):
        """Testa validação de valores negativos."""
        with pytest.raises(ValueError, match="deve estar entre 0 e 50mm"):
            MarginsConfig(top=-1)

    def test_validation_too_large(self):
        """Testa validação de valores muito grandes."""
        with pytest.raises(ValueError, match="deve estar entre 0 e 50mm"):
            MarginsConfig(right=51)

    def test_from_dict(self):
        """Testa criação a partir de dicionário."""
        data = {"top": 5, "left": 15}
        margins = MarginsConfig.from_dict(data)
        assert margins.top == 5
        assert margins.left == 15
        assert margins.right == 10  # valor padrão
        assert margins.bottom == 10  # valor padrão

    def test_immutable(self):
        """Testa que MarginsConfig é imutável."""
        margins = MarginsConfig()
        with pytest.raises(FrozenInstanceError):
            margins.top = 20  # type: ignore


class TestColorsConfig:
    """Testes para ColorsConfig."""

    def test_default_values(self):
        """Testa valores padrão."""
        colors = ColorsConfig()
        assert colors.primary == (41, 150, 161)
        assert colors.secondary == (94, 82, 64)
        assert colors.accent == (192, 21, 47)

    def test_custom_values(self):
        """Testa valores customizados."""
        colors = ColorsConfig(primary=(255, 0, 0))
        assert colors.primary == (255, 0, 0)

    def test_validation_invalid_length(self):
        """Testa validação de tupla com tamanho inválido."""
        with pytest.raises(ValueError, match="deve ter 3 componentes RGB"):
            ColorsConfig(primary=(255, 0))  # type: ignore

    def test_validation_out_of_range(self):
        """Testa validação de valores fora do intervalo."""
        with pytest.raises(ValueError, match="deve ter valores entre 0 e 255"):
            ColorsConfig(primary=(256, 0, 0))

    def test_from_dict(self):
        """Testa criação a partir de dicionário."""
        data = {"primary": [255, 0, 0], "secondary": [0, 255, 0]}
        colors = ColorsConfig.from_dict(data)
        assert colors.primary == (255, 0, 0)
        assert colors.secondary == (0, 255, 0)


class TestDANFEConfig:
    """Testes para DANFEConfig."""

    def test_default_values(self):
        """Testa valores padrão."""
        config = DANFEConfig()
        assert config.logo_path is None
        assert config.empresa_nome is None
        assert config.layout_type == "complete"
        assert config.show_logo is True

    def test_with_logo_path_string(self):
        """Testa conversão de string para Path."""
        config = DANFEConfig(logo_path="./logo.png")  # type: ignore
        assert isinstance(config.logo_path, Path)
        assert str(config.logo_path) == "logo.png"

    def test_invalid_layout_type(self):
        """Testa validação de layout_type."""
        with pytest.raises(ValueError, match="layout_type deve ser"):
            DANFEConfig(layout_type="invalid")

    def test_to_dict(self):
        """Testa conversão para dicionário."""
        config = DANFEConfig(
            logo_path=Path("./logo.png"),
            empresa_nome="Empresa Teste",
        )
        data = config.to_dict()
        assert data["logo_path"] == "logo.png"
        assert data["empresa_nome"] == "Empresa Teste"
        assert "margins" in data
        assert "colors" in data
