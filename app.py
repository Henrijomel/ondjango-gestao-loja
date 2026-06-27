# app.py
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv

# Importar Blueprints dos Controllers
from controllers.cliente_controller import cliente_bp
from controllers.fornecedor_controller import fornecedor_bp
from controllers.produto_controller import produto_bp
from controllers.compra_controller import compra_bp
from controllers.venda_controller import venda_bp
from controllers.inventario_controller import inventario_bp
from controllers.movimento_stock_controller import movimento_bp
from controllers.relatorio_controller import relatorio_bp
from controllers.configuracao_controller import configuracao_bp

# Carregar variáveis de ambiente
load_dotenv()

def create_app():
    """Factory function para criar a aplicação Flask"""
    
    app = Flask(__name__, 
                static_folder='frontend',
                static_url_path='/',
                template_folder='frontend')
    
    # Configurações
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', True)
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    
    # CORS - Permitir requisições do frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": ["localhost:*", "127.0.0.1:*", "*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Registro dos Blueprints da API
    app.register_blueprint(cliente_bp, url_prefix="/api")
    app.register_blueprint(fornecedor_bp, url_prefix="/api")
    app.register_blueprint(produto_bp, url_prefix="/api")
    app.register_blueprint(compra_bp, url_prefix="/api")
    app.register_blueprint(venda_bp, url_prefix="/api")
    app.register_blueprint(inventario_bp, url_prefix="/api")
    app.register_blueprint(movimento_bp, url_prefix="/api")
    app.register_blueprint(relatorio_bp, url_prefix="/api")
    app.register_blueprint(configuracao_bp, url_prefix="/api")
    
    # ==================== ROTAS DE PÁGINA ====================
    
    @app.route('/')
    def index():
        """Página inicial"""
        return app.send_static_file('index.html')
    
    @app.route('/pages/<page>')
    def page(page):
        """Servir páginas HTML"""
        page_path = f'pages/{page}.html'
        try:
            return app.send_static_file(page_path)
        except:
            return {'error': 'Página não encontrada'}, 404
    
    # ==================== ROTAS DE API ====================
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check da API"""
        return jsonify({
            'status': 'ok',
            'message': 'Servidor Ondjango está funcionando!',
            'timestamp': datetime.now().isoformat()
        }), 200
    
    @app.route('/api/version', methods=['GET'])
    def get_version():
        """Retorna a versão da API"""
        return jsonify({
            'name': 'Ondjango Gestão de Loja',
            'version': '1.0.0',
            'description': 'Plataforma de gestão de stocks, vendas e administração de processos',
            'author': 'Henrijomel',
            'timestamp': datetime.now().isoformat()
        }), 200
    
    @app.route('/api/stats', methods=['GET'])
    def get_stats():
        """Retorna estatísticas gerais do sistema"""
        return jsonify({
            'total_endpoints': 9,
            'database': 'MySQL',
            'framework': 'Flask',
            'version': '1.0.0'
        }), 200
    
    # ==================== TRATAMENTO DE ERROS ====================
    
    @app.errorhandler(404)
    def not_found(error):
        """Erro 404 - Não encontrado"""
        return jsonify({
            'error': 'Recurso não encontrado',
            'message': str(error),
            'status': 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Erro 500 - Erro interno do servidor"""
        return jsonify({
            'error': 'Erro interno do servidor',
            'message': str(error),
            'status': 500
        }), 500
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Erro 405 - Método não permitido"""
        return jsonify({
            'error': 'Método HTTP não permitido',
            'message': str(error),
            'status': 405
        }), 405
    
    # ==================== MIDDLEWARE ====================
    
    @app.before_request
    def before_request():
        """Executar antes de cada requisição"""
        # Você pode adicionar validações de autenticação aqui
        pass
    
    @app.after_request
    def after_request(response):
        """Executar após cada requisição"""
        # Adicionar headers de segurança
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
    
    # ==================== CONTEXT PROCESSORS ====================
    
    @app.context_processor
    def inject_app_info():
        """Injeta informações da app nos templates"""
        return {
            'app_name': 'Ondjango - Gestão de Loja',
            'version': '1.0.0',
            'year': datetime.now().year
        }
    
    return app


if __name__ == "__main__":
    app = create_app()
    
    # Configurações de execução
    debug_mode = os.getenv('FLASK_DEBUG', True)
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print(f"""
    ╔════════════════════════════════════════╗
    ║     Ondjango - Gestão de Loja         ║
    ║          v1.0.0                        ║
    ╚════════════════════════════════════════╝
    
    🚀 Servidor iniciado:
       URL: http://{host}:{port}
       Debug: {debug_mode}
       Ambiente: {'Desenvolvimento' if debug_mode else 'Produção'}
    
    📍 Endpoints disponíveis:
       - GET  /api/health         Health check
       - GET  /api/version        Versão da API
       - GET  /api/stats          Estatísticas
       - GET  /api/clientes       Listar clientes
       - POST /api/clientes       Criar cliente
       ... (e mais endpoints)
    
    ✅ Use Ctrl+C para parar o servidor
    """)
    
    app.run(
        host=host,
        port=port,
        debug=debug_mode,
        use_reloader=True
    )
