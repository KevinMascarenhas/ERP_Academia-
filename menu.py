from models import *
import repository
import services

def menu_planos(somente_consulta=False):
    while True:
        print("\n=== PLANOS ===")
        print("1 - Listar planos")
        if not somente_consulta:
            print("2 - Cadastrar plano")
            print("3 - Atualizar plano")
            print("4 - Remover plano")
        print("0 - Voltar")
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


def cadastrar_conteudo():
    print("\n--- Cadastrar Conteúdo ---")
    titulo = input("Título: ").strip()
    genero = input("Gênero: ").strip()
    tipo   = input("Tipo (Filme / Série / Documentário): ").strip()

    if not titulo or not genero or not tipo:
        print("Erro: todos os campos são obrigatórios.")
        return

    conteudos.append(Conteudo(titulo, genero, tipo))
    print(f"Conteúdo '{titulo}' cadastrado com sucesso!")


def listar_conteudos():
    print("\n--- Lista de Conteúdos ---")
    if not conteudos:
        print("Nenhum conteúdo cadastrado.")
        return
    for i, c in enumerate(conteudos):
        print(f"[{i}] ", end="")
        c.exibir()
        linha()


def atualizar_conteudo():
    listar_conteudos()
    if not conteudos:
        return
    try:
        idx = int(input("ID do conteúdo a atualizar: "))
        if idx < 0 or idx >= len(conteudos):
            print("ID inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    c = conteudos[idx]
    novo_titulo = input(f"Novo título [{c.get_titulo()}]: ").strip()
    novo_genero = input(f"Novo gênero [{c.get_genero()}]: ").strip()
    novo_tipo   = input(f"Novo tipo [{c.get_tipo()}]: ").strip()

    if novo_titulo:
        c.set_titulo(novo_titulo)
    if novo_genero:
        c.set_genero(novo_genero)
    if novo_tipo:
        c.set_tipo(novo_tipo)

    print("Conteúdo atualizado!")


def remover_conteudo():
    listar_conteudos()
    if not conteudos:
        return
    try:
        idx = int(input("ID do conteúdo a remover: "))
        if idx < 0 or idx >= len(conteudos):
            print("ID inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    removido = conteudos.pop(idx)
    print(f"Conteúdo '{removido.get_titulo()}' removido!")


def menu_conteudos(somente_consulta=False):
    while True:
        print("\n=== CONTEÚDOS ===")
        print("1 - Listar conteúdos")
        if not somente_consulta:
            print("2 - Cadastrar conteúdo")
            print("3 - Atualizar conteúdo")
            print("4 - Remover conteúdo")
        print("0 - Voltar")
        op = input("Escolha: ").strip()

        if op == "1":
            listar_conteudos()
        elif op == "2" and not somente_consulta:
            cadastrar_conteudo()
        elif op == "3" and not somente_consulta:
            atualizar_conteudo()
        elif op == "4" and not somente_consulta:
            remover_conteudo()
        elif op == "0":
            break
        else:
            print("Opção inválida ou sem permissão.")


# ════════════════════════════════════════════════════════════
# CRUD DE ASSINANTES
# ════════════════════════════════════════════════════════════

def cadastrar_assinante():
    print("\n--- Cadastrar Assinante ---")
    nome  = input("Nome: ").strip()
    email = input("Email: ").strip()
    senha = input("Senha (para login do assinante): ").strip()
    cpf   = input("CPF (ex: 123.456.789-01): ").strip()

    if not nome or not email or not senha or not cpf:
        print("Erro: todos os campos são obrigatórios.")
        return

    listar_planos()
    nome_plano = input("Nome do plano desejado: ").strip()
    plano = buscar_plano_por_nome(nome_plano)

    if not plano:
        print(f"Plano '{nome_plano}' não encontrado. Cadastre o plano antes.")
        return

    assinantes.append(Assinante(nome, email, senha, cpf, plano))
    print(f"Assinante '{nome}' cadastrado com sucesso!")


def listar_assinantes():
    print("\n--- Lista de Assinantes ---")
    if not assinantes:
        print("Nenhum assinante cadastrado.")
        return
    for i, a in enumerate(assinantes):
        print(f"[{i}] ", end="")
        a.exibir()
        linha()


def atualizar_assinante():
    listar_assinantes()
    if not assinantes:
        return
    try:
        idx = int(input("ID do assinante a atualizar: "))
        if idx < 0 or idx >= len(assinantes):
            print("ID inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    a = assinantes[idx]
    novo_nome  = input(f"Novo nome [{a.get_nome()}]: ").strip()
    novo_email = input(f"Novo email [{a.get_email()}]: ").strip()

    trocar_plano = input("Trocar plano? (s/n): ").strip().lower()
    novo_plano = None
    if trocar_plano == "s":
        listar_planos()
        nome_plano = input("Nome do novo plano: ").strip()
        novo_plano = buscar_plano_por_nome(nome_plano)
        if not novo_plano:
            print("Plano não encontrado. Plano não alterado.")

    if novo_nome:
        a.set_nome(novo_nome)
    if novo_email:
        a.set_email(novo_email)
    if novo_plano:
        a.set_plano(novo_plano)

    print("Assinante atualizado!")


def remover_assinante():
    listar_assinantes()
    if not assinantes:
        return
    try:
        idx = int(input("ID do assinante a remover: "))
        if idx < 0 or idx >= len(assinantes):
            print("ID inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    removido = assinantes.pop(idx)
    print(f"Assinante '{removido.get_nome()}' removido!")


def registrar_consumo():
    """Registra um conteúdo assistido no histórico do assinante."""
    listar_assinantes()
    if not assinantes:
        return
    try:
        idx = int(input("ID do assinante: "))
        if idx < 0 or idx >= len(assinantes):
            print("ID inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    listar_conteudos()
    titulo = input("Título do conteúdo assistido: ").strip()
    conteudo = buscar_conteudo_por_titulo(titulo)

    if not conteudo:
        print(f"Conteúdo '{titulo}' não encontrado. Cadastre-o antes.")
        return

    assinantes[idx].assistir(conteudo)
    print("Consumo registrado!")


def ver_historico():
    listar_assinantes()
    if not assinantes:
        return
    try:
        idx = int(input("ID do assinante: "))
        if idx < 0 or idx >= len(assinantes):
            print("ID inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    historico = assinantes[idx].get_historico()
    print(f"\nHistórico de {assinantes[idx].get_nome()}:")
    if not historico:
        print("  Nenhum conteúdo assistido ainda.")
    else:
        for c in historico:
            print(f"  - {c.get_titulo()} ({c.get_tipo()} | {c.get_genero()})")


def menu_assinantes():
    while True:
        print("\n=== ASSINANTES ===")
        print("1 - Cadastrar assinante")
        print("2 - Listar assinantes")
        print("3 - Atualizar assinante")
        print("4 - Remover assinante")
        print("5 - Registrar consumo")
        print("6 - Ver histórico de consumo")
        print("0 - Voltar")
        op = input("Escolha: ").strip()

        if op == "1":
            cadastrar_assinante()
        elif op == "2":
            listar_assinantes()
        elif op == "3":
            atualizar_assinante()
        elif op == "4":
            remover_assinante()
        elif op == "5":
            registrar_consumo()
        elif op == "6":
            ver_historico()
        elif op == "0":
            break
        else:
            print("Opção inválida.")


# ════════════════════════════════════════════════════════════
# MENU PRINCIPAL  (polimorfismo: menu varia por perfil)
# ════════════════════════════════════════════════════════════

def menu_principal(usuario):
    """Exibe o menu de acordo com o perfil do usuário logado (polimorfismo)."""
    eh_admin    = isinstance(usuario, Administrador)
    eh_assinante = isinstance(usuario, Assinante)

    while True:
        print(f"\n=== STREAMCLUB MANAGER | {usuario.get_perfil().upper()} ===")

        # Usa o método polimórfico da classe para mostrar as opções
        for opcao in usuario.exibir_menu():
            print(opcao)

        op = input("Escolha: ").strip()

        # ── Menu do Assinante ──────────────────────────────
        if eh_assinante:
            if op == "1":
                usuario.exibir()
            elif op == "2":
                historico = usuario.get_historico()
                print(f"\nHistórico de {usuario.get_nome()}:")
                if not historico:
                    print("  Nenhum conteúdo assistido ainda.")
                else:
                    for c in historico:
                        print(f"  - {c.get_titulo()} ({c.get_tipo()} | {c.get_genero()})")
            elif op == "3":
                listar_conteudos()
                titulo = input("Título do conteúdo assistido: ").strip()
                conteudo = buscar_conteudo_por_titulo(titulo)
                if conteudo:
                    usuario.assistir(conteudo)
                    print("Conteúdo registrado no seu histórico!")
                else:
                    print("Conteúdo não encontrado.")
            elif op == "4":
                novo_nome  = input(f"Novo nome [{usuario.get_nome()}]: ").strip()
                novo_email = input(f"Novo email [{usuario.get_email()}]: ").strip()
                nova_senha = input("Nova senha (deixe em branco para manter): ").strip()
                if novo_nome:
                    usuario.set_nome(novo_nome)
                if novo_email:
                    usuario.set_email(novo_email)
                if nova_senha:
                    usuario.set_senha(nova_senha)
                print("Dados atualizados!")
            elif op == "0":
                print(f"Até logo, {usuario.get_nome()}!")
                break
            else:
                print("Opção inválida.")

        # ── Menu do Administrador / Operador ───────────────
        else:
            if op == "1":
                menu_assinantes()
            elif op == "2":
                menu_planos(somente_consulta=not eh_admin)
            elif op == "3":
                menu_conteudos(somente_consulta=not eh_admin)
            elif op == "4" and eh_admin:
                menu_usuarios()
            elif op == "5":
                ver_historico()
            elif op == "0":
                print(f"Até logo, {usuario.get_nome()}!")
                break
            else:
                print("Opção inválida ou sem permissão.")


# ════════════════════════════════════════════════════════════
# INICIALIZAÇÃO  (dados de exemplo para testes)
# ════════════════════════════════════════════════════════════

def inicializar_dados():
    """Popula o sistema com dados iniciais para facilitar os testes."""

    # Usuários do sistema
    usuarios.append(Administrador("Admin", "admin@stream.com", "1234"))
    usuarios.append(Operador("Operador", "op@stream.com", "1234"))

    # Planos
    planos.append(Plano("Basic",   19.90, 1, "HD"))
    planos.append(Plano("Premium", 45.90, 4, "4K"))

    # Conteúdos
    conteudos.append(Conteudo("Norbit", "Comédia", "Filme"))
    conteudos.append(Conteudo("Todo mundo odeia o Chris", "Comédia", "Série"))
    conteudos.append(Conteudo("Planeta Terra", "Natureza", "Documentário"))

    # Assinante de exemplo — agora com senha para login
    plano_premium = buscar_plano_por_nome("Premium")
    maria = Assinante("Maria", "maria@email.com", "1234", "123.456.789-01", plano_premium)
    maria.assistir(conteudos[0])
    assinantes.append(maria)


# ════════════════════════════════════════════════════════════
# PONTO DE ENTRADA
# ════════════════════════════════════════════════════════════

def main():
    inicializar_dados()

    print("=== BEM-VINDO AO STREAMCLUB MANAGER ===")
    print("(Contas de teste: admin@stream.com / 1234  |  op@stream.com / 1234)")

    tentativas = 3
    while tentativas > 0:
        usuario = login()
        if usuario:
            menu_principal(usuario)
            break
        tentativas -= 1
        if tentativas > 0:
            print(f"Tentativas restantes: {tentativas}")
        else:
            print("Número de tentativas excedido. Encerrando.")


main()