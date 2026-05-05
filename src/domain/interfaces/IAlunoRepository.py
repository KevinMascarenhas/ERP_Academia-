from abc import ABC, abstractmethod
from domain.entities import Aluno, Modalidade, Treino

class IAlunoRepository(ABC):
    @abstractmethod
    def adicionar(self, aluno: Aluno):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def buscar_por_email(self, email: str):
        pass

    @abstractmethod
    def buscar_por_nome(self, nome: str):
        pass

    @abstractmethod
    def atualizar(self, idx: int, nome=None, email=None, cpf=None, plano=None):
        pass

    @abstractmethod
    def remover(self, idx: int):
        pass

    @abstractmethod
    def registrar_frequencia(self, idx: int, modalidade: Modalidade, data=None, hora=None):
        pass

    @abstractmethod
    def inscrever_em_modalidade(self, idx: int, modalidade: Modalidade):
        pass

    @abstractmethod
    def cancelar_inscricao_modalidade(self, idx: int, modalidade: Modalidade):
        pass

    @abstractmethod
    def agendar_aula(self, idx: int, modalidade: Modalidade, data, hora):
        pass

    @abstractmethod
    def listar_agenda(self, idx: int):
        pass

    @abstractmethod
    def confirmar_agendamento(self, idx: int, idx_inscricao: int):
        pass

    @abstractmethod
    def cancelar_agendamento(self, idx: int, idx_inscricao: int):
        pass

    @abstractmethod
    def registrar_treino(self, idx: int, treino: Treino):
        pass
