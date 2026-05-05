# Menu de funcionário. Funcionalidades: gerenciar alunos, registrar frequências, pagamentos, treinos.

from .menu_alunos import (listar_alunos as listar_alunos_base, cadastrar_aluno, 
                          atualizar_aluno, registrar_frequencia, remover_aluno)


def listar_alunos(aluno_repo):
    alunos = aluno_repo.listar()
    print("\n--- Lista de Alunos ---")
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return
    for i, a in enumerate(alunos):
        plano = a.get_plano().get_nome_plano() if a.get_plano() else "Sem plano"
        print(f"[{i}] {a.get_nome()} | CPF: {a.get_cpf()} | Plano: {plano}")


def gerenciar_pagamentos(pagamento_repo, aluno_repo, criar_pagamento_uc, confirmar_pagamento_uc, cancelar_pagamento_uc, marcar_atraso_uc):
    while True:
        print("\n=== GERENCIAR PAGAMENTOS ===")
        print("1 - Registrar novo pagamento")
        print("2 - Confirmar pagamento")
        print("3 - Marcar como atrasado")
        print("4 - Cancelar pagamento")
        print("5 - Listar pagamentos pendentes")
        print("6 - Listar pagamentos atrasados")
        print("7 - Listar pagamentos de um aluno")
        print("0 - Voltar")
        op = input("Escolha: ").strip()
        
        if op == "1":
            # Registrar novo pagamento
            listar_alunos(aluno_repo)
            try:
                idx_aluno = int(input("Escolha um aluno (idx): ").strip())
            except ValueError:
                print("Índice inválido.")
                continue
            
            alunos = aluno_repo.listar()
            if not (0 <= idx_aluno < len(alunos)):
                print("Índice inválido.")
                continue
            
            mes_ano = input("Mês/Ano (formato MM/YYYY): ").strip()
            valor = input("Valor da mensalidade: ").strip()
            
            pagamento = criar_pagamento_uc.executar(idx_aluno, mes_ano, valor)
            if not pagamento:
                print("Erro ao registrar pagamento!")
            else:
                print("Pagamento registrado com sucesso!")
        
        elif op == "2":
            # Confirmar pagamento
            pagamentos = pagamento_repo.listar()
            print("\n--- Pagamentos ---")
            for i, p in enumerate(pagamentos):
                print(f"[{i}] {p.get_aluno().get_nome()} | {p.get_mes_ano()} | Status: {p.get_status()}")
            
            try:
                idx_pag = int(input("Escolha um pagamento (idx): ").strip())
            except ValueError:
                print("Índice inválido.")
                continue
            
            data = input("Data do pagamento (opcional, YYYY-MM-DD): ").strip()
            pagamento = confirmar_pagamento_uc.executar(idx_pag, data if data else None)
            if not pagamento:
                print("Erro ao confirmar pagamento!")
            else:
                print("Pagamento confirmado!")
        
        elif op == "3":
            # Marcar como atrasado
            pagamentos = pagamento_repo.listar()
            print("\n--- Pagamentos Pendentes ---")
            for i, p in enumerate(pagamentos):
                if p.get_status() == "pendente":
                    print(f"[{i}] {p.get_aluno().get_nome()} | {p.get_mes_ano()} | R$ {p.get_valor():.2f}")
            
            try:
                idx_pag = int(input("Escolha um pagamento (idx): ").strip())
            except ValueError:
                print("Índice inválido.")
                continue
            
            pagamento = marcar_atraso_uc.executar(idx_pag)
            if not pagamento:
                print("Erro ao marcar como atrasado!")
            else:
                print("Pagamento marcado como atrasado!")
        
        elif op == "4":
            # Cancelar pagamento
            pagamentos = pagamento_repo.listar()
            print("\n--- Pagamentos ---")
            for i, p in enumerate(pagamentos):
                print(f"[{i}] {p.get_aluno().get_nome()} | {p.get_mes_ano()} | Status: {p.get_status()}")
            
            try:
                idx_pag = int(input("Escolha um pagamento (idx): ").strip())
            except ValueError:
                print("Índice inválido.")
                continue
            
            pagamento = cancelar_pagamento_uc.executar(idx_pag)
            if not pagamento:
                print("Erro ao cancelar pagamento!")
            else:
                print("Pagamento cancelado!")
        
        elif op == "5":
            # Listar pagamentos pendentes
            pendentes = pagamento_repo.listar_pendentes()
            print("\n--- Pagamentos Pendentes ---")
            if not pendentes:
                print("Nenhum pagamento pendente.")
            else:
                for p in pendentes:
                    print(f"  {p.get_aluno().get_nome()} | {p.get_mes_ano()} | R$ {p.get_valor():.2f}")
        
        elif op == "6":
            # Listar pagamentos atrasados
            atrasados = pagamento_repo.listar_atrasados()
            print("\n--- Pagamentos Atrasados ---")
            if not atrasados:
                print("Nenhum pagamento atrasado.")
            else:
                for p in atrasados:
                    print(f"  {p.get_aluno().get_nome()} | {p.get_mes_ano()} | R$ {p.get_valor():.2f}")
        
        elif op == "7":
            # Listar pagamentos de um aluno
            listar_alunos(aluno_repo)
            try:
                idx_aluno = int(input("Escolha um aluno (idx): ").strip())
            except ValueError:
                print("Índice inválido.")
                continue
            
            alunos = aluno_repo.listar()
            if not (0 <= idx_aluno < len(alunos)):
                print("Índice inválido.")
                continue
            
            aluno = alunos[idx_aluno]
            pagamentos = pagamento_repo.listar_por_aluno(aluno)
            print(f"\n--- Pagamentos de {aluno.get_nome()} ---")
            if not pagamentos:
                print("Nenhum pagamento registrado.")
            else:
                for p in pagamentos:
                    print(f"  {p.get_mes_ano()} | R$ {p.get_valor():.2f} | Status: {p.get_status()}")
        
        elif op == "0":
            break
        else:
            print("Opção inválida.")


