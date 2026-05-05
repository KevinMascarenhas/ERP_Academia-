# Menu de gerenciamento de planos. Funcionalidades: CRUD de planos de mensalidade da academia.

from .menu_admin import selecionar_idx


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


def cadastrar_plano(plano_repo, criar_plano_uc):
    print("\n--- Cadastrar Plano ---")
    nome = input("Nome do plano: ").strip()
    valor = float(input("Valor mensal: "))
    duracao = int(input("Duração (meses): "))
    modalidades = int(input("Modalidades inclusas: "))
    aulas_por_semana = int(input("Aulas por semana: "))

    resultado = criar_plano_uc.executar(nome, valor, duracao, modalidades, aulas_por_semana)
    if not resultado:
        print(f"Não foi possível cadastrar o plano.")
    else:
        print(f"Plano '{nome}' cadastrado com sucesso!")


def atualizar_plano(plano_repo):
    planos = plano_repo.listar()
    idx = selecionar_idx(planos, lambda: listar_planos(plano_repo))
    if idx is None:
        return

    p = planos[idx]
    nome = input(f"Novo nome [{p.get_nome_plano()}]: ").strip()
    valor = input(f"Novo valor [{p.get_valor()}]: ").strip()
    duracao = input(f"Nova duração [{p.get_duracao()}]: ").strip()
    modalidades = input(f"Novas modalidades inclusas [{p.get_modalidades_inclusas()}]: ").strip()
    aulas = input(f"Novas aulas por semana [{p.get_aulas_por_semana()}]: ").strip()

    nome = nome or None
    valor = float(valor) if valor else None
    duracao = int(duracao) if duracao else None
    modalidades = int(modalidades) if modalidades else None
    aulas = int(aulas) if aulas else None

    plano_repo.atualizar(idx, nome, valor, duracao, modalidades, aulas)
    print("Plano atualizado!")


def remover_plano(plano_repo):
    planos = plano_repo.listar()
    idx = selecionar_idx(planos, lambda: listar_planos(plano_repo))
    if idx is None:
        return
    removido = plano_repo.remover(idx)
    print(f"Plano '{removido.get_nome_plano()}' removido!")


def menu_planos(plano_repo, criar_plano_uc):
    while True:
        print("\n=== PLANOS ===")
        print("1 - Cadastrar\n2 - Listar\n3 - Atualizar\n4 - Remover\n0 - Voltar")
        op = input("Escolha: ").strip()
        if op == "1":   
            cadastrar_plano(plano_repo, criar_plano_uc)
        elif op == "2": 
            listar_planos(plano_repo)
        elif op == "3": 
            atualizar_plano(plano_repo)
        elif op == "4": 
            remover_plano(plano_repo)
        elif op == "0": 
            break
        else:           
            print("Opção inválida.")
