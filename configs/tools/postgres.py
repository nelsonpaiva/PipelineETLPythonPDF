#Bloco de importação das bibliotecas
import os
import psycopg2
from sqlalchemy import create_engine

class RDSPostgresSQLManager:
    def __init__(
            self, 
            db_name=None, 
            db_user=None,
            db_password=None,
            db_host=None, 
            db_port="5432"
    ):
        if(
            not self.check_environment_variables
            and db_name is None
            and db_user is None
            and db_password is None
            and db_host is None
        ):
            raise ValueError("As credenciais do Banco de Dados não foram fornecidas")
        
        self.db_name = db_name or os.getenv("DB_NAME")
        self.db_user = db_user or os.getenv("DB_USER")
        self.db_password = db_password or os.getenv("DB_PASSWORD")
        self.db_host = db_host or os.getenv("DB_HOST")
        self.db_port = db_port

    def connect(self):
        try:
            connection = psycopg2.connect(
                dbname = self.db_name,
                user = self.db_user,
                password = self.db_password,
                host = self.db_host,
                port = self.db_port
            )
            print("Conexão bem sucedida com o banco de dados PostgreSQL.")
            return connection
        except psycopg2.Error as e:
            print(f"Erro ao conectar com o banco de dados PostgreSQL: {e}")
            return None
        

        