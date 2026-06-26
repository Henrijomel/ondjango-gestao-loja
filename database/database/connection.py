# database/connection.py
import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self, host="localhost", database="gestao_loja", user="root", password=""):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Conexão estabelecida com sucesso ao MySQL.")
                return self.connection
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexão encerrada com MySQL.")
