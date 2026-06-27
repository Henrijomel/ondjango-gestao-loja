# Models/categoria.py
"""
Categoria Model
Representa uma categoria de produtos da loja Ondjango
"""

from Models.base_model import BaseModel
from typing import Optional, List
from datetime import datetime


class Categoria(BaseModel):
    """
    Modelo de Categoria de Produtos
    
    Atributos:
        id_categoria (int): Identificador único da categoria
        nome (str): Nome da categoria
        descricao (str): Descrição detalhada da categoria
        categoria_pai_id (int): ID da categoria pai (para subcategorias)
        codigo (str): Código único da categoria
        icone (str): Ícone ou emoji da categoria
        cor (str): Cor hexadecimal para identificação
        ordem (int): Ordem de exibição
        ativo (bool): Se a categoria está ativa
        total_produtos (int): Total de produtos na categoria
        data_criacao (datetime): Data de criação
        data_atualizacao (datetime): Data da última atualização
    """

    def __init__(
        self,
        id_categoria: Optional[int] = None,
        nome: Optional[str] = None,
        descricao: Optional[str] = None,
        categoria_pai_id: Optional[int] = None,
        codigo: Optional[str] = None,
        icone: Optional[str] = None,
        cor: Optional[str] = None,
        ordem: Optional[int] = 0,
        ativo: bool = True,
        total_produtos: Optional[int] = 0,
        **kwargs
    ):
        """
        Inicializar uma Categoria
        
        Args:
            id_categoria (int, optional): ID da categoria
            nome (str, optional): Nome da categoria
            descricao (str, optional): Descrição da categoria
            categoria_pai_id (int, optional): ID da categoria pai
            codigo (str, optional): Código único da categoria
            icone (str, optional): Ícone/emoji da categoria
            cor (str, optional): Cor hexadecimal
            ordem (int, optional): Ordem de exibição. Padrão: 0
            ativo (bool, optional): Status ativo. Padrão: True
            total_produtos (int, optional): Total de produtos. Padrão: 0
            **kwargs: Atributos adicionais
        """
        super().__init__()

        self.id_categoria = id_categoria
        self.nome = nome
        self.descricao = descricao
        self.categoria_pai_id = categoria_pai_id
        self.codigo = codigo
        self.icone = icone
        self.cor = cor
        self.ordem = ordem
        self.ativo = ativo
        self.total_produtos = total_produtos

        # Processar argumentos adicionais
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def is_valid(self) -> bool:
        """
        Valida a categoria
        
        Returns:
            bool: True se válida
        """
        if not self.nome or not str(self.nome).strip():
            return False
        if not self.codigo or not str(self.codigo).strip():
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
            errors.append("Nome da categoria é obrigatório")

        if not self.codigo or not str(self.codigo).strip():
            errors.append("Código da categoria é obrigatório")

        if self.codigo and len(str(self.codigo)) > 50:
            errors.append("Código não pode ter mais de 50 caracteres")

        if self.cor and not self.é_cor_hexadecimal_valida(self.cor):
            errors.append("Cor deve ser um código hexadecimal válido (#RRGGBB)")

        if self.ordem is not None and self.ordem < 0:
            errors.append("Ordem não pode ser negativa")

        return errors

    @staticmethod
    def é_cor_hexadecimal_valida(cor: str) -> bool:
        """
        Verifica se a cor é um código hexadecimal válido
        
        Args:
            cor (str): Código de cor
            
        Returns:
            bool: True se é válido
        """
        if not cor or not isinstance(cor, str):
            return False
        
        cor = cor.strip()
        if not cor.startswith("#"):
            return False
        
        if len(cor) != 7:
            return False
        
        try:
            int(cor[1:], 16)
            return True
        except ValueError:
            return False

    def é_subcategoria(self) -> bool:
        """
        Verifica se é uma subcategoria
        
        Returns:
            bool: True se é subcategoria
        """
        return self.categoria_pai_id is not None

    def é_categoria_raiz(self) -> bool:
        """
        Verifica se é uma categoria raiz (sem pai)
        
        Returns:
            bool: True se é categoria raiz
        """
        return self.categoria_pai_id is None

    def tem_produtos(self) -> bool:
        """
        Verifica se a categoria tem produtos
        
        Returns:
            bool: True se tem produtos
        """
        return self.total_produtos > 0

    def adicionar_produto(self) -> None:
        """Incrementa o contador de produtos"""
        self.total_produtos = (self.total_produtos or 0) + 1
        self.updated_at = datetime.now()

    def remover_produto(self) -> None:
        """Decrementa o contador de produtos"""
        if self.total_produtos and self.total_produtos > 0:
            self.total_produtos -= 1
            self.updated_at = datetime.now()

    def atualizar_total_produtos(self, quantidade: int) -> None:
        """
        Atualiza o total de produtos
        
        Args:
            quantidade (int): Nova quantidade
        """
        if quantidade >= 0:
            self.total_produtos = quantidade
            self.updated_at = datetime.now()

    def get_nome_display(self) -> str:
        """
        Retorna o nome formatado para exibição
        
        Returns:
            str: Nome com ícone se disponível
        """
        if self.icone:
            return f"{self.icone} {self.nome}"
        return self.nome

    def get_cor_rgb(self) -> tuple:
        """
        Converte a cor hexadecimal para RGB
        
        Returns:
            tuple: Tupla com (R, G, B)
        """
        if not self.cor or not self.é_cor_hexadecimal_valida(self.cor):
            return (200, 200, 200)  # Cor padrão cinzenta
        
        hex_color = self.cor.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def get_cor_rgba(self, alpha: float = 1.0) -> str:
        """
        Converte a cor hexadecimal para RGBA
        
        Args:
            alpha (float): Valor de transparência (0-1)
            
        Returns:
            str: String RGBA
        """
        r, g, b = self.get_cor_rgb()
        return f"rgba({r}, {g}, {b}, {alpha})"

    def get_info_completa(self) -> dict:
        """
        Retorna informações completas da categoria
        
        Returns:
            dict: Dicionário com informações da categoria
        """
        return {
            "id": self.id_categoria,
            "nome": self.nome,
            "nome_display": self.get_nome_display(),
            "descricao": self.descricao,
            "categoria_pai_id": self.categoria_pai_id,
            "é_subcategoria": self.é_subcategoria(),
            "codigo": self.codigo,
            "icone": self.icone,
            "cor": self.cor,
            "cor_rgb": self.get_cor_rgb(),
            "ordem": self.ordem,
            "ativo": self.ativo,
            "total_produtos": self.total_produtos,
            "tem_produtos": self.tem_produtos(),
            "data_criacao": self.created_at.isoformat() if self.created_at else None,
            "data_atualizacao": self.updated_at.isoformat() if self.updated_at else None,
        }

    def desativar(self) -> None:
        """Desativa a categoria"""
        self.ativo = False
        self.updated_at = datetime.now()

    def ativar(self) -> None:
        """Ativa a categoria"""
        self.ativo = True
        self.updated_at = datetime.now()

    def copiar_para_nova(self):
        """
        Cria uma nova categoria com base nesta (para duplicação)
        
        Returns:
            Categoria: Nova categoria com dados copiados
        """
        nova = Categoria(
            nome=f"{self.nome} (Cópia)",
            descricao=self.descricao,
            categoria_pai_id=self.categoria_pai_id,
            codigo=f"{self.codigo}_copia",
            icone=self.icone,
            cor=self.cor,
            ordem=self.ordem,
            ativo=True
        )
        return nova

    def __repr__(self) -> str:
        """Representação em string"""
        return f"Categoria(id={self.id_categoria}, nome='{self.nome}', produtos={self.total_produtos})"

    def __str__(self) -> str:
        """String amigável"""
        status = "✓ Ativa" if self.ativo else "✗ Inativa"
        tipo = "Subcategoria" if self.é_subcategoria() else "Categoria Raiz"
        return f"{self.get_nome_display()} ({tipo}) - {self.total_produtos} produtos - {status}"

    def __lt__(self, other):
        """Comparação para ordenação por ordem"""
        return self.ordem < other.ordem

    def __eq__(self, other):
        """Igualdade baseada no ID"""
        if not isinstance(other, Categoria):
            return False
        return self.id_categoria == other.id_categoria
