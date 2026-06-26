# services/compra_service.py
from repositories.compra_repository import CompraRepository
from repositories.item_compra_repository import ItemCompraRepository
from models.compra import Compra
from models.item_compra import ItemCompra

class CompraService:
    def __init__(self, connection):
        self.compra_repo = CompraRepository(connection)
        self.item_repo = ItemCompraRepository(connection)

    def criar_compra(self, compra: Compra, itens: list[ItemCompra]):
        # Validações de negócio
        if not compra.fornecedor_id:
            raise ValueError("Fornecedor é obrigatório.")
        if not itens or len(itens) == 0:
            raise ValueError("Compra deve ter pelo menos um item.")

        total = 0
        for item in itens:
            if item.quantidade <= 0:
                raise ValueError("Quantidade deve ser maior que zero.")
            if item.preco_unitario <= 0:
                raise ValueError("Preço unitário deve ser maior que zero.")
            total += item.quantidade * item.preco_unitario

        compra.total = total
        id_compra = self.compra_repo.create(compra)

        # Persistir itens vinculados à compra
        for item in itens:
            item.compra_id = id_compra
            self.item_repo.create(item)

        return id_compra

    def obter_compra(self, id_compra):
        return self.compra_repo.read(id_compra)

    def atualizar_compra(self, compra: Compra):
        if not compra.fornecedor_id:
            raise ValueError("Fornecedor é obrigatório.")
        return self.compra_repo.update(compra)

    def excluir_compra(self, id_compra):
        # Primeiro excluir itens vinculados
        # (dependendo da regra de negócio, pode ser necessário manter histórico)
        # Aqui vamos excluir todos os itens antes da compra
        # Nota: poderia ser feito com ON DELETE CASCADE no banco
        # mas mantemos explícito no serviço
        # Buscar itens e excluir
        # Exemplo simplificado:
        # itens = self.item_repo.listar_por_compra(id_compra)
        # for item in itens:
        #     self.item_repo.delete(item.id_item)
        return self.compra_repo.delete(id_compra)
