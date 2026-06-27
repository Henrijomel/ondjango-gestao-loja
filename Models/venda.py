# Models/venda.py
"""
Venda Model
Representa uma venda de produtos ao cliente
"""

from Models.base_model import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta


class Venda(BaseModel):
    """
    Modelo de Venda
    
    Atributos:
        id_venda (int): Identificador único da venda
        numero_venda (str): Número/referência da venda
        cliente_id (int): ID do cliente
        cliente_nome (str): Nome do cliente
        data_venda (datetime): Data em que foi realizada a venda
        data_entrega (datetime): Data de entrega
        status (str): Status da venda (Pendente, Processando, Enviada, Entregue, Cancelada)
        valor_total (float): Valor total da venda
        desconto (float): Desconto aplicado
        valor_final (float): Valor final após desconto
        moeda (str): Moeda da transação
        metodo_pagamento (str): Método de pagamento
        data_pagamento (datetime): Data do pagamento
        pago (bool): Se a venda foi paga
        observacoes (str): Observações adicionais
        numero_rastreamento (str): Número de rastreamento de envio
        endereco_entrega (str): Endereço de entrega
        data_criacao (datetime): Data de criação
        data_atualizacao (datetime): Data da última atualização
    """

    # Status possíveis
    STATUS_PENDENTE = "Pendente"
    STATUS_PROCESSANDO = "Processando"
    STATUS_ENVIADA = "Enviada"
    STATUS_ENTREGUE = "Entregue"
    STATUS_CANCELADA = "Cancelada"

    STATUSES = [STATUS_PENDENTE, STATUS_PROCESSANDO, STATUS_ENVIADA, STATUS_ENTREGUE, STATUS_CANCELADA]

    # Métodos de pagamento
    METODO_CARTAO = "Cartão de Crédito"
    METODO_TRANSFERENCIA = "Transferência Bancária"
    METODO_PAYPAL = "PayPal"
    METODO_DINHEIRO = "Dinheiro"
    METODO_CHEQUE = "Cheque"

    METODOS_PAGAMENTO = [METODO_CARTAO, METODO_TRANSFERENCIA, METODO_PAYPAL, METODO_DINHEIRO, METODO_CHEQUE]

    def __init__(
        self,
        id_venda: Optional[int] = None,
        numero_venda: Optional[str] = None,
        cliente_id: Optional[int] = None,
        cliente_nome: Optional[str] = None,
        data_venda: Optional[datetime] = None,
        data_entrega: Optional[datetime] = None,
        status: Optional[str] = STATUS_PENDENTE,
        valor_total: Optional[float] = 0.0,
        desconto: Optional[float] = 0.0,
        valor_final: Optional[float] = 0.0,
        moeda: Optional[str] = "EUR",
        metodo_pagamento: Optional[str] = None,
        data_pagamento: Optional[datetime] = None,
        pago: bool = False,
        observacoes: Optional[str] = None,
        numero_rastreamento: Optional[str] = None,
        endereco_entrega: Optional[str] = None,
        **kwargs
    ):
        """
        Inicializar uma Venda
        
        Args:
            id_venda (int, optional): ID da venda
            numero_venda (str, optional): Número da venda
            cliente_id (int, optional): ID do cliente
            cliente_nome (str, optional): Nome do cliente
            data_venda (datetime, optional): Data da venda. Padrão: agora
            data_entrega (datetime, optional): Data de entrega
            status (str, optional): Status. Padrão: Pendente
            valor_total (float, optional): Valor total. Padrão: 0.0
            desconto (float, optional): Desconto. Padrão: 0.0
            valor_final (float, optional): Valor final. Padrão: 0.0
            moeda (str, optional): Moeda. Padrão: "EUR"
            metodo_pagamento (str, optional): Método de pagamento
            data_pagamento (datetime, optional): Data do pagamento
            pago (bool, optional): Status pagamento. Padrão: False
            observacoes (str, optional): Observações
            numero_rastreamento (str, optional): Número de rastreamento
            endereco_entrega (str, optional): Endereço de entrega
            **kwargs: Atributos adicionais
        """
        super().__init__()

        self.id_venda = id_venda
        self.numero_venda = numero_venda
        self.cliente_id = cliente_id
        self.cliente_nome = cliente_nome
        self.data_venda = data_venda or datetime.now()
        self.data_entrega = data_entrega
        self.status = status
        self.valor_total = valor_total
        self.desconto = desconto
        self.valor_final = valor_final or (valor_total - desconto)
        self.moeda = moeda
        self.metodo_pagamento = metodo_pagamento
        self.data_pagamento = data_pagamento
        self.pago = pago
        self.observacoes = observacoes
        self.numero_rastreamento = numero_rastreamento
        self.endereco_entrega = endereco_entrega

        # Processar argumentos adicionais
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def is_valid(self) -> bool:
        """
        Valida a venda
        
        Returns:
            bool: True se válida
        """
        if not self.numero_venda or not str(self.numero_venda).strip():
            return False
        if self.cliente_id is None:
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

        if not self.numero_venda or not str(self.numero_venda).strip():
            errors.append("Número da venda é obrigatório")

        if self.cliente_id is None:
            errors.append("Cliente é obrigatório")

        if self.valor_total is None or self.valor_total < 0:
            errors.append("Valor total é obrigatório e deve ser positivo")

        if self.desconto and self.desconto < 0:
            errors.append("Desconto não pode ser negativo")

        if self.desconto and self.desconto > self.valor_total:
            errors.append("Desconto não pode ser maior que o valor total")

        if self.status not in self.STATUSES:
            errors.append(f"Status inválido. Deve ser um de: {', '.join(self.STATUSES)}")

        if self.metodo_pagamento and self.metodo_pagamento not in self.METODOS_PAGAMENTO:
            errors.append(f"Método de pagamento inválido")

        return errors

    def calcular_valor_final(self) -> float:
        """
        Calcula o valor final da venda
        
        Returns:
            float: Valor final
        """
        self.valor_final = self.valor_total - (self.desconto or 0)
        return round(self.valor_final, 2)

    def aplicar_desconto(self, desconto: float) -> float:
        """
        Aplica um desconto à venda
        
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

    def é_processando(self) -> bool:
        """Verifica se está sendo processada"""
        return self.status == self.STATUS_PROCESSANDO

    def é_enviada(self) -> bool:
        """Verifica se foi enviada"""
        return self.status == self.STATUS_ENVIADA

    def é_entregue(self) -> bool:
        """Verifica se foi entregue"""
        return self.status == self.STATUS_ENTREGUE

    def é_cancelada(self) -> bool:
        """Verifica se foi cancelada"""
        return self.status == self.STATUS_CANCELADA

    def pode_ser_cancelada(self) -> bool:
        """Verifica se pode ser cancelada"""
        return self.é_pendente() and not self.pago

    def mudar_para_processando(self) -> None:
        """Move a venda para processando"""
        if self.é_pendente():
            self.status = self.STATUS_PROCESSANDO
            self.updated_at = datetime.now()

    def mudar_para_enviada(self) -> None:
        """Move a venda para enviada"""
        if self.é_processando():
            self.status = self.STATUS_ENVIADA
            self.updated_at = datetime.now()

    def registrar_entrega(self) -> None:
        """Registra a entrega"""
        if self.é_enviada():
            self.status = self.STATUS_ENTREGUE
            self.data_entrega = datetime.now()
            self.updated_at = datetime.now()

    def cancelar(self) -> None:
        """Cancela a venda"""
        if self.pode_ser_cancelada():
            self.status = self.STATUS_CANCELADA
            self.updated_at = datetime.now()

    def registrar_pagamento(self, metodo: str, data: Optional[datetime] = None) -> None:
        """
        Registra o pagamento
        
        Args:
            metodo (str): Método de pagamento
            data (datetime, optional): Data do pagamento. Padrão: agora
        """
        if metodo not in self.METODOS_PAGAMENTO:
            return
        
        self.pago = True
        self.metodo_pagamento = metodo
        self.data_pagamento = data or datetime.now()
        self.updated_at = datetime.now()

    def pode_ser_entregue(self) -> bool:
        """
        Verifica se pode ser entregue
        
        Returns:
            bool: True se pode ser entregue
        """
        return self.pago and not self.é_entregue() and not self.é_cancelada()

    def gerar_numero_venda(self, prefixo: str = "VEN") -> str:
        """
        Gera um número de venda único
        
        Args:
            prefixo (str): Prefixo do número. Padrão: "VEN"
            
        Returns:
            str: Número de venda gerado
        """
        timestamp = int(self.data_venda.timestamp())
        self.numero_venda = f"{prefixo}-{timestamp}"
        return self.numero_venda

    def está_atrasada_entrega(self) -> bool:
        """
        Verifica se a entrega está atrasada
        
        Returns:
            bool: True se está atrasada
        """
        if not self.data_entrega:
            return False
        return datetime.now() > self.data_entrega and not self.é_entregue()

    def dias_desde_venda(self) -> int:
        """
        Calcula dias desde a venda
        
        Returns:
            int: Número de dias
        """
        diferenca = datetime.now() - self.data_venda
        return diferenca.days

    def dias_para_entrega(self) -> int:
        """
        Calcula dias até a entrega
        
        Returns:
            int: Número de dias (negativo se atrasada)
        """
        if not self.data_entrega:
            return 0
        
        diferenca = self.data_entrega - datetime.now()
        return diferenca.days

    def get_status_pagamento(self) -> str:
        """
        Retorna o status do pagamento
        
        Returns:
            str: Status com ícone
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
            self.STATUS_PROCESSANDO: "⚙️ Processando",
            self.STATUS_ENVIADA: "📦 Enviada",
            self.STATUS_ENTREGUE: "✓ Entregue",
            self.STATUS_CANCELADA: "✗ Cancelada"
        }
        return status_map.get(self.status, self.status)

    def calcular_tempo_entrega(self) -> Optional[int]:
        """
        Calcula o tempo de entrega em dias
        
        Returns:
            int: Número de dias entre venda e entrega
        """
        if not self.data_entrega or not self.é_entregue():
            return None
        
        diferenca = self.data_entrega - self.data_venda
        return diferenca.days

    def get_info_completa(self) -> dict:
        """
        Retorna informações completas da venda
        
        Returns:
            dict: Dicionário com informações da venda
        """
        return {
            "id": self.id_venda,
            "numero_venda": self.numero_venda,
            "cliente_id": self.cliente_id,
            "cliente_nome": self.cliente_nome,
            "data_venda": self.data_venda.isoformat() if self.data_venda else None,
            "data_entrega": self.data_entrega.isoformat() if self.data_entrega else None,
            "status": self.status,
            "status_entrega": self.get_status_entrega(),
            "valor_total": self.valor_total,
            "desconto": self.desconto,
            "valor_final": self.valor_final,
            "moeda": self.moeda,
            "metodo_pagamento": self.metodo_pagamento,
            "data_pagamento": self.data_pagamento.isoformat() if self.data_pagamento else None,
            "pago": self.pago,
            "status_pagamento": self.get_status_pagamento(),
            "numero_rastreamento": self.numero_rastreamento,
            "endereco_entrega": self.endereco_entrega,
            "observacoes": self.observacoes,
            "está_atrasada": self.está_atrasada_entrega(),
            "dias_para_entrega": self.dias_para_entrega(),
            "dias_desde_venda": self.dias_desde_venda(),
            "tempo_entrega": self.calcular_tempo_entrega(),
            "data_criacao": self.created_at.isoformat() if self.created_at else None,
            "data_atualizacao": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        """Representação em string"""
        return f"Venda(id={self.id_venda}, numero='{self.numero_venda}', cliente='{self.cliente_nome}')"

    def __str__(self) -> str:
        """String amigável"""
        return (f"{self.numero_venda} - {self.cliente_nome} - {self.valor_final}€ - "
                f"{self.get_status_entrega()} - {self.get_status_pagamento()}")
