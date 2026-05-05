from domain.entities import Plano
from domain.interfaces import IPlanoRepository

class PlanoRepository(IPlanoRepository):
    def __init__(self):
        self.planos = []

    def adicionar(self, plano: Plano):
        self.planos.append(plano)

    def listar(self):
        return list(self.planos)

    def buscar_por_nome(self, nome: str):
        for p in self.planos:
            if p.get_nome_plano().lower() == nome.lower():
                return p
        return None

    def atualizar(self, idx: int, preco=None, modalidades_qt=None, duracao=None):
        p = self.planos[idx]
        if preco is not None:
            p.set_preco(preco)
        if modalidades_qt is not None:
            p.set_modalidades_inclusas(modalidades_qt)
        if duracao is not None:
            p.set_duracao_meses(duracao)

    def remover(self, idx: int):
        return self.planos.pop(idx)
