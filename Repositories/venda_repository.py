# repositories/venda_repository.py
from repositories.base_repository import BaseRepository
from models.venda import Venda

class VendaRepository(BaseRepository):

    def create(self, venda: Venda):
        try:
            cursor = self.connection.cursor()
            sql = """INSERT INTO vendas (cliente_id, data, total) 
                     VALUES (%s, %s, %s)"""
            values = (venda.cliente_id, venda.data, venda.total)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar venda: {e}")
            return None

    def read(self, id_venda):
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT * FROM vendas WHERE id_venda = %s"
            cursor.execute(sql, (id_venda,))
            row = cursor.fetchone()
            if row:
                return Venda(**row)
            return None
        except Exception as e:
            print(f"Erro ao ler venda: {e}")
            return None

    def update(self, venda: Venda):
        try:
            cursor = self.connection.cursor()
            sql = """UPDATE vendas SET cliente_id=%s, data=%s, total=%s 
                     WHERE id_venda=%s"""
            values = (venda.cliente_id, venda.data, venda.total, venda.id_venda)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao atualizar venda: {e}")
            return None

    def delete(self, id_venda):
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM vendas WHERE id_venda=%s"
            cursor.execute(sql, (id_venda,))
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao excluir venda: {e}")
            return None
