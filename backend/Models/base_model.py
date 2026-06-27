# Models/base_model.py
"""
Base Model Class
Classe base para todos os modelos de dados da aplicação
Fornece funcionalidades comuns como serialização e validação
"""

from datetime import datetime
from typing import Dict, Any, List
import json


class BaseModel:
    """
    Classe base para todos os modelos de dados
    Fornece métodos comuns para serialização e manipulação de dados
    """

    def __init__(self):
        """Inicializar o modelo base"""
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o modelo para dicionário
        
        Returns:
            Dict[str, Any]: Dicionário com os atributos do modelo
        """
        return self.__dict__.copy()

    def to_json(self) -> str:
        """
        Converte o modelo para JSON
        
        Returns:
            str: String JSON com os dados do modelo
        """
        return json.dumps(self.to_dict(), default=str, indent=2)

    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Popula o modelo a partir de um dicionário
        
        Args:
            data (Dict[str, Any]): Dicionário com os dados
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def update(self, **kwargs) -> None:
        """
        Atualiza os atributos do modelo
        
        Args:
            **kwargs: Pares chave-valor com os atributos a atualizar
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

    def __repr__(self) -> str:
        """
        Representação em string do modelo
        
        Returns:
            str: String representando o modelo
        """
        class_name = self.__class__.__name__
        attrs = ', '.join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{class_name}({attrs})"

    def __str__(self) -> str:
        """
        String amigável do modelo
        
        Returns:
            str: String formatada do modelo
        """
        return f"{self.__class__.__name__}({self.to_dict()})"

    def __eq__(self, other) -> bool:
        """
        Compara dois modelos
        
        Args:
            other: Outro modelo para comparação
            
        Returns:
            bool: True se são iguais, False caso contrário
        """
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def is_valid(self) -> bool:
        """
        Valida o modelo (pode ser sobrescrito em subclasses)
        
        Returns:
            bool: True se o modelo é válido
        """
        return True

    def validate(self) -> List[str]:
        """
        Retorna lista de erros de validação (pode ser sobrescrito)
        
        Returns:
            List[str]: Lista de mensagens de erro
        """
        errors = []
        if not self.is_valid():
            errors.append("Modelo inválido")
        return errors

    @classmethod
    def from_json(cls, json_str: str):
        """
        Cria um modelo a partir de uma string JSON
        
        Args:
            json_str (str): String JSON com os dados
            
        Returns:
            BaseModel: Instância do modelo
        """
        data = json.loads(json_str)
        instance = cls()
        instance.from_dict(data)
        return instance

    def get_attribute(self, attr_name: str, default=None) -> Any:
        """
        Obtém um atributo com valor padrão
        
        Args:
            attr_name (str): Nome do atributo
            default: Valor padrão se atributo não existir
            
        Returns:
            Any: Valor do atributo ou valor padrão
        """
        return getattr(self, attr_name, default)

    def has_attribute(self, attr_name: str) -> bool:
        """
        Verifica se o modelo tem um atributo
        
        Args:
            attr_name (str): Nome do atributo
            
        Returns:
            bool: True se tem o atributo
        """
        return hasattr(self, attr_name)

    def get_attributes(self) -> List[str]:
        """
        Retorna lista de nomes de atributos
        
        Returns:
            List[str]: Lista de nomes de atributos
        """
        return list(self.__dict__.keys())

    def get_public_attributes(self) -> Dict[str, Any]:
        """
        Retorna apenas atributos públicos (sem underscore)
        
        Returns:
            Dict[str, Any]: Dicionário com atributos públicos
        """
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    def copy(self):
        """
        Cria uma cópia do modelo
        
        Returns:
            BaseModel: Cópia do modelo
        """
        import copy
        return copy.deepcopy(self)

    def clear(self) -> None:
        """
        Limpa todos os atributos do modelo (exceto timestamps)
        """
        for key in list(self.__dict__.keys()):
            if key not in ['created_at', 'updated_at']:
                setattr(self, key, None)

    def reset_timestamps(self) -> None:
        """
        Reseta os timestamps para o momento atual
        """
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    @property
    def age(self) -> int:
        """
        Retorna a idade do modelo em segundos desde sua criação
        
        Returns:
            int: Número de segundos desde criação
        """
        return int((datetime.now() - self.created_at).total_seconds())

    def __len__(self) -> int:
        """
        Retorna o número de atributos
        
        Returns:
            int: Número de atributos
        """
        return len(self.__dict__)

    def __iter__(self):
        """
        Permite iteração sobre os atributos
        
        Yields:
            tuple: Pares (chave, valor)
        """
        return iter(self.__dict__.items())
