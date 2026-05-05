from abc import ABC, abstractmethod
from domain.entities import Pagamento, Aluno


class IPagamentoRepository(ABC):
    @abstractmethod
    def adicionar(self, pagamento: Pagamento):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def listar_por_aluno(self, aluno: Aluno):
        pass

    @abstractmethod
    def listar_pendentes(self):
        pass

    @abstractmethod
    def listar_atrasados(self):
        pass

    @abstractmethod
    def buscar_por_aluno_mes(self, aluno: Aluno, mes_ano: str):
        pass

    @abstractmethod
    def atualizar_status(self, idx: int, novo_status: str, data_pagamento=None):
        pass

    @abstractmethod
    def remover(self, idx: int):
        pass
    
    