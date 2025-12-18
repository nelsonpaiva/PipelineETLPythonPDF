# 📄 PDF Extractor

Ferramenta para extrair e processar tabelas de PDFs com Python, usando Camelot + OpenCV, com opção de salvar em PostgreSQL.

Status: funcional para extração por regiões (stream). Ajustes de regras e áreas são necessários por documento.

---

## 🗂 Estrutura principal do projeto

- files/  
  - redrex/                — PDFs de exemplo (faturas)
  - jornada/               — PDFs de exemplo (jornada de dados)
- files/pdf_viz.py        — script de visualização e testes para `redrex`
***
# Pipeline ETL — PDF to PostgreSQL

Resumo
------
Projeto para extrair tabelas de PDFs, transformar e salvar em PostgreSQL. A pipeline usa Camelot para extração de tabelas, OpenCV/Pillow para suporte a imagens, pandas para manipulação e SQLAlchemy/psycopg2 para persistência no banco.

Status
------
- Funcional para extração por áreas configuráveis (stream/lattice)
- Regras de extração configuráveis em `configs/rules`

Estrutura principal
------------------
- `start.py`            — executor principal que itera PDFs e processa tabelas
- `main.py`             — arquivo vazio (pode ser usado como entrypoint alternativo)
- `configs/`            — configurações e regras (`configs/rules`, `configs/tools`)
- `files/`              — PDFs de entrada e scripts de visualização (`pdf_viz.py`, `pdf_viz_jornada.py`)
- `dbt_dashboard/`      — artefatos do dbt / app de exemplo
- `dbt_pdf_python/`     — projeto dbt relacionado (models, target, logs)
- `requirements.txt`    — lista de dependências (pip)
- `pyproject.toml`      — configuração Poetry (dependências/metadata)

Pré-requisitos
--------------
- Python 3.11+ (os arquivos indicam 3.13 em `pyproject.toml`, mas a stack funciona em 3.11+ na maioria dos casos)
- PostgreSQL (servidor acessível para salvar resultados)
- Ghostscript (recomendado para Camelot / manipulação de PDFs em algumas plataformas)

Instalação (recomendada)
-----------------------
1. Clone o repositório:

```bash
git clone <URL-do-repositório>
cd PipelineETLPythonPDF
```

2. Opção A — Usando Poetry (recomendado se quiser replicar ambiente do `pyproject.toml`):

```bash
# instalar o poetry se necessário
# pip install poetry
poetry install
# ativar shell do poetry (opcional)
poetry shell
```

3. Opção B — Usando virtualenv + pip e o `requirements.txt` (Windows/Powershell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # PowerShell
pip install --upgrade pip
pip install -r requirements.txt
```

Variáveis de ambiente
---------------------
Crie um `.env` na raiz ou exporte as variáveis. Variáveis esperadas:

- `DB_NAME` — nome do banco
- `DB_USER` — usuário do banco
- `DB_PASSWORD` — senha
- `DB_HOST` — host (ex.: localhost)
- `DB_PORT` — porta (opcional, padrão 5432)

Exemplos

Windows PowerShell (.env recomendado):

```powershell
$env:DB_NAME = "meu_banco"
$env:DB_USER = "usuario"
$env:DB_PASSWORD = "senha"
$env:DB_HOST = "localhost"
```

Linux / macOS:

```bash
export DB_NAME=meu_banco
export DB_USER=usuario
export DB_PASSWORD=senha
export DB_HOST=localhost
```

Como executar
-------------
- Rodar o executor principal (itera PDFs na pasta `files/<corretora>`):

```bash
# com poetry
poetry run python start.py
# ou, em venv/pip
python start.py
```

- Os scripts de visualização podem ajudar a ajustar `table_areas` e regras:

```bash
python files/pdf_viz.py
python files/pdf_viz_jornada.py
```

Notas sobre `start.py` e fluxo
------------------------------
- `start.py` cria a classe `PDFTableExtractor` que lê arquivos em `files/<nome>/`, aplica regras configuradas em `configs/rules/regras.py` e salva CSVs em `files/csv/` além de persistir no PostgreSQL via `RDSPostgreSQLManager` (`configs/tools/postgres.py`).
- A persistência usa `pandas.DataFrame.to_sql(..., con=engine)` com um engine SQLAlchemy criado em `RDSPostgreSQLManager.alchemy()`.

Dependências principais
-----------------------
As dependências estão em `requirements.txt` e `pyproject.toml`. Principais pacotes:

- camelot-py / opencv-python(-headless)
- pandas
- sqlalchemy
- psycopg2-binary
- ghostscript (externo)

Problemas comuns e soluções rápidas
---------------------------------
- Erro de import (ex.: `No module named 'camelot'`): verifique venv/Poetry e reinstale as dependências.
- `camelot.read_pdf` falha: confirme instalação do Ghostscript e verifique se a versão do Camelot é compatível com sua plataforma.
- Problemas de parsing (baixa acurácia): ajustar `flavor` (stream/lattice), `table_areas`, `columns`, e usar os scripts de visualização para validar.

Melhorias e observações técnicas
--------------------------------
- Em `configs/tools/postgres.py` há uma validação no construtor que checa o método `check_environment_variables` sem chamá-lo. Recomenda-se alterar `not self.check_environment_variables` para `not self.check_environment_variables()` para validar corretamente as variáveis de ambiente.
- `main.py` está vazio — pode ser usado para criar uma CLI/unidade de orquestração.

Contribuição
------------
1. Fork
2. Branch com nome claro (`feature/` ou `fix/`)
3. Commits pequenos e descritivos
4. PR com explicação das mudanças

Contato
-------
Para dúvidas ou suporte, abra uma issue ou contate o autor registrado no `pyproject.toml`.

***
- Erro ao `poetry add opencv-python` com pyproject inválido:

Comandos Diversos
------------
Execução do Poetry: poetry run [`nome do arquivo`]
Execução de pasta específica: poetry run --select [`nome do arquivo`]
Instalação com o Poetry: poetry add [`nome da biblioteca`]

Criar documentação automática do dbt: dbt docs generate –-cria a documentação
Criar documentação automática do dbt: dbt docs serve –-visualiza a documentação

Executando o streamlit: streamlit run [`pasta/nome do arquivo.py`]

