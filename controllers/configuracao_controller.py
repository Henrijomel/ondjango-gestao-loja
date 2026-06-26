# controllers/configuracao_controller.py
from flask import Blueprint, request, jsonify
from services.configuracao_service import ConfiguracaoService
from models.configuracao import Configuracao
from database.connection import DatabaseConnection

# Criar Blueprint para configurações
configuracao_bp = Blueprint("configuracao", __name__)

# Instanciar conexão e service
db = DatabaseConnection().connect()
configuracao_service = ConfiguracaoService(db)

# Rotas
@configuracao_bp.route("/configuracoes", methods=["POST"])
def criar_configuracao():
    data = request.json
    try:
        config = Configuracao(
            id_config=None,
            chave=data.get("chave"),
            valor=data.get("valor")
        )
        id_config = configuracao_service.criar_configuracao(config)
        return jsonify({"message": "Configuração criada com sucesso", "id": id_config}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@configuracao_bp.route("/configuracoes/<int:id_config>", methods=["GET"])
def obter_configuracao(id_config):
    config = configuracao_service.obter_configuracao(id_config)
    if config:
        return jsonify(config.__dict__), 200
    return jsonify({"error": "Configuração não encontrada"}), 404

@configuracao_bp.route("/configuracoes/<int:id_config>", methods=["PUT"])
def atualizar_configuracao(id_config):
    data = request.json
    try:
        config = Configuracao(
            id_config=id_config,
            chave=data.get("chave"),
            valor=data.get("valor")
        )
        linhas = configuracao_service.atualizar_configuracao(config)
        if linhas:
            return jsonify({"message": "Configuração atualizada com sucesso"}), 200
        return jsonify({"error": "Configuração não encontrada"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@configuracao_bp.route("/configuracoes/<int:id_config>", methods=["DELETE"])
def excluir_configuracao(id_config):
    linhas = configuracao_service.excluir_configuracao(id_config)
    if linhas:
        return jsonify({"message": "Configuração excluída com sucesso"}), 200
    return jsonify({"error": "Configuração não encontrada"}), 404
