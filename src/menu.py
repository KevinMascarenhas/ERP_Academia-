from models import *
import repository
import services


def linha():
    print("-" * 40)


# LOGIN 

def tela_login():
    print("\n=== ACADEMIA TOGURO ===")
    tentativas = 3
    while tentativas > 0:
        print("\n--- Login ---")
        email = input("Email: ").strip()
        senha = input("Senha: ").strip()

        usuario = services.autenticar(email, senha)
        if usuario:
            print(f"\nBem-vindo(a), {usuario.get_nome()}! [{usuario.get_perfil()}]")
            return usuario

        tentativas -= 1
        print("Email ou senha inválidos.", end=" ")
        if tentativas > 0:
            print(f"Tentativas restantes: {tentativas}")
        else:
            print("Encerrando.")
    return None


# USUÁRIOS 

def listar_usuarios():
    usuarios = repository.listar_usuarios()
    print("\n--- Usuários ---")
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    for i, u in enumerate(usuarios):
        print(f"[{i}] {u.get_nome()} | {u.get_email()} | {u.get_perfil()}")


def cadastrar_usuario():
    print("\n--- Cadastrar Usuário ---")
    nome   = input("Nome: ").strip()
    email  = input("Email: ").strip()
    senha  = input("Senha: ").strip()
    perfil = input("Perfil (admin / operador): ").strip().lower()

    _, erro = services.criar_usuario(nome, email, senha, perfil)
    print(f"Erro: {erro}" if erro else f"Usuário '{nome}' cadastrado!")


