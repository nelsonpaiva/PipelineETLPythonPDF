# 📄 PDF Extractor

Uma ferramenta poderosa para extrair e processar dados de arquivos PDF usando Python, com integração a banco de dados PostgreSQL.

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

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Faça um **fork** do repositório
2. Crie uma **branch** para suas alterações (`git checkout -b feature/sua-feature`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. **Push** para a branch (`git push origin feature/sua-feature`)
5. Abra um **Pull Request**

---

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📞 Suporte

Em caso de dúvidas ou problemas, abra uma [issue](../../issues) no repositório.