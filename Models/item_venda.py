# models/item_venda.py
from models.base_model import BaseModel

class ItemVenda(BaseModel):
    def __init__(self, id_item, venda_id, produto_id, quantidade, preco_unitario):
        self.id_item = id_item
        self.venda_id = venda_id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
