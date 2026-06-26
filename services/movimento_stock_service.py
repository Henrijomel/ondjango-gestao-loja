# services/movimento_stock_service.py
from repositories.movimento_stock_repository import MovimentoStockRepository
from repositories.produto_repository import ProdutoRepository
from models.movimento_stock import MovimentoStock

class MovimentoStockService:
    def __init__(self, connection):
        self.movimento_repo = MovimentoStockRepository(connection)
        self.produto_repo = ProdutoRepository(connection)

    def registrar_movimento(self, movimento: MovimentoStock):
        # Validações de negócio
        if not movimento.produto_id:
            raise ValueError("Produto é obrigatório.")
        if movimento.quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero.")
        if movimento.tipo not in ["entrada", "saida"]:
            raise ValueError("Tipo de movimento inválido. Use 'entrada' ou 'saida'.")

        # Verificar se produto existe
        produto = self.produto_repo.read(movimento.produto_id)
        if not produto:
            raise ValueError(f"Produto {movimento.produto_id} não encontrado.")

        # Atualizar stock conforme tipo
        if movimento.tipo == "entrada":
            produto.stock += movimento.quantidade
        elif movimento.tipo == "saida":
            if produto.stock < movimento.quantidade:
                raise ValueError(f"Stock insuficiente para saída do produto {produto.nome}.")
            produto.stock -= movimento.quantidade

        # Persistir movimento e atualizar produto
        id_movimento = self.movimento_repo.create(movimento)
        self.produto_repo.update(produto)

        return id_movimento

    def obter_movimento(self, id_movimento):
        return self.movimento_repo.read(id_movimento)

    def atualizar_movimento(self, movimento: MovimentoStock):
        # Nota: atualizar movimento pode ser delicado, pois afeta stock.
        # Dependendo da regra de negócio, pode ser proibido ou exigir auditoria.
        return self.movimento_repo.update(movimento)

    def excluir_movimento(self, id_movimento):
        # Atenção: excluir movimento não restaura stock automaticamente.
        # Dependendo da regra de negócio, pode ser necessário reverter o efeito.
        return self.movimento_repo.delete(id_movimento)
