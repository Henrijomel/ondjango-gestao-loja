# services/produto_service.py
from repositories.produto_repository import ProdutoRepository
from models.produto import Produto

class ProdutoService:
    def __init__(self, connection):
        self.repository = ProdutoRepository(connection)

    def criar_produto(self, produto: Produto):
        if produto.preco <= 0:
            raise ValueError("Preço deve ser maior que zero.")
        if produto.stock < 0:
            raise ValueError("Stock não pode ser negativo.")
        return self.repository.create(produto)

    def obter_produto(self, id_produto):
        return self.repository.read(id_produto)

    def atualizar_produto(self, produto: Produto):
        if not produto.nome:
            raise ValueError("Nome do produto é obrigatório.")
        return self.repository.update(produto)

    def excluir_produto(self, id_produto):
        return self.repository.delete(id_produto)
