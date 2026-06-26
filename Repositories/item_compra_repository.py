# repositories/item_compra_repository.py
from repositories.base_repository import BaseRepository
from models.item_compra import ItemCompra

class ItemCompraRepository(BaseRepository):

    def create(self, item: ItemCompra):
        try:
            cursor = self.connection.cursor()
            sql = """INSERT INTO itens_compra (compra_id, produto_id, quantidade, preco_unitario) 
                     VALUES (%s, %s, %s, %s)"""
            values = (item.compra_id, item.produto_id, item.quantidade, item.preco_unitario)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar item de compra: {e}")
            return None

    def read(self, id_item):
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT * FROM itens_compra WHERE id_item = %s"
            cursor.execute(sql, (id_item,))
            row = cursor.fetchone()
            if row:
                return ItemCompra(**row)
            return None
        except Exception as e:
            print(f"Erro ao ler item de compra: {e}")
            return None

    def update(self, item: ItemCompra):
        try:
            cursor = self.connection.cursor()
            sql = """UPDATE itens_compra 
                     SET compra_id=%s, produto_id=%s, quantidade=%s, preco_unitario=%s 
                     WHERE id_item=%s"""
            values = (item.compra_id, item.produto_id, item.quantidade, item.preco_unitario, item.id_item)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao atualizar item de compra: {e}")
            return None

    def delete(self, id_item):
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM itens_compra WHERE id_item=%s"
            cursor.execute(sql, (id_item,))
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao excluir item de compra: {e}")
            return None
