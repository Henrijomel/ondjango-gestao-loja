# services/configuracao_service.py
from repositories.configuracao_repository import ConfiguracaoRepository
from models.configuracao import Configuracao

class ConfiguracaoService:
    def __init__(self, connection):
        self.repository = ConfiguracaoRepository(connection)

    def criar_configuracao(self, config: Configuracao):
        # Validações de negócio
        if not config.chave or config.chave.strip() == "":
            raise ValueError("Chave da configuração é obrigatória.")
        if config.valor is None or str(config.valor).strip() == "":
            raise ValueError("Valor da configuração é obrigatório.")
        return self.repository.create(config)

    def obter_configuracao(self, id_config):
        return self.repository.read(id_config)

    def atualizar_configuracao(self, config: Configuracao):
        if not config.chave:
            raise ValueError("Chave da configuração é obrigatória.")
        if config.valor is None or str(config.valor).strip() == "":
            raise ValueError("Valor da configuração é obrigatório.")
        return self.repository.update(config)

    def excluir_configuracao(self, id_config):
        return self.repository.delete(id_config)
