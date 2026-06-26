# repositories/usuario_repository.py
from repositories.base_repository import BaseRepository
from models.usuario import Usuario

class UsuarioRepository(BaseRepository):

    def create(self, usuario: Usuario):
        try:
            cursor = self.connection.cursor()
            sql = """INSERT INTO usuarios (nome, email, senha, perfil) 
                     VALUES (%s, %s, %s, %s)"""
            values = (usuario.nome, usuario.email, usuario.senha, usuario.perfil)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return None

    def read(self, id_usuario):
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT * FROM usuarios WHERE id_usuario = %s"
            cursor.execute(sql, (id_usuario,))
            row = cursor.fetchone()
            if row:
                return Usuario(**row)
            return None
        except Exception as e:
            print(f"Erro ao ler usuário: {e}")
            return None

    def update(self, usuario: Usuario):
        try:
            cursor = self.connection.cursor()
            sql = """UPDATE usuarios SET nome=%s, email=%s, senha=%s, perfil=%s 
                     WHERE id_usuario=%s"""
            values = (usuario.nome, usuario.email, usuario.senha, usuario.perfil, usuario.id_usuario)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao atualizar usuário: {e}")
            return None

    def delete(self, id_usuario):
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM usuarios WHERE id_usuario=%s"
            cursor.execute(sql, (id_usuario,))
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao excluir usuário: {e}")
            return None
