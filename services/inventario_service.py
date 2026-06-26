# services/inventario_service.py
from repositories.inventario_repository import InventarioRepository
from repositories.produto_repository import ProdutoRepository
from models.inventario import Inventario

class InventarioService:
    def __init__(self, connection):
        self.inventario_repo = InventarioRepository(connection)
        self.produto_repo = ProdutoRepository(connection)

    def registrar_inventario(self, inventario: Inventario):
        # Validações de negócio
        if not inventario.produto_id:
            raise ValueError("Produto é obrigatório.")
        if inventario.quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa.")

        # Verificar se produto existe
        produto = self.produto_repo.read(inventario.produto_id)
        if not produto:
            raise ValueError(f"Produto {inventario.produto_id} não encontrado.")

        return self.inventario_repo.create(inventario)

    def obter_inventario(self, id_inventario):
        return self.inventario_repo.read(id_inventario)

    def atualizar_inventario(self, inventario: Inventario):
        if inventario.quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa.")
        return self.inventario_repo.update(inventario)

    def excluir_inventario(self, id_inventario):
        return self.inventario_repo.delete(id_inventario)
