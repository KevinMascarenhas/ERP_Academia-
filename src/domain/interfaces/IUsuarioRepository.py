from abc import ABC, abstractmethod
from domain.entities import Usuario

class IUsuarioRepository(ABC):
    @abstractmethod
    def adicionar(self, usuario: Usuario):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def buscar_por_email(self, email: str):
        pass

    @abstractmethod
    def atualizar(self, idx: int, nome=None, email=None, senha=None):
        pass

    @abstractmethod
    def remover(self, idx: int):
        pass
