# Models/__init__.py
"""
Models Package
Contém todas as classes de modelo (data models) da aplicação
"""

from Models.base_model import BaseModel
from Models.cliente import Cliente
from Models.fornecedor import Fornecedor
from Models.produto import Produto
from Models.categoria import Categoria
from Models.compra import Compra
from Models.item_compra import ItemCompra
from Models.venda import Venda

__all__ = [
    'BaseModel',
    'Cliente',
    'Fornecedor',
    'Produto',
    'Categoria',
    'Compra',
    'ItemCompra',
    'Venda',
]

__version__ = '1.0.0'
__author__ = 'Henrijomel'
__description__ = 'Data models for Ondjango Store Management System'
