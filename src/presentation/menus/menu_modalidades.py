# Menu de gerenciamento de modalidades (turmas). Funcionalidades: CRUD de modalidades, agendamento de aulas.

from .menu_admin import selecionar_idx


def listar_modalidades_disponiveis(modalidade_repo):
    modalidades = modalidade_repo.listar()
    print("\n--- Modalidades ---")
    if not modalidades:
        print("Nenhuma modalidade cadastrada.")
        return
    for i, m in enumerate(modalidades):
        dias = f" | Dias: {', '.join(m.get_dias_semana())}" if m.get_dias_semana() else " | Acesso livre"
        print(f"[{i}] {m.get_nome()} | {m.get_categoria()} | {m.get_horario()}{dias}")


def cadastrar_modalidade(modalidade_repo, criar_modalidade_uc):
    print("\n--- Cadastrar Modalidade ---")
    nome = input("Nome: ").strip()
    categoria = input("Categoria (ex: Musculação, Yoga, Natação): ").strip()
    horario = input("Horário (ex: 14:00): ").strip()
    
    dias = []
    resp = input("Modalidade tem dias específicos? (s/n): ").strip().lower()
    if resp == "s":
        dias_str = input("Dias (ex: segunda,quarta,sexta): ").strip()
        dias = [d.strip().capitalize() for d in dias_str.split(",")]

    resultado = criar_modalidade_uc.executar(nome, categoria, horario, dias)
    if not resultado:
        print(f"Não foi possível cadastrar a modalidade.")
    else:
        print(f"Modalidade '{nome}' cadastrada com sucesso!")


def atualizar_modalidade(modalidade_repo):
    modalidades = modalidade_repo.listar()
    idx = selecionar_idx(modalidades, lambda: listar_modalidades_disponiveis(modalidade_repo))
    if idx is None:
        return

    m = modalidades[idx]
    nome = input(f"Novo nome [{m.get_nome()}]: ").strip()
    categoria = input(f"Nova categoria [{m.get_categoria()}]: ").strip()
    horario = input(f"Novo horário [{m.get_horario()}]: ").strip()

    modalidade_repo.atualizar(idx, nome or None, categoria or None, horario or None)
    print("Modalidade atualizada!")


def remover_modalidade(modalidade_repo):
    modalidades = modalidade_repo.listar()
    idx = selecionar_idx(modalidades, lambda: listar_modalidades_disponiveis(modalidade_repo))
    if idx is None:
        return
    removida = modalidade_repo.remover(idx)
    print(f"Modalidade '{removida.get_nome()}' removida!")


def menu_modalidades(modalidade_repo, criar_modalidade_uc):
    while True:
        print("\n=== MODALIDADES ===")
        print("1 - Cadastrar\n2 - Listar\n3 - Atualizar\n4 - Remover\n0 - Voltar")
        op = input("Escolha: ").strip()
        if op == "1":   
            cadastrar_modalidade(modalidade_repo, criar_modalidade_uc)
        elif op == "2": 
            listar_modalidades_disponiveis(modalidade_repo)
        elif op == "3": 
            atualizar_modalidade(modalidade_repo)
        elif op == "4": 
            remover_modalidade(modalidade_repo)
        elif op == "0": 
            break
        else:           
            print("Opção inválida.")
