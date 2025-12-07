"""Testes para módulo de utilitários de cores."""

import pytest

from danfe_generator.utils.colors import darken_color, hex_to_rgb, lighten_color, rgb_to_hex


class TestHexToRgb:
    """Testes para hex_to_rgb."""

    def test_with_hash(self):
        """Testa conversão com #."""
        assert hex_to_rgb("#FF0000") == (255, 0, 0)
        assert hex_to_rgb("#00FF00") == (0, 255, 0)
        assert hex_to_rgb("#0000FF") == (0, 0, 255)

    def test_without_hash(self):
        """Testa conversão sem #."""
        assert hex_to_rgb("FF0000") == (255, 0, 0)
        assert hex_to_rgb("FFFFFF") == (255, 255, 255)
        assert hex_to_rgb("000000") == (0, 0, 0)

    def test_lowercase(self):
        """Testa cores em minúsculas."""
        assert hex_to_rgb("#ff0000") == (255, 0, 0)
        assert hex_to_rgb("abcdef") == (171, 205, 239)

    def test_invalid_length(self):
        """Testa erro com comprimento inválido."""
        with pytest.raises(ValueError, match="Cor hex inválida"):
            hex_to_rgb("#FFF")

    def test_invalid_characters(self):
        """Testa erro com caracteres inválidos."""
        with pytest.raises(ValueError, match="Cor hex inválida"):
            hex_to_rgb("#GGGGGG")


class TestRgbToHex:
    """Testes para rgb_to_hex."""

    def test_basic_colors(self):
        """Testa cores básicas."""
        assert rgb_to_hex(255, 0, 0) == "#FF0000"
        assert rgb_to_hex(0, 255, 0) == "#00FF00"
        assert rgb_to_hex(0, 0, 255) == "#0000FF"

    def test_black_white(self):
        """Testa preto e branco."""
        assert rgb_to_hex(0, 0, 0) == "#000000"
        assert rgb_to_hex(255, 255, 255) == "#FFFFFF"

    def test_out_of_range_negative(self):
        """Testa erro com valor negativo."""
        with pytest.raises(ValueError, match="fora do intervalo"):
            rgb_to_hex(-1, 0, 0)

    def test_out_of_range_large(self):
        """Testa erro com valor maior que 255."""
        with pytest.raises(ValueError, match="fora do intervalo"):
            rgb_to_hex(256, 0, 0)


class TestLightenColor:
    """Testes para lighten_color."""

    def test_lighten_red(self):
        """Testa clareamento de vermelho."""
        result = lighten_color((255, 0, 0), 0.2)
        # R permanece 255, G e B aumentam
        assert result[0] == 255
        assert result[1] > 0
        assert result[2] > 0

    def test_lighten_black(self):
        """Testa clareamento de preto."""
        result = lighten_color((0, 0, 0), 0.5)
        assert result == (127, 127, 127)

    def test_no_change_white(self):
        """Testa que branco não muda."""
        result = lighten_color((255, 255, 255), 0.5)
        assert result == (255, 255, 255)


class TestDarkenColor:
    """Testes para darken_color."""

    def test_darken_red(self):
        """Testa escurecimento de vermelho."""
        result = darken_color((255, 0, 0), 0.2)
        assert result[0] < 255
        assert result[1] == 0
        assert result[2] == 0

    def test_darken_white(self):
        """Testa escurecimento de branco."""
        result = darken_color((255, 255, 255), 0.5)
        assert result == (127, 127, 127)

    def test_no_change_black(self):
        """Testa que preto não muda."""
        result = darken_color((0, 0, 0), 0.5)
        assert result == (0, 0, 0)
