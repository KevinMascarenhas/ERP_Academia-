from models import *
import repository
import services


def linha():
    print("-" * 40)

# função para seleção de índice em listas (ex: escolher aluno, plano, modalidade)
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
    perfil = input("Perfil (Administrador): ").strip().lower()

    u, erro = services.criar_usuario(nome, email, senha, perfil)
    if not u:
        print(f"Não foi possível cadastrar: {erro}")
    else:
        print(f"Usuário '{nome}' cadastrado!")


def atualizar_usuario():
    usuarios = repository.listar_usuarios()
    idx = selecionar_idx(usuarios, listar_usuarios)
    if idx is None:
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
    idx = selecionar_idx(usuarios, listar_usuarios)
    if idx is None:
        return
    removido = repository.remover_usuario(idx)
    print(f"Usuário '{removido.get_nome()}' removido!")


def menu_usuarios():
    while True:
        print("\n=== USUÁRIOS ===")
        print("1 - Cadastrar\n2 - Listar\n3 - Atualizar\n4 - Remover\n0 - Voltar")
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


# ALUNOS 

def listar_alunos():
    alunos = repository.listar_alunos()
    print("\n--- Alunos ---")
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return
    for i, a in enumerate(alunos):
        plano_nome = a.get_plano().get_nome_plano() if a.get_plano() else "Sem plano"
        print(f"[{i}] {a.get_nome()} | {a.get_email()} | {plano_nome}")


def selecionar_modalidades_cadastro(plano):
    limite = plano.get_modalidades_inclusas()
    todas = repository.listar_modalidades()
    if not todas:
        print("Nenhuma modalidade disponível.")
        return []

    print(f"\nSeu plano permite até {limite} modalidade(s). Escolha agora (ou depois no menu).")
    listar_modalidades_disponiveis()

    escolhidas = []
    while len(escolhidas) < limite:
        restantes = limite - len(escolhidas)
        resp = input(f"Nome da modalidade ({restantes} restante(s), Enter para pular): ").strip()
        if not resp:
            break
        m = repository.buscar_modalidade_por_nome(resp)
        if not m:
            print(f"Modalidade '{resp}' não encontrada.")
        elif m.get_nome() in [e.get_nome() for e in escolhidas]:
            print("Modalidade já escolhida.")
        else:
            escolhidas.append(m)
            print(f" {m.get_nome()} adicionada.")

    return [m.get_nome() for m in escolhidas]


def cadastrar_aluno():
    print("\n--- Cadastrar Aluno ---")
    nome  = input("Nome: ").strip()
    email = input("Email: ").strip()
    senha = input("Senha: ").strip()
    cpf = input("CPF: ").strip()

    listar_planos()
    nome_plano = input("Nome do plano: ").strip()
    plano = repository.buscar_plano_por_nome(nome_plano)
    if not plano:
        print(f"Plano '{nome_plano}' não encontrado. Aluno não cadastrado.")
        return

    # Escolha de modalidades no ato do cadastro
    nomes_modalidades = selecionar_modalidades_cadastro(plano)

    aluno, aviso = services.criar_aluno(nome, email, senha, cpf, nome_plano, nomes_modalidades)
    if not aluno:
        print(f"Não foi possível cadastrar: {aviso}")
        return
    print(f"Aluno '{nome}' cadastrado com sucesso!")
    if nomes_modalidades:
        print(f"  Modalidades inscritas: {', '.join(nomes_modalidades)}")
    if aviso:
        print(f"  Aviso: {aviso}")


def atualizar_aluno():
    alunos = repository.listar_alunos()
    idx = selecionar_idx(alunos, listar_alunos)
    if idx is None:
        return

    a = alunos[idx]
    nome  = input(f"Novo nome [{a.get_nome()}]: ").strip()
    email = input(f"Novo email [{a.get_email()}]: ").strip()
    cpf = input(f"Novo CPF [{a.get_cpf()}]: ").strip()

    novo_plano = None
    if input("Trocar plano? (s/n): ").strip().lower() == "s":
        listar_planos()
        novo_plano = repository.buscar_plano_por_nome(input("Nome do plano: ").strip())
        if not novo_plano:
            print("Plano não encontrado. Plano não alterado.")

    repository.atualizar_aluno(idx, nome or None, email or None, cpf or None, novo_plano)
    print("Aluno atualizado!")


