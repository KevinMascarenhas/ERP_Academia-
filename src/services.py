from models import *
import repository


# AUTENTICAÇÃO 
def autenticar(email, senha: str):
    for busca in [
        repository.buscar_usuario_por_email,
        repository.buscar_admin_por_email,
        repository.buscar_aluno_por_email,
    ]:
        u = busca(email)
        if u and u.get_senha() == senha:
            return u
    return None


# USUÁRIOS / ADMINISTRADORES 

def criar_usuario(nome, email, senha, perfil):
    if not nome or not email or not senha:
        return None, "Todos os campos são obrigatórios."

    if (repository.buscar_usuario_por_email(email)
            or repository.buscar_admin_por_email(email)
            or repository.buscar_aluno_por_email(email)):
        return None, f"Email '{email}' já está cadastrado."

    if perfil.lower() == "administrador":
        u = Administrador(nome, email, senha)
        repository.adicionar_administrador(u)
        repository.adicionar_usuario(u)
        return u, None

    return None, "Perfil inválido. Use 'Administrador'."


# ALUNOS 

def criar_aluno(nome, email, senha, cpf, nome_plano, nomes_modalidades=None):
    if not nome or not email or not senha or not cpf:
        return None, "Todos os campos são obrigatórios."

    if repository.buscar_usuario_por_email(email) or repository.buscar_aluno_por_email(email):
        return None, f"Email '{email}' já está cadastrado."

    plano = repository.buscar_plano_por_nome(nome_plano)
    if not plano:
        return None, f"Plano '{nome_plano}' não encontrado."

    aluno = Aluno(nome, email, senha, cpf, plano)

    # Inscreve nas modalidades escolhidas, respeitando o limite do plano
    erros_modal = []
    if nomes_modalidades:
        for nm in nomes_modalidades:
            m = repository.buscar_modalidade_por_nome(nm)
            if not m:
                erros_modal.append(f"Modalidade '{nm}' não encontrada.")
                continue
            ok, err = aluno.inscrever_modalidade(m)
            if not ok:
                erros_modal.append(err)

    repository.adicionar_aluno(aluno)
    aviso = (" Avisos: " + " | ".join(erros_modal)) if erros_modal else ""
    return aluno, aviso if aviso else None


# FREQUÊNCIA LIVRE 

def registrar_frequencia(idx_aluno, nome_modalidade, data=None, hora=None):
    # Registra acesso livre (musculação ou modalidade sem agendamento).
    modalidade = repository.buscar_modalidade_por_nome(nome_modalidade)
    if not modalidade:
        return f"Modalidade '{nome_modalidade}' não encontrada."
    repository.registrar_frequencia(idx_aluno, modalidade, data, hora)
    return None


# INSCRIÇÃO EM MODALIDADES FIXAS 

def inscrever_em_modalidade(idx_aluno, nome_modalidade):
    # Matricula o aluno em uma modalidade com horário fixo.
    modalidade = repository.buscar_modalidade_por_nome(nome_modalidade)
    if not modalidade:
        return None, f"Modalidade '{nome_modalidade}' não encontrada."
    ok, erro = repository.inscrever_aluno_em_modalidade(idx_aluno, modalidade)
    if not ok:
        return None, erro
    return modalidade, None


def cancelar_inscricao_modalidade(idx_aluno, nome_modalidade):
    # Remove o aluno de uma modalidade fixa.
    modalidade = repository.buscar_modalidade_por_nome(nome_modalidade)
    if not modalidade:
        return f"Modalidade '{nome_modalidade}' não encontrada."
    ok, erro = repository.cancelar_inscricao_modalidade(idx_aluno, modalidade)
    return erro if not ok else None


# AGENDA / AGENDAMENTOS 

def agendar_aula(idx_aluno, nome_modalidade, data, hora):
    # Agenda uma aula para o aluno. O aluno deve estar inscrito na modalidade.
    modalidade = repository.buscar_modalidade_por_nome(nome_modalidade)
    if not modalidade:
        return None, f"Modalidade '{nome_modalidade}' não encontrada."

    aluno = repository.listar_alunos()[idx_aluno]
    if modalidade not in aluno.get_modalidades_inscritas():
        return None, f"Você não está matriculado em '{nome_modalidade}'. Inscreva-se primeiro."

    if not data or not hora:
        return None, "Data e hora são obrigatórios."

    ins = repository.agendar_aula(idx_aluno, modalidade, data, hora)
    return ins, None


def confirmar_agendamento(idx_aluno, idx_inscricao):
    ok = repository.confirmar_agendamento(idx_aluno, idx_inscricao)
    return None if ok else "Agendamento não encontrado."


def cancelar_agendamento(idx_aluno, idx_inscricao):
    ok = repository.cancelar_agendamento(idx_aluno, idx_inscricao)
    return None if ok else "Agendamento não encontrado."


# PLANOS 

def criar_plano(nome, preco_str, modalidades_str, duracao_str):
    if not nome:
        return None, "Nome do plano é obrigatório."
    try:
        preco = float(preco_str.replace(",", "."))
        modalidades = int(modalidades_str)
        duracao = int(duracao_str)
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


# MODALIDADES

def criar_modalidade(nome, categoria, horario, dias_semana=None):
    if not nome or not categoria or not horario:
        return None, "Todos os campos são obrigatórios."
    if repository.buscar_modalidade_por_nome(nome):
        return None, f"Modalidade '{nome}' já existe."
    modalidade = Modalidade(nome, categoria, horario, dias_semana)
    repository.adicionar_modalidade(modalidade)
    return modalidade, None


# TREINOS 

def registrar_treino(idx_aluno, grupo_muscular, series, repeticoes, data):
    if not grupo_muscular or not data:
        return None, "Grupo muscular e data são obrigatórios."
    exercicios = exercicios_por_grupo(grupo_muscular)
    if not exercicios:
        return None, f"Grupo muscular '{grupo_muscular}' não reconhecido."
    treino = Treino(grupo_muscular, exercicios, series, repeticoes, data)
    repository.registrar_treino(idx_aluno, treino)
    return treino, None


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

def sugerir_treino(grupo):
    exercicios = exercicios_por_grupo(grupo)
    if not exercicios:
        return None, f"Grupo muscular '{grupo}' não reconhecido."
    return exercicios, None