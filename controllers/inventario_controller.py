# controllers/inventario_controller.py
from flask import Blueprint, request, jsonify
from services.inventario_service import InventarioService
from models.inventario import Inventario
from database.connection import DatabaseConnection

# Criar Blueprint para inventário
inventario_bp = Blueprint("inventario", __name__)

# Instanciar conexão e service
db = DatabaseConnection().connect()
inventario_service = InventarioService(db)

# Rotas
@inventario_bp.route("/inventario", methods=["POST"])
def registrar_inventario():
    data = request.json
    try:
        inventario = Inventario(
            id_inventario=None,
            produto_id=data.get("produto_id"),
            quantidade=data.get("quantidade"),
            data=data.get("data")
        )
        id_inventario = inventario_service.registrar_inventario(inventario)
        return jsonify({"message": "Inventário registrado com sucesso", "id": id_inventario}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@inventario_bp.route("/inventario/<int:id_inventario>", methods=["GET"])
def obter_inventario(id_inventario):
    inventario = inventario_service.obter_inventario(id_inventario)
    if inventario:
        return jsonify(inventario.__dict__), 200
    return jsonify({"error": "Inventário não encontrado"}), 404

@inventario_bp.route("/inventario/<int:id_inventario>", methods=["PUT"])
def atualizar_inventario(id_inventario):
    data = request.json
    try:
        inventario = Inventario(
            id_inventario=id_inventario,
            produto_id=data.get("produto_id"),
            quantidade=data.get("quantidade"),
            data=data.get("data")
        )
        linhas = inventario_service.atualizar_inventario(inventario)
        if linhas:
            return jsonify({"message": "Inventário atualizado com sucesso"}), 200
        return jsonify({"error": "Inventário não encontrado"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@inventario_bp.route("/inventario/<int:id_inventario>", methods=["DELETE"])
def excluir_inventario(id_inventario):
    linhas = inventario_service.excluir_inventario(id_inventario)
    if linhas:
        return jsonify({"message": "Inventário excluído com sucesso"}), 200
    return jsonify({"error": "Inventário não encontrado"}), 404
