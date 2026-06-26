# repositories/cliente_repository.py
from repositories.base_repository import BaseRepository
from models.cliente import Cliente

class ClienteRepository(BaseRepository):

    def create(self, cliente: Cliente):
        try:
            cursor = self.connection.cursor()
            sql = """INSERT INTO clientes (nome, email, telefone, endereco) 
                     VALUES (%s, %s, %s, %s)"""
            values = (cliente.nome, cliente.email, cliente.telefone, cliente.endereco)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar cliente: {e}")
            return None

    def read(self, id_cliente):
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT * FROM clientes WHERE id_cliente = %s"
            cursor.execute(sql, (id_cliente,))
            row = cursor.fetchone()
            if row:
                return Cliente(**row)
            return None
        except Exception as e:
            print(f"Erro ao ler cliente: {e}")
            return None

    def update(self, cliente: Cliente):
        try:
            cursor = self.connection.cursor()
            sql = """UPDATE clientes SET nome=%s, email=%s, telefone=%s, endereco=%s 
                     WHERE id_cliente=%s"""
            values = (cliente.nome, cliente.email, cliente.telefone, cliente.endereco, cliente.id_cliente)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao atualizar cliente: {e}")
            return None

    def delete(self, id_cliente):
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM clientes WHERE id_cliente=%s"
            cursor.execute(sql, (id_cliente,))
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao excluir cliente: {e}")
            return None
