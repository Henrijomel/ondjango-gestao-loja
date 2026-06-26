# models/movimento_stock.py
from models.base_model import BaseModel

class MovimentoStock(BaseModel):
    def __init__(self, id_movimento, produto_id, tipo, quantidade, data):
        self.id_movimento = id_movimento
        self.produto_id = produto_id
        self.tipo = tipo  # entrada ou saída
        self.quantidade = quantidade
        self.data = data
