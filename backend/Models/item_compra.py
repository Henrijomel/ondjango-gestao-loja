# Models/item_compra.py
"""
ItemCompra Model
Representa um item individual dentro de uma compra
"""

from Models.base_model import BaseModel
from typing import Optional, List
from datetime import datetime


class ItemCompra(BaseModel):
    """
    Modelo de Item de Compra
    
    Atributos:
        id_item_compra (int): Identificador único do item
        compra_id (int): ID da compra a que pertence
        produto_id (int): ID do produto
        produto_nome (str): Nome do produto
        produto_codigo (str): Código do produto
        quantidade (int): Quantidade do item
        preco_unitario (float): Preço unitário
        desconto_item (float): Desconto específico do item
        valor_total_item (float): Valor total do item
        quantidade_recebida (int): Quantidade já recebida
        quantidade_pendente (int): Quantidade ainda a receber
        unidade_medida (str): Unidade de medida
        observacoes (str): Observações sobre o item
        data_criacao (datetime): Data de criação
        data_atualizacao (datetime): Data da última atualização
    """

    def __init__(
        self,
        id_item_compra: Optional[int] = None,
        compra_id: Optional[int] = None,
        produto_id: Optional[int] = None,
        produto_nome: Optional[str] = None,
        produto_codigo: Optional[str] = None,
        quantidade: Optional[int] = 1,
        preco_unitario: Optional[float] = 0.0,
        desconto_item: Optional[float] = 0.0,
        valor_total_item: Optional[float] = 0.0,
        quantidade_recebida: Optional[int] = 0,
        quantidade_pendente: Optional[int] = None,
        unidade_medida: Optional[str] = "Un",
        observacoes: Optional[str] = None,
        **kwargs
    ):
        """
        Inicializar um Item de Compra
        
        Args:
            id_item_compra (int, optional): ID do item
            compra_id (int, optional): ID da compra
            produto_id (int, optional): ID do produto
            produto_nome (str, optional): Nome do produto
            produto_codigo (str, optional): Código do produto
            quantidade (int, optional): Quantidade. Padrão: 1
            preco_unitario (float, optional): Preço unitário. Padrão: 0.0
            desconto_item (float, optional): Desconto. Padrão: 0.0
            valor_total_item (float, optional): Valor total. Padrão: 0.0
            quantidade_recebida (int, optional): Recebida. Padrão: 0
            quantidade_pendente (int, optional): Pendente
            unidade_medida (str, optional): Unidade. Padrão: "Un"
            observacoes (str, optional): Observações
            **kwargs: Atributos adicionais
        """
        super().__init__()

        self.id_item_compra = id_item_compra
        self.compra_id = compra_id
        self.produto_id = produto_id
        self.produto_nome = produto_nome
        self.produto_codigo = produto_codigo
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.desconto_item = desconto_item
        self.valor_total_item = valor_total_item or (quantidade * preco_unitario - desconto_item)
        self.quantidade_recebida = quantidade_recebida
        self.quantidade_pendente = quantidade_pendente or (quantidade - quantidade_recebida)
        self.unidade_medida = unidade_medida
        self.observacoes = observacoes

        # Processar argumentos adicionais
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def is_valid(self) -> bool:
        """
        Valida o item de compra
        
        Returns:
            bool: True se válido
        """
        if not self.compra_id:
            return False
        if not self.produto_id:
            return False
        if self.quantidade is None or self.quantidade <= 0:
            return False
        if self.preco_unitario is None or self.preco_unitario < 0:
            return False
        return True

    def validate(self) -> List[str]:
        """
        Retorna erros de validação
        
        Returns:
            List[str]: Lista de mensagens de erro
        """
        errors = []

        if not self.compra_id:
            errors.append("Compra é obrigatória")

        if not self.produto_id:
            errors.append("Produto é obrigatório")

        if self.quantidade is None or self.quantidade <= 0:
            errors.append("Quantidade deve ser maior que zero")

        if self.preco_unitario is None or self.preco_unitario < 0:
            errors.append("Preço unitário é obrigatório e deve ser positivo")

        if self.desconto_item and self.desconto_item < 0:
            errors.append("Desconto não pode ser negativo")

        if self.quantidade_recebida and self.quantidade_recebida < 0:
            errors.append("Quantidade recebida não pode ser negativa")

        if (self.quantidade_recebida is not None and 
            self.quantidade_recebida > self.quantidade):
            errors.append("Quantidade recebida não pode ser maior que a quantidade pedida")

        return errors

    def calcular_subtotal(self) -> float:
        """
        Calcula o subtotal do item (sem desconto)
        
        Returns:
            float: Subtotal
        """
        return round(self.quantidade * self.preco_unitario, 2)

    def calcular_valor_total(self) -> float:
        """
        Calcula o valor total do item (com desconto)
        
        Returns:
            float: Valor total
        """
        subtotal = self.calcular_subtotal()
        self.valor_total_item = subtotal - (self.desconto_item or 0)
        return round(self.valor_total_item, 2)

    def aplicar_desconto(self, desconto: float) -> float:
        """
        Aplica um desconto ao item
        
        Args:
            desconto (float): Valor do desconto
            
        Returns:
            float: Valor total após desconto
        """
        if desconto < 0:
            return self.valor_total_item
        
        self.desconto_item = min(desconto, self.calcular_subtotal())
        return self.calcular_valor_total()

    def aplicar_desconto_percentual(self, percentagem: float) -> float:
        """
        Aplica um desconto em percentagem
        
        Args:
            percentagem (float): Percentagem de desconto (0-100)
            
        Returns:
            float: Valor total após desconto
        """
        if percentagem < 0 or percentagem > 100:
            return self.valor_total_item
        
        subtotal = self.calcular_subtotal()
        desconto = (subtotal * percentagem) / 100
        return self.aplicar_desconto(desconto)

    def registrar_recebimento(self, quantidade: int) -> bool:
        """
        Registra o recebimento de quantidade
        
        Args:
            quantidade (int): Quantidade recebida
            
        Returns:
            bool: True se conseguiu registrar
        """
        if quantidade < 0 or (self.quantidade_recebida + quantidade) > self.quantidade:
            return False
        
        self.quantidade_recebida += quantidade
        self.quantidade_pendente = self.quantidade - self.quantidade_recebida
        self.updated_at = datetime.now()
        return True

    def registrar_recebimento_total(self) -> None:
        """Registra o recebimento completo do item"""
        self.quantidade_recebida = self.quantidade
        self.quantidade_pendente = 0
        self.updated_at = datetime.now()

    def é_totalmente_recebido(self) -> bool:
        """
        Verifica se o item foi totalmente recebido
        
        Returns:
            bool: True se recebido completamente
        """
        return self.quantidade_recebida >= self.quantidade

    def é_parcialmente_recebido(self) -> bool:
        """
        Verifica se o item foi parcialmente recebido
        
        Returns:
            bool: True se recebido parcialmente
        """
        return 0 < self.quantidade_recebida < self.quantidade

    def é_não_recebido(self) -> bool:
        """
        Verifica se o item ainda não foi recebido
        
        Returns:
            bool: True se não recebido
        """
        return self.quantidade_recebida == 0

    def get_percentagem_recebida(self) -> float:
        """
        Calcula a percentagem de quantidade recebida
        
        Returns:
            float: Percentagem (0-100)
        """
        if self.quantidade == 0:
            return 0.0
        return round((self.quantidade_recebida / self.quantidade) * 100, 2)

    def get_status_recebimento(self) -> str:
        """
        Retorna o status do recebimento
        
        Returns:
            str: Status com ícone
        """
        if self.é_totalmente_recebido():
            return "✓ Completo"
        elif self.é_parcialmente_recebido():
            return "📦 Parcial"
        else:
            return "⏳ Pendente"

    def calcular_custo_unitario_recebido(self) -> float:
        """
        Calcula o custo unitário do que foi recebido
        
        Returns:
            float: Custo unitário
        """
        if self.quantidade_recebida == 0:
            return 0.0
        return round(self.valor_total_item / self.quantidade_recebida, 2)

    def calcular_valor_pendente(self) -> float:
        """
        Calcula o valor ainda pendente de receber
        
        Returns:
            float: Valor pendente
        """
        if self.quantidade_pendente == 0:
            return 0.0
        
        # Proporção do valor total baseado na quantidade pendente
        valor_unitario = self.valor_total_item / self.quantidade
        return round(valor_unitario * self.quantidade_pendente, 2)

    def gerar_descricao_completa(self) -> str:
        """
        Gera uma descrição completa do item
        
        Returns:
            str: Descrição formatada
        """
        return (f"{self.produto_nome} ({self.produto_codigo}) - "
                f"{self.quantidade} {self.unidade_medida} x "
                f"{self.preco_unitario}€ = {self.valor_total_item}€")

    def get_info_completa(self) -> dict:
        """
        Retorna informações completas do item
        
        Returns:
            dict: Dicionário com informações do item
        """
        return {
            "id": self.id_item_compra,
            "compra_id": self.compra_id,
            "produto_id": self.produto_id,
            "produto_nome": self.produto_nome,
            "produto_codigo": self.produto_codigo,
            "quantidade": self.quantidade,
            "unidade_medida": self.unidade_medida,
            "preco_unitario": self.preco_unitario,
            "subtotal": self.calcular_subtotal(),
            "desconto_item": self.desconto_item,
            "valor_total_item": self.calcular_valor_total(),
            "quantidade_recebida": self.quantidade_recebida,
            "quantidade_pendente": self.quantidade_pendente,
            "status_recebimento": self.get_status_recebimento(),
            "percentagem_recebida": self.get_percentagem_recebida(),
            "valor_pendente": self.calcular_valor_pendente(),
            "descricao": self.gerar_descricao_completa(),
            "observacoes": self.observacoes,
            "data_criacao": self.created_at.isoformat() if self.created_at else None,
            "data_atualizacao": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        """Representação em string"""
        return f"ItemCompra(id={self.id_item_compra}, produto='{self.produto_nome}', qty={self.quantidade})"

    def __str__(self) -> str:
        """String amigável"""
        recebimento = self.get_status_recebimento()
        return f"{self.produto_nome} - {self.quantidade} x {self.preco_unitario}€ = {self.valor_total_item}€ - {recebimento}"