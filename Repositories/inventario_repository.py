# repositories/inventario_repository.py
from repositories.base_repository import BaseRepository
from models.inventario import Inventario

class InventarioRepository(BaseRepository):

    def create(self, inventario: Inventario):
        try:
            cursor = self.connection.cursor()
            sql = """INSERT INTO inventario (produto_id, quantidade, data) 
                     VALUES (%s, %s, %s)"""
            values = (inventario.produto_id, inventario.quantidade, inventario.data)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar inventário: {e}")
            return None

    def read(self, id_inventario):
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT * FROM inventario WHERE id_inventario = %s"
            cursor.execute(sql, (id_inventario,))
            row = cursor.fetchone()
            if row:
                return Inventario(**row)
            return None
        except Exception as e:
            print(f"Erro ao ler inventário: {e}")
            return None

    def update(self, inventario: Inventario):
        try:
            cursor = self.connection.cursor()
            sql = """UPDATE inventario 
                     SET produto_id=%s, quantidade=%s, data=%s 
                     WHERE id_inventario=%s"""
            values = (inventario.produto_id, inventario.quantidade, inventario.data, inventario.id_inventario)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao atualizar inventário: {e}")
            return None

    def delete(self, id_inventario):
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM inventario WHERE id_inventario=%s"
            cursor.execute(sql, (id_inventario,))
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao excluir inventário: {e}")
            return None
