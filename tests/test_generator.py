"""Testes para o módulo do gerador DANFE."""

from pathlib import Path

import pytest

from danfe_generator.core import DANFEConfig, DANFEGenerator
from danfe_generator.core.generator import BatchResult, GenerationResult
from danfe_generator.exceptions import DirectoryNotFoundError, XMLNotFoundError


class TestGenerationResult:
    """Testes para GenerationResult."""

    def test_success_result(self, temp_dir: Path):
        """Testa resultado de sucesso."""
        result = GenerationResult(
            xml_path=temp_dir / "test.xml",
            pdf_path=temp_dir / "test.pdf",
            success=True,
            file_size_kb=50.5,
        )
        assert result.success
        assert result.file_size_kb == 50.5
        assert result.error_message is None

    def test_error_result(self, temp_dir: Path):
        """Testa resultado de erro."""
        result = GenerationResult(
            xml_path=temp_dir / "test.xml",
            pdf_path=None,
            success=False,
            error_message="Erro de teste",
        )
        assert not result.success
        assert result.error_message == "Erro de teste"


class TestBatchResult:
    """Testes para BatchResult."""

    def test_empty_batch(self):
        """Testa lote vazio."""
        batch = BatchResult()
        assert batch.total == 0
        assert batch.successful == 0
        assert batch.failed == 0
        assert batch.success_rate == 0.0

    def test_success_rate_calculation(self):
        """Testa cálculo da taxa de sucesso."""
        batch = BatchResult(total=10, successful=7, failed=3)
        assert batch.success_rate == 70.0

    def test_all_successful(self):
        """Testa lote com 100% de sucesso."""
        batch = BatchResult(total=5, successful=5, failed=0)
        assert batch.success_rate == 100.0


class TestDANFEGenerator:
    """Testes para DANFEGenerator."""

    def test_init_default_config(self):
        """Testa inicialização com configuração padrão."""
        generator = DANFEGenerator()
        assert generator.config is not None

    def test_init_custom_config(self, default_config: DANFEConfig):
        """Testa inicialização com configuração customizada."""
        generator = DANFEGenerator(default_config)
        assert generator.config == default_config

    def test_generate_success(
        self,
        generator: DANFEGenerator,
        sample_xml_file: Path,
        temp_dir: Path,
    ):
        """Testa geração bem-sucedida."""
        output_path = temp_dir / "output.pdf"
        result = generator.generate(sample_xml_file, output_path)

        assert result.success
        assert result.pdf_path == output_path
        assert output_path.exists()
        assert result.file_size_kb > 0

    def test_generate_creates_output_directory(
        self,
        generator: DANFEGenerator,
        sample_xml_file: Path,
        temp_dir: Path,
    ):
        """Testa que diretório de saída é criado automaticamente."""
        nested_output = temp_dir / "nested" / "dir" / "output.pdf"
        result = generator.generate(sample_xml_file, nested_output)

        assert result.success
        assert nested_output.exists()

    def test_generate_default_output_path(
        self,
        generator: DANFEGenerator,
        sample_xml_file: Path,
    ):
        """Testa geração com caminho de saída padrão."""
        result = generator.generate(sample_xml_file)

        assert result.success
        expected_output = sample_xml_file.with_suffix(".pdf")
        assert result.pdf_path == expected_output

        # Cleanup
        if expected_output.exists():
            expected_output.unlink()

    def test_generate_xml_not_found(
        self,
        generator: DANFEGenerator,
        temp_dir: Path,
    ):
        """Testa erro com XML inexistente."""
        with pytest.raises(XMLNotFoundError):
            generator.generate(temp_dir / "nonexistent.xml")

    def test_generate_batch_success(
        self,
        generator: DANFEGenerator,
        sample_xml_file: Path,
        temp_dir: Path,
    ):
        """Testa geração em lote."""
        # Criar mais arquivos
        xml2 = temp_dir / "test2.xml"
        xml2.write_text(sample_xml_file.read_text())

        output_dir = temp_dir / "output"

        result = generator.generate_batch(
            [sample_xml_file, xml2],
            output_dir,
        )

        assert result.total == 2
        assert result.successful == 2
        assert result.failed == 0
        assert len(result.results) == 2

    def test_generate_batch_with_errors(
        self,
        generator: DANFEGenerator,
        sample_xml_file: Path,
        temp_dir: Path,
    ):
        """Testa lote com alguns erros."""
        invalid_xml = temp_dir / "invalid.xml"
        invalid_xml.write_text("<root>not a nfe</root>")

        output_dir = temp_dir / "output"

        result = generator.generate_batch(
            [sample_xml_file, invalid_xml],
            output_dir,
        )

        assert result.total == 2
        assert result.successful == 1
        assert result.failed == 1

    def test_generate_from_directory(
        self,
        generator: DANFEGenerator,
        sample_xml_file: Path,
        temp_dir: Path,
    ):
        """Testa geração a partir de diretório."""
        # sample_xml_file já está em temp_dir
        assert sample_xml_file.exists()
        output_dir = temp_dir / "output"

        result = generator.generate_from_directory(temp_dir, output_dir)

        assert result.total == 1
        assert result.successful == 1

    def test_generate_from_nonexistent_directory(
        self,
        generator: DANFEGenerator,
        temp_dir: Path,
    ):
        """Testa erro com diretório inexistente."""
        with pytest.raises(DirectoryNotFoundError) as exc_info:
            generator.generate_from_directory(
                temp_dir / "nonexistent",
                temp_dir / "output",
            )
        assert "nonexistent" in str(exc_info.value)

    def test_generate_stream(
        self,
        generator: DANFEGenerator,
        sample_xml_file: Path,
    ):
        """Testa geração via generator."""
        results = list(generator.generate_stream([sample_xml_file]))

        assert len(results) == 1
        assert results[0].success

        # Cleanup
        if results[0].pdf_path and results[0].pdf_path.exists():
            results[0].pdf_path.unlink()
