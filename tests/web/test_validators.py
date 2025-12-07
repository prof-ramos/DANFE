"""Testes para o módulo de validadores."""

from __future__ import annotations

import pytest

from danfe_generator.web.logic.validators import (
    ValidationResult,
    format_cep,
    format_cnpj,
    format_cpf,
    unformat,
    validate_cep,
    validate_cfop,
    validate_cnpj,
    validate_cpf,
    validate_ie,
    validate_ncm,
)


class TestValidateCNPJ:
    """Testes para validação de CNPJ."""

    def test_cnpj_valido(self) -> None:
        """Testa CNPJ válido."""
        # CNPJ válido de exemplo
        result = validate_cnpj("11222333000181")
        assert result.valid is True

    def test_cnpj_formatado_valido(self) -> None:
        """Testa CNPJ com formatação."""
        result = validate_cnpj("11.222.333/0001-81")
        assert result.valid is True

    def test_cnpj_tamanho_invalido(self) -> None:
        """Testa CNPJ com tamanho inválido."""
        result = validate_cnpj("1234567890")
        assert result.valid is False
        assert "14 dígitos" in result.message

    def test_cnpj_digitos_iguais(self) -> None:
        """Testa CNPJ com todos dígitos iguais."""
        result = validate_cnpj("11111111111111")
        assert result.valid is False

    def test_cnpj_digito_verificador_invalido(self) -> None:
        """Testa CNPJ com dígito verificador inválido."""
        result = validate_cnpj("11222333000182")  # Último dígito errado
        assert result.valid is False


class TestValidateCPF:
    """Testes para validação de CPF."""

    def test_cpf_valido(self) -> None:
        """Testa CPF válido."""
        result = validate_cpf("52998224725")
        assert result.valid is True

    def test_cpf_formatado_valido(self) -> None:
        """Testa CPF com formatação."""
        result = validate_cpf("529.982.247-25")
        assert result.valid is True

    def test_cpf_tamanho_invalido(self) -> None:
        """Testa CPF com tamanho inválido."""
        result = validate_cpf("123456789")
        assert result.valid is False
        assert "11 dígitos" in result.message

    def test_cpf_digitos_iguais(self) -> None:
        """Testa CPF com todos dígitos iguais."""
        result = validate_cpf("11111111111")
        assert result.valid is False


class TestValidateCEP:
    """Testes para validação de CEP."""

    def test_cep_valido(self) -> None:
        """Testa CEP válido."""
        result = validate_cep("01310100")
        assert result.valid is True

    def test_cep_formatado(self) -> None:
        """Testa CEP com formatação."""
        result = validate_cep("01310-100")
        assert result.valid is True

    def test_cep_invalido(self) -> None:
        """Testa CEP inválido."""
        result = validate_cep("12345")
        assert result.valid is False


class TestValidateNCM:
    """Testes para validação de NCM."""

    def test_ncm_valido(self) -> None:
        """Testa NCM válido."""
        result = validate_ncm("84713012")
        assert result.valid is True

    def test_ncm_invalido(self) -> None:
        """Testa NCM inválido."""
        result = validate_ncm("8471")
        assert result.valid is False


class TestValidateCFOP:
    """Testes para validação de CFOP."""

    def test_cfop_valido(self) -> None:
        """Testa CFOP válido."""
        result = validate_cfop("5102")
        assert result.valid is True

    def test_cfop_entrada(self) -> None:
        """Testa CFOP de entrada válido."""
        result = validate_cfop("1102")
        assert result.valid is True

    def test_cfop_invalido_primeiro_digito(self) -> None:
        """Testa CFOP com primeiro dígito inválido."""
        result = validate_cfop("8102")
        assert result.valid is False

    def test_cfop_tamanho_invalido(self) -> None:
        """Testa CFOP com tamanho inválido."""
        result = validate_cfop("510")
        assert result.valid is False


class TestValidateIE:
    """Testes para validação de IE."""

    def test_ie_valida(self) -> None:
        """Testa IE válida."""
        result = validate_ie("123456789012", "SP")
        assert result.valid is True

    def test_ie_vazia(self) -> None:
        """Testa IE vazia."""
        result = validate_ie("", "SP")
        assert result.valid is False

    def test_ie_muito_curta(self) -> None:
        """Testa IE muito curta."""
        result = validate_ie("12345", "SP")
        assert result.valid is False


class TestFormatters:
    """Testes para funções de formatação."""

    def test_format_cnpj(self) -> None:
        """Testa formatação de CNPJ."""
        assert format_cnpj("11222333000181") == "11.222.333/0001-81"

    def test_format_cnpj_invalido(self) -> None:
        """Testa formatação de CNPJ inválido retorna original."""
        assert format_cnpj("12345") == "12345"

    def test_format_cpf(self) -> None:
        """Testa formatação de CPF."""
        assert format_cpf("52998224725") == "529.982.247-25"

    def test_format_cpf_invalido(self) -> None:
        """Testa formatação de CPF inválido retorna original."""
        assert format_cpf("12345") == "12345"

    def test_format_cep(self) -> None:
        """Testa formatação de CEP."""
        assert format_cep("01310100") == "01310-100"

    def test_unformat(self) -> None:
        """Testa remoção de formatação."""
        assert unformat("11.222.333/0001-81") == "11222333000181"
        assert unformat("529.982.247-25") == "52998224725"
        assert unformat("01310-100") == "01310100"
