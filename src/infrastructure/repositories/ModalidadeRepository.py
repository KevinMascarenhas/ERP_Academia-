from domain.entities import Modalidade
from domain.interfaces import IModalidadeRepository

class ModalidadeRepository(IModalidadeRepository):
    def __init__(self):
        self.modalidades = []

    def adicionar(self, modalidade: Modalidade):
        self.modalidades.append(modalidade)

    def listar(self):
        return list(self.modalidades)

    def buscar_por_nome(self, nome: str):
        for m in self.modalidades:
            if m.get_nome().lower() == nome.lower():
                return m
        return None

    def atualizar(self, idx: int, categoria=None, horario=None, dias_semana=None):
        m = self.modalidades[idx]
        if categoria:
            m.set_categoria(categoria)
        if horario:
            m.set_horario(horario)
        if dias_semana is not None:
            m.set_dias_semana(dias_semana)

    def remover(self, idx: int):
        return self.modalidades.pop(idx)
