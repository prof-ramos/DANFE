"""Exceções customizadas para o DANFE Generator.

Este módulo define a hierarquia de exceções do DANFE Generator,
permitindo tratamento granular de erros.

Hierarquia::

    DANFEError (base)
    ├── XMLNotFoundError      # Arquivo XML não encontrado
    ├── InvalidXMLError       # XML malformado ou não é NFe
    ├── InvalidLogoError      # Logo inválida (formato/tamanho)
    ├── ConfigurationError    # Erro de configuração
    └── GenerationError       # Erro na geração do PDF

Example:
    Tratamento de erros::

        from danfe_generator import DANFEGenerator, XMLNotFoundError, GenerationError

        try:
            result = generator.generate("nota.xml")
        except XMLNotFoundError as e:
            print(f"Arquivo não encontrado: {e.details['path']}")
        except GenerationError as e:
            print(f"Erro na geração: {e.message}")
"""

from typing import Any


class DANFEError(Exception):
    """Exceção base para erros do DANFE Generator.

    Todas as exceções do pacote herdam desta classe, permitindo
    capturar qualquer erro do DANFE Generator.

    Attributes:
        message: Mensagem descritiva do erro.
        details: Dicionário com informações adicionais sobre o erro.

    Example:
        >>> try:
        ...     generator.generate("nota.xml")
        ... except DANFEError as e:
        ...     print(f"Erro: {e.message}")
        ...     print(f"Detalhes: {e.details}")
    """

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """Inicializa a exceção.

        Args:
            message: Mensagem descritiva do erro.
            details: Informações adicionais sobre o erro.
        """
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        """Retorna representação em string da exceção."""
        if self.details:
            return f"{self.message} - Detalhes: {self.details}"
        return self.message


class XMLNotFoundError(DANFEError):
    """Exceção quando arquivo XML não é encontrado.

    Attributes:
        path: Caminho do arquivo não encontrado (em details['path']).

    Example:
        >>> try:
        ...     generator.generate("inexistente.xml")
        ... except XMLNotFoundError as e:
        ...     print(f"Arquivo não encontrado: {e.details['path']}")
    """

    def __init__(self, path: str) -> None:
        """Inicializa a exceção.

        Args:
            path: Caminho do arquivo XML não encontrado.
        """
        super().__init__(
            message=f"Arquivo XML não encontrado: {path}",
            details={"path": path},
        )


class DirectoryNotFoundError(DANFEError):
    """Exceção quando diretório não é encontrado.

    Attributes:
        path: Caminho do diretório não encontrado (em details['path']).
    """

    def __init__(self, path: str) -> None:
        """Inicializa a exceção.

        Args:
            path: Caminho do diretório não encontrado.
        """
        super().__init__(
            message=f"Diretório não encontrado: {path}",
            details={"path": path},
        )


class InvalidXMLError(DANFEError):
    """Exceção quando XML é inválido ou malformado.

    O XML pode ser inválido por diversos motivos:
    - Não é um arquivo XML válido
    - Não contém as tags obrigatórias de NFe
    - Encoding incorreto

    Attributes:
        path: Caminho do arquivo (em details['path']).
        reason: Motivo da invalidação (em details['reason']).
    """

    def __init__(self, path: str, reason: str) -> None:
        """Inicializa a exceção.

        Args:
            path: Caminho do arquivo XML.
            reason: Motivo pelo qual o XML é inválido.
        """
        super().__init__(
            message=f"XML inválido: {reason}",
            details={"path": path, "reason": reason},
        )


class InvalidLogoError(DANFEError):
    """Exceção quando logo é inválida.

    A logo pode ser inválida por:
    - Formato não suportado (apenas PNG, JPG, JPEG, BMP)
    - Arquivo muito grande (máximo 500KB)
    - Arquivo não encontrado

    Attributes:
        path: Caminho do arquivo de logo (em details['path']).
        reason: Motivo da invalidação (em details['reason']).
    """

    def __init__(self, path: str, reason: str) -> None:
        """Inicializa a exceção.

        Args:
            path: Caminho do arquivo de logo.
            reason: Motivo pelo qual a logo é inválida.
        """
        super().__init__(
            message=f"Logo inválida: {reason}",
            details={"path": path, "reason": reason},
        )


class ConfigurationError(DANFEError):
    """Exceção para erros de configuração.

    Ocorre quando valores de configuração são inválidos:
    - Margens fora do range permitido (0-50mm)
    - Valores RGB fora do range (0-255)
    - Layout type inválido

    Attributes:
        field: Campo com erro (em details['field']).
        reason: Motivo do erro (em details['reason']).
    """

    def __init__(self, field: str, reason: str) -> None:
        """Inicializa a exceção.

        Args:
            field: Nome do campo de configuração com erro.
            reason: Motivo do erro de configuração.
        """
        super().__init__(
            message=f"Configuração inválida em '{field}': {reason}",
            details={"field": field, "reason": reason},
        )


class GenerationError(DANFEError):
    """Exceção quando a geração do PDF falha.

    Ocorre quando há erro durante a conversão de XML para PDF,
    após o XML ter sido validado com sucesso.

    Attributes:
        xml_path: Caminho do XML (em details['xml_path']).
        reason: Motivo da falha (em details['reason']).
    """

    def __init__(self, xml_path: str, reason: str) -> None:
        """Inicializa a exceção.

        Args:
            xml_path: Caminho do arquivo XML sendo processado.
            reason: Motivo da falha na geração.
        """
        super().__init__(
            message=f"Falha ao gerar DANFE: {reason}",
            details={"xml_path": xml_path, "reason": reason},
        )
