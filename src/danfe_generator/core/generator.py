"""Gerador principal de DANFE.

Este módulo contém a classe principal DANFEGenerator que encapsula
toda a lógica de geração de documentos DANFE a partir de arquivos XML.

Classes:
    GenerationResult: Resultado da geração de um único DANFE.
    BatchResult: Resultado de processamento em lote.
    DANFEGenerator: Classe principal para geração de DANFEs.

Example:
    Uso básico::

        from danfe_generator import DANFEGenerator, DANFEConfig
        from pathlib import Path

        config = DANFEConfig(logo_path=Path("./logo.png"))
        generator = DANFEGenerator(config)
        result = generator.generate("nota.xml")

        if result.is_valid:
            print(f"PDF gerado: {result.pdf_path}")

    Processamento em lote::

        batch = generator.generate_from_directory("./xmls", "./output")
        print(f"Sucesso: {batch.success_rate:.1f}%")

    Processamento com generator (memory-efficient)::

        for result in generator.generate_stream(xml_files):
            if result.success:
                print(f"✅ {result.pdf_path}")
"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from brazilfiscalreport.danfe import Danfe
from brazilfiscalreport.danfe.config import DanfeConfig, Margins

from danfe_generator.core.config import DANFEConfig
from danfe_generator.core.validators import LogoValidator, XMLValidator
from danfe_generator.exceptions import DirectoryNotFoundError, GenerationError

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


@dataclass
class GenerationResult:
    """Resultado da geração de um DANFE."""

    xml_path: Path
    pdf_path: Path | None
    success: bool
    error_message: str | None = None
    file_size_kb: float = 0.0


@dataclass
class BatchResult:
    """Resultado de geração em lote."""

    total: int = 0
    successful: int = 0
    failed: int = 0
    results: list[GenerationResult] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Taxa de sucesso em porcentagem."""
        if self.total == 0:
            return 0.0
        return (self.successful / self.total) * 100


