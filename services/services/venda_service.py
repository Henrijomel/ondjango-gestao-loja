# services/venda_service.py
from repositories.venda_repository import VendaRepository
from repositories.item_venda_repository import ItemVendaRepository
from repositories.produto_repository import ProdutoRepository
from models.venda import Venda
from models.item_venda import ItemVenda

class VendaService:
    def __init__(self, connection):
        self.venda_repo = VendaRepository(connection)
        self.item_repo = ItemVendaRepository(connection)
        self.produto_repo = ProdutoRepository(connection)

    def criar_venda(self, venda: Venda, itens: list[ItemVenda]):
        # Validações de negócio
        if not venda.cliente_id:
            raise ValueError("Cliente é obrigatório.")
        if not itens or len(itens) == 0:
            raise ValueError("Venda deve ter pelo menos um item.")

        total = 0
        for item in itens:
            if item.quantidade <= 0:
                raise ValueError("Quantidade deve ser maior que zero.")
            if item.preco_unitario <= 0:
                raise ValueError("Preço unitário deve ser maior que zero.")

            # Verificar stock disponível
            produto = self.produto_repo.read(item.produto_id)
            if not produto:
                raise ValueError(f"Produto {item.produto_id} não encontrado.")
            if produto.stock < item.quantidade:
                raise ValueError(f"Stock insuficiente para o produto {produto.nome}.")

            total += item.quantidade * item.preco_unitario

        venda.total = total
        id_venda = self.venda_repo.create(venda)

        # Persistir itens vinculados à venda e atualizar stock
        for item in itens:
            item.venda_id = id_venda
            self.item_repo.create(item)

            # Atualizar stock do produto
            produto = self.produto_repo.read(item.produto_id)
            produto.stock -= item.quantidade
            self.produto_repo.update(produto)

        return id_venda

    def obter_venda(self, id_venda):
        return self.venda_repo.read(id_venda)

    def atualizar_venda(self, venda: Venda):
        if not venda.cliente_id:
            raise ValueError("Cliente é obrigatório.")
        return self.venda_repo.update(venda)

    def excluir_venda(self, id_venda):
        # Dependendo da regra de negócio, pode ser necessário restaurar stock
        # Aqui simplificamos apenas para excluir a venda
        return self.venda_repo.delete(id_venda)
