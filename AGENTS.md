# Repository Guidelines

## Visão geral e estrutura
- `src/danfe_generator`: núcleo; `core/` (generator, configs, validators), `cli/main.py`, `web/app.py`, `utils/`, `exceptions.py`.
- `tests/`: suíte pytest; `scripts/`: utilidades (ex.: `generate_test_assets.py`).
- Dados e exemplos em `data/`, `xmls/`; saídas em `danfes_saida/`; script de entrada rápida `run_app.sh`.
- Configurações centrais em `pyproject.toml` e `config.yaml`.

## Ambiente e comandos principais
- Requisitos: Python 3.12+, uv/pip. Instalação típica: `uv pip install -e ".[dev]"` (ou `pip install -e ".[dev]"`); crie venv com `uv venv`.
- Web: `./run_app.sh` ou `streamlit run src/danfe_generator/web/app.py`.
- CLI: `danfe --help`; exemplo: `danfe xmls/nota.xml -o danfes_saida/nota.pdf --logo logos/logo.png`.
- Geração de assets de teste: `python scripts/generate_test_assets.py`.

## Release e empacotamento
- Versão em `pyproject.toml`; atualize antes de lançar e crie tag correspondente.
- Build local: `uv build` (ou `python -m build`) gera wheel/sdist em `dist/`.
- Validação do pacote: `pip install dist/*.whl` em venv limpa e rode `danfe --help` + `pytest` para garantir CLI e API.
- Publicação (quando aplicável): use credenciais PyPI e `uv publish` ou `twine upload dist/*`.

## Estilo de código e convenções
- Python com indentação de 4 espaços; largura de linha 100. Formate com `black src tests`.
- Lint: `ruff check src tests` (seleciona E,W,F,I,B,C4,UP,ARG,SIM; ignora E501,B008). Ordenação com isort integrada (`known-first-party = danfe_generator`).
- Tipagem: `mypy src` com modo estrito (sem defs sem tipo).
- Nomeação: módulos/variáveis em `snake_case`, classes em `PascalCase`, constantes em MAIÚSCULO; funções CLI priorizam verbos curtos.

## Testes e cobertura
- Rodar `pytest` (busca em `tests`, arquivos `test_*.py`, funções `test_*`).
- Marcadores disponíveis: `slow`, `integration`; exemplos: `pytest -m "not slow"`, `pytest -m integration`.
- Cobertura: `pytest --cov=src/danfe_generator --cov-report=html`; meta mínima configurada em 80%.
- Coloque fixtures/dados auxiliares em `tests/` ou `data/`; evite escrever fora de `danfes_saida/`.

## Commits e PRs
- Histórico atual curto (`initial commit`); use mensagens concisas no imperativo, com prefixo de escopo quando ajudar (`feat: ...`, `fix: ...`).
- Antes de abrir PR: execute `ruff check`, `black --check src tests`, `mypy src`, `pytest`; inclua saídas relevantes.
- PRs devem trazer resumo objetivo, passos de teste, issues vinculadas e evidências visuais (PDF gerado ou screenshot do Streamlit) quando aplicável.
- Prefira lotes pequenos e bem descritos; mencione qualquer impacto em CLI, API pública ou `config.yaml`.

## Dicas rápidas de config e segurança
- Não versionar PDFs grandes nem dados sensíveis; use `danfes_saida/` para artefatos temporários e limpe antes de commitar.
- `config.yaml` pode conter dados de empresa; para repositórios públicos, utilize valores fictícios ou variáveis de ambiente.
- Logos/ativos em `data/` ou `logos/` com caminhos relativos; confirme legibilidade em fundo branco.
