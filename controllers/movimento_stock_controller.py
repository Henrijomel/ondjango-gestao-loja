# controllers/movimento_stock_controller.py
from flask import Blueprint, request, jsonify
from services.movimento_stock_service import MovimentoStockService
from models.movimento_stock import MovimentoStock
from database.connection import DatabaseConnection

# Criar Blueprint para movimentos de stock
movimento_bp = Blueprint("movimento_stock", __name__)

# Instanciar conexão e service
db = DatabaseConnection().connect()
movimento_service = MovimentoStockService(db)

# Rotas
@movimento_bp.route("/movimentos", methods=["POST"])
def registrar_movimento():
    data = request.json
    try:
        movimento = MovimentoStock(
            id_movimento=None,
            produto_id=data.get("produto_id"),
            tipo=data.get("tipo"),  # "entrada" ou "saida"
            quantidade=data.get("quantidade"),
            data=data.get("data")
        )
        id_movimento = movimento_service.registrar_movimento(movimento)
        return jsonify({"message": "Movimento registrado com sucesso", "id": id_movimento}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@movimento_bp.route("/movimentos/<int:id_movimento>", methods=["GET"])
def obter_movimento(id_movimento):
    movimento = movimento_service.obter_movimento(id_movimento)
    if movimento:
        return jsonify(movimento.__dict__), 200
    return jsonify({"error": "Movimento não encontrado"}), 404

@movimento_bp.route("/movimentos/<int:id_movimento>", methods=["PUT"])
def atualizar_movimento(id_movimento):
    data = request.json
    try:
        movimento = MovimentoStock(
            id_movimento=id_movimento,
            produto_id=data.get("produto_id"),
            tipo=data.get("tipo"),
            quantidade=data.get("quantidade"),
            data=data.get("data")
        )
        linhas = movimento_service.atualizar_movimento(movimento)
        if linhas:
            return jsonify({"message": "Movimento atualizado com sucesso"}), 200
        return jsonify({"error": "Movimento não encontrado"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@movimento_bp.route("/movimentos/<int:id_movimento>", methods=["DELETE"])
def excluir_movimento(id_movimento):
    linhas = movimento_service.excluir_movimento(id_movimento)
    if linhas:
        return jsonify({"message": "Movimento excluído com sucesso"}), 200
    return jsonify({"error": "Movimento não encontrado"}), 404
