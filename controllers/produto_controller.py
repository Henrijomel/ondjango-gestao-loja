# controllers/produto_controller.py
from flask import Blueprint
from services.produto_service import ProdutoService
from models.produto import Produto
from database.connection import DatabaseConnection
from controllers.base_controller import BaseController

# Criar Blueprint para produtos
produto_bp = Blueprint("produto", __name__)

# Instanciar conexão e service
db = DatabaseConnection().connect()
produto_service = ProdutoService(db)

# Instanciar controller base
base_controller = BaseController(produto_service, Produto)

# Rotas
@produto_bp.route("/produtos", methods=["POST"])
def criar_produto():
    return base_controller.create()

@produto_bp.route("/produtos/<int:id_produto>", methods=["GET"])
def obter_produto(id_produto):
    return base_controller.read(id_produto)

@produto_bp.route("/produtos/<int:id_produto>", methods=["PUT"])
def atualizar_produto(id_produto):
    return base_controller.update(id_produto)

@produto_bp.route("/produtos/<int:id_produto>", methods=["DELETE"])
def excluir_produto(id_produto):
    return base_controller.delete(id_produto)
