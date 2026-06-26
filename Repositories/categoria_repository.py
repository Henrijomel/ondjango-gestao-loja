# repositories/categoria_repository.py
from repositories.base_repository import BaseRepository
from models.categoria import Categoria

class CategoriaRepository(BaseRepository):

    def create(self, categoria: Categoria):
        try:
            cursor = self.connection.cursor()
            sql = """INSERT INTO categorias (nome, descricao) 
                     VALUES (%s, %s)"""
            values = (categoria.nome, categoria.descricao)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar categoria: {e}")
            return None

    def read(self, id_categoria):
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT * FROM categorias WHERE id_categoria = %s"
            cursor.execute(sql, (id_categoria,))
            row = cursor.fetchone()
            if row:
                return Categoria(**row)
            return None
        except Exception as e:
            print(f"Erro ao ler categoria: {e}")
            return None

    def update(self, categoria: Categoria):
        try:
            cursor = self.connection.cursor()
            sql = """UPDATE categorias SET nome=%s, descricao=%s 
                     WHERE id_categoria=%s"""
            values = (categoria.nome, categoria.descricao, categoria.id_categoria)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao atualizar categoria: {e}")
            return None

    def delete(self, id_categoria):
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM categorias WHERE id_categoria=%s"
            cursor.execute(sql, (id_categoria,))
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao excluir categoria: {e}")
            return None
