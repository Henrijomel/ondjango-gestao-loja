# models/fornecedor.py
from models.base_model import BaseModel

class Fornecedor(BaseModel):
    def __init__(self, id_fornecedor, nome, email, telefone, endereco):
        self.id_fornecedor = id_fornecedor
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
