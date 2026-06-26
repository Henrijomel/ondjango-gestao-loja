# repositories/configuracao_repository.py
from repositories.base_repository import BaseRepository
from models.configuracao import Configuracao

class ConfiguracaoRepository(BaseRepository):

    def create(self, config: Configuracao):
        try:
            cursor = self.connection.cursor()
            sql = """INSERT INTO configuracoes (chave, valor) 
                     VALUES (%s, %s)"""
            values = (config.chave, config.valor)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar configuração: {e}")
            return None

    def read(self, id_config):
        try:
            cursor = self.connection.cursor(dictionary=True)
            sql = "SELECT * FROM configuracoes WHERE id_config = %s"
            cursor.execute(sql, (id_config,))
            row = cursor.fetchone()
            if row:
                return Configuracao(**row)
            return None
        except Exception as e:
            print(f"Erro ao ler configuração: {e}")
            return None

    def update(self, config: Configuracao):
        try:
            cursor = self.connection.cursor()
            sql = """UPDATE configuracoes SET chave=%s, valor=%s 
                     WHERE id_config=%s"""
            values = (config.chave, config.valor, config.id_config)
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao atualizar configuração: {e}")
            return None

    def delete(self, id_config):
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM configuracoes WHERE id_config=%s"
            cursor.execute(sql, (id_config,))
            self.connection.commit()
            return cursor.rowcount
        except Exception as e:
            print(f"Erro ao excluir configuração: {e}")
            return None
