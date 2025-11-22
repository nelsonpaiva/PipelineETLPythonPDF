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
        