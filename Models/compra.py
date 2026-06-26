# models/compra.py
from models.base_model import BaseModel

class Compra(BaseModel):
    def __init__(self, id_compra, fornecedor_id, data, total):
        self.id_compra = id_compra
        self.fornecedor_id = fornecedor_id
        self.data = data
        self.total = total
