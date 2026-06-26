# models/configuracao.py
from models.base_model import BaseModel

class Configuracao(BaseModel):
    def __init__(self, id_config, chave, valor):
        self.id_config = id_config
        self.chave = chave
        self.valor = valor
