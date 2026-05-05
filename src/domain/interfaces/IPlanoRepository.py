from abc import ABC, abstractmethod
from domain.entities import Plano

class IPlanoRepository(ABC):
    @abstractmethod
    def adicionar(self, plano: Plano):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def buscar_por_nome(self, nome: str):
        pass

    @abstractmethod
    def atualizar(self, idx: int, preco=None, modalidades_qt=None, duracao=None):
        pass

    @abstractmethod
    def remover(self, idx: int):
        pass