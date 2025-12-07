"""Validadores para campos do formulário de NF-e.

Implementa validação de CNPJ, CPF, IE e outros campos fiscais.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Resultado de uma validação."""

    valid: bool
    message: str = ""


def validate_cnpj(cnpj: str) -> ValidationResult:
    """Valida um número de CNPJ.

    Args:
        cnpj: CNPJ a ser validado (pode conter formatação).

    Returns:
        ValidationResult com status e mensagem.
    """
    # Remove caracteres não numéricos
    cnpj = re.sub(r"[^\d]", "", cnpj)

    if len(cnpj) != 14:
        return ValidationResult(False, "CNPJ deve ter 14 dígitos")

    # Verifica se todos os dígitos são iguais
    if cnpj == cnpj[0] * 14:
        return ValidationResult(False, "CNPJ inválido")

    # Cálculo do primeiro dígito verificador
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    if int(cnpj[12]) != digito1:
        return ValidationResult(False, "CNPJ inválido (dígito verificador)")

    # Cálculo do segundo dígito verificador
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    if int(cnpj[13]) != digito2:
        return ValidationResult(False, "CNPJ inválido (dígito verificador)")

    return ValidationResult(True, "CNPJ válido")


def validate_cpf(cpf: str) -> ValidationResult:
    """Valida um número de CPF.

    Args:
        cpf: CPF a ser validado (pode conter formatação).

    Returns:
        ValidationResult com status e mensagem.
    """
    # Remove caracteres não numéricos
    cpf = re.sub(r"[^\d]", "", cpf)

    if len(cpf) != 11:
        return ValidationResult(False, "CPF deve ter 11 dígitos")

    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return ValidationResult(False, "CPF inválido")

    # Cálculo do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    if int(cpf[9]) != digito1:
        return ValidationResult(False, "CPF inválido (dígito verificador)")

    # Cálculo do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    if int(cpf[10]) != digito2:
        return ValidationResult(False, "CPF inválido (dígito verificador)")

    return ValidationResult(True, "CPF válido")


def validate_cep(cep: str) -> ValidationResult:
    """Valida um CEP.

    Args:
        cep: CEP a ser validado.

    Returns:
        ValidationResult com status e mensagem.
    """
    cep = re.sub(r"[^\d]", "", cep)

    if len(cep) != 8:
        return ValidationResult(False, "CEP deve ter 8 dígitos")

    return ValidationResult(True, "CEP válido")


def validate_ncm(ncm: str) -> ValidationResult:
    """Valida um código NCM.

    Args:
        ncm: NCM a ser validado.

    Returns:
        ValidationResult com status e mensagem.
    """
    ncm = re.sub(r"[^\d]", "", ncm)

    if len(ncm) != 8:
        return ValidationResult(False, "NCM deve ter 8 dígitos")

    return ValidationResult(True, "NCM válido")


def validate_cfop(cfop: str) -> ValidationResult:
    """Valida um código CFOP.

    Args:
        cfop: CFOP a ser validado.

    Returns:
        ValidationResult com status e mensagem.
    """
    cfop = re.sub(r"[^\d]", "", cfop)

    if len(cfop) != 4:
        return ValidationResult(False, "CFOP deve ter 4 dígitos")

    # Primeiro dígito deve ser entre 1 e 7
    if cfop[0] not in "1234567":
        return ValidationResult(False, "CFOP inválido")

    return ValidationResult(True, "CFOP válido")


def validate_ie(ie: str, uf: str) -> ValidationResult:
    """Valida uma Inscrição Estadual.

    Nota: A validação completa de IE varia por UF.
    Esta implementação faz apenas validação básica.

    Args:
        ie: Inscrição Estadual a ser validada.
        uf: Sigla do estado.

    Returns:
        ValidationResult com status e mensagem.
    """
    ie = re.sub(r"[^\d]", "", ie)

    if not ie:
        return ValidationResult(False, "IE não pode ser vazia")

    # Validação básica de tamanho (varia por UF)
    # Aceita entre 8 e 14 dígitos como regra geral
    if len(ie) < 8 or len(ie) > 14:
        return ValidationResult(False, "IE deve ter entre 8 e 14 dígitos")

    return ValidationResult(True, f"IE válida para {uf}")


def format_cnpj(cnpj: str) -> str:
    """Formata um CNPJ para exibição.

    Args:
        cnpj: CNPJ apenas com números.

    Returns:
        CNPJ formatado (XX.XXX.XXX/XXXX-XX).
    """
    cnpj = re.sub(r"[^\d]", "", cnpj)
    if len(cnpj) != 14:
        return cnpj
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"


def format_cpf(cpf: str) -> str:
    """Formata um CPF para exibição.

    Args:
        cpf: CPF apenas com números.

    Returns:
        CPF formatado (XXX.XXX.XXX-XX).
    """
    cpf = re.sub(r"[^\d]", "", cpf)
    if len(cpf) != 11:
        return cpf
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def format_cep(cep: str) -> str:
    """Formata um CEP para exibição.

    Args:
        cep: CEP apenas com números.

    Returns:
        CEP formatado (XXXXX-XXX).
    """
    cep = re.sub(r"[^\d]", "", cep)
    if len(cep) != 8:
        return cep
    return f"{cep[:5]}-{cep[5:]}"


def unformat(value: str) -> str:
    """Remove formatação de um campo, mantendo apenas dígitos.

    Args:
        value: Valor formatado.

    Returns:
        Valor apenas com dígitos.
    """
    return re.sub(r"[^\d]", "", value)
