# models/usuario.py
from models.base_model import BaseModel

class Usuario(BaseModel):
    def __init__(self, id_usuario, nome, email, senha, perfil):
        self.id_usuario = id_usuario
        self.nome = nome
        self.email = email
        self.senha = senha
        self.perfil = perfil  # admin, operador, etc.
