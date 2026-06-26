# app.py
from flask import Flask
from controllers.cliente_controller import cliente_bp
from controllers.fornecedor_controller import fornecedor_bp
from controllers.produto_controller import produto_bp
from controllers.compra_controller import compra_bp
from controllers.venda_controller import venda_bp
from controllers.inventario_controller import inventario_bp
from controllers.movimento_stock_controller import movimento_bp
from controllers.relatorio_controller import relatorio_bp
from controllers.configuracao_controller import configuracao_bp

def create_app():
    app = Flask(__name__)

    # Registro dos Blueprints
    app.register_blueprint(cliente_bp, url_prefix="/api")
    app.register_blueprint(fornecedor_bp, url_prefix="/api")
    app.register_blueprint(produto_bp, url_prefix="/api")
    app.register_blueprint(compra_bp, url_prefix="/api")
    app.register_blueprint(venda_bp, url_prefix="/api")
    app.register_blueprint(inventario_bp, url_prefix="/api")
    app.register_blueprint(movimento_bp, url_prefix="/api")
    app.register_blueprint(relatorio_bp, url_prefix="/api")
    app.register_blueprint(configuracao_bp, url_prefix="/api")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
