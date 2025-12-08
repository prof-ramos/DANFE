# DANFE Generator

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type Checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy-lang.org/)

**Gerador de DANFE (Documento Auxiliar da Nota Fiscal Eletrônica) personalizado**, desenvolvido em Python. Converta arquivos XML de NFe em documentos PDF profissionais com facilidade.

![Exemplo de DANFE gerado](docs/images/danfe_example.png)

---

## ✨ Principais Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| 📄 **Geração de DANFE** | Converta XML de NFe em PDF de alta qualidade |
| 🎨 **Personalização Visual** | Configure cores, margens e adicione logo da empresa |
| 🖥️ **Interface Web** | Aplicação Streamlit com design "Fiscal Dark" premium |
| ✏️ **Criação de NF-e** | Crie notas fiscais manualmente via formulário completo |
| ⌨️ **Interface CLI** | Linha de comando para automação e scripts |
| 📦 **Processamento em Lote** | Processe múltiplos XMLs de uma só vez |
| 🐳 **Docker Ready** | Container otimizado para deploy em produção |
| ✅ **Validação Integrada** | Validação automática de arquivos XML e logos |
| 🐍 **Biblioteca Python** | Use como módulo em seus próprios projetos |
| 🧪 **Testado** | Suite completa de testes com pytest |

---

## 🛠️ Tech Stack

