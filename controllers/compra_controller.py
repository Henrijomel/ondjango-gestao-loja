# controllers/compra_controller.py
from flask import Blueprint, request, jsonify
from services.compra_service import CompraService
from models.compra import Compra
from models.item_compra import ItemCompra
from database.connection import DatabaseConnection

# Criar Blueprint para compras
compra_bp = Blueprint("compra", __name__)

# Instanciar conexão e service
db = DatabaseConnection().connect()
compra_service = CompraService(db)

# Rotas
@compra_bp.route("/compras", methods=["POST"])
def criar_compra():
    data = request.json
    try:
        compra = Compra(
            id_compra=None,
            fornecedor_id=data.get("fornecedor_id"),
            data=data.get("data"),
            total=0  # calculado no service
        )
        itens = [
            ItemCompra(
                id_item=None,
                compra_id=None,
                produto_id=item.get("produto_id"),
                quantidade=item.get("quantidade"),
                preco_unitario=item.get("preco_unitario")
            )
            for item in data.get("itens", [])
        ]
        id_compra = compra_service.criar_compra(compra, itens)
        return jsonify({"message": "Compra criada com sucesso", "id": id_compra}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@compra_bp.route("/compras/<int:id_compra>", methods=["GET"])
def obter_compra(id_compra):
    compra = compra_service.obter_compra(id_compra)
    if compra:
        return jsonify(compra.__dict__), 200
    return jsonify({"error": "Compra não encontrada"}), 404

@compra_bp.route("/compras/<int:id_compra>", methods=["PUT"])
def atualizar_compra(id_compra):
    data = request.json
    try:
        compra = Compra(
            id_compra=id_compra,
            fornecedor_id=data.get("fornecedor_id"),
            data=data.get("data"),
            total=data.get("total", 0)
        )
        linhas = compra_service.atualizar_compra(compra)
        if linhas:
            return jsonify({"message": "Compra atualizada com sucesso"}), 200
        return jsonify({"error": "Compra não encontrada"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@compra_bp.route("/compras/<int:id_compra>", methods=["DELETE"])
def excluir_compra(id_compra):
    linhas = compra_service.excluir_compra(id_compra)
    if linhas:
        return jsonify({"message": "Compra excluída com sucesso"}), 200
    return jsonify({"error": "Compra não encontrada"}), 404
