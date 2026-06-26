# repositories/movimento_stock_repository.py
from repositories.base_repository import BaseRepository
from models.movimento_stock import MovimentoStock

class MovimentoStockRepository(BaseRepository):

    def create(self, movimento: MovimentoStock):
        try:
            cursor = self.connection.cursor()
            sql = """INSERT INTO movimentos_stock (produto_id, tipo, quantidade, data) 
                     VALUES (%s, %s, %s, %s)"""
            values = (movimento.produto_id, movimento.tipo, movimento.quantidade, movimento.data)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar movimento de stock: {e}")
            return None

    def read(self, id_movimento):
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT * FROM movimentos_stock WHERE id_movimento = %s"
            cursor.execute(sql, (id_movimento,))
            row = cursor.fetchone()
            if row:
                return MovimentoStock(**row)
            return None
        except Exception as e:
            print(f"Erro ao ler movimento de stock: {e}")
            return None

    def update(self, movimento: MovimentoStock):
        try:
            cursor = self.connection.cursor()
            sql = """UPDATE movimentos_stock 
                     SET produto_id=%s, tipo=%s, quantidade=%s, data=%s 
                     WHERE id_movimento=%s"""
            values = (movimento.produto_id, movimento.tipo, movimento.quantidade, movimento.data, movimento.id_movimento)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao atualizar movimento de stock: {e}")
            return None

    def delete(self, id_movimento):
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM movimentos_stock WHERE id_movimento=%s"
            cursor.execute(sql, (id_movimento,))
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao excluir movimento de stock: {e}")
            return None