def remover_aluno():
    alunos = repository.listar_alunos()
    idx = selecionar_idx(alunos, listar_alunos)
    if idx is None:
        return
    removido = repository.remover_aluno(idx)
    print(f"Aluno '{removido.get_nome()}' removido!")


def ver_historico_aluno(aluno=None):
    if not aluno:
        alunos = repository.listar_alunos()
        idx = selecionar_idx(alunos, listar_alunos)
        if idx is None:
            return
        aluno = alunos[idx]

    print(f"\n--- Frequências registradas por {aluno.get_nome()} ---")
    aluno.exibir_info()


def registrar_frequencia(aluno=None):
    if not aluno:
        alunos = repository.listar_alunos()
        idx = selecionar_idx(alunos, listar_alunos)
        if idx is None:
            return
    else:
        alunos = repository.listar_alunos()
        idx = alunos.index(aluno)

    listar_modalidades_disponiveis()
    nome = input("Nome da modalidade: ").strip()
    data = input("Data (ex: DD/MM/AAAA): ").strip()
    hora = input("Hora (ex: 15:30): ").strip()
    resultado = services.registrar_frequencia(idx, nome, data, hora)
    if resultado:
        print(f"Não foi possível registrar: {resultado}")
    else:
        print("Frequência registrada!")


def menu_alunos():
    while True:
        print("\n=== ALUNOS ===")
        print("1 - Cadastrar\n2 - Listar\n3 - Atualizar\n4 - Remover\n5 - Registrar frequência\n6 - Sugestão de treino\n7 - Ver histórico\n0 - Voltar")
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
            sugestao_treino() 
        elif op == "7": 
            ver_historico_aluno()
        elif op == "0": 
            break
        else:           
            print("Opção inválida.")


# PLANOS 

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
    nome = input("Nome: ").strip()
    preco = input("Preço: ").strip()
    modalidades = input("Qtd. modalidades inclusas: ").strip()
    duracao = input("Duração (meses): ").strip()

    p, erro = services.criar_plano(nome, preco, modalidades, duracao)
    if not p:
        print(f"Não foi possível cadastrar: {erro}")
    else:
        print(f"Plano '{nome}' cadastrado!")


def atualizar_plano():
    planos = repository.listar_planos()
    idx = selecionar_idx(planos, listar_planos)
    if idx is None:
        return

    p = planos[idx]
    preco = input(f"Novo preço [{p.get_preco()}]: ").strip()
    modalidades = input(f"Novas modalidades [{p.get_modalidades_inclusas()}]: ").strip()
    duracao = input(f"Nova duração [{p.get_duracao_meses()}]: ").strip()

    try:
        repository.atualizar_plano(
            idx,
            preco=float(preco.replace(",", ".")) if preco else None,
            modalidades_qt=int(modalidades) if modalidades else None,
            duracao=int(duracao) if duracao else None
        )
        print("Plano atualizado!")
    except ValueError:
        print("Valor inválido.")


def remover_plano():
    planos = repository.listar_planos()
    idx = selecionar_idx(planos, listar_planos)
    if idx is None:
        return
    removido = repository.remover_plano(idx)
    print(f"Plano '{removido.get_nome_plano()}' removido!")


def menu_planos():
    while True:
        print("\n=== PLANOS ===")
        print("1 - Listar\n2 - Cadastrar\n3 - Atualizar\n4 - Remover\n0 - Voltar")
        op = input("Escolha: ").strip()
        if op == "1":                       
            listar_planos()
        elif op == "2": 
            cadastrar_plano()
        elif op == "3": 
            atualizar_plano()
        elif op == "4": 
            remover_plano()
        elif op == "0":                     
            break
        else:                               
            print("Opção inválida ou sem permissão.")


