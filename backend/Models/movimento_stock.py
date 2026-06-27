# Models/movimento_stock.py
"""
MovimentoStock Model
Representa um movimento de stock (entrada ou saída de produtos)
"""

from Models.base_model import BaseModel
from typing import Optional, List
from datetime import datetime


class MovimentoStock(BaseModel):
    """
    Modelo de Movimento de Stock
    
    Atributos:
        id_movimento (int): Identificador único do movimento
        produto_id (int): ID do produto
        produto_nome (str): Nome do produto
        tipo_movimento (str): Tipo de movimento (Entrada, Saída, Devolução, Ajuste)
        quantidade (int): Quantidade movimentada
        motivo (str): Motivo do movimento (Compra, Venda, Devolução, Perda, Ajuste, etc)
        referencia_tipo (str): Tipo de referência (Compra, Venda, Devolução)
        referencia_id (int): ID da referência (ID da compra, venda, etc)
        numero_referencia (str): Número/referência do documento (NV, NC)
        quantidade_antes (int): Quantidade antes do movimento
        quantidade_depois (int): Quantidade depois do movimento
        valor_unitario (float): Valor unitário do movimento
        valor_total (float): Valor total do movimento
        utilizador_id (int): ID do utilizador que registou o movimento
        utilizador_nome (str): Nome do utilizador
        observacoes (str): Observações sobre o movimento
        data_movimento (datetime): Data do movimento
        data_criacao (datetime): Data de criação
        data_atualizacao (datetime): Data da última atualização
    """

    # Tipos de movimento
    TIPO_ENTRADA = "Entrada"
    TIPO_SAIDA = "Saída"
    TIPO_DEVOLUCAO = "Devolução"
    TIPO_AJUSTE = "Ajuste"

    TIPOS_MOVIMENTO = [TIPO_ENTRADA, TIPO_SAIDA, TIPO_DEVOLUCAO, TIPO_AJUSTE]

    # Motivos de movimento
    MOTIVO_COMPRA = "Compra"
    MOTIVO_VENDA = "Venda"
    MOTIVO_DEVOLUCAO = "Devolução"
    MOTIVO_PERDA = "Perda"
    MOTIVO_DANO = "Dano"
    MOTIVO_AJUSTE = "Ajuste"
    MOTIVO_INVENTARIO = "Inventário"
    MOTIVO_TRANSFERENCIA = "Transferência"

    MOTIVOS = [MOTIVO_COMPRA, MOTIVO_VENDA, MOTIVO_DEVOLUCAO, MOTIVO_PERDA, 
               MOTIVO_DANO, MOTIVO_AJUSTE, MOTIVO_INVENTARIO, MOTIVO_TRANSFERENCIA]

    # Tipos de referência
    REF_COMPRA = "Compra"
    REF_VENDA = "Venda"
    REF_DEVOLUCAO = "Devolução"
    REF_INTERNO = "Interno"

    def __init__(
        self,
        id_movimento: Optional[int] = None,
        produto_id: Optional[int] = None,
        produto_nome: Optional[str] = None,
        tipo_movimento: Optional[str] = TIPO_ENTRADA,
        quantidade: Optional[int] = 0,
        motivo: Optional[str] = None,
        referencia_tipo: Optional[str] = None,
        referencia_id: Optional[int] = None,
        numero_referencia: Optional[str] = None,
        quantidade_antes: Optional[int] = 0,
        quantidade_depois: Optional[int] = 0,
        valor_unitario: Optional[float] = 0.0,
        valor_total: Optional[float] = 0.0,
        utilizador_id: Optional[int] = None,
        utilizador_nome: Optional[str] = None,
        observacoes: Optional[str] = None,
        data_movimento: Optional[datetime] = None,
        **kwargs
    ):
        """
        Inicializar um Movimento de Stock
        
        Args:
            id_movimento (int, optional): ID do movimento
            produto_id (int, optional): ID do produto
            produto_nome (str, optional): Nome do produto
            tipo_movimento (str, optional): Tipo. Padrão: Entrada
            quantidade (int, optional): Quantidade. Padrão: 0
            motivo (str, optional): Motivo do movimento
            referencia_tipo (str, optional): Tipo de referência
            referencia_id (int, optional): ID da referência
            numero_referencia (str, optional): Número da referência
            quantidade_antes (int, optional): Quantidade antes. Padrão: 0
            quantidade_depois (int, optional): Quantidade depois. Padrão: 0
            valor_unitario (float, optional): Valor unitário. Padrão: 0.0
            valor_total (float, optional): Valor total. Padrão: 0.0
            utilizador_id (int, optional): ID do utilizador
            utilizador_nome (str, optional): Nome do utilizador
            observacoes (str, optional): Observações
            data_movimento (datetime, optional): Data do movimento. Padrão: agora
            **kwargs: Atributos adicionais
        """
        super().__init__()

        self.id_movimento = id_movimento
        self.produto_id = produto_id
        self.produto_nome = produto_nome
        self.tipo_movimento = tipo_movimento
        self.quantidade = quantidade
        self.motivo = motivo
        self.referencia_tipo = referencia_tipo
        self.referencia_id = referencia_id
        self.numero_referencia = numero_referencia
        self.quantidade_antes = quantidade_antes
        self.quantidade_depois = quantidade_depois
        self.valor_unitario = valor_unitario
        self.valor_total = valor_total or (quantidade * valor_unitario)
        self.utilizador_id = utilizador_id
        self.utilizador_nome = utilizador_nome
        self.observacoes = observacoes
        self.data_movimento = data_movimento or datetime.now()

        # Processar argumentos adicionais
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def is_valid(self) -> bool:
        """
        Valida o movimento de stock
        
        Returns:
            bool: True se válido
        """
        if not self.produto_id:
            return False
        if self.quantidade is None or self.quantidade == 0:
            return False
        if self.tipo_movimento not in self.TIPOS_MOVIMENTO:
            return False
        if not self.motivo or self.motivo not in self.MOTIVOS:
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

        if self.quantidade is None or self.quantidade == 0:
            errors.append("Quantidade é obrigatória e deve ser diferente de zero")

        if self.tipo_movimento not in self.TIPOS_MOVIMENTO:
            errors.append(f"Tipo de movimento inválido. Deve ser um de: {', '.join(self.TIPOS_MOVIMENTO)}")

        if not self.motivo or self.motivo not in self.MOTIVOS:
            errors.append(f"Motivo inválido. Deve ser um de: {', '.join(self.MOTIVOS)}")

        if self.valor_unitario and self.valor_unitario < 0:
            errors.append("Valor unitário não pode ser negativo")

        if self.quantidade_antes is not None and self.quantidade_antes < 0:
            errors.append("Quantidade antes não pode ser negativa")

        if self.quantidade_depois is not None and self.quantidade_depois < 0:
            errors.append("Quantidade depois não pode ser negativa")

        return errors

    def é_entrada(self) -> bool:
        """Verifica se é um movimento de entrada"""
        return self.tipo_movimento == self.TIPO_ENTRADA

    def é_saida(self) -> bool:
        """Verifica se é um movimento de saída"""
        return self.tipo_movimento == self.TIPO_SAIDA

    def é_devolucao(self) -> bool:
        """Verifica se é uma devolução"""
        return self.tipo_movimento == self.TIPO_DEVOLUCAO

    def é_ajuste(self) -> bool:
        """Verifica se é um ajuste"""
        return self.tipo_movimento == self.TIPO_AJUSTE

    def calcular_valor_total(self) -> float:
        """
        Calcula o valor total do movimento
        
        Returns:
            float: Valor total
        """
        self.valor_total = self.quantidade * self.valor_unitario
        return round(self.valor_total, 2)

    def calcular_diferenca_quantidade(self) -> int:
        """
        Calcula a diferença de quantidade
        
        Returns:
            int: Diferença (quantidade_depois - quantidade_antes)
        """
        return self.quantidade_depois - self.quantidade_antes

    def é_consistente(self) -> bool:
        """
        Verifica se o movimento é consistente
        
        Returns:
            bool: True se consistente
        """
        diferenca = self.calcular_diferenca_quantidade()
        
        if self.é_entrada():
            return diferenca == self.quantidade
        elif self.é_saida():
            return diferenca == -self.quantidade
        elif self.é_devolucao():
            return diferenca == self.quantidade or diferenca == -self.quantidade
        elif self.é_ajuste():
            return abs(diferenca) == self.quantidade or diferenca == self.quantidade
        
        return True

    def é_saida_para_venda(self) -> bool:
        """
        Verifica se é uma saída relacionada a venda
        
        Returns:
            bool: True se é saída para venda
        """
        return self.é_saida() and (
            self.motivo == self.MOTIVO_VENDA or 
            self.referencia_tipo == self.REF_VENDA
        )

    def é_entrada_de_compra(self) -> bool:
        """
        Verifica se é uma entrada relacionada a compra
        
        Returns:
            bool: True se é entrada de compra
        """
        return self.é_entrada() and (
            self.motivo == self.MOTIVO_COMPRA or 
            self.referencia_tipo == self.REF_COMPRA
        )

    def é_negativa(self) -> bool:
        """
        Verifica se é um movimento negativo (saída/perda)
        
        Returns:
            bool: True se negativo
        """
        return self.é_saida() or self.motivo in [self.MOTIVO_PERDA, self.MOTIVO_DANO]

    def é_positiva(self) -> bool:
        """
        Verifica se é um movimento positivo (entrada)
        
        Returns:
            bool: True se positivo
        """
        return self.é_entrada() or self.é_devolucao()

    def gerar_descricao(self) -> str:
        """
        Gera uma descrição do movimento
        
        Returns:
            str: Descrição formatada
        """
        referencia = f" ({self.numero_referencia})" if self.numero_referencia else ""
        return (f"{self.tipo_movimento} - {self.motivo}: {self.quantidade} unidades "
                f"de {self.produto_nome}{referencia}")

    def é_movimentacao_recente(self, horas: int = 24) -> bool:
        """
        Verifica se o movimento é recente
        
        Args:
            horas (int): Número de horas. Padrão: 24
            
        Returns:
            bool: True se é recente
        """
        diferenca = datetime.now() - self.data_movimento
        return diferenca.total_seconds() < (horas * 3600)

    def horas_desde_movimento(self) -> float:
        """
        Calcula horas desde o movimento
        
        Returns:
            float: Número de horas
        """
        diferenca = datetime.now() - self.data_movimento
        return diferenca.total_seconds() / 3600

    def dias_desde_movimento(self) -> int:
        """
        Calcula dias desde o movimento
        
        Returns:
            int: Número de dias
        """
        diferenca = datetime.now() - self.data_movimento
        return diferenca.days

    def get_sinal_movimento(self) -> str:
        """
        Retorna o sinal do movimento (+/-)
        
        Returns:
            str: Sinal do movimento
        """
        if self.é_positiva():
            return "+"
        elif self.é_negativa():
            return "-"
        return "±"

    def get_icon_tipo(self) -> str:
        """
        Retorna ícone representativo do tipo
        
        Returns:
            str: Ícone com descrição
        """
        icons = {
            self.TIPO_ENTRADA: "📥 Entrada",
            self.TIPO_SAIDA: "📤 Saída",
            self.TIPO_DEVOLUCAO: "🔄 Devolução",
            self.TIPO_AJUSTE: "⚙️ Ajuste"
        }
        return icons.get(self.tipo_movimento, self.tipo_movimento)

    def get_info_completa(self) -> dict:
        """
        Retorna informações completas do movimento
        
        Returns:
            dict: Dicionário com informações do movimento
        """
        return {
            "id": self.id_movimento,
            "produto_id": self.produto_id,
            "produto_nome": self.produto_nome,
            "tipo_movimento": self.tipo_movimento,
            "tipo_icon": self.get_icon_tipo(),
            "quantidade": self.quantidade,
            "sinal": self.get_sinal_movimento(),
            "motivo": self.motivo,
            "referencia_tipo": self.referencia_tipo,
            "referencia_id": self.referencia_id,
            "numero_referencia": self.numero_referencia,
            "quantidade_antes": self.quantidade_antes,
            "quantidade_depois": self.quantidade_depois,
            "diferenca": self.calcular_diferenca_quantidade(),
            "é_consistente": self.é_consistente(),
            "valor_unitario": self.valor_unitario,
            "valor_total": self.calcular_valor_total(),
            "utilizador_id": self.utilizador_id,
            "utilizador_nome": self.utilizador_nome,
            "observacoes": self.observacoes,
            "data_movimento": self.data_movimento.isoformat() if self.data_movimento else None,
            "horas_desde_movimento": self.horas_desde_movimento(),
            "dias_desde_movimento": self.dias_desde_movimento(),
            "é_recente": self.é_movimentacao_recente(),
            "descricao": self.gerar_descricao(),
            "data_criacao": self.created_at.isoformat() if self.created_at else None,
            "data_atualizacao": self.updated_at.isoformat() if self.updated_at else None,
        }

    def get_info_resumida(self) -> dict:
        """
        Retorna informações resumidas do movimento
        
        Returns:
            dict: Dicionário com informações básicas
        """
        return {
            "id": self.id_movimento,
            "produto": self.produto_nome,
            "tipo": self.get_icon_tipo(),
            "quantidade": f"{self.get_sinal_movimento()}{self.quantidade}",
            "motivo": self.motivo,
            "valor": self.calcular_valor_total(),
            "data": self.data_movimento.strftime("%d/%m/%Y %H:%M"),
        }

    def __repr__(self) -> str:
        """Representação em string"""
        return (f"MovimentoStock(id={self.id_movimento}, produto='{self.produto_nome}', "
                f"tipo='{self.tipo_movimento}', qty={self.get_sinal_movimento()}{self.quantidade})")

    def __str__(self) -> str:
        """String amigável"""
        return (f"{self.get_icon_tipo()} - {self.produto_nome} - "
                f"{self.get_sinal_movimento()}{self.quantidade} unidades - "
                f"{self.motivo}")

    def __lt__(self, other):
        """Comparação para ordenação por data"""
        if not isinstance(other, MovimentoStock):
            return False
        return self.data_movimento < other.data_movimento

    def __eq__(self, other):
        """Igualdade baseada no ID"""
        if not isinstance(other, MovimentoStock):
            return False
        return self.id_movimento == other.id_movimento
