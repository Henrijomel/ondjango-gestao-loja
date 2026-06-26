# controllers/fornecedor_controller.py
from flask import Blueprint
from services.fornecedor_service import FornecedorService
from models.fornecedor import Fornecedor
from database.connection import DatabaseConnection
from controllers.base_controller import BaseController

# Criar Blueprint para fornecedores
fornecedor_bp = Blueprint("fornecedor", __name__)

# Instanciar conexão e service
db = DatabaseConnection().connect()
fornecedor_service = FornecedorService(db)

# Instanciar controller base
base_controller = BaseController(fornecedor_service, Fornecedor)

# Rotas
@fornecedor_bp.route("/fornecedores", methods=["POST"])
def criar_fornecedor():
    return base_controller.create()

@fornecedor_bp.route("/fornecedores/<int:id_fornecedor>", methods=["GET"])
def obter_fornecedor(id_fornecedor):
    return base_controller.read(id_fornecedor)

@fornecedor_bp.route("/fornecedores/<int:id_fornecedor>", methods=["PUT"])
def atualizar_fornecedor(id_fornecedor):
    return base_controller.update(id_fornecedor)

@fornecedor_bp.route("/fornecedores/<int:id_fornecedor>", methods=["DELETE"])
def excluir_fornecedor(id_fornecedor):
    return base_controller.delete(id_fornecedor)
