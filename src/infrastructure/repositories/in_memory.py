# Implementação concreta dos repositórios usando armazenamento em memória. Gerencia todas as operações CRUD de usuários, alunos, planos, modalidades e pagamentos.

from domain.interfaces.repositories import (
    IUsuarioRepository,
    IAdminRepository,
    IAlunoRepository,
    IPlanoRepository,
    IModalidadeRepository,
    IFuncionarioRepository,
    FuncionarioRepository
)
from domain.entities.models import Usuario, Administrador, Aluno, Plano, Modalidade, Treino, Funcionario, Pagamento


class UsuarioRepository(IUsuarioRepository):
    def __init__(self):
        self.usuarios = []

    def adicionar(self, usuario: Usuario):
        self.usuarios.append(usuario)

    def listar(self):
        return list(self.usuarios)

    def buscar_por_email(self, email: str):
        for u in self.usuarios:
            if u.get_email().lower() == email.lower():
                return u
        return None

    def atualizar(self, idx: int, nome=None, email=None, senha=None):
        u = self.usuarios[idx]
        if nome:
            u.set_nome(nome)
        if email:
            u.set_email(email)
        if senha:
            u.set_senha(senha)

    def remover(self, idx: int):
        return self.usuarios.pop(idx)


class AdminRepository(IAdminRepository):
    def __init__(self):
        self.administradores = []

    def adicionar(self, admin: Administrador):
        self.administradores.append(admin)

    def listar(self):
        return list(self.administradores)

    def buscar_por_email(self, email: str):
        for a in self.administradores:
            if a.get_email().lower() == email.lower():
                return a
        return None

    def atualizar(self, idx: int, nome=None, email=None, senha=None):
        a = self.administradores[idx]
        if nome:
            a.set_nome(nome)
        if email:
            a.set_email(email)
        if senha:
            a.set_senha(senha)

    def remover(self, idx: int):
        return self.administradores.pop(idx)


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


class PagamentoRepository:
    # Repositório para gerenciar pagamentos dos alunos.
    
    def __init__(self):
        self.pagamentos = []
    
    def adicionar(self, pagamento: Pagamento):
        self.pagamentos.append(pagamento)
    
    def listar(self):
        return list(self.pagamentos)
    
    def listar_por_aluno(self, aluno: Aluno):
        # Lista todos os pagamentos de um aluno específico.
        return [p for p in self.pagamentos if p.get_aluno() == aluno]
    
    def listar_pendentes(self):
        # Lista todos os pagamentos pendentes.
        return [p for p in self.pagamentos if p.get_status() == Pagamento.STATUS_PENDENTE]
    
    def listar_atrasados(self):
        # Lista todos os pagamentos atrasados.
        return [p for p in self.pagamentos if p.get_status() == Pagamento.STATUS_ATRASADO]
    
    def buscar_por_aluno_mes(self, aluno: Aluno, mes_ano: str):
        # Busca o pagamento de um aluno em um mês específico.
        for p in self.pagamentos:
            if p.get_aluno() == aluno and p.get_mes_ano() == mes_ano:
                return p
        return None
    
    def atualizar_status(self, idx: int, novo_status: str, data_pagamento=None):
        # Atualiza o status de um pagamento.
        p = self.pagamentos[idx]
        if novo_status == Pagamento.STATUS_PAGO:
            p.pagar(data_pagamento)
        elif novo_status == Pagamento.STATUS_ATRASADO:
            p.marcar_atrasado()
    
    def remover(self, idx: int):
        return self.pagamentos.pop(idx)


class FuncionarioRepository(IFuncionarioRepository):
    # Repositório para gerenciar funcionários da academia.
    
    def __init__(self):
        self.funcionarios = []

    def adicionar(self, funcionario: Funcionario):
        self.funcionarios.append(funcionario)

    def listar(self):
        return list(self.funcionarios)

    def buscar_por_email(self, email: str):
        for f in self.funcionarios:
            if f.get_email().lower() == email.lower():
                return f
        return None

    def buscar_por_id(self, id_funcionario: str):
        for f in self.funcionarios:
            if f.get_id() == id_funcionario:
                return f
        return None

    def atualizar(self, idx: int, nome=None, email=None, senha=None):
        f = self.funcionarios[idx]
        if nome:
            f.set_nome(nome)
        if email:
            f.set_email(email)
        if senha:
            f.set_senha(senha)

    def remover(self, idx: int):
        return self.funcionarios.pop(idx)
