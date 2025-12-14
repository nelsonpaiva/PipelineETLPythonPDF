"""
Módulo de utilitários para conexão com PostgreSQL (RDS/local).

Este arquivo fornece a classe `RDSPostgreSQLManager` que encapsula
operações básicas de conexão, execução de queries e criação de
engine SQLAlchemy para uso em pipelines ETL.

Observação: a classe aceita credenciais por parâmetro ou por
variáveis de ambiente (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`).
"""

import os

import psycopg2
from sqlalchemy import create_engine


class RDSPostgreSQLManager:
    """Gerencia conexões e operações simples contra um banco PostgreSQL.

    Parâmetros (todos opcionais — podem vir de variáveis de ambiente):
      db_name: nome do banco de dados
      db_user: usuário do banco
      db_password: senha do usuário
      db_host: host/endpoint do banco
      db_port: porta do serviço (padrão: "5432")

    Observação sobre validação das credenciais:
    - A validação atual no construtor verifica a existência do método
      `check_environment_variables` em vez de chamá-lo. Isso parece ser
      um erro lógico (o método não está sendo invocado). Não alterei o
      comportamento original aqui — apenas documentei a intenção.
    """

    def __init__(
        self, db_name=None, db_user=None, db_password=None, db_host=None, db_port="5432"
    ):

        # ATENÇÃO: o código original faz `not self.check_environment_variables` —
        # isso verifica apenas se o atributo/método existe (sempre True), e
        # provavelmente deveria chamar `self.check_environment_variables()`.
        # Não alteramos o comportamento para evitar regressões.
        if (
            not self.check_environment_variables
            and db_name is None
            and db_user is None
            and db_password is None
            and db_host is None
        ):
            raise ValueError("As credenciais do Banco não foram fornecidas.")

        # Usa valores passados por parâmetro ou tenta obter das variáveis de
        # ambiente correspondentes.
        self.db_name = db_name or os.getenv("DB_NAME")
        self.db_user = db_user or os.getenv("DB_USER")
        self.db_password = db_password or os.getenv("DB_PASSWORD")
        self.db_host = db_host or os.getenv("DB_HOST")
        self.db_port = db_port

    def connect(self):
        """Estabelece uma conexão síncrona com o PostgreSQL usando psycopg2.

        Retorna um objeto de conexão se bem-sucedido, ou `None` em caso de erro.
        O método também imprime mensagens de status para facilitar debug
        em execuções locais/pipeline.
        """
        try:
            connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
            )
            print("Conexão bem-sucedida ao banco de dados PostgreSQL.")
            return connection
        except psycopg2.Error as e:
            # Em produção é preferível logar em vez de imprimir
            print(f"Erro ao conectar ao banco de dados PostgreSQL: {e}")
            return None

    def execute_query(self, query):
        """Executa uma consulta SQL que retorna linhas (SELECT).

        Parâmetros:
          query (str): instrução SQL a ser executada.

        Retorna a lista de tuplas com os resultados, ou `None` em caso de erro.
        O método abre uma conexão, cria cursor, busca todos os resultados e
        fecha/commit/fecha a conexão ao final.
        """
        try:
            connection = self.connect()
            if connection:
                cursor = connection.cursor()
                cursor.execute(query)
                result = cursor.fetchall()
                cursor.close()
                connection.commit()
                connection.close()
                return result
            else:
                print("Não foi possível estabelecer a conexão com o banco de dados.")
                return None
        except psycopg2.Error as e:
            print(f"Erro ao executar a consulta SQL: {e}")
            return None

    def execute_insert(self, query, values):
        """Executa uma instrução INSERT/UPDATE com parâmetros.

        Parâmetros:
          query (str): instrução SQL parametrizada (ex: INSERT INTO ... VALUES (%s, %s))
          values (tuple/list): valores a serem vinculados na query

        Não retorna valor; imprime status e captura erros.
        """
        try:
            connection = self.connect()
            if connection:
                cursor = connection.cursor()
                cursor.execute(query, values)
                connection.commit()
                cursor.close()
                connection.close()
                print("Inserção bem-sucedida.")
            else:
                print("Não foi possível estabelecer a conexão com o banco de dados.")
        except psycopg2.Error as e:
            print(f"Erro ao executar a inserção SQL: {e}")

    @staticmethod
    def check_environment_variables():
        """Verifica se as variáveis de ambiente necessárias estão definidas.

        Retorna `True` se todas as variáveis necessárias estiverem presentes,
        `False` caso contrário. Imprime uma mensagem de status.
        """
        if (
            not os.getenv("DB_NAME")
            or not os.getenv("DB_USER")
            or not os.getenv("DB_PASSWORD")
            or not os.getenv("DB_HOST")
        ):
            print("As variáveis de ambiente do banco não estão configuradas.")
            return False
        else:
            print("Variáveis de ambiente para o Banco foram configuradas corretamente.")
            return True

    def alchemy(self):
        """Cria e retorna um engine SQLAlchemy para o banco configurado.

        Uso típico:
          engine = manager.alchemy()
          df.to_sql(..., con=engine)
        """
        self.engine = create_engine(
            f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        )
        return self.engine