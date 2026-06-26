# services/relatorio_service.py
from repositories.relatorio_repository import RelatorioRepository
from models.relatorio import Relatorio

class RelatorioService:
    def __init__(self, connection):
        self.repository = RelatorioRepository(connection)

    def criar_relatorio(self, relatorio: Relatorio):
        # Validações de negócio
        if not relatorio.tipo or relatorio.tipo.strip() == "":
            raise ValueError("Tipo de relatório é obrigatório.")
        if not relatorio.data_inicio or not relatorio.data_fim:
            raise ValueError("Datas de início e fim são obrigatórias.")
        if relatorio.data_inicio > relatorio.data_fim:
            raise ValueError("Data de início não pode ser posterior à data de fim.")
        return self.repository.create(relatorio)

    def obter_relatorio(self, id_relatorio):
        return self.repository.read(id_relatorio)

    def atualizar_relatorio(self, relatorio: Relatorio):
        if not relatorio.tipo:
            raise ValueError("Tipo de relatório é obrigatório.")
        return self.repository.update(relatorio)

    def excluir_relatorio(self, id_relatorio):
        return self.repository.delete(id_relatorio)

    def gerar_relatorio_personalizado(self, tipo: str, data_inicio, data_fim, conteudo: str):
        # Método auxiliar para criar relatórios rapidamente
        relatorio = Relatorio(
            id_relatorio=None,
            tipo=tipo,
            data_inicio=data_inicio,
            data_fim=data_fim,
            conteudo=conteudo
        )
        return self.criar_relatorio(relatorio)
