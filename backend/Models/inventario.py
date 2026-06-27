# Models/inventario.py
"""
Inventario Model
Representa o inventário de produtos da loja Ondjango
"""

from Models.base_model import BaseModel
from typing import Optional, List
from datetime import datetime


class Inventario(BaseModel):
    """
    Modelo de Inventário
    
    Atributos:
        id_inventario (int): Identificador único do inventário
        produto_id (int): ID do produto
        produto_nome (str): Nome do produto
        quantidade_total (int): Quantidade total em stock
        quantidade_minima (int): Quantidade mínima recomendada
        quantidade_maxima (int): Quantidade máxima permitida
        localizacao (str): Localização física do produto (prateleira, armazém, etc)
        lote (str): Número do lote do produto
        data_validade (datetime): Data de validade (para produtos perecíveis)
        data_ultimo_reabastecimento (datetime): Data do último reabastecimento
        data_ultimo_movimento (datetime): Data do último movimento
        valor_stock_custo (float): Valor total do stock a preço de custo
        valor_stock_venda (float): Valor total do stock a preço de venda
        movimentos_pendentes (int): Número de movimentos ainda não registados
        status (str): Status do stock (Normal, Crítico, Excesso, Expirado)
        observacoes (str): Observações sobre o stock
        data_criacao (datetime): Data de criação
        data_atualizacao (datetime): Data da última atualização
    """

    # Status possíveis
    STATUS_NORMAL = "Normal"
    STATUS_CRITICO = "Crítico"
    STATUS_EXCESSO = "Excesso"
    STATUS_EXPIRADO = "Expirado"

    STATUSES = [STATUS_NORMAL, STATUS_CRITICO, STATUS_EXCESSO, STATUS_EXPIRADO]

    def __init__(
        self,
        id_inventario: Optional[int] = None,
        produto_id: Optional[int] = None,
        produto_nome: Optional[str] = None,
        quantidade_total: Optional[int] = 0,
        quantidade_minima: Optional[int] = 0,
        quantidade_maxima: Optional[int] = 0,
        localizacao: Optional[str] = None,
        lote: Optional[str] = None,
        data_validade: Optional[datetime] = None,
        data_ultimo_reabastecimento: Optional[datetime] = None,
        data_ultimo_movimento: Optional[datetime] = None,
        valor_stock_custo: Optional[float] = 0.0,
        valor_stock_venda: Optional[float] = 0.0,
        movimentos_pendentes: Optional[int] = 0,
        status: Optional[str] = STATUS_NORMAL,
        observacoes: Optional[str] = None,
        **kwargs
    ):
        """
        Inicializar um Inventário
        
        Args:
            id_inventario (int, optional): ID do inventário
            produto_id (int, optional): ID do produto
            produto_nome (str, optional): Nome do produto
            quantidade_total (int, optional): Quantidade total. Padrão: 0
            quantidade_minima (int, optional): Quantidade mínima. Padrão: 0
            quantidade_maxima (int, optional): Quantidade máxima. Padrão: 0
            localizacao (str, optional): Localização do produto
            lote (str, optional): Número do lote
            data_validade (datetime, optional): Data de validade
            data_ultimo_reabastecimento (datetime, optional): Data reabastecimento
            data_ultimo_movimento (datetime, optional): Data último movimento
            valor_stock_custo (float, optional): Valor do stock a custo. Padrão: 0.0
            valor_stock_venda (float, optional): Valor do stock a venda. Padrão: 0.0
            movimentos_pendentes (int, optional): Movimentos pendentes. Padrão: 0
            status (str, optional): Status. Padrão: Normal
            observacoes (str, optional): Observações
            **kwargs: Atributos adicionais
        """
        super().__init__()

        self.id_inventario = id_inventario
        self.produto_id = produto_id
        self.produto_nome = produto_nome
        self.quantidade_total = quantidade_total
        self.quantidade_minima = quantidade_minima
        self.quantidade_maxima = quantidade_maxima
        self.localizacao = localizacao
        self.lote = lote
        self.data_validade = data_validade
        self.data_ultimo_reabastecimento = data_ultimo_reabastecimento
        self.data_ultimo_movimento = data_ultimo_movimento
        self.valor_stock_custo = valor_stock_custo
        self.valor_stock_venda = valor_stock_venda
        self.movimentos_pendentes = movimentos_pendentes
        self.status = status
        self.observacoes = observacoes

        # Processar argumentos adicionais
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def is_valid(self) -> bool:
        """
        Valida o inventário
        
        Returns:
            bool: True se válido
        """
        if not self.produto_id:
            return False
        if self.quantidade_total is None or self.quantidade_total < 0:
            return False
        if self.status not in self.STATUSES:
            return False
        return True

    def validate(self) -> List[str]:
        """
        Retorna erros de validação
        
        Returns:
            List[str]: Lista de mensagens de erro
        """
        errors = []

        if not self.produto_id:
            errors.append("Produto é obrigatório")

        if self.quantidade_total is None or self.quantidade_total < 0:
            errors.append("Quantidade total deve ser um valor positivo")

        if self.quantidade_minima and self.quantidade_minima < 0:
            errors.append("Quantidade mínima não pode ser negativa")

        if self.quantidade_maxima and self.quantidade_maxima < 0:
            errors.append("Quantidade máxima não pode ser negativa")

        if (self.quantidade_minima is not None and self.quantidade_maxima is not None
            and self.quantidade_minima > self.quantidade_maxima):
            errors.append("Quantidade mínima não pode ser maior que a máxima")

        if self.status not in self.STATUSES:
            errors.append(f"Status inválido. Deve ser um de: {', '.join(self.STATUSES)}")

        if self.valor_stock_custo and self.valor_stock_custo < 0:
            errors.append("Valor do stock a custo não pode ser negativo")

        if self.valor_stock_venda and self.valor_stock_venda < 0:
            errors.append("Valor do stock a venda não pode ser negativo")

        return errors

    def atualizar_quantidade(self, nova_quantidade: int) -> bool:
        """
        Atualiza a quantidade total
        
        Args:
            nova_quantidade (int): Nova quantidade
            
        Returns:
            bool: True se conseguiu atualizar
        """
        if nova_quantidade < 0:
            return False
        
        self.quantidade_total = nova_quantidade
        self.data_ultimo_movimento = datetime.now()
        self.atualizar_status()
        self.updated_at = datetime.now()
        return True

    def adicionar_quantidade(self, quantidade: int) -> bool:
        """
        Adiciona quantidade ao stock
        
        Args:
            quantidade (int): Quantidade a adicionar
            
        Returns:
            bool: True se conseguiu adicionar
        """
        if quantidade <= 0:
            return False
        
        self.quantidade_total += quantidade
        self.data_ultimo_reabastecimento = datetime.now()
        self.data_ultimo_movimento = datetime.now()
        self.atualizar_status()
        self.updated_at = datetime.now()
        return True

    def remover_quantidade(self, quantidade: int) -> bool:
        """
        Remove quantidade do stock
        
        Args:
            quantidade (int): Quantidade a remover
            
        Returns:
            bool: True se conseguiu remover
        """
        if quantidade <= 0 or self.quantidade_total < quantidade:
            return False
        
        self.quantidade_total -= quantidade
        self.data_ultimo_movimento = datetime.now()
        self.atualizar_status()
        self.updated_at = datetime.now()
        return True

    def atualizar_status(self) -> None:
        """Atualiza o status do stock automaticamente"""
        if self.está_expirado():
            self.status = self.STATUS_EXPIRADO
        elif self.é_stock_critico():
            self.status = self.STATUS_CRITICO
        elif self.é_stock_excesso():
            self.status = self.STATUS_EXCESSO
        else:
            self.status = self.STATUS_NORMAL

    def é_stock_baixo(self) -> bool:
        """
        Verifica se o stock está abaixo do mínimo
        
        Returns:
            bool: True se stock está baixo
        """
        if self.quantidade_minima is None or self.quantidade_minima == 0:
            return False
        return self.quantidade_total <= self.quantidade_minima

    def é_stock_critico(self) -> bool:
        """
        Verifica se o stock está crítico (zero ou muito baixo)
        
        Returns:
            bool: True se stock está crítico
        """
        return self.quantidade_total == 0 or (
            self.quantidade_minima is not None 
            and self.quantidade_total < (self.quantidade_minima * 0.5)
        )

    def é_stock_alto(self) -> bool:
        """
        Verifica se o stock está acima do máximo
        
        Returns:
            bool: True se stock está alto
        """
        if self.quantidade_maxima is None or self.quantidade_maxima == 0:
            return False
        return self.quantidade_total >= self.quantidade_maxima

    def é_stock_excesso(self) -> bool:
        """
        Verifica se há excesso de stock
        
        Returns:
            bool: True se há excesso
        """
        if self.quantidade_maxima is None or self.quantidade_maxima == 0:
            return False
        return self.quantidade_total > self.quantidade_maxima

    def é_stock_normal(self) -> bool:
        """
        Verifica se o stock está normal
        
        Returns:
            bool: True se stock normal
        """
        return not (self.é_stock_baixo() or self.é_stock_alto() or self.está_expirado())

    def está_expirado(self) -> bool:
        """
        Verifica se o produto está expirado
        
        Returns:
            bool: True se expirado
        """
        if not self.data_validade:
            return False
        return datetime.now() > self.data_validade

    def dias_para_expirar(self) -> Optional[int]:
        """
        Calcula dias até expiração
        
        Returns:
            int: Número de dias (negativo se já expirado)
        """
        if not self.data_validade:
            return None
        
        diferenca = self.data_validade - datetime.now()
        return diferenca.days

    def precisa_reabastecimento(self) -> bool:
        """
        Verifica se o produto precisa ser reabastecido
        
        Returns:
            bool: True se precisa reabastecimento
        """
        return self.é_stock_baixo()

    def obter_quantidade_reabastecimento(self) -> int:
        """
        Calcula a quantidade recomendada para reabastecimento
        
        Returns:
            int: Quantidade recomendada
        """
        if self.quantidade_maxima is None:
            return 0
        return max(0, self.quantidade_maxima - self.quantidade_total)

    def calcular_valor_stock_custo(self, preco_custo_unitario: float) -> float:
        """
        Calcula o valor total do stock a preço de custo
        
        Args:
            preco_custo_unitario (float): Preço de custo por unidade
            
        Returns:
            float: Valor total do stock
        """
        self.valor_stock_custo = self.quantidade_total * preco_custo_unitario
        return round(self.valor_stock_custo, 2)

    def calcular_valor_stock_venda(self, preco_venda_unitario: float) -> float:
        """
        Calcula o valor total do stock a preço de venda
        
        Args:
            preco_venda_unitario (float): Preço de venda por unidade
            
        Returns:
            float: Valor total do stock
        """
        self.valor_stock_venda = self.quantidade_total * preco_venda_unitario
        return round(self.valor_stock_venda, 2)

    def calcular_margem_stock(self) -> float:
        """
        Calcula a margem de lucro potencial do stock
        
        Returns:
            float: Margem em percentagem
        """
        if self.valor_stock_custo <= 0:
            return 0.0
        
        margem = ((self.valor_stock_venda - self.valor_stock_custo) / self.valor_stock_custo) * 100
        return round(margem, 2)

    def dias_desde_reabastecimento(self) -> Optional[int]:
        """
        Calcula dias desde o último reabastecimento
        
        Returns:
            int: Número de dias
        """
        if not self.data_ultimo_reabastecimento:
            return None
        
        diferenca = datetime.now() - self.data_ultimo_reabastecimento
        return diferenca.days

    def dias_desde_movimento(self) -> Optional[int]:
        """
        Calcula dias desde o último movimento
        
        Returns:
            int: Número de dias
        """
        if not self.data_ultimo_movimento:
            return None
        
        diferenca = datetime.now() - self.data_ultimo_movimento
        return diferenca.days

    def get_status_icon(self) -> str:
        """
        Retorna um ícone representativo do status
        
        Returns:
            str: Ícone do status
        """
        status_map = {
            self.STATUS_NORMAL: "✓ Normal",
            self.STATUS_CRITICO: "⚠️ Crítico",
            self.STATUS_EXCESSO: "📈 Excesso",
            self.STATUS_EXPIRADO: "✗ Expirado"
        }
        return status_map.get(self.status, self.status)

    def get_info_completa(self) -> dict:
        """
        Retorna informações completas do inventário
        
        Returns:
            dict: Dicionário com informações do inventário
        """
        return {
            "id": self.id_inventario,
            "produto_id": self.produto_id,
            "produto_nome": self.produto_nome,
            "quantidade_total": self.quantidade_total,
            "quantidade_minima": self.quantidade_minima,
            "quantidade_maxima": self.quantidade_maxima,
            "status": self.status,
            "status_icon": self.get_status_icon(),
            "é_stock_normal": self.é_stock_normal(),
            "é_stock_baixo": self.é_stock_baixo(),
            "é_stock_critico": self.é_stock_critico(),
            "é_stock_alto": self.é_stock_alto(),
            "localizacao": self.localizacao,
            "lote": self.lote,
            "data_validade": self.data_validade.isoformat() if self.data_validade else None,
            "dias_para_expirar": self.dias_para_expirar(),
            "está_expirado": self.está_expirado(),
            "data_ultimo_reabastecimento": self.data_ultimo_reabastecimento.isoformat() if self.data_ultimo_reabastecimento else None,
            "dias_desde_reabastecimento": self.dias_desde_reabastecimento(),
            "data_ultimo_movimento": self.data_ultimo_movimento.isoformat() if self.data_ultimo_movimento else None,
            "dias_desde_movimento": self.dias_desde_movimento(),
            "valor_stock_custo": self.valor_stock_custo,
            "valor_stock_venda": self.valor_stock_venda,
            "margem_stock": self.calcular_margem_stock(),
            "precisa_reabastecimento": self.precisa_reabastecimento(),
            "quantidade_reabastecimento": self.obter_quantidade_reabastecimento(),
            "movimentos_pendentes": self.movimentos_pendentes,
            "observacoes": self.observacoes,
            "data_criacao": self.created_at.isoformat() if self.created_at else None,
            "data_atualizacao": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        """Representação em string"""
        return f"Inventario(id={self.id_inventario}, produto='{self.produto_nome}', qty={self.quantidade_total})"

    def __str__(self) -> str:
        """String amigável"""
        return (f"{self.produto_nome} - Stock: {self.quantidade_total} - "
                f"{self.get_status_icon()}")
