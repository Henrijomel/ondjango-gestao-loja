# models/venda.py
from models.base_model import BaseModel

class Venda(BaseModel):
    def __init__(self, id_venda, cliente_id, data, total):
        self.id_venda = id_venda
        self.cliente_id = cliente_id
        self.data = data
        self.total = total
