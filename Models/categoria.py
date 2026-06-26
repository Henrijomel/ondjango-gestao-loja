# models/categoria.py
from models.base_model import BaseModel

class Categoria(BaseModel):
    def __init__(self, id_categoria, nome, descricao=None):
        self.id_categoria = id_categoria
        self.nome = nome
        self.descricao = descricao
