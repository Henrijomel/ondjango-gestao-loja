# models/inventario.py
from models.base_model import BaseModel

class Inventario(BaseModel):
    def __init__(self, id_inventario, produto_id, quantidade, data):
        self.id_inventario = id_inventario
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.data = data
