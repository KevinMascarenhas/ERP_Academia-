# Camada de acesso a dados.
# Na 2ª etapa, este arquivo será integrado com banco de dados.

from models import *

usuarios = []
planos = []
modalidades = []
administradores = []
alunos = []


# USUÁRIOS 

def adicionar_usuario(usuario: Usuario):
    usuarios.append(usuario)

def listar_usuarios():
    return list(usuarios)

def buscar_usuario_por_nome(nome):
    for u in usuarios:
        if u.get_nome().lower() == nome.lower():
            return u
    return None

def buscar_usuario_por_email(email):
    for u in usuarios:
        if u.get_email().lower() == email.lower():
            return u
    return None

def atualizar_usuario(idx, nome=None, email=None, senha=None):
    u = usuarios[idx]
    if nome:  u.set_nome(nome)
    if email: u.set_email(email)
    if senha: u.set_senha(senha)

def remover_usuario(idx):
    return usuarios.pop(idx)


# ADMINISTRADORES 

def adicionar_administrador(admin: Administrador):
    administradores.append(admin)

def listar_administradores():
    return list(administradores)

def buscar_admin_por_nome(nome):
    for a in administradores:
        if a.get_nome().lower() == nome.lower():
            return a
    return None

def buscar_admin_por_email(email):
    for a in administradores:
        if a.get_email().lower() == email.lower():
            return a
    return None

def atualizar_admin(idx, nome=None, email=None, senha=None):
    a = administradores[idx]
    if nome:  a.set_nome(nome)
    if email: a.set_email(email)
    if senha: a.set_senha(senha)

def remover_admin(idx):
    return administradores.pop(idx)


# ALUNOS 

def adicionar_aluno(aluno: Aluno):
    alunos.append(aluno)

def listar_alunos():
    return list(alunos)

def buscar_aluno_por_nome(nome):
    for a in alunos:
        if a.get_nome().lower() == nome.lower():
            return a
    return None

def buscar_aluno_por_email(email):
    for a in alunos:
        if a.get_email().lower() == email.lower():
            return a
    return None

def atualizar_aluno(idx, nome=None, email=None, cpf=None, plano=None):
    a = alunos[idx]
    if nome:  a.set_nome(nome)
    if email: a.set_email(email)
    if cpf:   a.set_cpf(cpf)
    if plano: a.set_plano(plano)

def remover_aluno(idx):
    return alunos.pop(idx)

def registrar_frequencia(idx, modalidade: Modalidade, data=None, hora=None):
    alunos[idx].frequentar(modalidade, data, hora)


# INSCRIÇÕES EM MODALIDADES FIXAS 

def inscrever_aluno_em_modalidade(idx_aluno, modalidade: Modalidade):
    return alunos[idx_aluno].inscrever_modalidade(modalidade)

def cancelar_inscricao_modalidade(idx_aluno, modalidade: Modalidade):
    # Cancela a inscrição do aluno em uma modalidade com horário fixo
    return alunos[idx_aluno].cancelar_inscricao_modalidade(modalidade)

def listar_modalidades_aluno(idx_aluno):
    """Retorna as modalidades nas quais o aluno está inscrito."""
    return alunos[idx_aluno].get_modalidades_inscritas()


# AGENDA / AGENDAMENTOS 

def agendar_aula(idx_aluno, modalidade: Modalidade, data, hora):
    return alunos[idx_aluno].agendar(modalidade, data, hora)

def listar_agenda_aluno(idx_aluno):
    return alunos[idx_aluno].get_agenda()

def confirmar_agendamento(idx_aluno, idx_inscricao):
    agenda = alunos[idx_aluno].get_agenda()
    if 0 <= idx_inscricao < len(agenda):
        agenda[idx_inscricao].confirmar()
        return True
    return False

def cancelar_agendamento(idx_aluno, idx_inscricao):
    agenda = alunos[idx_aluno].get_agenda()
    if 0 <= idx_inscricao < len(agenda):
        agenda[idx_inscricao].cancelar()
        return True
    return False


# PLANOS 

def adicionar_plano(plano: Plano):
    planos.append(plano)

def listar_planos():
    return list(planos)

def buscar_plano_por_nome(nome_plano):
    for p in planos:
        if p.get_nome_plano().lower() == nome_plano.lower():
            return p
    return None

def atualizar_plano(idx, preco=None, modalidades_qt=None, duracao=None):
    p = planos[idx]
    if preco is not None:        p.set_preco(preco)
    if modalidades_qt is not None: p.set_modalidades_inclusas(modalidades_qt)
    if duracao is not None:      p.set_duracao_meses(duracao)

def remover_plano(idx):
    return planos.pop(idx)


# MODALIDADES 

def adicionar_modalidade(modalidade: Modalidade):
    modalidades.append(modalidade)

def listar_modalidades():
    return list(modalidades)

def buscar_modalidade_por_nome(nome):
    for m in modalidades:
        if m.get_nome().lower() == nome.lower():
            return m
    return None

def atualizar_modalidade(idx, nome=None, categoria=None, horario=None, dias_semana=None):
    m = modalidades[idx]
    if nome:        # nome não pode ser editado (identificador único)
        print("O nome da modalidade não pode ser editado.")
    if categoria:   m.set_categoria(categoria)
    if horario:     m.set_horario(horario)
    if dias_semana is not None: m.set_dias_semana(dias_semana)

def remover_modalidade(idx):
    return modalidades.pop(idx)


# TREINOS 

def registrar_treino(idx, treino: Treino):
    alunos[idx].registrar_treino(treino)


# SEED 

def inicializar_dados():
    adicionar_administrador(Administrador("Admin", "admin@academia.com", "1234"))
    adicionar_usuario(Administrador("Admin", "admin@academia.com", "1234"))

    adicionar_plano(Plano("Básico", 59.90,  1, 1))
    adicionar_plano(Plano("Standard", 99.90,  3, 1))
    adicionar_plano(Plano("Premium(Anual)", 85.90,  5, 12))

    adicionar_modalidade(Modalidade("Musculação", "Força", "06:00 - 22:00"))
    adicionar_modalidade(Modalidade("Natação", "Aquática", "07:00 - 08:00", ["Terça", "Quinta"]))
    adicionar_modalidade(Modalidade("Yoga", "Relaxamento", "08:00 - 09:00", ["Segunda", "Quarta", "Sexta"]))
    adicionar_modalidade(Modalidade("Muay Thai", "Luta", "19:00 - 20:30", ["Segunda", "Quarta"]))

    # Aluno de exemplo com plano Standard (3 modalidades)
    plano_standard = buscar_plano_por_nome("Standard")
    joao = Aluno("João Silva", "joao@email.com", "1234", "111.111.111-11", plano_standard)

    joao.inscrever_modalidade(listar_modalidades()[0])  # Musculação
    joao.inscrever_modalidade(listar_modalidades()[3])  # Muay Thai

    # Agenda uma aula de Natação (pendente) e outra confirmada
    ins1 = joao.agendar(listar_modalidades()[3], "15/04/2026", "19:00")
    ins2 = joao.agendar(listar_modalidades()[3], "20/04/2026", "20:00")
    ins2.confirmar()
    adicionar_aluno(joao)

    # Aluno Kevin sem plano definido ainda
    adicionar_aluno(Aluno("Kevin Mascarenhas", "kevin@gmail.com", "1234", "123.456.789-00", None))