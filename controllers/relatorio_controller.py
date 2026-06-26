# controllers/relatorio_controller.py
from flask import Blueprint, request, jsonify
from services.relatorio_service import RelatorioService
from models.relatorio import Relatorio
from database.connection import DatabaseConnection

# Criar Blueprint para relatórios
relatorio_bp = Blueprint("relatorio", __name__)

# Instanciar conexão e service
db = DatabaseConnection().connect()
relatorio_service = RelatorioService(db)

# Rotas
@relatorio_bp.route("/relatorios", methods=["POST"])
def criar_relatorio():
    data = request.json
    try:
        relatorio = Relatorio(
            id_relatorio=None,
            tipo=data.get("tipo"),
            data_inicio=data.get("data_inicio"),
            data_fim=data.get("data_fim"),
            conteudo=data.get("conteudo")
        )
        id_relatorio = relatorio_service.criar_relatorio(relatorio)
        return jsonify({"message": "Relatório criado com sucesso", "id": id_relatorio}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@relatorio_bp.route("/relatorios/<int:id_relatorio>", methods=["GET"])
def obter_relatorio(id_relatorio):
    relatorio = relatorio_service.obter_relatorio(id_relatorio)
    if relatorio:
        return jsonify(relatorio.__dict__), 200
    return jsonify({"error": "Relatório não encontrado"}), 404

@relatorio_bp.route("/relatorios/<int:id_relatorio>", methods=["PUT"])
def atualizar_relatorio(id_relatorio):
    data = request.json
    try:
        relatorio = Relatorio(
            id_relatorio=id_relatorio,
            tipo=data.get("tipo"),
            data_inicio=data.get("data_inicio"),
            data_fim=data.get("data_fim"),
            conteudo=data.get("conteudo")
        )
        linhas = relatorio_service.atualizar_relatorio(relatorio)
        if linhas:
            return jsonify({"message": "Relatório atualizado com sucesso"}), 200
        return jsonify({"error": "Relatório não encontrado"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@relatorio_bp.route("/relatorios/<int:id_relatorio>", methods=["DELETE"])
def excluir_relatorio(id_relatorio):
    linhas = relatorio_service.excluir_relatorio(id_relatorio)
    if linhas:
        return jsonify({"message": "Relatório excluído com sucesso"}), 200
    return jsonify({"error": "Relatório não encontrado"}), 404

@relatorio_bp.route("/relatorios/personalizado", methods=["POST"])
def gerar_relatorio_personalizado():
    data = request.json
    try:
        id_relatorio = relatorio_service.gerar_relatorio_personalizado(
            tipo=data.get("tipo"),
            data_inicio=data.get("data_inicio"),
            data_fim=data.get("data_fim"),
            conteudo=data.get("conteudo")
        )
        return jsonify({"message": "Relatório personalizado gerado com sucesso", "id": id_relatorio}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
