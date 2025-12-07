# DANFE Generator

Gerador de **DANFE** (Documento Auxiliar da Nota Fiscal Eletrônica) em PDF a partir de arquivos XML de NFe.

## 🛠 Tech Stack

- **Python 3.12+** com type hints completos
- **brazilfiscalreport** - Geração de PDFs fiscais
- **streamlit** - Interface web
- **uv** / pip - Gerenciamento de dependências

## 📂 Estrutura do Projeto

```text
src/danfe_generator/
├── __init__.py           # Exports públicos
├── exceptions.py         # Exceções tipadas
├── core/
│   ├── generator.py      # DANFEGenerator
│   ├── config.py         # Dataclasses imutáveis
│   └── validators.py     # Padrão Strategy
├── cli/main.py           # CLI
├── web/app.py            # Streamlit
└── utils/                # Utilitários
```

## 📖 Documentação

- [README.md](README.md) - Guia completo de uso
- [docs/API.md](docs/API.md) - Referência da API
- [docs/XML_STRUCTURE.md](docs/XML_STRUCTURE.md) - Estrutura do XML NFe

## 🚀 Comandos Rápidos

```bash
# Instalar
uv pip install -e ".[all]"

# Interface Web
./run_app.sh

# CLI
danfe nota.xml
danfe --batch ./xmls

# Testes
pytest --cov=src/danfe_generator
```

## 🐍 Uso como Biblioteca

```python
from danfe_generator import DANFEGenerator, DANFEConfig
from pathlib import Path

config = DANFEConfig(logo_path=Path("./logo.png"))
generator = DANFEGenerator(config)
result = generator.generate("nota.xml")
```

## ⚙️ Ferramentas

| Ferramenta | Propósito |
|------------|-----------|
| pytest | Testes |
| ruff | Linting |
| mypy | Type checking |
| black | Formatação |
