from models import *
import repository


def autenticar(email, senha: str):
    usuario = repository.buscar_usuario_por_email(email)
    if usuario and usuario.get_senha() == senha:
        return usuario
    
    administrador = repository.buscar_admin_por_email(email)
    if administrador and administrador.get_senha() == senha:
        return administrador

    aluno = repository.buscar_aluno_por_email(email)
    if aluno and aluno.get_senha() == senha:
        return aluno

    return None


def criar_usuario(nome, email, senha, perfil):
    if not nome or not email or not senha:
        return None, "Todos os campos são obrigatórios."

    if repository.buscar_usuario_por_email(email) or repository.buscar_admin_por_email(email) or repository.buscar_aluno_por_email(email):
        return None, f"Email '{email}' já está cadastrado."

    if perfil == "Administrador":
        u = Administrador(nome, email, senha)
    if perfil == "Usuário":
        u = Usuario(nome, email, senha)
    else:
        return None, "Perfil inválido. Use 'Administrador' ou 'Usuário'."

    repository.adicionar_usuario(u)
    return u, None


def criar_aluno(nome, email, senha, cpf, nome_plano):
    if not nome or not email or not senha or not cpf:
        return None, "Todos os campos são obrigatórios."

    if repository.buscar_usuario_por_email(email) or repository.buscar_aluno_por_email(email):
        return None, f"Email '{email}' já está cadastrado."

    plano = repository.buscar_plano_por_nome(nome_plano)
    if not plano:
        return None, f"Plano '{nome_plano}' não encontrado."

    aluno = Aluno(nome, email, senha, cpf, plano)
    repository.adicionar_aluno(aluno)
    return aluno, None


def registrar_frequencia(idx_aluno, nome_modalidade):
    modalidade = repository.buscar_modalidade_por_nome(nome_modalidade)
    if not modalidade:
        return False, f"Modalidade '{nome_modalidade}' não encontrada."
 
    repository.registrar_frequencia(idx_aluno, modalidade)
    return True, None
 
 
def registrar_treino(idx_aluno, grupo_muscular, series, repeticoes, data):
    if not grupo_muscular or not data:
        return None, "Grupo muscular e data são obrigatórios."
 
    exercicios = exercicios_por_grupo(grupo_muscular)
    if not exercicios:
        return None, f"Grupo muscular '{grupo_muscular}' não reconhecido."
 
    treino = Treino(grupo_muscular, exercicios, series, repeticoes, data)
    repository.registrar_treino(idx_aluno, treino)
    return treino, None
 
 
def criar_plano(nome, preco_str, modalidades_str, duracao_str):
    if not nome:
        return None, "Nome do plano é obrigatório."
 
    try:
        preco       = float(preco_str.replace(",", "."))
        modalidades = int(modalidades_str)
        duracao     = int(duracao_str)
    except ValueError:
        return None, "Preço, modalidades ou duração com valor inválido."
 
    if preco <= 0:
        return None, "O preço deve ser maior que zero."
    if modalidades <= 0:
        return None, "O número de modalidades deve ser maior que zero."
    if duracao <= 0:
        return None, "A duração deve ser maior que zero."
 
    plano = Plano(nome, preco, modalidades, duracao)
    repository.adicionar_plano(plano)
    return plano, None
 
 
def criar_modalidade(nome, categoria, horario):
    if not nome or not categoria or not horario:
        return None, "Todos os campos são obrigatórios."
 
    if repository.buscar_modalidade_por_nome(nome):
        return None, f"Modalidade '{nome}' já existe."
 
    modalidade = Modalidade(nome, categoria, horario)
    repository.adicionar_modalidade(modalidade)
    return modalidade, None
 
 
def exercicios_por_grupo(grupo):
    tabela = {
        "Peito":   ["Supino reto", "Supino inclinado", "Crucifixo", "Crossover"],
        "Costas":  ["Puxada frontal", "Remada curvada", "Remada unilateral", "Pulldown"],
        "Pernas":  ["Agachamento", "Leg press", "Cadeira extensora", "Cadeira flexora"],
        "Ombro":   ["Desenvolvimento com halteres", "Elevação lateral", "Elevação frontal", "Encolhimento"],
        "Bíceps":  ["Rosca direta", "Rosca alternada", "Rosca concentrada", "Rosca martelo"],
        "Tríceps": ["Tríceps testa", "Tríceps pulley", "Tríceps francês", "Mergulho no banco"],
        "Abdômen": ["Abdominal crunch", "Prancha", "Abdominal oblíquo", "Elevação de pernas"]
    }
 
    for chave, exercicios in tabela.items():
        if chave.lower() == grupo.lower():
            return exercicios
 
    return []