class DANFEGenerator:
    """
    Gerador de DANFE personalizado.

    Esta classe encapsula a lógica de geração de DANFE usando a biblioteca
    brazilfiscalreport, com suporte a personalização de logo, cores e margens.

    Exemplo:
        >>> config = DANFEConfig(logo_path=Path("./logo.png"))
        >>> generator = DANFEGenerator(config)
        >>> result = generator.generate(Path("nota.xml"))
        >>> print(f"PDF gerado: {result.pdf_path}")
    """

    def __init__(self, config: DANFEConfig | None = None) -> None:
        """
        Inicializa o gerador.

        Args:
            config: Configurações do gerador. Se None, usa valores padrão.
        """
        self.config = config or DANFEConfig()
        self._logo_validator = LogoValidator()
        self._xml_validator = XMLValidator()
        self._validated_logo: Path | None = None
        self._logo_validation_done: bool = False

    def _validate_logo(self) -> Path | None:
        """Valida e retorna o caminho da logo se válido."""
        if self._logo_validation_done:
            return self._validated_logo

        self._logo_validation_done = True

        if self.config.logo_path is None:
            return None

        result = self._logo_validator.validate(self.config.logo_path)
        if result.is_valid:
            self._validated_logo = result.value
            logger.info("Logo validada: %s", self.config.logo_path)
            return self._validated_logo

        logger.warning("Logo inválida: %s", result.error_message)
        return None

    def _build_danfe_config(self) -> DanfeConfig:
        """Constrói configuração do brazilfiscalreport."""
        logo_path = self._validate_logo()

        margins = Margins(
            top=self.config.margins.top,
            right=self.config.margins.right,
            bottom=self.config.margins.bottom,
            left=self.config.margins.left,
        )

        return DanfeConfig(
            logo=str(logo_path) if logo_path else None,
            margins=margins,
        )

    def generate(
        self,
        xml_path: str | Path,
        output_path: str | Path | None = None,
    ) -> GenerationResult:
        """
        Gera DANFE a partir de XML.

        Args:
            xml_path: Caminho do arquivo XML
            output_path: Caminho de saída do PDF. Se None, usa mesmo nome do XML.

        Returns:
            GenerationResult com detalhes da geração

        Raises:
            XMLNotFoundError: Se XML não existir
            GenerationError: Se ocorrer erro na geração
        """
        xml_path = Path(xml_path)
        logger.info("Gerando DANFE para: %s", xml_path)

        # Validar XML
        self._xml_validator.validate_or_raise(xml_path)

        # Definir output
        output_path = xml_path.with_suffix(".pdf") if output_path is None else Path(output_path)

        # Garantir que diretório de saída existe
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Ler XML
            xml_content = xml_path.read_text(encoding="utf-8")

            # Criar DANFE
            danfe_config = self._build_danfe_config()
            danfe = Danfe(xml_content, config=danfe_config)

            # Gerar PDF
            danfe.output(str(output_path))

            # Stats
            file_size_kb = output_path.stat().st_size / 1024

            logger.info("DANFE gerada com sucesso: %s (%.2f KB)", output_path, file_size_kb)

            return GenerationResult(
                xml_path=xml_path,
                pdf_path=output_path,
                success=True,
                file_size_kb=file_size_kb,
            )

        except Exception as e:
            logger.exception("Erro ao gerar DANFE: %s", e)
            raise GenerationError(str(xml_path), str(e)) from e

    def generate_batch(
        self,
        xml_paths: Sequence[str | Path],
        output_dir: str | Path | None = None,
    ) -> BatchResult:
        """
        Gera DANFEs em lote.

        Args:
            xml_paths: Lista de caminhos de XMLs
            output_dir: Diretório de saída. Se None, usa mesmo diretório de cada XML.

        Returns:
            BatchResult com estatísticas e resultados individuais
        """
        output_dir = Path(output_dir) if output_dir else None
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)

        batch_result = BatchResult(total=len(xml_paths))

        for xml_path in xml_paths:
            xml_path = Path(xml_path)

            # Calcular output
            out_path = output_dir / f"{xml_path.stem}.pdf" if output_dir else None

            try:
                result = self.generate(xml_path, out_path)
                batch_result.successful += 1
                batch_result.results.append(result)
            except Exception as e:
                logger.error("Erro processando %s: %s", xml_path, e)
                batch_result.failed += 1
                batch_result.results.append(
                    GenerationResult(
                        xml_path=xml_path,
                        pdf_path=None,
                        success=False,
                        error_message=str(e),
                    )
                )

        logger.info(
            "Lote concluído: %d/%d sucesso (%.1f%%)",
            batch_result.successful,
            batch_result.total,
            batch_result.success_rate,
        )

        return batch_result

    def generate_from_directory(
        self,
        input_dir: str | Path,
        output_dir: str | Path | None = None,
        pattern: str = "*.xml",
    ) -> BatchResult:
        """
        Gera DANFEs para todos XMLs em um diretório.

        Args:
            input_dir: Diretório contendo XMLs
            output_dir: Diretório de saída
            pattern: Padrão glob para filtrar arquivos

        Returns:
            BatchResult com estatísticas
        """
        input_dir = Path(input_dir)

        if not input_dir.exists():
            logger.error("Diretório não encontrado: %s", input_dir)
            raise DirectoryNotFoundError(str(input_dir))

        xml_files = list(input_dir.glob(pattern))
        logger.info("Encontrados %d arquivos em %s", len(xml_files), input_dir)

        return self.generate_batch(xml_files, output_dir)

    def generate_stream(
        self,
        xml_paths: Sequence[str | Path],
        output_dir: str | Path | None = None,
    ) -> Iterator[GenerationResult]:
        """
        Gera DANFEs como generator (memory-efficient para grandes lotes).

        Args:
            xml_paths: Sequência de caminhos de XMLs
            output_dir: Diretório de saída opcional

        Yields:
            GenerationResult para cada XML processado
        """
        output_dir = Path(output_dir) if output_dir else None

        for xml_path in xml_paths:
            xml_path = Path(xml_path)
            out_path = output_dir / f"{xml_path.stem}.pdf" if output_dir else None

            try:
                yield self.generate(xml_path, out_path)
            except Exception as e:
                yield GenerationResult(
                    xml_path=xml_path,
                    pdf_path=None,
                    success=False,
                    error_message=str(e),
                )
