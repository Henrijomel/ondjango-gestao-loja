# services/usuario_service.py
from repositories.usuario_repository import UsuarioRepository
from models.usuario import Usuario

class UsuarioService:
    def __init__(self, connection):
        self.repository = UsuarioRepository(connection)

    def criar_usuario(self, usuario: Usuario):
        # Validações de negócio
        if not usuario.email or "@" not in usuario.email:
            raise ValueError("Email inválido.")
        if not usuario.senha or len(usuario.senha) < 6:
            raise ValueError("Senha deve ter pelo menos 6 caracteres.")
        return self.repository.create(usuario)

    def obter_usuario(self, id_usuario):
        return self.repository.read(id_usuario)

    def atualizar_usuario(self, usuario: Usuario):
        if not usuario.nome:
            raise ValueError("Nome é obrigatório.")
        return self.repository.update(usuario)

    def excluir_usuario(self, id_usuario):
        return self.repository.delete(id_usuario)
