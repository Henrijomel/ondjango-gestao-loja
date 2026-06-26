# models/item_compra.py
from models.base_model import BaseModel

class ItemCompra(BaseModel):
    def __init__(self, id_item, compra_id, produto_id, quantidade, preco_unitario):
        self.id_item = id_item
        self.compra_id = compra_id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
