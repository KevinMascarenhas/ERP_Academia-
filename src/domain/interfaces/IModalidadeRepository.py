from abc import ABC, abstractmethod
from domain.entities import Modalidade

class IModalidadeRepository(ABC):
    @abstractmethod
    def adicionar(self, modalidade: Modalidade):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def buscar_por_nome(self, nome: str):
        pass

    @abstractmethod
    def atualizar(self, idx: int, categoria=None, horario=None, dias_semana=None):
        pass

    @abstractmethod
    def remover(self, idx: int):
        pass