"""Testes para o módulo de validadores."""

import os
from pathlib import Path

import pytest
from PIL import Image

from danfe_generator.core.validators import LogoValidator, XMLValidator
from danfe_generator.exceptions import InvalidLogoError, InvalidXMLError, XMLNotFoundError


class TestLogoValidator:
    """Testes para LogoValidator."""

    @pytest.fixture
    def validator(self) -> LogoValidator:
        return LogoValidator()

    @pytest.fixture
    def valid_logo(self, temp_dir: Path) -> Path:
        """Cria logo válida para teste."""
        logo_path = temp_dir / "test_logo.png"
        img = Image.new("RGB", (100, 100), color="white")
        img.save(logo_path)
        return logo_path

    def test_validate_existing_valid_logo(self, validator: LogoValidator, valid_logo: Path):
        """Testa validação de logo válida."""
        result = validator.validate(valid_logo)
        assert result.is_valid
        assert result.value == valid_logo
        assert result.error_message is None

    def test_validate_nonexistent_file(self, validator: LogoValidator, temp_dir: Path):
        """Testa validação de arquivo inexistente."""
        result = validator.validate(temp_dir / "nonexistent.png")
        assert not result.is_valid
        assert "não encontrado" in result.error_message.lower()

    def test_validate_invalid_extension(self, validator: LogoValidator, temp_dir: Path):
        """Testa validação de extensão inválida."""
        txt_path = temp_dir / "file.txt"
        txt_path.write_text("test")
        result = validator.validate(txt_path)
        assert not result.is_valid
        assert "extensão inválida" in result.error_message.lower()

    def test_validate_too_large(self, validator: LogoValidator, temp_dir: Path):
        """Testa validação de arquivo muito grande."""
        large_logo = temp_dir / "large_logo.png"
        # Criar imagem grande com ruído para garantir >500KB comprimido
        random_bytes = os.urandom(1500 * 1500 * 3)
        img = Image.frombytes("RGB", (1500, 1500), random_bytes)
        img.save(large_logo, compress_level=0)  # Sem compressão

        result = validator.validate(large_logo)
        assert not result.is_valid
        assert "muito grande" in result.error_message.lower()

    def test_validate_or_raise_valid(self, validator: LogoValidator, valid_logo: Path):
        """Testa validate_or_raise com logo válida."""
        result = validator.validate_or_raise(valid_logo)
        assert result == valid_logo

    def test_validate_or_raise_invalid(self, validator: LogoValidator, temp_dir: Path):
        """Testa validate_or_raise com logo inválida."""
        with pytest.raises(InvalidLogoError):
            validator.validate_or_raise(temp_dir / "invalid.png")


class TestXMLValidator:
    """Testes para XMLValidator."""

    @pytest.fixture
    def validator(self) -> XMLValidator:
        return XMLValidator()

    def test_validate_valid_xml(self, validator: XMLValidator, sample_xml_file: Path):
        """Testa validação de XML válido."""
        result = validator.validate(sample_xml_file)
        assert result.is_valid
        assert result.value == sample_xml_file

    def test_validate_nonexistent_file(self, validator: XMLValidator, temp_dir: Path):
        """Testa validação de arquivo inexistente."""
        result = validator.validate(temp_dir / "nonexistent.xml")
        assert not result.is_valid
        assert "não encontrado" in result.error_message.lower()

    def test_validate_invalid_extension(self, validator: XMLValidator, temp_dir: Path):
        """Testa validação de extensão inválida."""
        txt_path = temp_dir / "file.txt"
        txt_path.write_text("test")
        result = validator.validate(txt_path)
        assert not result.is_valid
        assert "extensão inválida" in result.error_message.lower()

    def test_validate_invalid_content(self, validator: XMLValidator, temp_dir: Path):
        """Testa validação de conteúdo inválido."""
        invalid_xml = temp_dir / "invalid.xml"
        invalid_xml.write_text("<root><data>test</data></root>")
        result = validator.validate(invalid_xml)
        assert not result.is_valid
        assert "não parece ser uma NFe válida" in result.error_message

    def test_validate_or_raise_valid(self, validator: XMLValidator, sample_xml_file: Path):
        """Testa validate_or_raise com XML válido."""
        result = validator.validate_or_raise(sample_xml_file)
        assert result == sample_xml_file

    def test_validate_or_raise_not_found(self, validator: XMLValidator, temp_dir: Path):
        """Testa validate_or_raise com arquivo não encontrado."""
        with pytest.raises(XMLNotFoundError):
            validator.validate_or_raise(temp_dir / "nonexistent.xml")

    def test_validate_or_raise_invalid(self, validator: XMLValidator, temp_dir: Path):
        """Testa validate_or_raise com XML inválido."""
        invalid_xml = temp_dir / "invalid.xml"
        invalid_xml.write_text("<root>test</root>")
        with pytest.raises(InvalidXMLError):
            validator.validate_or_raise(invalid_xml)
