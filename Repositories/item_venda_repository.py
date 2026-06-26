# repositories/item_venda_repository.py
from repositories.base_repository import BaseRepository
from models.item_venda import ItemVenda

class ItemVendaRepository(BaseRepository):

    def create(self, item: ItemVenda):
        try:
            cursor = self.connection.cursor()
            sql = """INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario) 
                     VALUES (%s, %s, %s, %s)"""
            values = (item.venda_id, item.produto_id, item.quantidade, item.preco_unitario)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar item de venda: {e}")
            return None

    def read(self, id_item):
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT * FROM itens_venda WHERE id_item = %s"
            cursor.execute(sql, (id_item,))
            row = cursor.fetchone()
            if row:
                return ItemVenda(**row)
            return None
        except Exception as e:
            print(f"Erro ao ler item de venda: {e}")
            return None

    def update(self, item: ItemVenda):
        try:
            cursor = self.connection.cursor()
            sql = """UPDATE itens_venda 
                     SET venda_id=%s, produto_id=%s, quantidade=%s, preco_unitario=%s 
                     WHERE id_item=%s"""
            values = (item.venda_id, item.produto_id, item.quantidade, item.preco_unitario, item.id_item)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao atualizar item de venda: {e}")
            return None

    def delete(self, id_item):
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM itens_venda WHERE id_item=%s"
            cursor.execute(sql, (id_item,))
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao excluir item de venda: {e}")
            return None
