# services/fornecedor_service.py
from repositories.fornecedor_repository import FornecedorRepository
from models.fornecedor import Fornecedor

class FornecedorService:
    def __init__(self, connection):
        self.repository = FornecedorRepository(connection)

    def criar_fornecedor(self, fornecedor: Fornecedor):
        # Validações de negócio
        if not fornecedor.nome or fornecedor.nome.strip() == "":
            raise ValueError("Nome do fornecedor é obrigatório.")
        if not fornecedor.email or "@" not in fornecedor.email:
            raise ValueError("Email inválido.")
        if not fornecedor.telefone or len(fornecedor.telefone) < 9:
            raise ValueError("Telefone inválido.")
        return self.repository.create(fornecedor)

    def obter_fornecedor(self, id_fornecedor):
        return self.repository.read(id_fornecedor)

    def atualizar_fornecedor(self, fornecedor: Fornecedor):
        if not fornecedor.nome:
            raise ValueError("Nome do fornecedor é obrigatório.")
        return self.repository.update(fornecedor)

    def excluir_fornecedor(self, id_fornecedor):
        return self.repository.delete(id_fornecedor)
