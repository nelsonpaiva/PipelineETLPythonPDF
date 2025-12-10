# 📄 PDF Extractor

Ferramenta para extrair e processar tabelas de PDFs com Python, usando Camelot + OpenCV, com opção de salvar em PostgreSQL.

Status: funcional para extração por regiões (stream). Ajustes de regras e áreas são necessários por documento.

---

## 🗂 Estrutura principal do projeto

- files/  
  - redrex/                — PDFs de exemplo (faturas)
  - jornada/               — PDFs de exemplo (jornada de dados)
- files/pdf_viz.py        — script de visualização e testes para `redrex`
- files/pdf_viz_jornada.py— script de visualização e testes para `jornada`
- pyproject.toml
- README.md

---

## 🚀 Características

- ✅ Extração automática de dados de PDFs
- ✅ Processamento de tabelas e imagens
- ✅ Integração com PostgreSQL
- ✅ Visualização de áreas de extração
- ✅ Configuração flexível de regras

---

## 📋 Pré-requisitos

- Python 3.12 ou superior
- PostgreSQL instalado e configurado
- Poetry para gerenciamento de dependências

---

## 📦 Instalação (Poetry)

1. Na raiz do projeto:
```bash
poetry install
```

2. Se precisar adicionar um pacote:
```bash
poetry add camelot-py
poetry add opencv-python
```

Observações:
- Se receber erros sobre pyproject.toml (ex.: `dependences`), corrija o typo para `dependencies`.
- Se Poetry avisar sobre versão Python incompatível, ajuste a versão em pyproject.toml ou aponte o Poetry para um Python compatível:
```bash
poetry env use C:\caminho\para\python.exe
```

---

## 📦 Dependências

```
python = "^3.12"
camelot-py = "^0.11.0"
opencv-python = "^4.9.0.80"
matplotlib = "^3.8.3"
ghostscript = "^0.7"
pandas = "^2.2.2"
psycopg2-binary = "^2.9.9"
sqlalchemy = "^2.0.32"
unidecode = "^1.3.8"
```

---

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
DB_NAME=seu_nome_de_banco_de_dados
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
```

| Variável | Descrição |
|----------|-----------|
| `DB_NAME` | Nome do banco de dados PostgreSQL |
| `DB_USER` | Usuário do banco de dados |
| `DB_PASSWORD` | Senha de acesso |
| `DB_HOST` | Host do servidor (localhost ou IP) |

---

## 🛠️ Instalação

### 1. Clone o repositório

```bash
git clone <URL do repositório>
cd <nome do repositório>
```

### 2. Instale as dependências

```bash
poetry install
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto (veja seção acima).

### 4. Execute o projeto

```bash
poetry run python src/start.py
```

---

## 📖 Como Usar

### Passo a Passo

1. **Organize os arquivos PDF**
   - Crie uma subpasta em `src/files/` correspondente ao tipo de documento

2. **Configure as regras de extração**
   - Edite `src/configs/rules/notas.py` com as regras específicas

3. **Visualize as áreas de extração** (opcional)
   - Execute `pdf_viz.py` para obter referência visual das regiões a extrair

4. **Ajuste o script principal**
   - Modifique `src/start.py` conforme necessário

5. **Execute a extração**
   - O sistema processará automaticamente todos os PDFs e salvará no banco de dados

---

## 🐞 Resolução de problemas comuns

- ModuleNotFoundError (ex.: No module named 'camelot'):
  - Verifique que o pacote está instalado no venv do Poetry:
    ```bash
    poetry run python -c "import camelot, matplotlib; print('OK')"
    ```
  - Se OK, selecione o interpretador do venv no VS Code (`Python: Select Interpreter`).

- FileNotFoundError ao abrir PDF:
  - Verifique o caminho usado no script (`path = os.path.abspath(f"files/jornada/{file_name}.pdf")`)
  - Confirme nome correto da pasta (`jornada`) e do arquivo.

- Erro ao `poetry add opencv-python` com pyproject inválido:
  - Corrija `dependences` → `dependencies` no pyproject.toml.

- Mensagem do Poetry sobre versões Python:
  - Ajuste a especificação de python no pyproject.toml (ex.: `python = ">=3.13.2,<4.0.0"`) ou use `poetry env use` para apontar para um Python compatível.

- Camelot pode precisar de Ghostscript e/ou OpenCV; se ocorrer erro ao abrir PDFs ou ao `camelot.read_pdf`, instale Ghostscript e garanta que está no PATH.

---

## 🔎 Dicas para ajustar extração (Camelot)

- Se `tables[0].parsing_report` indicar baixa `accuracy` ou alto `whitespace`:
  - Teste `flavor='lattice'` vs `flavor='stream'`
  - Ajuste `table_areas`, `columns`, `edge_tol`, `row_tol`
  - Visualize com:
    ```python
    import camelot, matplotlib.pyplot as plt
    camelot.plot(tables[0], kind="contour")
    plt.show()
    ```

---

## 💡 Boas práticas

- Mantenha PDFs de teste organizados em `files/<tipo>/`
- Versione mudanças de regras de extração (configs/rules)
- Teste cada alteração com `poetry run python files/pdf_viz*.py`

---

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Faça um **fork** do repositório
2. Crie uma **branch** para suas alterações (`git checkout -b feature/sua-feature`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. **Push** para a branch (`git push origin feature/sua-feature`)
5. Abra um **Pull Request**

---
