# Models/fornecedor.py
"""
Fornecedor Model
Representa um fornecedor da loja Ondjango
"""

from Models.base_model import BaseModel
from typing import Optional, List
from datetime import datetime

class Fornecedor(BaseModel):
    """
    Modelo de Fornecedor
    
    Atributos:
        id_fornecedor (int): Identificador único do fornecedor
        nome (str): Nome da empresa fornecedora
        email (str): Email do fornecedor
        telefone (str): Telefone do fornecedor
        endereco (str): Endereço do fornecedor
        cidade (str): Cidade do fornecedor
        codigo_postal (str): Código postal
        pais (str): País do fornecedor
        numero_id (str): Número de ID (NIPC)
        nome_contacto (str): Nome da pessoa de contacto
        telefone_contacto (str): Telefone da pessoa de contacto
        email_contacto (str): Email da pessoa de contacto
        categoria_fornecimento (str): Categoria de produtos que fornece
        condicoes_pagamento (str): Condições de pagamento
        margem_lucro (float): Margem de lucro aplicada aos produtos
        prazo_entrega_dias (int): Prazo de entrega em dias
        ativo (bool): Se o fornecedor está ativo
        rating (float): Avaliação do fornecedor (0-5)
        data_criacao (datetime): Data de criação
        data_atualizacao (datetime): Data da última atualização
    """

    def __init__(
        self,
        id_fornecedor: Optional[int] = None,
        nome: Optional[str] = None,
        email: Optional[str] = None,
        telefone: Optional[str] = None,
        endereco: Optional[str] = None,
        cidade: Optional[str] = None,
        codigo_postal: Optional[str] = None,
        pais: Optional[str] = "Portugal",
        numero_id: Optional[str] = None,
        nome_contacto: Optional[str] = None,
        telefone_contacto: Optional[str] = None,
        email_contacto: Optional[str] = None,
        categoria_fornecimento: Optional[str] = None,
        condicoes_pagamento: Optional[str] = "30 dias",
        margem_lucro: Optional[float] = 0.0,
        prazo_entrega_dias: Optional[int] = 7,
        ativo: bool = True,
        rating: Optional[float] = 0.0,
        **kwargs
    ):
        """
        Inicializar um Fornecedor
        
        Args:
            id_fornecedor (int, optional): ID do fornecedor
            nome (str, optional): Nome da empresa
            email (str, optional): Email do fornecedor
            telefone (str, optional): Telefone do fornecedor
            endereco (str, optional): Endereço do fornecedor
            cidade (str, optional): Cidade do fornecedor
            codigo_postal (str, optional): Código postal
            pais (str, optional): País. Padrão: "Portugal"
            numero_id (str, optional): Número de ID (NIPC)
            nome_contacto (str, optional): Nome da pessoa de contacto
            telefone_contacto (str, optional): Telefone da pessoa de contacto
            email_contacto (str, optional): Email da pessoa de contacto
            categoria_fornecimento (str, optional): Categoria de fornecimento
            condicoes_pagamento (str, optional): Condições. Padrão: "30 dias"
            margem_lucro (float, optional): Margem de lucro. Padrão: 0.0
            prazo_entrega_dias (int, optional): Prazo em dias. Padrão: 7
            ativo (bool, optional): Status ativo. Padrão: True
            rating (float, optional): Avaliação. Padrão: 0.0
            **kwargs: Atributos adicionais
        """
        super().__init__()

        self.id_fornecedor = id_fornecedor
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.cidade = cidade
        self.codigo_postal = codigo_postal
        self.pais = pais
        self.numero_id = numero_id
        self.nome_contacto = nome_contacto
        self.telefone_contacto = telefone_contacto
        self.email_contacto = email_contacto
        self.categoria_fornecimento = categoria_fornecimento
        self.condicoes_pagamento = condicoes_pagamento
        self.margem_lucro = margem_lucro
        self.prazo_entrega_dias = prazo_entrega_dias
        self.ativo = ativo
        self.rating = rating

        # Processar argumentos adicionais
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def is_valid(self) -> bool:
        """
        Valida o fornecedor
        
        Returns:
            bool: True se válido
        """
        if not self.nome or not str(self.nome).strip():
            return False
        if not self.email or "@" not in str(self.email):
            return False
        if not self.telefone or len(str(self.telefone)) < 9:
            return False
        if not self.numero_id or len(str(self.numero_id)) < 8:
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
            errors.append("Nome é obrigatório")

        if not self.email:
            errors.append("Email é obrigatório")
        elif "@" not in str(self.email):
            errors.append("Email inválido")

        if not self.telefone:
            errors.append("Telefone é obrigatório")
        elif len(str(self.telefone)) < 9:
            errors.append("Telefone deve ter pelo menos 9 dígitos")

        if not self.numero_id:
            errors.append("Número de ID (NIPC) é obrigatório")
        elif len(str(self.numero_id)) < 8:
            errors.append("NIPC inválido")

        if self.margem_lucro and (self.margem_lucro < 0 or self.margem_lucro > 100):
            errors.append("Margem de lucro deve estar entre 0 e 100")

        if self.rating and (self.rating < 0 or self.rating > 5):
            errors.append("Rating deve estar entre 0 e 5")

        if self.prazo_entrega_dias and self.prazo_entrega_dias < 0:
            errors.append("Prazo de entrega não pode ser negativo")

        return errors

    def get_info_completa(self) -> dict:
        """
        Retorna informações completas do fornecedor
        
        Returns:
            dict: Dicionário com informações do fornecedor
        """
        return {
            "id": self.id_fornecedor,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "endereco": self.endereco,
            "cidade": self.cidade,
            "codigo_postal": self.codigo_postal,
            "pais": self.pais,
            "numero_id": self.numero_id,
            "nome_contacto": self.nome_contacto,
            "telefone_contacto": self.telefone_contacto,
            "email_contacto": self.email_contacto,
            "categoria_fornecimento": self.categoria_fornecimento,
            "condicoes_pagamento": self.condicoes_pagamento,
            "margem_lucro": self.margem_lucro,
            "prazo_entrega_dias": self.prazo_entrega_dias,
            "ativo": self.ativo,
            "rating": self.rating,
            "data_criacao": self.created_at.isoformat() if self.created_at else None,
            "data_atualizacao": self.updated_at.isoformat() if self.updated_at else None,
        }

    def get_contacto_principal(self) -> dict:
        """
        Retorna dados do contacto principal
        
        Returns:
            dict: Dicionário com dados de contacto
        """
        return {
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone
        }

    def get_contacto_alternativo(self) -> dict:
        """
        Retorna dados do contacto alternativo
        
        Returns:
            dict: Dicionário com dados de contacto alternativo
        """
        return {
            "nome": self.nome_contacto,
            "email": self.email_contacto,
            "telefone": self.telefone_contacto
        }

    def get_endereco_completo(self) -> str:
        """
        Retorna o endereço completo formatado
        
        Returns:
            str: Endereço completo
        """
        partes = []
        if self.endereco:
            partes.append(str(self.endereco))
        if self.codigo_postal:
            partes.append(str(self.codigo_postal))
        if self.cidade:
            partes.append(str(self.cidade))
        if self.pais:
            partes.append(str(self.pais))

        return ", ".join(partes) if partes else "Endereço não cadastrado"

    def get_rating_stars(self) -> str:
        """
        Retorna a avaliação em formato de estrelas
        
        Returns:
            str: Estrelas representando o rating
        """
        if not self.rating:
            return "☆☆☆☆☆"
        
        stars = int(self.rating)
        half_star = "½" if (self.rating % 1) >= 0.5 else ""
        
        return ("★" * stars) + half_star + ("☆" * (5 - stars - (1 if half_star else 0)))

    def pode_fornecer(self, categoria: str) -> bool:
        """
        Verifica se o fornecedor pode fornecer uma categoria
        
        Args:
            categoria (str): Categoria a verificar
            
        Returns:
            bool: True se pode fornecer
        """
        if not self.categoria_fornecimento or not self.ativo:
            return False
        
        categorias = str(self.categoria_fornecimento).lower().split(",")
        return categoria.lower().strip() in [c.strip() for c in categorias]

    def desativar(self) -> None:
        """Desativa o fornecedor"""
        self.ativo = False
        self.updated_at = datetime.now()

    def ativar(self) -> None:
        """Ativa o fornecedor"""
        self.ativo = True
        self.updated_at = datetime.now()

    def atualizar_rating(self, novo_rating: float) -> None:
        """
        Atualiza o rating do fornecedor
        
        Args:
            novo_rating (float): Novo rating (0-5)
        """
        if 0 <= novo_rating <= 5:
            self.rating = novo_rating
            self.updated_at = datetime.now()

    def é_confiavel(self) -> bool:
        """
        Verifica se o fornecedor é confiável (rating >= 4)
        
        Returns:
            bool: True se é confiável
        """
        return self.ativo and self.rating >= 4.0

    def __repr__(self) -> str:
        """Representação em string"""
        return f"Fornecedor(id={self.id_fornecedor}, nome='{self.nome}', email='{self.email}')"

    def __str__(self) -> str:
        """String amigável"""
        status = "✓ Ativo" if self.ativo else "✗ Inativo"
        return f"{self.nome} ({self.numero_id}) - {self.get_rating_stars()} - {status}"