# MODALIDADES 
def listar_modalidades_disponiveis():
    modalidades = repository.listar_modalidades()
    print("\n--- Modalidades Disponíveis ---")
    if not modalidades:
        print("Nenhuma modalidade cadastrada.")
        return
    for i, m in enumerate(modalidades):
        dias = f" | Dias: {', '.join(m.get_dias_semana())}" if m.get_dias_semana() else " | Acesso livre"
        print(f"[{i}] {m.get_nome()} | {m.get_categoria()} | {m.get_horario()}{dias}")

def cadastrar_modalidade():
    print("\n--- Cadastrar Modalidade ---")
    nome  = input("Nome: ").strip()
    categoria = input("Categoria: ").strip()
    horario = input("Horário (ex: 07:00 - 08:00): ").strip()

    dias_semana = []
    if input("Esta modalidade tem dias fixos de aula? (s/n): ").strip().lower() == "s":
        print("Digite os dias separados por vírgula (ex: Segunda,Quarta,Sexta):")
        entrada = input("> ").strip()
        dias_semana = [d.strip().capitalize() for d in entrada.split(",") if d.strip()]

    m = services.criar_modalidade(nome, categoria, horario, dias_semana if dias_semana else None)
    if not m:
        print(f"Não foi possível cadastrar. Verifique se o nome já existe ou se os campos estão corretos.")
    else:
        tipo = f"Dias fixos: {', '.join(dias_semana)}" if dias_semana else "Acesso livre"
        print(f"Modalidade '{nome}' cadastrada! ({tipo})")


def atualizar_modalidade():
    modalidades = repository.listar_modalidades()
    idx = selecionar_idx(modalidades, listar_modalidades_disponiveis)
    if idx is None:
        return

    m = modalidades[idx]
    categoria = input(f"Nova categoria [{m.get_categoria()}]: ").strip()
    horario   = input(f"Novo horário [{m.get_horario()}]: ").strip()

    dias_semana = None
    if input("Atualizar dias da semana? (s/n): ").strip().lower() == "s":
        print("Digite os dias separados por vírgula (vazio = acesso livre):")
        entrada = input("> ").strip()
        dias_semana = [d.strip().capitalize() for d in entrada.split(",") if d.strip()]

    repository.atualizar_modalidade(
        idx,
        categoria=categoria or None,
        horario=horario or None,
        dias_semana=dias_semana
    )
    print("Modalidade atualizada!")


def remover_modalidade():
    modalidades = repository.listar_modalidades()
    idx = selecionar_idx(modalidades, listar_modalidades_disponiveis)
    if idx is None:
        return
    removido = repository.remover_modalidade(idx)
    print(f"Modalidade '{removido.get_nome()}' removida!")


def menu_modalidades():
    while True:
        print("\n=== MODALIDADES ===")
        print("1 - Listar\n2 - Cadastrar\n3 - Atualizar\n4 - Remover\n0 - Voltar")
        op = input("Escolha: ").strip()
        if op == "1":                            
            listar_modalidades_disponiveis()
        elif op == "2": 
            cadastrar_modalidade()
        elif op == "3": 
            atualizar_modalidade()
        elif op == "4": 
            remover_modalidade()
        elif op == "0":                          
            break
        else:                                    
            print("Opção inválida ou sem permissão.")


# MENU DE MODALIDADES E AGENDA (ALUNO) 

def menu_modalidades_aluno(aluno):
    alunos = repository.listar_alunos()
    idx = alunos.index(aluno)

    while True:
        print(f"\n=== MODALIDADES & AGENDA ===")
        inscritas = aluno.get_modalidades_inscritas()
        plano = aluno.get_plano()
        limite = plano.get_modalidades_inclusas() if plano else 0
        print(f"Modalidades inscritas: {len(inscritas)}/{limite}")

        print("\n1 - Ver modalidades disponíveis")
        print("2 - Inscrever-se em modalidade")
        print("3 - Cancelar matrícula em modalidade")
        print("4 - Agendar aula")
        print("5 - Ver minha agenda")
        print("6 - Confirmar/Cancelar agendamento")
        print("0 - Voltar")
        op = input("Escolha: ").strip()

        if op == "1":
            ver_modalidades_com_agenda(aluno)
        elif op == "2":
            inscrever_aluno(aluno, idx, limite)
        elif op == "3":
            cancelar_inscricao(aluno, idx)
        elif op == "4":
            agendar_aula(aluno, idx)
        elif op == "5":
            ver_agenda(aluno)
        elif op == "6":
            gerenciar_agendamento(aluno, idx)
        elif op == "0":
            break
        else:
            print("Opção inválida.")


