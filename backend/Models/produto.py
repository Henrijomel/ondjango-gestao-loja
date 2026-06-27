# Models/produto.py
"""
Produto Model
Representa um produto da loja Ondjango
"""

from Models.base_model import BaseModel
from typing import Optional, List
from datetime import datetime


class Produto(BaseModel):
    """
    Modelo de Produto
    
    Atributos:
        id_produto (int): Identificador único do produto
        nome (str): Nome do produto
        descricao (str): Descrição detalhada do produto
        categoria_id (int): ID da categoria do produto
        categoria_nome (str): Nome da categoria
        preco_custo (float): Preço de custo
        preco_venda (float): Preço de venda
        margem_lucro (float): Margem de lucro em percentagem
        stock_quantidade (int): Quantidade em stock
        stock_minimo (int): Stock mínimo para alerta
        stock_maximo (int): Stock máximo recomendado
        unidade_medida (str): Unidade de medida (Un, Kg, L, etc)
        codigo_barras (str): Código de barras do produto
        codigo_interno (str): Código interno da loja
        fornecedor_id (int): ID do fornecedor principal
        fornecedor_nome (str): Nome do fornecedor
        peso (float): Peso do produto em kg
        dimensoes (str): Dimensões do produto (L x A x P)
        sku (str): SKU do produto
        ativo (bool): Se o produto está ativo
        data_criacao (datetime): Data de criação
        data_atualizacao (datetime): Data da última atualização
    """

    def __init__(
        self,
        id_produto: Optional[int] = None,
        nome: Optional[str] = None,
        descricao: Optional[str] = None,
        categoria_id: Optional[int] = None,
        categoria_nome: Optional[str] = None,
        preco_custo: Optional[float] = 0.0,
        preco_venda: Optional[float] = 0.0,
        margem_lucro: Optional[float] = 0.0,
        stock_quantidade: Optional[int] = 0,
        stock_minimo: Optional[int] = 0,
        stock_maximo: Optional[int] = 0,
        unidade_medida: Optional[str] = "Un",
        codigo_barras: Optional[str] = None,
        codigo_interno: Optional[str] = None,
        fornecedor_id: Optional[int] = None,
        fornecedor_nome: Optional[str] = None,
        peso: Optional[float] = 0.0,
        dimensoes: Optional[str] = None,
        sku: Optional[str] = None,
        ativo: bool = True,
        **kwargs
    ):
        """
        Inicializar um Produto
        
        Args:
            id_produto (int, optional): ID do produto
            nome (str, optional): Nome do produto
            descricao (str, optional): Descrição do produto
            categoria_id (int, optional): ID da categoria
            categoria_nome (str, optional): Nome da categoria
            preco_custo (float, optional): Preço de custo. Padrão: 0.0
            preco_venda (float, optional): Preço de venda. Padrão: 0.0
            margem_lucro (float, optional): Margem de lucro. Padrão: 0.0
            stock_quantidade (int, optional): Quantidade em stock. Padrão: 0
            stock_minimo (int, optional): Stock mínimo. Padrão: 0
            stock_maximo (int, optional): Stock máximo. Padrão: 0
            unidade_medida (str, optional): Unidade. Padrão: "Un"
            codigo_barras (str, optional): Código de barras
            codigo_interno (str, optional): Código interno
            fornecedor_id (int, optional): ID do fornecedor
            fornecedor_nome (str, optional): Nome do fornecedor
            peso (float, optional): Peso em kg. Padrão: 0.0
            dimensoes (str, optional): Dimensões
            sku (str, optional): SKU do produto
            ativo (bool, optional): Status ativo. Padrão: True
            **kwargs: Atributos adicionais
        """
        super().__init__()

        self.id_produto = id_produto
        self.nome = nome
        self.descricao = descricao
        self.categoria_id = categoria_id
        self.categoria_nome = categoria_nome
        self.preco_custo = preco_custo
        self.preco_venda = preco_venda
        self.margem_lucro = margem_lucro
        self.stock_quantidade = stock_quantidade
        self.stock_minimo = stock_minimo
        self.stock_maximo = stock_maximo
        self.unidade_medida = unidade_medida
        self.codigo_barras = codigo_barras
        self.codigo_interno = codigo_interno
        self.fornecedor_id = fornecedor_id
        self.fornecedor_nome = fornecedor_nome
        self.peso = peso
        self.dimensoes = dimensoes
        self.sku = sku
        self.ativo = ativo

        # Processar argumentos adicionais
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def is_valid(self) -> bool:
        """
        Valida o produto
        
        Returns:
            bool: True se válido
        """
        if not self.nome or not str(self.nome).strip():
            return False
        if self.preco_custo is None or self.preco_custo < 0:
            return False
        if self.preco_venda is None or self.preco_venda < 0:
            return False
        if self.stock_quantidade is None or self.stock_quantidade < 0:
            return False
        return True

    def validate(self) -> List[str]:
        """
        Retorna erros de validação
        
        Returns:
            List[str]: Lista de mensagens de erro
        """
        errors = []

        if not self.nome or not str(self.nome).strip():
            errors.append("Nome do produto é obrigatório")

        if self.preco_custo is None or self.preco_custo < 0:
            errors.append("Preço de custo é obrigatório e deve ser positivo")

        if self.preco_venda is None or self.preco_venda < 0:
            errors.append("Preço de venda é obrigatório e deve ser positivo")

        if self.preco_venda < self.preco_custo:
            errors.append("Preço de venda não pode ser menor que o preço de custo")

        if self.stock_quantidade is None or self.stock_quantidade < 0:
            errors.append("Quantidade em stock deve ser um valor positivo")

        if self.stock_minimo is not None and self.stock_minimo < 0:
            errors.append("Stock mínimo não pode ser negativo")

        if self.stock_maximo is not None and self.stock_maximo < 0:
            errors.append("Stock máximo não pode ser negativo")

        if (self.stock_minimo is not None and self.stock_maximo is not None 
            and self.stock_minimo > self.stock_maximo):
            errors.append("Stock mínimo não pode ser maior que o máximo")

        if self.margem_lucro and (self.margem_lucro < 0 or self.margem_lucro > 100):
            errors.append("Margem de lucro deve estar entre 0 e 100%")

        return errors

    def calcular_margem_lucro(self) -> float:
        """
        Calcula a margem de lucro baseado nos preços
        
        Returns:
            float: Margem de lucro em percentagem
        """
        if self.preco_custo <= 0:
            return 0.0
        
        margem = ((self.preco_venda - self.preco_custo) / self.preco_custo) * 100
        return round(margem, 2)

    def calcular_preco_venda(self, margem_percentagem: float) -> float:
        """
        Calcula o preço de venda baseado numa margem desejada
        
        Args:
            margem_percentagem (float): Margem de lucro desejada em %
            
        Returns:
            float: Preço de venda calculado
        """
        if self.preco_custo <= 0:
            return 0.0
        
        preco = self.preco_custo * (1 + (margem_percentagem / 100))
        return round(preco, 2)

    def calcular_lucro_unitario(self) -> float:
        """
        Calcula o lucro unitário
        
        Returns:
            float: Lucro por unidade
        """
        return round(self.preco_venda - self.preco_custo, 2)

    def calcular_valor_stock(self) -> float:
        """
        Calcula o valor total do stock
        
        Returns:
            float: Valor total do stock
        """
        return round(self.preco_custo * self.stock_quantidade, 2)

    def calcular_valor_stock_venda(self) -> float:
        """
        Calcula o valor de venda do stock
        
        Returns:
            float: Valor de venda do stock
        """
        return round(self.preco_venda * self.stock_quantidade, 2)

    def é_stock_baixo(self) -> bool:
        """
        Verifica se o stock está abaixo do mínimo
        
        Returns:
            bool: True se stock está baixo
        """
        if self.stock_minimo is None or self.stock_minimo == 0:
            return False
        return self.stock_quantidade <= self.stock_minimo

    def é_stock_alto(self) -> bool:
        """
        Verifica se o stock está acima do máximo
        
        Returns:
            bool: True se stock está alto
        """
        if self.stock_maximo is None or self.stock_maximo == 0:
            return False
        return self.stock_quantidade >= self.stock_maximo

    def tem_stock(self, quantidade: int = 1) -> bool:
        """
        Verifica se tem stock disponível
        
        Args:
            quantidade (int): Quantidade a verificar. Padrão: 1
            
        Returns:
            bool: True se tem stock
        """
        return self.stock_quantidade >= quantidade

    def reduzir_stock(self, quantidade: int) -> bool:
        """
        Reduz o stock
        
        Args:
            quantidade (int): Quantidade a reduzir
            
        Returns:
            bool: True se conseguiu reduzir
        """
        if not self.tem_stock(quantidade):
            return False
        
        self.stock_quantidade -= quantidade
        self.updated_at = datetime.now()
        return True

    def aumentar_stock(self, quantidade: int) -> None:
        """
        Aumenta o stock
        
        Args:
            quantidade (int): Quantidade a aumentar
        """
        self.stock_quantidade += quantidade
        self.updated_at = datetime.now()

    def get_status_stock(self) -> str:
        """
        Retorna o status do stock
        
        Returns:
            str: Status (Crítico, Baixo, Normal, Alto)
        """
        if self.é_stock_baixo():
            return "Crítico" if self.stock_quantidade == 0 else "Baixo"
        elif self.é_stock_alto():
            return "Alto"
        else:
            return "Normal"

    def get_info_completa(self) -> dict:
        """
        Retorna informações completas do produto
        
        Returns:
            dict: Dicionário com informações do produto
        """
        return {
            "id": self.id_produto,
            "nome": self.nome,
            "descricao": self.descricao,
            "categoria_id": self.categoria_id,
            "categoria_nome": self.categoria_nome,
            "preco_custo": self.preco_custo,
            "preco_venda": self.preco_venda,
            "margem_lucro": self.calcular_margem_lucro(),
            "lucro_unitario": self.calcular_lucro_unitario(),
            "stock_quantidade": self.stock_quantidade,
            "stock_minimo": self.stock_minimo,
            "stock_maximo": self.stock_maximo,
            "status_stock": self.get_status_stock(),
            "valor_stock": self.calcular_valor_stock(),
            "valor_stock_venda": self.calcular_valor_stock_venda(),
            "unidade_medida": self.unidade_medida,
            "codigo_barras": self.codigo_barras,
            "codigo_interno": self.codigo_interno,
            "sku": self.sku,
            "fornecedor_id": self.fornecedor_id,
            "fornecedor_nome": self.fornecedor_nome,
            "peso": self.peso,
            "dimensoes": self.dimensoes,
            "ativo": self.ativo,
            "data_criacao": self.created_at.isoformat() if self.created_at else None,
            "data_atualizacao": self.updated_at.isoformat() if self.updated_at else None,
        }

    def desativar(self) -> None:
        """Desativa o produto"""
        self.ativo = False
        self.updated_at = datetime.now()

    def ativar(self) -> None:
        """Ativa o produto"""
        self.ativo = True
        self.updated_at = datetime.now()

    def __repr__(self) -> str:
        """Representação em string"""
        return f"Produto(id={self.id_produto}, nome='{self.nome}', preco={self.preco_venda}€)"

    def __str__(self) -> str:
        """String amigável"""
        status = "✓ Ativo" if self.ativo else "✗Inativo"
        stock_status = self.get_status_stock()
        return f"{self.nome} - {self.preco_venda}€ (Stock: {self.stock_quantidade} - {stock_status}) - {status}"
