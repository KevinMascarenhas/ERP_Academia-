# camada de acesso a dados, onde ficam as funções para manipular os dados do sistema, como adicionar, listar, buscar, atualizar e remover usuários, assinantes, planos e conteúdos. Essas funções operam sobre as listas que armazenam os objetos dessas entidades.
# na 2° etapa, este arquivo sofrerá manutenção para integrar o sistema com um banco de dados, substituindo as listas por consultas e operações de banco. Por enquanto, ele serve como uma camada intermediária para organizar as operações de dados e facilitar a manutenção do código.

from models import *

usuarios  = list[Usuario]()   
planos = list[Plano]()   
modalidades = list[Modalidade]()  
administradores = list[Administrador]() 
alunos = list[Aluno]()

# USUÁRIOS

def adicionar_usuario(usuario, usuario: Usuario):    # para que usuarios seja uma lista de objetos da classe Usuario, defini o type hint "usuario: Usuario". O mesmo ocorre com as outras funções abaixo.
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
 
def atualizar_usuario(idx, nome=None, email=None, senha=None, perfil=None, nome_usuario=None):
    u = usuarios[idx]
    if nome:
        u.set_nome(nome)
    if email:
        u.set_email(email)
    if senha:
        u.set_senha(senha)
    if perfil:
        u.set_perfil(perfil)
    if nome_usuario:
        u.set_nome_usuario(nome_usuario)
 
def remover_usuario(idx):
    return usuarios.pop(idx)
 

# ADMINISTRADORES


def adicionar_administrador(admin, admin: Administrador):    # para que usuarios seja uma lista de objetos da classe Usuario, defini o type hint "usuario: Usuario". O mesmo ocorre com as outras funções abaixo.
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
 
def atualizar_admin(idx, nome=None, email=None, senha=None, perfil=None, nome_usuario=None):
    a = administradores[idx]
    if nome:
        a.set_nome(nome)
    if email:
        a.set_email(email)
    if senha:
        a.set_senha(senha)
    if perfil:
        a.set_perfil(perfil)
    if nome_usuario:
        a.set_nome_usuario(nome_usuario)
 
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
    if nome:
        a.set_nome(nome)
    if email:
        a.set_email(email)
    if cpf:
        a.set_cpf(cpf)
    if plano:
        a.set_plano(plano)
 
def remover_aluno(idx):
    return alunos.pop(idx)
 
def registrar_frequencia(idx, modalidade: Modalidade):
    alunos[idx].frequentar(modalidade)
 
 
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
 
def atualizar_plano(idx, preco=None, telas_simultaneas=None, resolucao=None):
    p = planos[idx]
    if preco is not None:
        p.set_preco(preco)
    if telas_simultaneas is not None:
        p.set_telas_simultaneas(telas_simultaneas)
    if resolucao:
        p.set_resolucao(resolucao)
 
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

def atualizar_modalidade(idx, categoria=None, horario=None):
    m = modalidades[idx]
    if nome:   # nome não pode ser editado, pois é o identificador único da modalidade. Se fosse permitido editar o nome, isso poderia causar problemas de integridade dos dados, já que outras partes do sistema podem estar referenciando a modalidade pelo nome. Por isso, optei por não permitir a edição do nome da modalidade.
        print("O nome da modalidade não pode ser editado.")
    if categoria:
        m.set_categoria(categoria)
    if horario:
        m.set_horario(horario)

def remover_modalidade(idx):
    return modalidades.pop(idx)