| Componente | Tecnologia | Propósito |
|------------|------------|-----------|
| **Linguagem** | Python 3.12+ | Runtime principal |
| **PDF Generation** | [brazilfiscalreport](https://pypi.org/project/brazilfiscalreport/) | Biblioteca de geração de documentos fiscais |
| **Interface Web** | [Streamlit](https://streamlit.io/) | Framework de aplicações web |
| **Config Management** | PyYAML | Carregamento de configurações |
| **Package Manager** | [uv](https://github.com/astral-sh/uv) / pip | Gerenciamento de dependências |
| **Testing** | pytest + pytest-cov | Testes e cobertura |
| **Quality** | ruff, mypy, black | Linting, type checking, formatação |

---

## 📂 Estrutura do Projeto

```text
DANFE/
├── src/
│   └── danfe_generator/           # 📦 Pacote principal
│       ├── __init__.py            # Exports públicos
│       ├── exceptions.py          # Exceções customizadas tipadas
│       ├── core/                  # 🧠 Lógica de negócio
│       │   ├── generator.py       # DANFEGenerator - classe principal
│       │   ├── config.py          # Dataclasses de configuração
│       │   └── validators.py      # Validadores (padrão Strategy)
│       ├── cli/                   # ⌨️ Interface de linha de comando
│       │   └── main.py
│       ├── web/                   # 🌐 Interface Streamlit
│       │   ├── app.py             # Aplicação principal
│       │   ├── components/        # Componentes de UI reutilizáveis
│       │   │   ├── icons.py       # Ícones SVG inline
│       │   │   └── layout.py      # Layout, CSS e theming
│       │   ├── logic/             # Lógica de negócio web
│       │   │   ├── models.py      # Dataclasses e state
│       │   │   ├── validators.py  # Validações de formulário
│       │   │   └── xml_builder.py # Construtor de XML NF-e
│       │   └── views/             # Views/Páginas
│       │       ├── create.py      # Criação manual de NF-e
│       │       └── upload.py      # Upload de XMLs existentes
│       └── utils/                 # 🔧 Utilitários
│           ├── colors.py          # Manipulação de cores
│           └── file_handlers.py   # Operações de arquivo
├── tests/                         # 🧪 Suite de testes
│   ├── conftest.py                # Fixtures compartilhadas
│   ├── test_generator.py
│   ├── test_config.py
│   ├── test_validators.py
│   └── ...
├── scripts/                       # 🛠️ Scripts utilitários
│   └── generate_test_assets.py
├── data/                          # 📁 Dados
│   ├── logos/                     # Logos para uso
│   ├── xmls/                      # XMLs de exemplo
│   └── output/                    # PDFs gerados
├── docs/                          # 📖 Documentação adicional
│   ├── API.md                     # Documentação da API
│   └── XML_STRUCTURE.md           # Estrutura do XML NFe
├── pyproject.toml                 # ⚙️ Configuração do projeto
├── config.yaml                    # 📝 Configuração externa
└── run_app.sh                     # 🚀 Script de execução web
```

---

## 🚀 Instalação

### Pré-requisitos

- **Python 3.12+**
- **uv** (recomendado) ou pip

### Com uv (Recomendado)

```bash
# Clonar repositório
git clone https://github.com/gabrielramos/danfe-generator.git
cd danfe-generator

# Criar ambiente virtual
uv venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Instalar com todas as dependências
uv pip install -e ".[all]"
```

### Com pip

```bash
# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate

# Instalar
pip install -e ".[all]"
```

### Instalação Mínima

```bash
pip install -e .           # Core apenas (geração de PDF)
pip install -e ".[web]"    # + Interface web Streamlit
pip install -e ".[dev]"    # + Ferramentas de desenvolvimento
pip install -e ".[all]"    # Tudo incluído
```

---

## 📖 Uso

### 🌐 Interface Web (Streamlit)

A maneira mais fácil de começar!

```bash
# Opção 1: Script de execução
./run_app.sh

# Opção 2: Comando direto
streamlit run src/danfe_generator/web/app.py
```

Acesse no navegador: **[http://localhost:8501](http://localhost:8501)**

#### Funcionalidades da Interface Web

**Upload de XMLs existentes:**

- ✅ Upload de múltiplos XMLs via drag-and-drop
- ✅ Upload de logo personalizada
- ✅ Seleção de cores primária, secundária e destaque
- ✅ Configuração de margens
- ✅ Download individual de cada PDF gerado
- ✅ Resumo de processamento com métricas

**Criação de NF-e manual:**

- ✅ Formulário completo com validação em tempo real
- ✅ Cadastro de emitente, destinatário e produtos
- ✅ Cálculo automático de impostos
- ✅ Geração de XML válido e download

**Design "Fiscal Dark":**

- ✅ Tema escuro premium inspirado em code editors
- ✅ Cores da bandeira brasileira (verde, azul-petróleo, dourado)
- ✅ Ícones SVG consistentes e micro-animações
- ✅ Tema segue preferência do sistema (`prefers-color-scheme`)

> **Nota sobre temas:** O tema é detectado automaticamente via CSS `prefers-color-scheme`.
> Para forçar um tema específico, configure `STREAMLIT_THEME_BASE=dark` ou `light`.

---

### ⌨️ CLI (Linha de Comando)

```bash
# Modo interativo (menu de seleção)
danfe

# Gerar DANFE para um arquivo específico
danfe nota.xml

# Especificar arquivo de saída
danfe nota.xml -o ./output/nota.pdf

# Com logo personalizada
danfe nota.xml --logo ./minha_logo.png

# Processar todos XMLs de um diretório
danfe --batch ./data/xmls -o ./data/output

# Usar arquivo de configuração
danfe nota.xml --config config.yaml

# Modo verboso (debug)
danfe nota.xml -v

# Formato de saída detalhado
danfe nota.xml --format detailed

# Ver ajuda completa
danfe --help
```

#### Opções CLI

| Opção | Descrição |
|-------|-----------|
| `-o, --output PATH` | Caminho de saída do PDF |
| `-l, --logo PATH` | Caminho da logo da empresa |
| `-c, --config FILE` | Arquivo de configuração YAML |
| `-v, --verbose` | Modo verboso (debug) |
| `--batch DIR` | Modo lote: processa todos XMLs do diretório |
| `--format simple\|detailed\|json` | Formato de saída |
| `-h, --help` | Mostra ajuda |

---

### 🐍 Como Biblioteca Python

```python
from pathlib import Path
from danfe_generator import DANFEGenerator, DANFEConfig, MarginsConfig, ColorsConfig

# === Configuração Básica ===
config = DANFEConfig(
    logo_path=Path("./data/logos/logo.png"),
)
generator = DANFEGenerator(config)

# Gerar DANFE
result = generator.generate("nota.xml")
print(f"✅ PDF gerado: {result.pdf_path}")
print(f"   Tamanho: {result.file_size_kb:.2f} KB")


# === Configuração Avançada ===
config = DANFEConfig(
    logo_path=Path("./logo.png"),
    empresa_nome="Minha Empresa LTDA",
    margins=MarginsConfig(
        top=10,
        right=10,
        bottom=10,
        left=10,
    ),
    colors=ColorsConfig(
        primary=(41, 150, 161),    # Azul esverdeado
        secondary=(94, 82, 64),    # Marrom
        accent=(192, 21, 47),      # Vermelho
    ),
    layout_type="complete",        # ou "simplified"
    show_logo=True,
    show_company_info=True,
    show_additional_info=True,
)

generator = DANFEGenerator(config)


# === Processamento em Lote ===
batch_result = generator.generate_from_directory(
    input_dir="./data/xmls",
    output_dir="./data/output",
    pattern="*.xml",
)

print(f"📊 Processados: {batch_result.total}")
print(f"   ✅ Sucesso: {batch_result.successful}")
print(f"   ❌ Falhas: {batch_result.failed}")
print(f"   📈 Taxa: {batch_result.success_rate:.1f}%")


# === Generator Stream (Memory-efficient) ===
xml_files = list(Path("./xmls").glob("*.xml"))

for result in generator.generate_stream(xml_files):
    if result.success:
        print(f"✅ {result.xml_path.name} → {result.pdf_path}")
    else:
        print(f"❌ {result.xml_path.name}: {result.error_message}")


# === Tratamento de Erros ===
from danfe_generator import XMLNotFoundError, GenerationError

try:
    result = generator.generate("arquivo_inexistente.xml")
except XMLNotFoundError as e:
    print(f"Arquivo não encontrado: {e.details['path']}")
except GenerationError as e:
    print(f"Erro na geração: {e.message}")
```

---

## ⚙️ Configuração

### Via Código (DANFEConfig)

```python
from pathlib import Path
from danfe_generator import DANFEConfig, MarginsConfig, ColorsConfig

config = DANFEConfig(
    # Logo da empresa
    logo_path=Path("./logo.png"),

    # Nome da empresa (opcional)
    empresa_nome="Minha Empresa LTDA",

    # Margens em mm (0-50)
    margins=MarginsConfig(top=10, right=10, bottom=10, left=10),

    # Cores RGB
    colors=ColorsConfig(
        primary=(41, 150, 161),      # Elementos principais
        secondary=(94, 82, 64),      # Elementos secundários
        accent=(192, 21, 47),        # Destaques
        text=(0, 0, 0),              # Texto
        background=(245, 245, 245),  # Fundo
    ),

    # Layout
    layout_type="complete",  # "complete" ou "simplified"
    show_logo=True,
    show_company_info=True,
    show_additional_info=True,
)
```

### Via YAML (config.yaml)

```yaml
# config.yaml
issuer:
  name: "EMPRESA TESTE LTDA"

logo:
  path: "./data/logos/logo.png"

margins:
  top: 10
  right: 10
  bottom: 10
  left: 10

colors:
  primary: [41, 150, 161]
  secondary: [94, 82, 64]
  accent: [192, 21, 47]
  text: [0, 0, 0]
  background: [245, 245, 245]

layout:
  type: "complete"
  show_logo: true
  show_company_info: true
  show_additional_info: true
```

```python
# Carregar configuração YAML
config = DANFEConfig.from_yaml("config.yaml")
generator = DANFEGenerator(config)
```

---

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Com cobertura de código
pytest --cov=src/danfe_generator

# Relatório HTML de cobertura
pytest --cov=src/danfe_generator --cov-report=html
# Abrir: htmlcov/index.html

# Testes específicos
pytest tests/test_generator.py -v
pytest tests/test_config.py -v
pytest tests/test_validators.py -v

# Excluir testes lentos
pytest -m "not slow"

# Apenas testes de integração
pytest -m integration
```

---

## 🐳 Docker

### Build Local

```bash
# Build da imagem
docker build -t danfe-generator .

# Executar container
docker run -d -p 8501:8501 --name danfe danfe-generator

# Acessar aplicação
open http://localhost:8501
```

### Docker Compose

O projeto inclui configurações otimizadas para desenvolvimento e produção.

#### Desenvolvimento (Hot Reload)

Use este modo para desenvolver. As alterações no código são refletidas imediatamente.

```bash
# Iniciar em modo desenvolvimento
docker compose -f docker-compose.dev.yml up
```

#### Produção

Use este modo para deploy. A imagem é otimizada e segura (non-root).

```bash
# Iniciar em modo produção (detached)
docker compose -f docker-compose.yml up -d
```

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `STREAMLIT_SERVER_PORT` | Porta do servidor Streamlit | `8501` |
| `STREAMLIT_SERVER_ADDRESS` | Endereço de bind do servidor | `0.0.0.0` |
| `STREAMLIT_SERVER_HEADLESS` | Modo headless (sem browser) | `true` |
| `STREAMLIT_THEME_BASE` | Tema base da UI (`light` ou `dark`) | `light` |
| `STREAMLIT_ENV` | Ambiente de execução | `production` |
| `STREAMLIT_BROWSER_GATHER_USAGE_STATS` | Coleta de estatísticas | `false` |
| `PYTHONPATH` | Caminho do código fonte | `/app/src` |
| `PYTHONDONTWRITEBYTECODE` | Desabilita .pyc | `1` |
| `PYTHONUNBUFFERED` | Output sem buffer | `1` |

---

## 🔧 Desenvolvimento

### Configurar Ambiente de Desenvolvimento

```bash
# Instalar com dependências de dev
uv pip install -e ".[dev]"

# Gerar assets de teste (logo PNG, XMLs de exemplo)
python scripts/generate_test_assets.py
```

### Linting e Formatação

```bash
# Verificar código com ruff
ruff check src tests

# Corrigir automaticamente
ruff check src tests --fix

# Formatação com black
black src tests

# Type checking com mypy
mypy src
```

### Pre-commit Hooks

```bash
# Instalar hooks
pre-commit install

# Executar em todos os arquivos
pre-commit run --all-files
```

---

## 📝 Changelog

### v0.3.0 (Atual) — 2025-12-08

> **Sem breaking changes.** Esta versão é compatível com v0.2.0.
> Imagem Docker: `~300MB` (multi-stage build com python:3.12-slim).

- 🎨 **Design "Fiscal Dark" premium**
  - Tema escuro inspirado em code editors
  - Paleta de cores da bandeira brasileira
  - Ícones SVG customizados com animações
  - Detecção automática de tema via `prefers-color-scheme`
- ✏️ **Criação de NF-e via formulário**
  - Interface completa para preenchimento manual
  - Validação em tempo real de campos
  - Geração de XML válido
- 🐳 **Docker ready**
  - Dockerfile multi-stage otimizado
  - Non-root user para segurança
  - Healthcheck integrado (Python-based)
- 🛠️ **Arquitetura web modular**
  - Componentes reutilizáveis (`components/`)
  - Lógica separada (`logic/`)
  - Views organizadas (`views/`)

### v0.2.0

- ✨ **Reorganização completa da codebase**
  - Estrutura de pacote Python adequada
  - Módulos separados: `core`, `cli`, `web`, `utils`
- 🧪 **Suite de testes com pytest**
  - Cobertura mínima de 80%
  - Fixtures reutilizáveis
- 🔧 **Configuração via dataclasses imutáveis**
  - `DANFEConfig`, `MarginsConfig`, `ColorsConfig`
  - Carregamento de YAML
- 🚨 **Exceções customizadas tipadas**
  - `XMLNotFoundError`, `InvalidLogoError`, `GenerationError`
- 📊 **Validadores com padrão Strategy**
  - `LogoValidator`, `XMLValidator`
- ⚡ **Generator para processamento memory-efficient**
  - `generate_stream()` para grandes lotes

### v0.1.0

- 🎉 Versão inicial

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'feat: Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está licenciado sob a **[MIT License](LICENSE)**.

---

## 🙏 Agradecimentos

- [BrazilFiscalReport](https://github.com/luan-rock/brazilfiscalreport) - Biblioteca de geração de documentos fiscais
- [Streamlit](https://streamlit.io/) - Framework de aplicações web
- [uv](https://github.com/astral-sh/uv) - Gerenciador de pacotes Python ultrarrápido

---

Desenvolvido com ❤️ usando Python e BrazilFiscalReport
