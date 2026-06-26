# repositories/compra_repository.py
from repositories.base_repository import BaseRepository
from models.compra import Compra

class CompraRepository(BaseRepository):

    def create(self, compra: Compra):
        try:
            cursor = self.connection.cursor()
            sql = """INSERT INTO compras (fornecedor_id, data, total) 
                     VALUES (%s, %s, %s)"""
            values = (compra.fornecedor_id, compra.data, compra.total)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar compra: {e}")
            return None

    def read(self, id_compra):
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT * FROM compras WHERE id_compra = %s"
            cursor.execute(sql, (id_compra,))
            row = cursor.fetchone()
            if row:
                return Compra(**row)
            return None
        except Exception as e:
            print(f"Erro ao ler compra: {e}")
            return None

    def update(self, compra: Compra):
        try:
            cursor = self.connection.cursor()
            sql = """UPDATE compras SET fornecedor_id=%s, data=%s, total=%s 
                     WHERE id_compra=%s"""
            values = (compra.fornecedor_id, compra.data, compra.total, compra.id_compra)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao atualizar compra: {e}")
            return None

    def delete(self, id_compra):
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM compras WHERE id_compra=%s"
            cursor.execute(sql, (id_compra,))
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao excluir compra: {e}")
            return None
