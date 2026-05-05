# Menu de administrador. Gerencia administradores, alunos, planos, modalidades, treinos e funcionários.

def selecionar_idx(lista, listar_fn):
    listar_fn()
    if not lista:
        return None
    try:
        idx = int(input("ID: "))
        if idx < 0 or idx >= len(lista):
            print("ID inválido.")
            return None
    except ValueError:
        print("Entrada inválida.")
        return None
    return idx


# === ADMINISTRADORES ===

def listar_administradores(admin_repo):
    admins = admin_repo.listar()
    print("\n--- Administradores ---")
    if not admins:
        print("Nenhum administrador cadastrado.")
        return
    for i, u in enumerate(admins):
        print(f"[{i}] {u.get_nome()} | {u.get_email()} | {u.get_perfil()}")


def cadastrar_admin(admin_repo, criar_usuario_uc):
    print("\n--- Cadastrar Administrador ---")
    nome   = input("Nome: ").strip()
    email  = input("Email: ").strip()
    senha  = input("Senha: ").strip()
    perfil = input("Perfil (Administrador): ").strip().lower()

    usuario = criar_usuario_uc.executar(nome, email, senha, perfil)
    if not usuario:
        print(f"Não foi possível cadastrar o administrador.")
    else:
        print(f"Administrador '{nome}' cadastrado!")


def atualizar_admin(admin_repo):
    admins = admin_repo.listar()
    idx = selecionar_idx(admins, lambda: listar_administradores(admin_repo))
    if idx is None:
        return

    u = admins[idx]
    nome  = input(f"Novo nome [{u.get_nome()}]: ").strip()
    email = input(f"Novo email [{u.get_email()}]: ").strip()
    senha = input("Nova senha (em branco para manter): ").strip()
    admin_repo.atualizar(idx, nome or None, email or None, senha or None)
    print("Administrador atualizado!")


def remover_admin(admin_repo):
    listar_administradores(admin_repo)
    admins = admin_repo.listar()
    idx = selecionar_idx(admins, lambda: listar_administradores(admin_repo))
    if idx is None:
        return
    removido = admin_repo.remover(idx)
    print(f"Administrador '{removido.get_nome()}' removido!")


def menu_admin(admin_repo, criar_usuario_uc):
    while True:
        print("\n=== ADMINISTRADORES ===")
        print("1 - Cadastrar\n2 - Listar\n3 - Atualizar\n4 - Remover\n0 - Voltar")
        op = input("Escolha: ").strip()
        if op == "1":
            cadastrar_admin(admin_repo, criar_usuario_uc)
        elif op == "2":
            listar_administradores(admin_repo)
        elif op == "3":
            atualizar_admin(admin_repo)
        elif op == "4":
            remover_admin(admin_repo)
        elif op == "0":
            break
        else:
            print("Opção inválida.")


# === FUNCIONÁRIOS ===

def listar_funcionarios(funcionario_repo):
    funcionarios = funcionario_repo.listar()
    print("\n--- Funcionários ---")
    if not funcionarios:
        print("Nenhum funcionário cadastrado.")
        return
    for i, f in enumerate(funcionarios):
        print(f"[{i}] {f.get_nome()} | {f.get_email()} | ID: {f.get_id()}")


def cadastrar_funcionario(funcionario_repo, criar_funcionario_uc):
    print("\n--- Cadastrar Funcionário ---")
    nome   = input("Nome: ").strip()
    email  = input("Email: ").strip()
    senha  = input("Senha: ").strip()
    id_func = input("ID do Funcionário: ").strip()

    funcionario = criar_funcionario_uc.executar(nome, email, senha, id_func)
    if not funcionario:
        print(f"Não foi possível cadastrar o funcionário.")
    else:
        print(f"Funcionário '{nome}' cadastrado!")


def atualizar_funcionario(funcionario_repo):
    funcionarios = funcionario_repo.listar()
    idx = selecionar_idx(funcionarios, lambda: listar_funcionarios(funcionario_repo))
    if idx is None:
        return

    f = funcionarios[idx]
    nome  = input(f"Novo nome [{f.get_nome()}]: ").strip()
    email = input(f"Novo email [{f.get_email()}]: ").strip()
    senha = input("Nova senha (em branco para manter): ").strip()
    funcionario_repo.atualizar(idx, nome or None, email or None, senha or None)
    print("Funcionário atualizado!")


def remover_funcionario(funcionario_repo):
    listar_funcionarios(funcionario_repo)
    funcionarios = funcionario_repo.listar()
    idx = selecionar_idx(funcionarios, lambda: listar_funcionarios(funcionario_repo))
    if idx is None:
        return
    removido = funcionario_repo.remover(idx)
    print(f"Funcionário '{removido.get_nome()}' removido!")


def menu_funcionarios(funcionario_repo, criar_funcionario_uc):
    while True:
        print("\n=== FUNCIONÁRIOS ===")
        print("1 - Cadastrar\n2 - Listar\n3 - Atualizar\n4 - Remover\n0 - Voltar")
        op = input("Escolha: ").strip()
        if op == "1":
            cadastrar_funcionario(funcionario_repo, criar_funcionario_uc)
        elif op == "2":
            listar_funcionarios(funcionario_repo)
        elif op == "3":
            atualizar_funcionario(funcionario_repo)
        elif op == "4":
            remover_funcionario(funcionario_repo)
        elif op == "0":
            break
        else:
            print("Opção inválida.")

