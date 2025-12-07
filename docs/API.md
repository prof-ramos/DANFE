# 📚 Documentação da API - DANFE Generator

Documentação completa da API pública do pacote `danfe_generator`.

---

## 📑 Índice

- [DANFEGenerator](#danfegenerator)
- [Configurações](#configurações)
- [Tipos de Resultado](#tipos-de-resultado)
- [Validadores](#validadores)
- [Exceções](#exceções)
- [Utilitários](#utilitários)

---

## DANFEGenerator

Classe principal para geração de DANFE.

### Importação

```python
from danfe_generator import DANFEGenerator, DANFEConfig
```

### Construtor

```python
def __init__(self, config: DANFEConfig | None = None) -> None
```

**Args:**

- `config`: Configurações do gerador. Se `None`, usa valores padrão.

### Métodos

#### `generate()`

```python
def generate(
    self,
    xml_path: str | Path,
    output_path: str | Path | None = None,
) -> GenerationResult
```

Gera DANFE a partir de um arquivo XML.

**Args:**

- `xml_path`: Caminho do arquivo XML de NFe
- `output_path`: Caminho de saída do PDF. Se `None`, usa mesmo nome do XML.

**Returns:** `GenerationResult` com detalhes da geração

**Raises:**

- `XMLNotFoundError`: Se o arquivo XML não existir
- `InvalidXMLError`: Se o XML não for uma NFe válida
- `GenerationError`: Se ocorrer erro durante a geração

**Exemplo:**

```python
result = generator.generate("nota.xml")
if result.success:
    print(f"PDF: {result.pdf_path} ({result.file_size_kb:.2f} KB)")
```

#### `generate_batch()`

```python
def generate_batch(
    self,
    xml_paths: Sequence[str | Path],
    output_dir: str | Path | None = None,
) -> BatchResult
```

Processa múltiplos XMLs em lote.

**Args:**

- `xml_paths`: Lista de caminhos de arquivos XML
- `output_dir`: Diretório de saída. Se `None`, usa diretório de cada XML.

**Returns:** `BatchResult` com estatísticas e resultados individuais

#### `generate_from_directory()`

```python
def generate_from_directory(
    self,
    input_dir: str | Path,
    output_dir: str | Path | None = None,
    pattern: str = "*.xml",
) -> BatchResult
```

Processa todos os XMLs de um diretório.

**Args:**

- `input_dir`: Diretório contendo arquivos XML
- `output_dir`: Diretório de saída dos PDFs
- `pattern`: Padrão glob para filtrar arquivos (default: `"*.xml"`)

#### `generate_stream()`

```python
def generate_stream(
    self,
    xml_paths: Sequence[str | Path],
) -> Iterator[GenerationResult]
```

Generator para processamento memory-efficient de grandes volumes.

---

## Configurações

### DANFEConfig

```python
from danfe_generator import DANFEConfig, MarginsConfig, ColorsConfig
```

| Atributo | Tipo | Default | Descrição |
|----------|------|---------|-----------|
| `logo_path` | `Path \| None` | `None` | Caminho do arquivo de logo |
| `empresa_nome` | `str \| None` | `None` | Nome da empresa |
| `margins` | `MarginsConfig` | `MarginsConfig()` | Margens do documento |
| `colors` | `ColorsConfig` | `ColorsConfig()` | Cores do documento |
| `layout_type` | `str` | `"complete"` | `"complete"` ou `"simplified"` |
| `show_logo` | `bool` | `True` | Exibir logo |

**Métodos:**

- `from_yaml(yaml_path)`: Carrega de arquivo YAML
- `to_dict()`: Converte para dicionário

### MarginsConfig

Margens do documento em milímetros (range: 0-50).

| Atributo | Tipo | Default |
|----------|------|---------|
| `top` | `int` | `10` |
| `right` | `int` | `10` |
| `bottom` | `int` | `10` |
| `left` | `int` | `10` |

### ColorsConfig

Cores RGB do documento.

| Atributo | Tipo | Default |
|----------|------|---------|
| `primary` | `tuple[int,int,int]` | `(41, 150, 161)` |
| `secondary` | `tuple[int,int,int]` | `(94, 82, 64)` |
| `accent` | `tuple[int,int,int]` | `(192, 21, 47)` |
| `text` | `tuple[int,int,int]` | `(0, 0, 0)` |
| `background` | `tuple[int,int,int]` | `(245, 245, 245)` |

---

## Tipos de Resultado

### GenerationResult

| Atributo | Tipo | Descrição |
|----------|------|-----------|
| `xml_path` | `Path` | Caminho do XML processado |
| `pdf_path` | `Path \| None` | Caminho do PDF gerado |
| `success` | `bool` | Se foi bem-sucedido |
| `error_message` | `str \| None` | Mensagem de erro |
| `file_size_kb` | `float` | Tamanho em KB |

### BatchResult

| Atributo | Tipo | Descrição |
|----------|------|-----------|
| `total` | `int` | Total processados |
| `successful` | `int` | Sucessos |
| `failed` | `int` | Falhas |
| `results` | `list[GenerationResult]` | Resultados individuais |
| `success_rate` | `float` (property) | Taxa de sucesso (%) |

---

## Validadores

### LogoValidator

Valida arquivos de logo.

- **Extensões:** `.png, .jpg, .jpeg, .bmp`
- **Tamanho máximo:** 500KB

### XMLValidator

Valida arquivos XML de NFe.

- **Tags obrigatórias:** `nfeProc`, `NFe`, `infNFe`

```python
from danfe_generator.core.validators import LogoValidator, XMLValidator

validator = XMLValidator()
result = validator.validate(Path("nota.xml"))
if not result.is_valid:
    print(result.error_message)
```

---

## Exceções

```text
DANFEError (base)
├── XMLNotFoundError      # XML não encontrado
├── InvalidXMLError       # XML inválido
├── InvalidLogoError      # Logo inválida
├── ConfigurationError    # Erro de config
└── GenerationError       # Erro na geração
```

Todas possuem `.message` e `.details`.

---

## Utilitários

### Cores

```python
from danfe_generator.utils.colors import hex_to_rgb, rgb_to_hex

rgb = hex_to_rgb("#FF5500")      # (255, 85, 0)
hex_str = rgb_to_hex(255, 85, 0) # "#FF5500"
```

### Arquivos

```python
from danfe_generator.utils.file_handlers import (
    ensure_directory,
    safe_write_file,
    get_file_size_formatted,
    list_files_by_extension,
)
```

---

**Versão:** 0.2.0
