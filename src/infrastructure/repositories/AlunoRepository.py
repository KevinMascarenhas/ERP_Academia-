from domain.entities.models import Aluno
from domain.entities import Modalidade, Treino
from domain.interfaces import IAlunoRepository

class AlunoRepository(IAlunoRepository):
    def __init__(self):
        self.alunos = []

    def adicionar(self, aluno: Aluno):
        self.alunos.append(aluno)

    def listar(self):
        return list(self.alunos)

    def buscar_por_email(self, email: str):
        for a in self.alunos:
            if a.get_email().lower() == email.lower():
                return a
        return None

    def buscar_por_nome(self, nome: str):
        for a in self.alunos:
            if a.get_nome().lower() == nome.lower():
                return a
        return None

    def atualizar(self, idx: int, nome=None, email=None, cpf=None, plano=None):
        a = self.alunos[idx]
        if nome:
            a.set_nome(nome)
        if email:
            a.set_email(email)
        if cpf:
            a.set_cpf(cpf)
        if plano:
            a.set_plano(plano)

    def remover(self, idx: int):
        return self.alunos.pop(idx)

    def registrar_frequencia(self, idx: int, modalidade: Modalidade, data=None, hora=None):
        self.alunos[idx].frequentar(modalidade, data, hora)

    def inscrever_em_modalidade(self, idx: int, modalidade: Modalidade):
        return self.alunos[idx].inscrever_modalidade(modalidade)

    def cancelar_inscricao_modalidade(self, idx: int, modalidade: Modalidade):
        return self.alunos[idx].cancelar_inscricao_modalidade(modalidade)

    def agendar_aula(self, idx: int, modalidade: Modalidade, data, hora):
        return self.alunos[idx].agendar(modalidade, data, hora)

    def listar_agenda(self, idx: int):
        return self.alunos[idx].get_agenda()

    def confirmar_agendamento(self, idx: int, idx_inscricao: int) -> bool:
        agenda = self.alunos[idx].get_agenda()
        if 0 <= idx_inscricao < len(agenda):
            agenda[idx_inscricao].confirmar()
            return True
        return False

    def cancelar_agendamento(self, idx: int, idx_inscricao: int) -> bool:
        agenda = self.alunos[idx].get_agenda()
        if 0 <= idx_inscricao < len(agenda):
            agenda[idx_inscricao].cancelar()
            return True
        return False

    def registrar_treino(self, idx: int, treino: Treino):
        self.alunos[idx].registrar_treino(treino)

