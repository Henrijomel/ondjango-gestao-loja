# repositories/relatorio_repository.py
from repositories.base_repository import BaseRepository
from models.relatorio import Relatorio

class RelatorioRepository(BaseRepository):

    def create(self, relatorio: Relatorio):
        try:
            cursor = self.connection.cursor()
            sql = """INSERT INTO relatorios (tipo, data_inicio, data_fim, conteudo) 
                     VALUES (%s, %s, %s, %s)"""
            values = (relatorio.tipo, relatorio.data_inicio, relatorio.data_fim, relatorio.conteudo)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar relatório: {e}")
            return None

    def read(self, id_relatorio):
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT * FROM relatorios WHERE id_relatorio = %s"
            cursor.execute(sql, (id_relatorio,))
            row = cursor.fetchone()
            if row:
                return Relatorio(**row)
            return None
        except Exception as e:
            print(f"Erro ao ler relatório: {e}")
            return None

    def update(self, relatorio: Relatorio):
        try:
            cursor = self.connection.cursor()
            sql = """UPDATE relatorios 
                     SET tipo=%s, data_inicio=%s, data_fim=%s, conteudo=%s 
                     WHERE id_relatorio=%s"""
            values = (relatorio.tipo, relatorio.data_inicio, relatorio.data_fim, relatorio.conteudo, relatorio.id_relatorio)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao atualizar relatório: {e}")
            return None

    def delete(self, id_relatorio):
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM relatorios WHERE id_relatorio=%s"
            cursor.execute(sql, (id_relatorio,))
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao excluir relatório: {e}")
            return None
