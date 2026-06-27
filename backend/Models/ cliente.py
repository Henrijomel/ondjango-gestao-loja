# Models/cliente.py
"""
Cliente Model
Representa um cliente da loja Ondjango
"""

from Models.base_model import BaseModel
from typing import Optional, List
from datetime import datetime


class Cliente(BaseModel):
    """
    Modelo de Cliente
    
    Atributos:
        id_cliente (int): Identificador único do cliente
        nome (str): Nome completo do cliente
        email (str): Email do cliente
        telefone (str): Telefone do cliente
        endereco (str): Endereço do cliente
        cidade (str): Cidade do cliente
        codigo_postal (str): Código postal
        pais (str): País do cliente
        tipo_cliente (str): Tipo de cliente (Pessoa Física ou Jurídica)
        numero_id (str): Número de ID (NIF/NIPC)
        data_nascimento (str): Data de nascimento
        genero (str): Género (M/F/Outro)
        ativo (bool): Se o cliente está ativo
        data_criacao (datetime): Data de criação
        data_atualizacao (datetime): Data da última atualização
    """

    def __init__(
        self,
        id_cliente: Optional[int] = None,
        nome: Optional[str] = None,
        email: Optional[str] = None,
        telefone: Optional[str] = None,
        endereco: Optional[str] = None,
        cidade: Optional[str] = None,
        codigo_postal: Optional[str] = None,
        pais: Optional[str] = "Portugal",
        tipo_cliente: Optional[str] = "Pessoa Física",
        numero_id: Optional[str] = None,
        data_nascimento: Optional[str] = None,
        genero: Optional[str] = None,
        ativo: bool = True,
        **kwargs
    ):
        """
        Inicializar um Cliente
        
        Args:
            id_cliente (int, optional): ID do cliente
            nome (str, optional): Nome do cliente
            email (str, optional): Email do cliente
            telefone (str, optional): Telefone do cliente
            endereco (str, optional): Endereço do cliente
            cidade (str, optional): Cidade do cliente
            codigo_postal (str, optional): Código postal
            pais (str, optional): País. Padrão: "Portugal"
            tipo_cliente (str, optional): Tipo. Padrão: "Pessoa Física"
            numero_id (str, optional): Número de ID (NIF/NIPC)
            data_nascimento (str, optional): Data de nascimento
            genero (str, optional): Género
            ativo (bool, optional): Status ativo. Padrão: True
            **kwargs: Atributos adicionais
        """
        super().__init__()

        self.id_cliente = id_cliente
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.cidade = cidade
        self.codigo_postal = codigo_postal
        self.pais = pais
        self.tipo_cliente = tipo_cliente
        self.numero_id = numero_id
        self.data_nascimento = data_nascimento
        self.genero = genero
        self.ativo = ativo

        # Processar argumentos adicionais
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def is_valid(self) -> bool:
        """
        Valida o cliente
        
        Returns:
            bool: True se válido
        """
        if not self.nome or not str(self.nome).strip():
            return False
        if not self.email or "@" not in str(self.email):
            return False
        if not self.telefone or len(str(self.telefone)) < 9:
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

        if self.numero_id and len(str(self.numero_id)) < 9:
            errors.append("NIF/NIPC inválido")

        if self.genero and self.genero not in ["M", "F", "Outro"]:
            errors.append("Género inválido (M/F/Outro)")

        return errors

    def get_info_completa(self) -> dict:
        """
        Retorna informações completas do cliente
        
        Returns:
            dict: Dicionário com informações do cliente
        """
        return {
            "id": self.id_cliente,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "endereco": self.endereco,
            "cidade": self.cidade,
            "codigo_postal": self.codigo_postal,
            "pais": self.pais,
            "tipo_cliente": self.tipo_cliente,
            "numero_id": self.numero_id,
            "data_nascimento": self.data_nascimento,
            "genero": self.genero,
            "ativo": self.ativo,
            "data_criacao": self.created_at.isoformat() if self.created_at else None,
            "data_atualizacao": self.updated_at.isoformat() if self.updated_at else None,
        }

    def get_nome_completo(self) -> str:
        """
        Retorna o nome completo formatado
        
        Returns:
            str: Nome do cliente
        """
        return str(self.nome).strip() if self.nome else "Sem Nome"

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

    def é_pessoa_juridica(self) -> bool:
        """
        Verifica se é pessoa jurídica
        
        Returns:
            bool: True se é pessoa jurídica
        """
        return self.tipo_cliente == "Pessoa Jurídica"

    def é_pessoa_fisica(self) -> bool:
        """
        Verifica se é pessoa física
        
        Returns:
            bool: True se é pessoa física
        """
        return self.tipo_cliente == "Pessoa Física"

    def desativar(self) -> None:
        """Desativa o cliente"""
        self.ativo = False
        self.updated_at = datetime.now()

    def ativar(self) -> None:
        """Ativa o cliente"""
        self.ativo = True
        self.updated_at = datetime.now()

    def __repr__(self) -> str:
        """Representação em string"""
        return f"Cliente(id={self.id_cliente}, nome='{self.nome}', email='{self.email}')"

    def __str__(self) -> str:
        """String amigável"""
        status = "✓ Ativo" if self.ativo else "✗ Inativo"
        return f"{self.get_nome_completo()} ({self.email}) - {status}"