def ver_modalidades_com_agenda(aluno):
    print("\n--- Modalidades Disponíveis ---")
    inscritas = aluno.get_modalidades_inscritas()
    for m in repository.listar_modalidades():
        status = " [INSCRITO]" if m in inscritas else ""
        print(f"\n  {m.get_nome()}{status}")
        m.exibir_info()


def inscrever_aluno(aluno, idx, limite):
    inscritas = aluno.get_modalidades_inscritas()
    if len(inscritas) >= limite:
        print(f"Seu plano permite apenas {limite} modalidade(s). Cancele uma para trocar.")
        return
    listar_modalidades_disponiveis()
    nome = input("Nome da modalidade: ").strip()
    m, erro = services.inscrever_em_modalidade(idx, nome)
    if not m:
        print(f"Não foi possível inscrever: {erro}")
    else:
        print(f"Inscrito em '{nome}' com sucesso!")


def cancelar_inscricao(aluno, idx):
    inscritas = aluno.get_modalidades_inscritas()
    if not inscritas:
        print("Você não está inscrito em nenhuma modalidade.")
        return
    print("\nSuas modalidades:")
    for i, m in enumerate(inscritas):
        print(f"  [{i}] {m.get_nome()}")
    try:
        escolha = int(input("Número da modalidade para cancelar: "))
        if escolha < 0 or escolha >= len(inscritas):
            print("Número inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return
    nome = inscritas[escolha].get_nome()
    resultado = services.cancelar_inscricao_modalidade(idx, nome)
    if resultado:
        print(f"Não foi possível cancelar: {resultado}")
    else:
        print(f"Matrícula em '{nome}' cancelada. Agendamentos futuros também cancelados.")


def agendar_aula(aluno, idx):
    inscritas = aluno.get_modalidades_inscritas()
    # Filtra apenas modalidades com horário fixo (não musculação)
    fixas = [m for m in inscritas if m.tem_horario_fixo()]
    if not fixas:
        print("Você não está inscrito em nenhuma modalidade com aulas agendáveis.")
        return
    print("\nModalidades disponíveis para agendamento:")
    for i, m in enumerate(fixas):
        print(f"  [{i}] {m.get_nome()} | {m.get_horario()} | Dias: {', '.join(m.get_dias_semana())}")
    try:
        escolha = int(input("Número: "))
        if escolha < 0 or escolha >= len(fixas):
            print("Número inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    m = fixas[escolha]
    data = input(f"Data da aula (Ex: DD/MM/AAAA) | Dias: {', '.join(m.get_dias_semana())}: ").strip()
    hora = input(f"Hora (padrão {m.get_horario()}, ou outra): ").strip() or m.get_horario().split(" - ")[0]

    ins, resultado = services.agendar_aula(idx, m.get_nome(), data, hora)
    if not ins:
        print(f"Não foi possível agendar: {resultado}")
    else:
        print("Aula agendada!")
        ins.exibir_info()


def ver_agenda(aluno):
    agenda = aluno.get_agenda()
    print(f"\n--- Agenda de {aluno.get_nome()} ---")
    if not agenda:
        print("Nenhum agendamento encontrado.")
        return
    for i, ins in enumerate(agenda):
        print(f"[{i}] ", end="")
        ins.exibir_info()

def gerenciar_agendamento(aluno, idx):
    ver_agenda(aluno)
    agenda = aluno.get_agenda()
    if not agenda:
        return
    try:
        i = int(input("Número do agendamento: "))
        if i < 0 or i >= len(agenda):
            print("Número inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    ins = agenda[i]
    if ins.get_status() == Inscricao.STATUS_CANCELADO:
        print("Este agendamento já está cancelado.")
        return

    print(f"\nAgendamento selecionado:")
    ins.exibir_info()
    print("1 - Confirmar presença  2 - Cancelar  0 - Voltar")
    op = input("Escolha: ").strip()
    if op == "1":
        resultado = services.confirmar_agendamento(idx, i)
        if resultado:
            print(f"Não foi possível confirmar: {resultado}")
        else:
            print("Presença confirmada!")
    elif op == "2":
        resultado = services.cancelar_agendamento(idx, i)
        if resultado:
            print(f"Não foi possível cancelar: {resultado}")
        else:
            print("Agendamento cancelado.")
    elif op == "0":
        pass
    else:
        print("Opção inválida.")


# TREINOS (aluno) 

def sugestao_treino():
    grupos = ["Peito", "Costas", "Pernas", "Ombro", "Bíceps", "Tríceps", "Abdômen"]
    print("\n--- Sugestão de Treino ---")
    print("Grupos disponíveis:", ", ".join(grupos))
    grupo = input("Grupo muscular: ").strip()
    exercicios, erro = services.sugerir_treino(grupo)
    if not exercicios:
        print(f"Não foi possível sugerir: {erro}")
    else:
        print(f"\nExercícios sugeridos para {grupo.capitalize()}:")
        for e in exercicios:
            print(f"  - {e}")


def ver_historico_treinos(aluno):
    treinos = aluno.get_historico_treinos()
    print(f"\nHistórico de treinos de {aluno.get_nome()}:")
    if not treinos:
        print("Nenhum treino registrado ainda.")
        return
    for t in treinos:
        t.exibir_info()
        linha()


def registrar_treino_aluno(aluno):
    print("\n--- Registrar Treino ---")
    grupos = ["Peito", "Costas", "Pernas", "Ombro", "Bíceps", "Tríceps", "Abdômen"]
    print("Grupos disponíveis:", ", ".join(grupos))
    grupo  = input("Grupo muscular: ").strip()
    series = input("Séries: ").strip()
    reps = input("Repetições: ").strip()
    data = input("Data (ex: DD/MM/AAAA): ").strip()

    try:
        alunos = repository.listar_alunos()
        idx    = alunos.index(aluno)
        treino, resultado = services.registrar_treino(idx, grupo, int(series), int(reps), data)
        if not treino:
            print(f"Não foi possível registrar: {resultado}")
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
            match op:
                case "1":
                    usuario.exibir_info()
                case "2":
                    ver_historico_aluno(aluno=usuario)
                case "3":
                    registrar_frequencia(aluno=usuario)
                case "4":
                    menu_modalidades_aluno(usuario)
                case "5":
                    ver_historico_treinos(usuario)
                case "6":
                    sugestao_treino()
                case "7":
                    alunos = repository.listar_alunos()
                    idx = alunos.index(usuario)
                    nome = input(f"Novo nome [{usuario.get_nome()}]: ").strip()
                    email = input(f"Novo email [{usuario.get_email()}]: ").strip()
                    senha = input("Nova senha (em branco para manter): ").strip()
                    repository.atualizar_aluno(idx, nome or None, email or None, None, None)
                    if senha:
                        usuario.set_senha(senha)
                    print("Dados atualizados!")
                case "0":
                    print(f"Até logo, {usuario.get_nome()}!")
                    break
                case _:
                    print("Opção inválida.")

        elif eh_admin:
            match op:
                case "1":
                    menu_usuarios()
                case "2":
                    menu_alunos()
                case "3":
                    menu_planos()
                case "4":
                    menu_modalidades()
                case "5":
                    # Admin pode ver treinos de qualquer aluno
                    listar_alunos()
                    alunos = repository.listar_alunos()
                    if alunos:
                        try:
                            idx = int(input("ID do aluno: "))
                            ver_historico_treinos(alunos[idx])
                        except (ValueError, IndexError):
                            print("ID inválido.")
                case "0":
                    print(f"Até logo, {usuario.get_nome()}!")
                    break
                case _:
                    print("Opção inválida.")


# PONTO DE ENTRADA 

def main():
    repository.inicializar_dados()
    usuario = tela_login()
    if usuario:
        menu_principal(usuario)

main()