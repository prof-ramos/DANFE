"""Validadores para arquivos de entrada.

Este módulo implementa o padrão Strategy para validação de arquivos,
fornecendo validadores específicos para diferentes tipos de entrada.

Classes:
    ValidationResult: Resultado de uma validação (sucesso/erro).
    Validator: Interface base abstrata para validadores.
    LogoValidator: Valida arquivos de imagem para logo.
    XMLValidator: Valida arquivos XML de NFe.

Example:
    Validação de XML::

        from danfe_generator.core.validators import XMLValidator
        from pathlib import Path

        validator = XMLValidator()
        result = validator.validate(Path("nota.xml"))

        if result.is_valid:
            print("XML válido!")
        else:
            print(f"Erro: {result.error_message}")

    Validação com exceção::

        try:
            validator.validate_or_raise(Path("nota.xml"))
        except InvalidXMLError as e:
            print(f"XML inválido: {e.message}")
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree

from danfe_generator.exceptions import InvalidLogoError, InvalidXMLError, XMLNotFoundError


@dataclass
class ValidationResult[T]:
    """Resultado de uma validação."""

    is_valid: bool
    value: T | None = None
    error_message: str | None = None


class Validator[T](ABC):
    """Interface base para validadores."""

    @abstractmethod
    def validate(self, value: T) -> ValidationResult[T]:
        """Valida o valor e retorna resultado."""
        ...


class LogoValidator(Validator[Path]):
    """Validador de arquivos de logo."""

    VALID_EXTENSIONS: frozenset[str] = frozenset({".png", ".jpg", ".jpeg", ".bmp"})
    MAX_SIZE_BYTES: int = 512 * 1024  # 512KB

    def validate(self, path: Path) -> ValidationResult[Path]:
        """
        Valida arquivo de logo.

        Args:
            path: Caminho do arquivo de logo

        Returns:
            ValidationResult com resultado da validação
        """
        if not path.exists():
            return ValidationResult(
                is_valid=False,
                error_message=f"Arquivo não encontrado: {path}",
            )

        if path.suffix.lower() not in self.VALID_EXTENSIONS:
            return ValidationResult(
                is_valid=False,
                error_message=f"Extensão inválida: {path.suffix}. "
                f"Extensões válidas: {', '.join(self.VALID_EXTENSIONS)}",
            )

        try:
            file_size = path.stat().st_size
            if file_size > self.MAX_SIZE_BYTES:
                size_kb = file_size / 1024
                max_kb = self.MAX_SIZE_BYTES / 1024
                return ValidationResult(
                    is_valid=False,
                    error_message=f"Arquivo muito grande: {size_kb:.1f}KB (máx: {max_kb:.0f}KB)",
                )
        except OSError as e:
            return ValidationResult(
                is_valid=False,
                error_message=f"Não foi possível acessar o arquivo: {e}",
            )

        return ValidationResult(is_valid=True, value=path)

    def validate_or_raise(self, path: Path) -> Path:
        """Valida e levanta exceção se inválido."""
        result = self.validate(path)
        if not result.is_valid:
            raise InvalidLogoError(str(path), result.error_message or "Erro desconhecido")
        return path


class XMLValidator(Validator[Path]):
    """Validador de arquivos XML de NFe."""

    # Tags que indicam um XML de NFe válido (pelo menos uma deve estar na raiz ou logo abaixo)
    REQUIRED_TAGS: tuple[str, ...] = ("nfeProc", "NFe", "infNFe")

    def validate(self, path: Path) -> ValidationResult[Path]:
        """
        Valida arquivo XML.

        Args:
            path: Caminho do arquivo XML

        Returns:
            ValidationResult com resultado da validação
        """
        if not path.exists():
            return ValidationResult(
                is_valid=False,
                error_message=f"Arquivo não encontrado: {path}",
            )

        if path.suffix.lower() != ".xml":
            return ValidationResult(
                is_valid=False,
                error_message=f"Extensão inválida: {path.suffix}. Esperado: .xml",
            )

        # Validação básica de conteúdo usando parser
        try:
            # Parse iterativo para não carregar tudo na memória se for muito grande
            # Mas para validação estrutural básica, parse direto é suficiente e seguro
            # pois ElementTree é robusto.
            tree = ElementTree.parse(path)
            root = tree.getroot()

            # Remove namespace para verificação simples
            root_tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag

            valid_root = root_tag in self.REQUIRED_TAGS

            # Se a raiz não for válida, verifica se tem filhos válidos (ex: nfeProc contendo NFe)
            if not valid_root:
                # Verifica primeiro nível de filhos
                for child in root:
                    child_tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
                    if child_tag in self.REQUIRED_TAGS:
                        valid_root = True
                        break

            if not valid_root:
                return ValidationResult(
                    is_valid=False,
                    error_message="XML não parece ser uma NFe válida (tags NFe/nfeProc não encontradas)",
                )

        except ElementTree.ParseError as e:
            return ValidationResult(
                is_valid=False,
                error_message=f"XML malformado: {e}",
            )
        except (OSError, UnicodeDecodeError) as e:
            return ValidationResult(
                is_valid=False,
                error_message=f"Erro ao ler arquivo: {e}",
            )

        return ValidationResult(is_valid=True, value=path)

    def validate_or_raise(self, path: Path) -> Path:
        """Valida e levanta exceção se inválido."""
        # Check existence first explicitly to raise correct exception type
        if not path.exists():
             raise XMLNotFoundError(str(path))

        result = self.validate(path)
        if not result.is_valid:
            raise InvalidXMLError(str(path), result.error_message or "Erro desconhecido")
        return path
