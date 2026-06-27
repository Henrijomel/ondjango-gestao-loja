# Models/item_venda.py
"""
ItemVenda Model
Representa um item individual dentro de uma venda
"""

from Models.base_model import BaseModel
from typing import Optional, List
from datetime import datetime


class ItemVenda(BaseModel):
    """
    Modelo de Item de Venda
    
    Atributos:
        id_item_venda (int): Identificador único do item
        venda_id (int): ID da venda a que pertence
        produto_id (int): ID do produto
        produto_nome (str): Nome do produto
        produto_codigo (str): Código do produto
        quantidade (int): Quantidade do item
        preco_unitario (float): Preço unitário de venda
        desconto_item (float): Desconto específico do item
        valor_total_item (float): Valor total do item
        unidade_medida (str): Unidade de medida
        observacoes (str): Observações sobre o item
        data_criacao (datetime): Data de criação
        data_atualizacao (datetime): Data da última atualização
    """

    def __init__(
        self,
        id_item_venda: Optional[int] = None,
        venda_id: Optional[int] = None,
        produto_id: Optional[int] = None,
        produto_nome: Optional[str] = None,
        produto_codigo: Optional[str] = None,
        quantidade: Optional[int] = 1,
        preco_unitario: Optional[float] = 0.0,
        desconto_item: Optional[float] = 0.0,
        valor_total_item: Optional[float] = 0.0,
        unidade_medida: Optional[str] = "Un",
        observacoes: Optional[str] = None,
        **kwargs
    ):
        """
        Inicializar um Item de Venda
        
        Args:
            id_item_venda (int, optional): ID do item
            venda_id (int, optional): ID da venda
            produto_id (int, optional): ID do produto
            produto_nome (str, optional): Nome do produto
            produto_codigo (str, optional): Código do produto
            quantidade (int, optional): Quantidade. Padrão: 1
            preco_unitario (float, optional): Preço unitário. Padrão: 0.0
            desconto_item (float, optional): Desconto. Padrão: 0.0
            valor_total_item (float, optional): Valor total. Padrão: 0.0
            unidade_medida (str, optional): Unidade. Padrão: "Un"
            observacoes (str, optional): Observações
            **kwargs: Atributos adicionais
        """
        super().__init__()

        self.id_item_venda = id_item_venda
        self.venda_id = venda_id
        self.produto_id = produto_id
        self.produto_nome = produto_nome
        self.produto_codigo = produto_codigo
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.desconto_item = desconto_item
        self.valor_total_item = valor_total_item or (quantidade * preco_unitario - desconto_item)
        self.unidade_medida = unidade_medida
        self.observacoes = observacoes

        # Processar argumentos adicionais
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def is_valid(self) -> bool:
        """
        Valida o item de venda
        
        Returns:
            bool: True se válido
        """
        if not self.venda_id:
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

        if not self.venda_id:
            errors.append("Venda é obrigatória")

        if not self.produto_id:
            errors.append("Produto é obrigatório")

        if self.quantidade is None or self.quantidade <= 0:
            errors.append("Quantidade deve ser maior que zero")

        if self.preco_unitario is None or self.preco_unitario < 0:
            errors.append("Preço unitário é obrigatório e deve ser positivo")

        if self.desconto_item and self.desconto_item < 0:
            errors.append("Desconto não pode ser negativo")

        if self.desconto_item and self.desconto_item > self.calcular_subtotal():
            errors.append("Desconto não pode ser maior que o subtotal")

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

    def calcular_margem_lucro(self, preco_custo: float) -> float:
        """
        Calcula a margem de lucro do item
        
        Args:
            preco_custo (float): Preço de custo unitário
            
        Returns:
            float: Margem de lucro em percentagem
        """
        if preco_custo <= 0:
            return 0.0
        
        margem = ((self.preco_unitario - preco_custo) / preco_custo) * 100
        return round(margem, 2)

    def calcular_lucro_unitario(self, preco_custo: float) -> float:
        """
        Calcula o lucro unitário
        
        Args:
            preco_custo (float): Preço de custo unitário
            
        Returns:
            float: Lucro por unidade
        """
        return round(self.preco_unitario - preco_custo, 2)

    def calcular_lucro_total(self, preco_custo: float) -> float:
        """
        Calcula o lucro total do item
        
        Args:
            preco_custo (float): Preço de custo unitário
            
        Returns:
            float: Lucro total
        """
        lucro_unitario = self.calcular_lucro_unitario(preco_custo)
        return round(lucro_unitario * self.quantidade, 2)

    def gerar_descricao_completa(self) -> str:
        """
        Gera uma descrição completa do item
        
        Returns:
            str: Descrição formatada
        """
        return (f"{self.produto_nome} ({self.produto_codigo}) - "
                f"{self.quantidade} {self.unidade_medida} x "
                f"{self.preco_unitario}€ = {self.valor_total_item}€")

    def obter_preco_unitario_com_desconto(self) -> float:
        """
        Calcula o preço unitário após desconto
        
        Returns:
            float: Preço unitário com desconto
        """
        if self.quantidade == 0:
            return self.preco_unitario
        
        valor_desconto_unitario = self.desconto_item / self.quantidade
        return round(self.preco_unitario - valor_desconto_unitario, 2)

    def pode_ser_removido(self) -> bool:
        """
        Verifica se o item pode ser removido
        
        Returns:
            bool: True se pode ser removido
        """
        # Um item de venda pode ser removido se a venda ainda está pendente
        return True

    def duplicar(self):
        """
        Cria uma cópia do item de venda
        
        Returns:
            ItemVenda: Cópia do item
        """
        novo_item = ItemVenda(
            venda_id=self.venda_id,
            produto_id=self.produto_id,
            produto_nome=self.produto_nome,
            produto_codigo=self.produto_codigo,
            quantidade=self.quantidade,
            preco_unitario=self.preco_unitario,
            desconto_item=self.desconto_item,
            valor_total_item=self.valor_total_item,
            unidade_medida=self.unidade_medida,
            observacoes=self.observacoes
        )
        return novo_item

    def atualizar_quantidade(self, nova_quantidade: int) -> bool:
        """
        Atualiza a quantidade do item
        
        Args:
            nova_quantidade (int): Nova quantidade
            
        Returns:
            bool: True se conseguiu atualizar
        """
        if nova_quantidade <= 0:
            return False
        
        self.quantidade = nova_quantidade
        self.calcular_valor_total()
        self.updated_at = datetime.now()
        return True

    def atualizar_preco_unitario(self, novo_preco: float) -> bool:
        """
        Atualiza o preço unitário
        
        Args:
            novo_preco (float): Novo preço
            
        Returns:
            bool: True se conseguiu atualizar
        """
        if novo_preco < 0:
            return False
        
        self.preco_unitario = novo_preco
        self.calcular_valor_total()
        self.updated_at = datetime.now()
        return True

    def get_info_completa(self) -> dict:
        """
        Retorna informações completas do item
        
        Returns:
            dict: Dicionário com informações do item
        """
        return {
            "id": self.id_item_venda,
            "venda_id": self.venda_id,
            "produto_id": self.produto_id,
            "produto_nome": self.produto_nome,
            "produto_codigo": self.produto_codigo,
            "quantidade": self.quantidade,
            "unidade_medida": self.unidade_medida,
            "preco_unitario": self.preco_unitario,
            "subtotal": self.calcular_subtotal(),
            "desconto_item": self.desconto_item,
            "preco_unitario_com_desconto": self.obter_preco_unitario_com_desconto(),
            "valor_total_item": self.calcular_valor_total(),
            "descricao": self.gerar_descricao_completa(),
            "observacoes": self.observacoes,
            "data_criacao": self.created_at.isoformat() if self.created_at else None,
            "data_atualizacao": self.updated_at.isoformat() if self.updated_at else None,
        }

    def get_info_resumida(self) -> dict:
        """
        Retorna informações resumidas do item
        
        Returns:
            dict: Dicionário com informações básicas
        """
        return {
            "id": self.id_item_venda,
            "produto": self.produto_nome,
            "codigo": self.produto_codigo,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
            "valor_total": self.calcular_valor_total(),
        }

    def __repr__(self) -> str:
        """Representação em string"""
        return f"ItemVenda(id={self.id_item_venda}, produto='{self.produto_nome}', qty={self.quantidade})"

    def __str__(self) -> str:
        """String amigável"""
        return f"{self.produto_nome} - {self.quantidade} x {self.preco_unitario}€ = {self.valor_total_item}€"

    def __eq__(self, other):
        """Comparação entre items"""
        if not isinstance(other, ItemVenda):
            return False
        return self.id_item_venda == other.id_item_venda

    def __lt__(self, other):
        """Comparação para ordenação"""
        if not isinstance(other, ItemVenda):
            return False
        return self.id_item_venda < other.id_item_venda
