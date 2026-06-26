# models/cliente.py
from models.base_model import BaseModel

class Cliente(BaseModel):
    def __init__(self, id_cliente, nome, email, telefone, endereco):
        self.id_cliente = id_cliente
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
