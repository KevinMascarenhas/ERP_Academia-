from .menu_admin import selecionar_idx


def listar_modalidades_disponiveis(modalidade_repo):
    modalidades = modalidade_repo.listar()
    print("\n--- Modalidades Disponíveis ---")
    if not modalidades:
        print("Nenhuma modalidade cadastrada.")
        return
    for i, m in enumerate(modalidades):
        dias = f" | Dias: {', '.join(m.get_dias_semana())}" if m.get_dias_semana() else " | Acesso livre"
        print(f"[{i}] {m.get_nome()} | {m.get_categoria()} | {m.get_horario()}{dias}")


def ver_modalidades_com_agenda(aluno, inscrever_em_modalidade_uc):
    print(f"\n--- Modalidades de {aluno.get_nome()} ---")
    modalidades = aluno.get_modalidades_inscritas()
    if not modalidades:
        print("Nenhuma modalidade.")
        return []
    for i, m in enumerate(modalidades):
        print(f"[{i}] {m.get_nome()} | {m.get_horario()}")
    return modalidades


def inscrever_aluno(aluno_repo, modalidade_repo, inscrever_em_modalidade_uc, aluno_logado=None):
    alunos = aluno_repo.listar()
    
    # Se aluno logado, usa direto; se não, mostra lista (para admin)
    if aluno_logado:
        print(f"\n--- Inscrever {aluno_logado.get_nome()} em Modalidade ---")
        idx = alunos.index(aluno_logado)
    else:
        print("\n--- Listar Alunos ---")
        for i, a in enumerate(alunos):
            print(f"[{i}] {a.get_nome()}")
        
        try:
            idx = int(input("Escolha um aluno (idx): ").strip())
        except ValueError:
            return
        
        if not (0 <= idx < len(alunos)):
            print("Índice inválido.")
            return

    listar_modalidades_disponiveis(modalidade_repo)
    nome = input("Nome da modalidade: ").strip()
    modalidade = inscrever_em_modalidade_uc.executar(idx, nome)
    if not modalidade:
        print(f"Não foi possível inscrever.")
    else:
        print(f"Aluno inscrito em '{nome}'!")


def cancelar_inscricao(aluno_repo, cancelar_inscricao_modalidade_uc, aluno_logado=None):
    alunos = aluno_repo.listar()
    
    # Se aluno logado, usa direto; se não, mostra lista (para admin)
    if aluno_logado:
        print(f"\n--- Cancelar Inscrição de {aluno_logado.get_nome()} ---")
        idx = alunos.index(aluno_logado)
    else:
        print("\n--- Cancelar Inscrição ---")
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
    modalidades = ver_modalidades_com_agenda(aluno, None)
    if not modalidades:
        return

    try:
        m_idx = int(input("Escolha uma modalidade (idx): ").strip())
    except ValueError:
        return

    if not (0 <= m_idx < len(modalidades)):
        print("Índice inválido.")
        return

    resultado = cancelar_inscricao_modalidade_uc.executar(idx, m_idx)
    if not resultado:
        print(f"Não foi possível cancelar.")
    else:
        print("Inscrição cancelada!")


def agendar_aula(aluno_repo, agendar_aula_uc, aluno_logado=None):
    alunos = aluno_repo.listar()
    
    # Se aluno logado, usa direto; se não, mostra lista (para admin)
    if aluno_logado:
        print(f"\n--- Agendar Aula para {aluno_logado.get_nome()} ---")
        idx = alunos.index(aluno_logado)
    else:
        print("\n--- Agendar Aula ---")
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
    modalidades = ver_modalidades_com_agenda(aluno, None)
    if not modalidades:
        return

    try:
        m_idx = int(input("Escolha uma modalidade (idx): ").strip())
    except ValueError:
        return

    if not (0 <= m_idx < len(modalidades)):
        print("Índice inválido.")
        return

    data = input("Data (ex: DD/MM/AAAA): ").strip()
    hora = input("Hora (ex: 14:00): ").strip()
    nome_modalidade = modalidades[m_idx].get_nome()
    inscricao = agendar_aula_uc.executar(idx, nome_modalidade, data, hora)
    if not inscricao:
        print(f"Não foi possível agendar.")
    else:
        print("Aula agendada!")


def ver_agenda(aluno_repo, aluno_logado=None):
    alunos = aluno_repo.listar()
    
    # Se aluno logado, usa direto; se não, mostra lista (para admin)
    if aluno_logado:
        print(f"\n--- Agenda de {aluno_logado.get_nome()} ---")
        aluno = aluno_logado
    else:
        print("\n--- Ver Agenda ---")
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
        print(f"\n--- Agenda de {aluno.get_nome()} ---")

    agenda = aluno.get_agenda()
    if not agenda:
        print("Nenhum agendamento.")
    else:
        for i, inscricao in enumerate(agenda):
            inscricao.exibir_info()


def gerenciar_agendamento(aluno_repo, confirmar_agendamento_uc, cancelar_agendamento_uc, aluno_logado=None):
    alunos = aluno_repo.listar()
    
    # Se aluno logado, usa direto; se não, mostra lista (para admin)
    if aluno_logado:
        print(f"\n--- Gerenciar Agendamentos de {aluno_logado.get_nome()} ---")
        idx = alunos.index(aluno_logado)
    else:
        print("\n--- Gerenciar Agendamentos ---")
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
    agenda = aluno.get_agenda()
    
    if not agenda:
        print("Nenhum agendamento.")
        return
    
    print("\n--- Agendamentos ---")
    for i, inscricao in enumerate(agenda):
        print(f"[{i}] ", end="")
        inscricao.exibir_info()
    
    print("1 - Confirmar\n2 - Cancelar")
    op = input("Escolha: ").strip()

    try:
        ag_idx = int(input("Escolha um agendamento (idx): ").strip())
    except ValueError:
        return

    if op == "1":
        inscricao = confirmar_agendamento_uc.executar(idx, ag_idx)
    elif op == "2":
        inscricao = cancelar_agendamento_uc.executar(idx, ag_idx)
    else:
        print("Opção inválida.")
        return

    if not inscricao:
        print(f"Erro na operação.")
    else:
        print("Agendamento confirmado!" if op == "1" else "Agendamento cancelado!")


def menu_modalidades_aluno(aluno_repo, modalidade_repo, inscrever_em_modalidade_uc, cancelar_inscricao_modalidade_uc, agendar_aula_uc, confirmar_agendamento_uc, cancelar_agendamento_uc, aluno_logado=None):
    while True:
        print("\n=== MODALIDADES (ALUNO) ===")
        print("1 - Inscrever em modalidade\n2 - Cancelar inscrição\n3 - Agendar aula\n4 - Ver agenda\n5 - Gerenciar agendamentos\n0 - Voltar")
        op = input("Escolha: ").strip()
        if op == "1":   
            inscrever_aluno(aluno_repo, modalidade_repo, inscrever_em_modalidade_uc, aluno_logado=aluno_logado)
        elif op == "2": 
            cancelar_inscricao(aluno_repo, cancelar_inscricao_modalidade_uc, aluno_logado=aluno_logado)
        elif op == "3": 
            agendar_aula(aluno_repo, agendar_aula_uc, aluno_logado=aluno_logado)
        elif op == "4": 
            ver_agenda(aluno_repo, aluno_logado=aluno_logado)
        elif op == "5": 
            gerenciar_agendamento(aluno_repo, confirmar_agendamento_uc, cancelar_agendamento_uc, aluno_logado=aluno_logado)
        elif op == "0": 
            break
        else:           
            print("Opção inválida.")
