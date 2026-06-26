# repositories/produto_repository.py
from repositories.base_repository import BaseRepository
from models.produto import Produto

class ProdutoRepository(BaseRepository):

    def create(self, produto: Produto):
        try:
            cursor = self.connection.cursor()
            sql = """INSERT INTO produtos (nome, categoria_id, preco, stock) 
                     VALUES (%s, %s, %s, %s)"""
            values = (produto.nome, produto.categoria_id, produto.preco, produto.stock)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar produto: {e}")
            return None

    def read(self, id_produto):
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT * FROM produtos WHERE id_produto = %s"
            cursor.execute(sql, (id_produto,))
            row = cursor.fetchone()
            if row:
                return Produto(**row)
            return None
        except Exception as e:
            print(f"Erro ao ler produto: {e}")
            return None

    def update(self, produto: Produto):
        try:
            cursor = self.connection.cursor()
            sql = """UPDATE produtos SET nome=%s, categoria_id=%s, preco=%s, stock=%s 
                     WHERE id_produto=%s"""
            values = (produto.nome, produto.categoria_id, produto.preco, produto.stock, produto.id_produto)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao atualizar produto: {e}")
            return None

    def delete(self, id_produto):
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM produtos WHERE id_produto=%s"
            cursor.execute(sql, (id_produto,))
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao excluir produto: {e}")
            return None
