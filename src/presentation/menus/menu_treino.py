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


def ver_historico_treinos(aluno_repo):
    alunos = aluno_repo.listar()
    print("\n--- Ver Histórico de Treinos ---")
    for i, a in enumerate(alunos):
        print(f"[{i}] {a.get_nome()}")
    
    try:
        idx = int(input("Escolha um aluno (idx): ").strip())
    except ValueError:
        return

    if not (0 <= idx < len(alunos)):
        print("Índice inválido.")
        return

    aluno = alunos[idx]
    print(f"\n--- Histórico de Treinos de {aluno.get_nome()} ---")
    aluno.exibir_info()


def registrar_treino_aluno(aluno_repo, sugerir_treino_uc, registrar_treino_uc):
    alunos = aluno_repo.listar()
    print("\n--- Registrar Treino ---")
    for i, a in enumerate(alunos):
        print(f"[{i}] {a.get_nome()}")
    
    try:
        idx = int(input("Escolha um aluno (idx): ").strip())
    except ValueError:
        return

    if not (0 <= idx < len(alunos)):
        print("Índice inválido.")
        return

    grupos = ["Peito", "Costas", "Pernas", "Ombro", "Bíceps", "Tríceps", "Abdômen"]
    print("Grupos disponíveis:", ", ".join(grupos))
    grupo = input("Grupo muscular: ").strip()

    exercicios = sugerir_treino_uc.executar(grupo)
    if not exercicios:
        print(f"Grupo muscular não encontrado.")
        return

    print(f"\nExerccios sugeridos para {grupo.capitalize()}:")
    for i, e in enumerate(exercicios):
        print(f"  [{i}] {e}")

    try:
        opcao = int(input("Escolha qual exercício (idx): ").strip())
    except ValueError:
        return

    if not (0 <= opcao < len(exercicios)):
        print("Índice inválido.")
        return

    exercicio = exercicios[opcao]
    series = int(input("Séries: "))
    repeticoes = int(input("Repetições: "))
    carga = float(input("Carga (kg): "))
    data = input("Data (ex: DD/MM/AAAA): ").strip()
    hora = input("Hora (ex: 15:30): ").strip()

    resultado = registrar_treino_uc.executar(idx, exercicio, series, repeticoes, carga, data, hora)
    if not resultado:
        print(f"Não foi possível registrar o treino.")
    else:
        print("Treino registrado!")