def gerenciar_treinos_alunos(aluno_repo):
    while True:
        print("\n=== GERENCIAR TREINOS DE ALUNOS ===")
        print("1 - Ver histórico de treinos de um aluno")
        print("0 - Voltar")
        op = input("Escolha: ").strip()
        
        if op == "1":
            listar_alunos(aluno_repo)
            try:
                idx_aluno = int(input("Escolha um aluno (idx): ").strip())
            except ValueError:
                print("Índice inválido.")
                continue
            
            alunos = aluno_repo.listar()
            if not (0 <= idx_aluno < len(alunos)):
                print("Índice inválido.")
                continue
            
            aluno = alunos[idx_aluno]
            treinos = aluno.get_historico_treinos()
            print(f"\n--- Histórico de Treinos de {aluno.get_nome()} ---")
            if not treinos:
                print("Nenhum treino registrado.")
            else:
                for i, t in enumerate(treinos):
                    print(f"\n[{i}]")
                    t.exibir_info()
        
        elif op == "0":
            break
        else:
            print("Opção inválida.")


def gerenciar_alunos_funcionario(aluno_repo, plano_repo, modalidade_repo, criar_aluno_uc, registrar_frequencia_uc):
    while True:
        print("\n=== GERENCIAR ALUNOS ===")
        print("1 - Listar Alunos")
        print("2 - Cadastrar Aluno")
        print("3 - Atualizar Aluno")
        print("4 - Registrar Frequência")
        print("5 - Remover Aluno")
        print("0 - Voltar")
        op = input("Escolha: ").strip()
        
        if op == "1":
            listar_alunos(aluno_repo)
        
        elif op == "2":
            cadastrar_aluno(aluno_repo, plano_repo, modalidade_repo, criar_aluno_uc)
        
        elif op == "3":
            atualizar_aluno(aluno_repo, plano_repo)
        
        elif op == "4":
            registrar_frequencia(aluno_repo, modalidade_repo, registrar_frequencia_uc)
        
        elif op == "5":
            remover_aluno(aluno_repo)
        
        elif op == "0":
            break
        else:
            print("Opção inválida.")


def menu_funcionario(aluno_repo, plano_repo, modalidade_repo, pagamento_repo, criar_aluno_uc, criar_pagamento_uc, confirmar_pagamento_uc, cancelar_pagamento_uc, marcar_atraso_uc, registrar_frequencia_uc):
    while True:
        print("\n=== FUNCIONÁRIO - MENU PRINCIPAL ===")
        print("1 - Listar Alunos")
        print("2 - Cadastrar Aluno")
        print("3 - Atualizar Aluno")
        print("4 - Registrar Frequência")
        print("5 - Sugestão de Treino")
        print("6 - Gerenciar Pagamentos")
        print("7 - Gerenciar Treinos de Alunos")
        print("8 - Ver meu perfil")
        print("0 - Sair")
        op = input("Escolha: ").strip()
        
        if op == "1":
            listar_alunos(aluno_repo)
        
        elif op == "2":
            cadastrar_aluno(aluno_repo, plano_repo, modalidade_repo, criar_aluno_uc)
        
        elif op == "3":
            atualizar_aluno(aluno_repo, plano_repo)
        
        elif op == "4":
            registrar_frequencia(aluno_repo, modalidade_repo, registrar_frequencia_uc)
        
        elif op == "5":
            print("Sugestão de Treino - A implementar")
        
        elif op == "6":
            gerenciar_pagamentos(pagamento_repo, aluno_repo, criar_pagamento_uc, confirmar_pagamento_uc, cancelar_pagamento_uc, marcar_atraso_uc)
        
        elif op == "7":
            gerenciar_treinos_alunos(aluno_repo)
        
        elif op == "8":
            print("Ver meu perfil - A implementar")
        
        elif op == "0":
            break
        else:
            print("Opção inválida.")
