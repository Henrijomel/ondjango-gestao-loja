# services/cliente_service.py
from repositories.cliente_repository import ClienteRepository
from models.cliente import Cliente

class ClienteService:
    def __init__(self, connection):
        self.repository = ClienteRepository(connection)

    def criar_cliente(self, cliente: Cliente):
        # Validações de negócio
        if not cliente.nome or cliente.nome.strip() == "":
            raise ValueError("Nome é obrigatório.")
        if not cliente.email or "@" not in cliente.email:
            raise ValueError("Email inválido.")
        if not cliente.telefone or len(cliente.telefone) < 9:
            raise ValueError("Telefone inválido.")
        return self.repository.create(cliente)

    def obter_cliente(self, id_cliente):
        return self.repository.read(id_cliente)

    def atualizar_cliente(self, cliente: Cliente):
        if not cliente.nome:
            raise ValueError("Nome é obrigatório.")
        return self.repository.update(cliente)

    def excluir_cliente(self, id_cliente):
        return self.repository.delete(id_cliente)
