# models/relatorio.py
from models.base_model import BaseModel

class Relatorio(BaseModel):
    def __init__(self, id_relatorio, tipo, data_inicio, data_fim, conteudo):
        self.id_relatorio = id_relatorio
        self.tipo = tipo
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.conteudo = conteudo
