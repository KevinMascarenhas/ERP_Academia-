# Menu de administração de alunos. Funcionalidades: CRUD de alunos, registrar frequência, histórico de frequências.

from .menu_admin import selecionar_idx


def listar_alunos(aluno_repo):
    alunos = aluno_repo.listar()
    print("\n--- Alunos ---")
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return
    for i, a in enumerate(alunos):
        plano_nome = a.get_plano().get_nome_plano() if a.get_plano() else "Sem plano"
        print(f"[{i}] {a.get_nome()} | {a.get_email()} | {plano_nome}")


def selecionar_modalidades_cadastro(plano, modalidade_repo):
    limite = plano.get_modalidades_inclusas()
    todas = modalidade_repo.listar()
    if not todas:
        print("Nenhuma modalidade disponível.")
        return []

    print(f"\nSeu plano permite até {limite} modalidade(s). Escolha agora (ou depois no menu).")
    listar_modalidades_disponiveis(modalidade_repo)

    escolhidas = []
    while len(escolhidas) < limite:
        restantes = limite - len(escolhidas)
        resp = input(f"Nome da modalidade ({restantes} restante(s), Enter para pular): ").strip()
        if not resp:
            break
        m = modalidade_repo.buscar_por_nome(resp)
        if not m:
            print(f"Modalidade '{resp}' não encontrada.")
        elif m.get_nome() in [e.get_nome() for e in escolhidas]:
            print("Modalidade já escolhida.")
        else:
            escolhidas.append(m)
            print(f" {m.get_nome()} adicionada.")

    return [m.get_nome() for m in escolhidas]


def listar_modalidades_disponiveis(modalidade_repo):
    modalidades = modalidade_repo.listar()
    print("\n--- Modalidades Disponíveis ---")
    if not modalidades:
        print("Nenhuma modalidade cadastrada.")
        return
    for i, m in enumerate(modalidades):
        dias = f" | Dias: {', '.join(m.get_dias_semana())}" if m.get_dias_semana() else " | Acesso livre"
        print(f"[{i}] {m.get_nome()} | {m.get_categoria()} | {m.get_horario()}{dias}")


def cadastrar_aluno(aluno_repo, plano_repo, modalidade_repo, criar_aluno_uc):
    print("\n--- Cadastrar Aluno ---")
    nome  = input("Nome: ").strip()
    email = input("Email: ").strip()
    senha = input("Senha: ").strip()
    cpf = input("CPF: ").strip()

    listar_planos(plano_repo)
    nome_plano = input("Nome do plano: ").strip()
    plano = plano_repo.buscar_por_nome(nome_plano)
    if not plano:
        print(f"Plano '{nome_plano}' não encontrado. Aluno não cadastrado.")
        return

    nomes_modalidades = selecionar_modalidades_cadastro(plano, modalidade_repo)

    aluno = criar_aluno_uc.executar(nome, email, senha, cpf, nome_plano, nomes_modalidades)
    if not aluno:
        print(f"Não foi possível cadastrar o aluno.")
        return
    print(f"Aluno '{nome}' cadastrado com sucesso!")
    if nomes_modalidades:
        print(f"  Modalidades inscritas: {', '.join(nomes_modalidades)}")


def atualizar_aluno(aluno_repo, plano_repo):
    alunos = aluno_repo.listar()
    idx = selecionar_idx(alunos, lambda: listar_alunos(aluno_repo))
    if idx is None:
        return

    a = alunos[idx]
    nome  = input(f"Novo nome [{a.get_nome()}]: ").strip()
    email = input(f"Novo email [{a.get_email()}]: ").strip()
    cpf = input(f"Novo CPF [{a.get_cpf()}]: ").strip()

    novo_plano = None
    if input("Trocar plano? (s/n): ").strip().lower() == "s":
        listar_planos(plano_repo)
        novo_plano = plano_repo.buscar_por_nome(input("Nome do plano: ").strip())
        if not novo_plano:
            print("Plano não encontrado. Plano não alterado.")

    aluno_repo.atualizar(idx, nome or None, email or None, cpf or None, novo_plano)
    print("Aluno atualizado!")


def remover_aluno(aluno_repo):
    alunos = aluno_repo.listar()
    idx = selecionar_idx(alunos, lambda: listar_alunos(aluno_repo))
    if idx is None:
        return
    removido = aluno_repo.remover(idx)
    print(f"Aluno '{removido.get_nome()}' removido!")


def ver_historico_aluno(aluno_repo, aluno=None):
    if not aluno:
        alunos = aluno_repo.listar()
        idx = selecionar_idx(alunos, lambda: listar_alunos(aluno_repo))
        if idx is None:
            return
        aluno = alunos[idx]

    print(f"\n--- Frequências registradas por {aluno.get_nome()} ---")
    aluno.exibir_info()


def registrar_frequencia(aluno_repo, modalidade_repo, registrar_frequencia_uc, aluno=None):
    if not aluno:
        alunos = aluno_repo.listar()
        idx = selecionar_idx(alunos, lambda: listar_alunos(aluno_repo))
        if idx is None:
            return
    else:
        alunos = aluno_repo.listar()
        idx = alunos.index(aluno)

    listar_modalidades_disponiveis(modalidade_repo)
    nome = input("Nome da modalidade: ").strip()
    data = input("Data (ex: DD/MM/AAAA): ").strip()
    hora = input("Hora (ex: 15:30): ").strip()
    resultado = registrar_frequencia_uc.executar(idx, nome, data, hora)
    if resultado:
        print("Frequência registrada!")
    else:
        print("Não foi possível registrar!")


def listar_planos(plano_repo):
    planos = plano_repo.listar()
    print("\n--- Planos ---")
    if not planos:
        print("Nenhum plano cadastrado.")
        return
    for i, p in enumerate(planos):
        print(f"[{i}] ", end="")
        p.exibir_info()
        print("-" * 40)


def menu_alunos(aluno_repo, plano_repo, modalidade_repo, criar_aluno_uc, registrar_frequencia_uc, sugerir_treino_uc, registrar_treino_uc):
    while True:
        print("\n=== ALUNOS ===")
        print("1 - Cadastrar\n2 - Listar\n3 - Atualizar\n4 - Remover\n5 - Registrar frequência\n6 - Sugestão de treino\n7 - Ver histórico\n0 - Voltar")
        op = input("Escolha: ").strip()
        if op == "1":   
            cadastrar_aluno(aluno_repo, plano_repo, modalidade_repo, criar_aluno_uc)
        elif op == "2": 
            listar_alunos(aluno_repo)
        elif op == "3": 
            atualizar_aluno(aluno_repo, plano_repo)
        elif op == "4": 
            remover_aluno(aluno_repo)
        elif op == "5": 
            registrar_frequencia(aluno_repo, modalidade_repo, registrar_frequencia_uc)
        elif op == "6":
            sugestao_treino(sugerir_treino_uc) 
        elif op == "7": 
            ver_historico_aluno(aluno_repo)
        elif op == "0": 
            break
        else:           
            print("Opção inválida.")


def sugestao_treino(sugerir_treino_uc):
    grupos = ["Peito", "Costas", "Pernas", "Ombro", "Bíceps", "Tríceps", "Abdômen"]
    print("\n--- Sugestão de Treino ---")
    print("Grupos disponíveis:", ", ".join(grupos))
    grupo = input("Grupo muscular: ").strip()
    exercicios = sugerir_treino_uc.executar(grupo)
    if not exercicios:
        print(f"Grupo muscular não encontrado.")
    else:
        print(f"\nExercícios sugeridos para {grupo.capitalize()}:")
        for e in exercicios:
            print(f"  - {e}")