def atualizar_usuario():
    listar_usuarios()
    usuarios = repository.listar_usuarios()
    if not usuarios:
        return
    try:
        idx = int(input("ID: "))
        if idx < 0 or idx >= len(usuarios):
            print("ID inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    u = usuarios[idx]
    nome  = input(f"Novo nome [{u.get_nome()}]: ").strip()
    email = input(f"Novo email [{u.get_email()}]: ").strip()
    senha = input("Nova senha (em branco para manter): ").strip()
    repository.atualizar_usuario(idx, nome or None, email or None, senha or None)
    print("Usuário atualizado!")


def remover_usuario():
    listar_usuarios()
    usuarios = repository.listar_usuarios()
    if not usuarios:
        return
    try:
        idx = int(input("ID: "))
        if idx < 0 or idx >= len(usuarios):
            print("ID inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return
    removido = repository.remover_usuario(idx)
    print(f"Usuário '{removido.get_nome()}' removido!")


def menu_usuarios():
    while True:
        print("\n=== USUÁRIOS ===")
        print("1 - Cadastrar  2 - Listar  3 - Atualizar  4 - Remover  0 - Voltar")
        op = input("Escolha: ").strip()
        if op == "1":
            cadastrar_usuario()
        elif op == "2":
            listar_usuarios()
        elif op == "3":
            atualizar_usuario()
        elif op == "4":
            remover_usuario()
        elif op == "0":
            break
        else:
            print("Opção inválida.")


# ── ALUNOS ────────────────────────────────────────────────────

def listar_alunos():
    alunos = repository.listar_alunos()
    print("\n--- Alunos ---")
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return
    for i, a in enumerate(alunos):
        print(f"[{i}] {a.get_nome()} | {a.get_email()} | {a.get_plano().get_nome()}")


def cadastrar_aluno():
    print("\n--- Cadastrar Aluno ---")
    nome  = input("Nome: ").strip()
    email = input("Email: ").strip()
    senha = input("Senha: ").strip()
    cpf   = input("CPF: ").strip()
    listar_planos()
    plano = input("Nome do plano: ").strip()

    _, erro = services.criar_aluno(nome, email, senha, cpf, plano)
    print(f"Erro: {erro}" if erro else f"Aluno '{nome}' cadastrado!")


def atualizar_aluno():
    listar_alunos()
    alunos = repository.listar_alunos()
    if not alunos:
        return
    try:
        idx = int(input("ID: "))
        if idx < 0 or idx >= len(alunos):
            print("ID inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    a = alunos[idx]
    nome  = input(f"Novo nome [{a.get_nome()}]: ").strip()
    email = input(f"Novo email [{a.get_email()}]: ").strip()
    cpf   = input(f"Novo CPF [{a.get_cpf()}]: ").strip()

    novo_plano = None
    if input("Trocar plano? (s/n): ").strip().lower() == "s":
        listar_planos()
        novo_plano = repository.buscar_plano_por_nome(input("Nome do plano: ").strip())
        if not novo_plano:
            print("Plano não encontrado. Plano não alterado.")

    repository.atualizar_aluno(idx, nome or None, email or None, cpf or None, novo_plano)
    print("Aluno atualizado!")


def remover_aluno():
    listar_alunos()
    alunos = repository.listar_alunos()
    if not alunos:
        return
    try:
        idx = int(input("ID: "))
        if idx < 0 or idx >= len(alunos):
            print("ID inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return
    removido = repository.remover_aluno(idx)
    print(f"Aluno '{removido.get_nome()}' removido!")


def ver_historico_aluno(aluno=None):
    if not aluno:
        listar_alunos()
        alunos = repository.listar_alunos()
        if not alunos:
            return
        try:
            idx = int(input("ID do aluno: "))
            if idx < 0 or idx >= len(alunos):
                print("ID inválido.")
                return
        except ValueError:
            print("Entrada inválida.")
            return
        aluno = alunos[idx]

    historico = aluno.get_historico()
    print(f"\nModalidades frequentadas por {aluno.get_nome()}:")
    if not historico:
        print("  Nenhuma modalidade frequentada ainda.")
    else:
        for m in historico:
            print(f"  - {m.get_nome()} | {m.get_categoria()} | {m.get_horario()}")


def registrar_frequencia(aluno=None):
    if not aluno:
        listar_alunos()
        alunos = repository.listar_alunos()
        if not alunos:
            return
        try:
            idx = int(input("ID do aluno: "))
            if idx < 0 or idx >= len(alunos):
                print("ID inválido.")
                return
        except ValueError:
            print("Entrada inválida.")
            return
    else:
        alunos = repository.listar_alunos()
        idx = alunos.index(aluno)

    listar_modalidades()
    nome = input("Nome da modalidade: ").strip()
    ok, erro = services.registrar_frequencia(idx, nome)
    print(f"Erro: {erro}" if erro else "Frequência registrada!")


def menu_alunos():
    while True:
        print("\n=== ALUNOS ===")
        print("1 - Cadastrar  2 - Listar  3 - Atualizar  4 - Remover")
        print("5 - Registrar frequência  6 - Ver histórico  0 - Voltar")
        op = input("Escolha: ").strip()
        if op == "1":
            cadastrar_aluno()
        elif op == "2":
            listar_alunos()
        elif op == "3":
            atualizar_aluno()
        elif op == "4":
            remover_aluno()
        elif op == "5":
            registrar_frequencia()
        elif op == "6":
            ver_historico_aluno()
        elif op == "0":
            break
        else:
            print("Opção inválida.")


# ── PLANOS ────────────────────────────────────────────────────

def listar_planos():
    planos = repository.listar_planos()
    print("\n--- Planos ---")
    if not planos:
        print("Nenhum plano cadastrado.")
        return
    for i, p in enumerate(planos):
        print(f"[{i}] ", end="")
        p.exibir_info()
        linha()


def cadastrar_plano():
    print("\n--- Cadastrar Plano ---")
    nome       = input("Nome: ").strip()
    preco      = input("Preço (R$): ").strip()
    modalidades = input("Modalidades inclusas: ").strip()
    duracao    = input("Duração (meses): ").strip()

    _, erro = services.criar_plano(nome, preco, modalidades, duracao)
    print(f"Erro: {erro}" if erro else f"Plano '{nome}' cadastrado!")


def atualizar_plano():
    listar_planos()
    planos = repository.listar_planos()
    if not planos:
        return
    try:
        idx = int(input("ID: "))
        if idx < 0 or idx >= len(planos):
            print("ID inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    p = planos[idx]
    preco      = input(f"Novo preço [{p.get_preco()}]: ").strip()
    modalidades = input(f"Novas modalidades [{p.get_modalidades_inclusas()}]: ").strip()
    duracao    = input(f"Nova duração [{p.get_duracao_meses()}]: ").strip()

    try:
        repository.atualizar_plano(
            idx,
            preco=float(preco.replace(",", ".")) if preco else None,
            modalidades=int(modalidades) if modalidades else None,
            duracao=int(duracao) if duracao else None
        )
        print("Plano atualizado!")
    except ValueError:
        print("Valor inválido.")


def remover_plano():
    listar_planos()
    planos = repository.listar_planos()
    if not planos:
        return
    try:
        idx = int(input("ID: "))
        if idx < 0 or idx >= len(planos):
            print("ID inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return
    removido = repository.remover_plano(idx)
    print(f"Plano '{removido.get_nome()}' removido!")


def menu_planos(somente_consulta=False):
    while True:
        print("\n=== PLANOS ===")
        print("1 - Listar", end="")
        if not somente_consulta:
            print("  2 - Cadastrar  3 - Atualizar  4 - Remover", end="")
        print("  0 - Voltar")
        op = input("Escolha: ").strip()
        if op == "1":
            listar_planos()
        elif op == "2" and not somente_consulta:
            cadastrar_plano()
        elif op == "3" and not somente_consulta:
            atualizar_plano()
        elif op == "4" and not somente_consulta:
            remover_plano()
        elif op == "0":
            break
        else:
            print("Opção inválida ou sem permissão.")


# ── MODALIDADES ───────────────────────────────────────────────

def listar_modalidades():
    modalidades = repository.listar_modalidades()
    print("\n--- Modalidades ---")
    if not modalidades:
        print("Nenhuma modalidade cadastrada.")
        return
    for i, m in enumerate(modalidades):
        print(f"[{i}] ", end="")
        m.exibir_info()
        linha()


def cadastrar_modalidade():
    print("\n--- Cadastrar Modalidade ---")
    nome      = input("Nome: ").strip()
    categoria = input("Categoria: ").strip()
    horario   = input("Horário (ex: 07:00 - 08:00): ").strip()

    _, erro = services.criar_modalidade(nome, categoria, horario)
    print(f"Erro: {erro}" if erro else f"Modalidade '{nome}' cadastrada!")


def atualizar_modalidade():
    listar_modalidades()
    modalidades = repository.listar_modalidades()
    if not modalidades:
        return
    try:
        idx = int(input("ID: "))
        if idx < 0 or idx >= len(modalidades):
            print("ID inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    m = modalidades[idx]
    categoria = input(f"Nova categoria [{m.get_categoria()}]: ").strip()
    horario   = input(f"Novo horário [{m.get_horario()}]: ").strip()
    repository.atualizar_modalidade(idx, categoria or None, horario or None)
    print("Modalidade atualizada!")


def remover_modalidade():
    listar_modalidades()
    modalidades = repository.listar_modalidades()
    if not modalidades:
        return
    try:
        idx = int(input("ID: "))
        if idx < 0 or idx >= len(modalidades):
            print("ID inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return
    removido = repository.remover_modalidade(idx)
    print(f"Modalidade '{removido.get_nome()}' removida!")


def menu_modalidades(somente_consulta=False):
    while True:
        print("\n=== MODALIDADES ===")
        print("1 - Listar", end="")
        if not somente_consulta:
            print("  2 - Cadastrar  3 - Atualizar  4 - Remover", end="")
        print("  0 - Voltar")
        op = input("Escolha: ").strip()
        if op == "1":
            listar_modalidades()
        elif op == "2" and not somente_consulta:
            cadastrar_modalidade()
        elif op == "3" and not somente_consulta:
            atualizar_modalidade()
        elif op == "4" and not somente_consulta:
            remover_modalidade()
        elif op == "0":
            break
        else:
            print("Opção inválida ou sem permissão.")


# ── TREINOS (menu do aluno) ───────────────────────────────────

def ver_historico_treinos(aluno):
    treinos = aluno.get_historico_treinos()
    print(f"\nHistórico de treinos de {aluno.get_nome()}:")
    if not treinos:
        print("  Nenhum treino registrado ainda.")
        return
    for t in treinos:
        t.exibir_info()
        linha()


def registrar_treino_aluno(aluno):
    print("\n--- Registrar Treino ---")
    grupos = ["Peito", "Costas", "Pernas", "Ombro", "Bíceps", "Tríceps", "Abdômen"]
    print("Grupos disponíveis:", ", ".join(grupos))
    grupo = input("Grupo muscular: ").strip()
    series = input("Séries: ").strip()
    reps = input("Repetições: ").strip()
    data = input("Data (ex: DD/MM/AAAA): ").strip()

    try:
        alunos = repository.listar_alunos()
        idx = alunos.index(aluno)
        treino, erro = services.registrar_treino(idx, grupo, int(series), int(reps), data)
        if erro:
            print(f"Erro: {erro}")
        else:
            print(f"\nTreino de {grupo} registrado!")
            treino.exibir_info()
    except ValueError:
        print("Séries e repetições devem ser números.")


# MENU PRINCIPAL 

def menu_principal(usuario):
    eh_admin = isinstance(usuario, Administrador)
    eh_aluno = isinstance(usuario, Aluno)

    while True:
        print(f"\n=== ACADEMIA TOGURO | {usuario.get_perfil().upper()} ===")
        for opcao in usuario.exibir_menu():
            print(opcao)

        op = input("Escolha: ").strip()

        if eh_aluno:
            if op == "1":
                usuario.exibir_info()
            elif op == "2":
                ver_historico_aluno(aluno=usuario)
            elif op == "3":
                registrar_frequencia(aluno=usuario)
            elif op == "4":
                ver_historico_treinos(usuario)
            elif op == "5":
                registrar_treino_aluno(usuario)
            elif op == "6":
                alunos = repository.listar_alunos()
                idx = alunos.index(usuario)
                nome  = input(f"Novo nome [{usuario.get_nome()}]: ").strip()
                email = input(f"Novo email [{usuario.get_email()}]: ").strip()
                senha = input("Nova senha (em branco para manter): ").strip()
                repository.atualizar_aluno(idx, nome or None, email or None)
                if senha:
                    usuario.set_senha(senha)
                print("Dados atualizados!")
            elif op == "0":
                print(f"Até logo, {usuario.get_nome()}!")
                break
            else:
                print("Opção inválida.")

        else:
            somente_consulta = eh_operador
            if op == "1":
                menu_alunos()
            elif op == "2":
                menu_planos(somente_consulta=somente_consulta)
            elif op == "3":
                menu_modalidades(somente_consulta=somente_consulta)
            elif op == "4" and eh_admin:
                menu_usuarios()
            elif op == "5":
                ver_historico_aluno()
            elif op == "0":
                print(f"Até logo, {usuario.get_nome()}!")
                break
            else:
                print("Opção inválida ou sem permissão.")


# PONTO DE ENTRADA 

def main():
    repository.inicializar_dados()
    usuario = tela_login()
    if usuario:
        menu_principal(usuario)

main()