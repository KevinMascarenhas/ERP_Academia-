from abc import ABC, abstractmethod
from domain.entities import Funcionario

class IFuncionarioRepository(ABC):
    @abstractmethod
    def adicionar(self, funcionario: Funcionario):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def buscar_por_email(self, email: str):
        pass

    @abstractmethod
    def buscar_por_id(self, id_funcionario: str):
        pass

    @abstractmethod
    def atualizar(self, idx: int, nome=None, email=None, senha=None):
        pass

    @abstractmethod
    def remover(self, idx: int):
        pass