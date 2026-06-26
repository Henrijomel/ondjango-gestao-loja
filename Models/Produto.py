# models/produto.py
from models.base_model import BaseModel

class Produto(BaseModel):
    def __init__(self, id_produto, nome, categoria_id, preco, stock):
        self.id_produto = id_produto
        self.nome = nome
        self.categoria_id = categoria_id
        self.preco = preco
        self.stock = stock

