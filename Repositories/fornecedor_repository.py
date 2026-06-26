# repositories/fornecedor_repository.py
from repositories.base_repository import BaseRepository
from models.fornecedor import Fornecedor

class FornecedorRepository(BaseRepository):

    def create(self, fornecedor: Fornecedor):
        try:
            cursor = self.connection.cursor()
            sql = """INSERT INTO fornecedores (nome, email, telefone, endereco) 
                     VALUES (%s, %s, %s, %s)"""
            values = (fornecedor.nome, fornecedor.email, fornecedor.telefone, fornecedor.endereco)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar fornecedor: {e}")
            return None

    def read(self, id_fornecedor):
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT * FROM fornecedores WHERE id_fornecedor = %s"
            cursor.execute(sql, (id_fornecedor,))
            row = cursor.fetchone()
            if row:
                return Fornecedor(**row)
            return None
        except Exception as e:
            print(f"Erro ao ler fornecedor: {e}")
            return None

    def update(self, fornecedor: Fornecedor):
        try:
            cursor = self.connection.cursor()
            sql = """UPDATE fornecedores SET nome=%s, email=%s, telefone=%s, endereco=%s 
                     WHERE id_fornecedor=%s"""
            values = (fornecedor.nome, fornecedor.email, fornecedor.telefone, fornecedor.endereco, fornecedor.id_fornecedor)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao atualizar fornecedor: {e}")
            return None

    def delete(self, id_fornecedor):
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM fornecedores WHERE id_fornecedor=%s"
            cursor.execute(sql, (id_fornecedor,))
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao excluir fornecedor: {e}")
            return None
