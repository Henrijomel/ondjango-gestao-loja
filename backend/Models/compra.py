# Models/compra.py
"""
Compra Model
Representa uma compra de produtos ao fornecedor
"""

from Models.base_model import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta


class Compra(BaseModel):
    """
    Modelo de Compra
    
    Atributos:
        id_compra (int): Identificador único da compra
        numero_compra (str): Número/referência da compra
        fornecedor_id (int): ID do fornecedor
        fornecedor_nome (str): Nome do fornecedor
        data_compra (datetime): Data em que foi realizada a compra
        data_entrega_esperada (datetime): Data esperada de entrega
        data_entrega_real (datetime): Data real de entrega
        status (str): Status da compra (Pendente, Parcial, Entregue, Cancelada)
        valor_total (float): Valor total da compra
        desconto (float): Desconto aplicado
        valor_final (float): Valor final após desconto
        moeda (str): Moeda da transação
        condicoes_pagamento (str): Condições de pagamento
        data_pagamento (datetime): Data do pagamento
        pago (bool): Se a compra foi paga
        observacoes (str): Observações adicionais
        referencia_externa (str): Referência do fornecedor
        data_criacao (datetime): Data de criação
        data_atualizacao (datetime): Data da última atualização
    """

    # Status possíveis
    STATUS_PENDENTE = "Pendente"
    STATUS_PARCIAL = "Parcial"
    STATUS_ENTREGUE = "Entregue"
    STATUS_CANCELADA = "Cancelada"

    STATUSES = [STATUS_PENDENTE, STATUS_PARCIAL, STATUS_ENTREGUE, STATUS_CANCELADA]

    def __init__(
        self,
        id_compra: Optional[int] = None,
        numero_compra: Optional[str] = None,
        fornecedor_id: Optional[int] = None,
        fornecedor_nome: Optional[str] = None,
        data_compra: Optional[datetime] = None,
        data_entrega_esperada: Optional[datetime] = None,
        data_entrega_real: Optional[datetime] = None,
        status: Optional[str] = STATUS_PENDENTE,
        valor_total: Optional[float] = 0.0,
        desconto: Optional[float] = 0.0,
        valor_final: Optional[float] = 0.0,
        moeda: Optional[str] = "KZ",
        condicoes_pagamento: Optional[str] = "30 dias",
        data_pagamento: Optional[datetime] = None,
        pago: bool = False,
        observacoes: Optional[str] = None,
        referencia_externa: Optional[str] = None,
        **kwargs
    ):
        """
        Inicializar uma Compra
        
        Args:
            id_compra (int, optional): ID da compra
            numero_compra (str, optional): Número da compra
            fornecedor_id (int, optional): ID do fornecedor
            fornecedor_nome (str, optional): Nome do fornecedor
            data_compra (datetime, optional): Data da compra. Padrão: agora
            data_entrega_esperada (datetime, optional): Data esperada de entrega
            data_entrega_real (datetime, optional): Data real de entrega
            status (str, optional): Status. Padrão: Pendente
            valor_total (float, optional): Valor total. Padrão: 0.0
            desconto (float, optional): Desconto. Padrão: 0.0
            valor_final (float, optional): Valor final. Padrão: 0.0
            moeda (str, optional): Moeda. Padrão: "EUR"
            condicoes_pagamento (str, optional): Condições. Padrão: "30 dias"
            data_pagamento (datetime, optional): Data do pagamento
            pago (bool, optional): Status pagamento. Padrão: False
            observacoes (str, optional): Observações
            referencia_externa (str, optional): Referência externa
            **kwargs: Atributos adicionais
        """
        super().__init__()

        self.id_compra = id_compra
        self.numero_compra = numero_compra
        self.fornecedor_id = fornecedor_id
        self.fornecedor_nome = fornecedor_nome
        self.data_compra = data_compra or datetime.now()
        self.data_entrega_esperada = data_entrega_esperada
        self.data_entrega_real = data_entrega_real
        self.status = status
        self.valor_total = valor_total
        self.desconto = desconto
        self.valor_final = valor_final or (valor_total - desconto)
        self.moeda = moeda
        self.condicoes_pagamento = condicoes_pagamento
        self.data_pagamento = data_pagamento
        self.pago = pago
        self.observacoes = observacoes
        self.referencia_externa = referencia_externa

        # Processar argumentos adicionais
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def is_valid(self) -> bool:
        """
        Valida a compra
        
        Returns:
            bool: True se válida
        """
        if not self.numero_compra or not str(self.numero_compra).strip():
            return False
        if self.fornecedor_id is None:
            return False
        if self.valor_total is None or self.valor_total < 0:
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

        if not self.numero_compra or not str(self.numero_compra).strip():
            errors.append("Número da compra é obrigatório")

        if self.fornecedor_id is None:
            errors.append("Fornecedor é obrigatório")

        if self.valor_total is None or self.valor_total < 0:
            errors.append("Valor total é obrigatório e deve ser positivo")

        if self.desconto and self.desconto < 0:
            errors.append("Desconto não pode ser negativo")

        if self.desconto and self.desconto > self.valor_total:
            errors.append("Desconto não pode ser maior que o valor total")

        if self.status not in self.STATUSES:
            errors.append(f"Status inválido. Deve ser um de: {', '.join(self.STATUSES)}")

        if self.data_entrega_esperada and self.data_entrega_real:
            if self.data_entrega_real < self.data_compra:
                errors.append("Data de entrega não pode ser anterior à data da compra")

        return errors

    def calcular_valor_final(self) -> float:
        """
        Calcula o valor final da compra
        
        Returns:
            float: Valor final
        """
        self.valor_final = self.valor_total - (self.desconto or 0)
        return round(self.valor_final, 2)

    def aplicar_desconto(self, desconto: float) -> float:
        """
        Aplica um desconto à compra
        
        Args:
            desconto (float): Valor do desconto
            
        Returns:
            float: Valor final após desconto
        """
        if desconto < 0 or desconto > self.valor_total:
            return self.valor_final
        
        self.desconto = desconto
        return self.calcular_valor_final()

    def aplicar_desconto_percentual(self, percentagem: float) -> float:
        """
        Aplica um desconto em percentagem
        
        Args:
            percentagem (float): Percentagem de desconto (0-100)
            
        Returns:
            float: Valor final após desconto
        """
        if percentagem < 0 or percentagem > 100:
            return self.valor_final
        
        desconto = (self.valor_total * percentagem) / 100
        return self.aplicar_desconto(desconto)

    def é_pendente(self) -> bool:
        """Verifica se está pendente"""
        return self.status == self.STATUS_PENDENTE

    def é_parcial(self) -> bool:
        """Verifica se é parcial"""
        return self.status == self.STATUS_PARCIAL

    def é_entregue(self) -> bool:
        """Verifica se foi entregue"""
        return self.status == self.STATUS_ENTREGUE

    def é_cancelada(self) -> bool:
        """Verifica se foi cancelada"""
        return self.status == self.STATUS_CANCELADA

    def pode_ser_entregue(self) -> bool:
        """Verifica se pode ser entregue"""
        return self.é_pendente() or self.é_parcial()

    def registrar_entrega(self) -> None:
        """Registra a entrega"""
        if self.pode_ser_entregue():
            self.status = self.STATUS_ENTREGUE
            self.data_entrega_real = datetime.now()
            self.updated_at = datetime.now()

    def registrar_entrega_parcial(self) -> None:
        """Registra entrega parcial"""
        if self.é_pendente():
            self.status = self.STATUS_PARCIAL
            self.updated_at = datetime.now()

    def cancelar(self) -> None:
        """Cancela a compra"""
        if not self.é_entregue() and not self.pago:
            self.status = self.STATUS_CANCELADA
            self.updated_at = datetime.now()

    def registrar_pagamento(self, data: Optional[datetime] = None) -> None:
        """
        Registra o pagamento
        
        Args:
            data (datetime, optional): Data do pagamento. Padrão: agora
        """
        self.pago = True
        self.data_pagamento = data or datetime.now()
        self.updated_at = datetime.now()

    def está_atrasada(self) -> bool:
        """
        Verifica se a entrega está atrasada
        
        Returns:
            bool: True se está atrasada
        """
        if not self.data_entrega_esperada:
            return False
        return datetime.now() > self.data_entrega_esperada and not self.é_entregue()

    def dias_para_entrega(self) -> int:
        """
        Calcula dias até a entrega esperada
        
        Returns:
            int: Número de dias (negativo se atrasada)
        """
        if not self.data_entrega_esperada:
            return 0
        
        diferenca = self.data_entrega_esperada - datetime.now()
        return diferenca.days

    def dias_desde_compra(self) -> int:
        """
        Calcula dias desde a compra
        
        Returns:
            int: Número de dias
        """
        diferenca = datetime.now() - self.data_compra
        return diferenca.days

    def gerar_numero_compra(self, prefixo: str = "COMP") -> str:
        """
        Gera um número de compra único
        
        Args:
            prefixo (str): Prefixo do número. Padrão: "COMP"
            
        Returns:
            str: Número de compra gerado
        """
        timestamp = int(self.data_compra.timestamp())
        self.numero_compra = f"{prefixo}-{timestamp}"
        return self.numero_compra

    def get_status_pagamento(self) -> str:
        """
        Retorna o status do pagamento
        
        Returns:
            str: Status (Pago, Pendente)
        """
        return "✓ Pago" if self.pago else "✗ Pendente"

    def get_status_entrega(self) -> str:
        """
        Retorna o status da entrega
        
        Returns:
            str: Status com ícone
        """
        status_map = {
            self.STATUS_PENDENTE: "⏳ Pendente",
            self.STATUS_PARCIAL: "📦 Parcial",
            self.STATUS_ENTREGUE: "✓ Entregue",
            self.STATUS_CANCELADA: "✗ Cancelada"
        }
        return status_map.get(self.status, self.status)

    def get_info_completa(self) -> dict:
        """
        Retorna informações completas da compra
        
        Returns:
            dict: Dicionário com informações da compra
        """
        return {
            "id": self.id_compra,
            "numero_compra": self.numero_compra,
            "fornecedor_id": self.fornecedor_id,
            "fornecedor_nome": self.fornecedor_nome,
            "data_compra": self.data_compra.isoformat() if self.data_compra else None,
            "data_entrega_esperada": self.data_entrega_esperada.isoformat() if self.data_entrega_esperada else None,
            "data_entrega_real": self.data_entrega_real.isoformat() if self.data_entrega_real else None,
            "status": self.status,
            "status_entrega": self.get_status_entrega(),
            "valor_total": self.valor_total,
            "desconto": self.desconto,
            "valor_final": self.valor_final,
            "moeda": self.moeda,
            "condicoes_pagamento": self.condicoes_pagamento,
            "data_pagamento": self.data_pagamento.isoformat() if self.data_pagamento else None,
            "pago": self.pago,
            "status_pagamento": self.get_status_pagamento(),
            "observacoes": self.observacoes,
            "referencia_externa": self.referencia_externa,
            "está_atrasada": self.está_atrasada(),
            "dias_para_entrega": self.dias_para_entrega(),
            "dias_desde_compra": self.dias_desde_compra(),
            "data_criacao": self.created_at.isoformat() if self.created_at else None,
            "data_atualizacao": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        """Representação em string"""
        return f"Compra(id={self.id_compra}, numero='{self.numero_compra}', fornecedor='{self.fornecedor_nome}')"

    def __str__(self) -> str:
        """String amigável"""
        return f"{self.numero_compra} - {self.fornecedor_nome} - {self.valor_final}€ - {self.get_status_entrega()} - {self.get_status_pagamento()}"
