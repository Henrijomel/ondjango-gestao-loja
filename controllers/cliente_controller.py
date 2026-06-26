# controllers/cliente_controller.py
from flask import Blueprint
from services.cliente_service import ClienteService
from models.cliente import Cliente
from database.connection import DatabaseConnection
from controllers.base_controller import BaseController

# Criar Blueprint para clientes
cliente_bp = Blueprint("cliente", __name__)

# Instanciar conexão e service
db = DatabaseConnection().connect()
cliente_service = ClienteService(db)

# Instanciar controller base
base_controller = BaseController(cliente_service, Cliente)

# Rotas
@cliente_bp.route("/clientes", methods=["POST"])
def criar_cliente():
    return base_controller.create()

@cliente_bp.route("/clientes/<int:id_cliente>", methods=["GET"])
def obter_cliente(id_cliente):
    return base_controller.read(id_cliente)

@cliente_bp.route("/clientes/<int:id_cliente>", methods=["PUT"])
def atualizar_cliente(id_cliente):
    return base_controller.update(id_cliente)

@cliente_bp.route("/clientes/<int:id_cliente>", methods=["DELETE"])
def excluir_cliente(id_cliente):
    return base_controller.delete(id_cliente)
