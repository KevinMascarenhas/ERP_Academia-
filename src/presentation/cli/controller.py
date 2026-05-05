# Controlador principal da CLI. Orquestra o fluxo da aplicação: autenticação, menu principal, e roteamento para funcionalidades por tipo de usuário.

# Infrastructure
from infrastructure.repositories.in_memory import *
from infrastructure.database.seed import *
from infrastructure.logging import Logger

# Use Cases
from use_cases.usuario import *
from use_cases.modalidade import *
from use_cases.plano import CriarPlanoUseCase
from use_cases.treino import *
from use_cases.pagamento import *
from use_cases.funcionario import CriarFuncionarioUseCase

# Domain
from domain.entities.models import Administrador, Aluno, Funcionario

# Presentation
from presentation.menus.login import tela_login
from presentation.menus.menu_admin import menu_admin, menu_funcionarios
from presentation.menus.menu_alunos import menu_alunos, ver_historico_aluno, registrar_frequencia
from presentation.menus.menu_planos import menu_planos
from presentation.menus.menu_modalidades import menu_modalidades
from presentation.menus.menu_modalidades_aluno import menu_modalidades_aluno
from presentation.menus.menu_treino import ver_historico_treinos, sugestao_treino
from presentation.menus.menu_funcionario import menu_funcionario

# Instanciar repositórios
usuario_repo = UsuarioRepository()
admin_repo = AdminRepository()
aluno_repo = AlunoRepository()
plano_repo = PlanoRepository()
modalidade_repo = ModalidadeRepository()
funcionario_repo = FuncionarioRepository()
pagamento_repo = PagamentoRepository()

# Instanciar logger
logger = Logger("log.txt")

# Instanciar use cases
autenticar_uc = AutenticarUseCase(usuario_repo, admin_repo, aluno_repo, funcionario_repo, logger=logger)
criar_usuario_uc = CriarUsuarioUseCase(usuario_repo, admin_repo)
criar_admin_uc = CriarAdminUseCase(usuario_repo, admin_repo, logger=logger)
criar_aluno_uc = CriarAlunoUseCase(usuario_repo, aluno_repo, plano_repo, modalidade_repo, logger=logger)
criar_funcionario_uc = CriarFuncionarioUseCase(funcionario_repo, usuario_repo, logger=logger)
criar_modalidade_uc = CriarModalidadeUseCase(modalidade_repo, logger=logger)
inscrever_modalidade_uc = InscreverEmModalidadeUseCase(aluno_repo, modalidade_repo, logger=logger)
cancelar_inscricao_uc = CancelarInscricaoModalidadeUseCase(aluno_repo, modalidade_repo, logger=logger)
registrar_frequencia_uc = RegistrarFrequenciaUseCase(aluno_repo, modalidade_repo, logger=logger)
agendar_aula_uc = AgendarAulaUseCase(aluno_repo, modalidade_repo, logger=logger)
confirmar_agendamento_uc = ConfirmarAgendamentoUseCase(aluno_repo, logger=logger)
cancelar_agendamento_uc = CancelarAgendamentoUseCase(aluno_repo, logger=logger)
criar_plano_uc = CriarPlanoUseCase(plano_repo, logger=logger)
registrar_treino_uc = RegistrarTreinoUseCase(aluno_repo)
sugerir_treino_uc = SugerirTreinoUseCase()
criar_pagamento_uc = CriarPagamentoUseCase(pagamento_repo, aluno_repo, logger=logger)
confirmar_pagamento_uc = ConfirmarPagamentoUseCase(pagamento_repo, aluno_repo, logger=logger)
cancelar_pagamento_uc = CancelarPagamentoUseCase(pagamento_repo, aluno_repo, logger=logger)
marcar_atraso_uc = MarcarAtrasoUseCase(pagamento_repo, logger=logger)


def menu_principal(usuario):
    eh_admin = isinstance(usuario, Administrador)
    eh_aluno = isinstance(usuario, Aluno)
    eh_funcionario = isinstance(usuario, Funcionario)

    while True:
        print(f"\n=== ACADEMIA WINNER | {usuario.get_perfil().upper()} ===")
        for opcao in usuario.exibir_menu():
            print(opcao)

        op = input("Escolha: ").strip()

        if eh_aluno:
            match op:
                case "1":
                    usuario.exibir_info()
                case "2":
                    ver_historico_aluno(aluno_repo, aluno=usuario)
                case "3":
                    registrar_frequencia(aluno_repo, modalidade_repo, registrar_frequencia_uc, aluno=usuario)
                case "4":
                    menu_modalidades_aluno(
                        aluno_repo, modalidade_repo, 
                        inscrever_modalidade_uc, cancelar_inscricao_uc, 
                        agendar_aula_uc, confirmar_agendamento_uc, cancelar_agendamento_uc,
                        aluno_logado=usuario
                    )
                case "5":
                    ver_historico_treinos(aluno_repo)
                case "6":
                    sugestao_treino(sugerir_treino_uc)
                case "7":
                    nome  = input(f"Novo nome [{usuario.get_nome()}]: ").strip()
                    email = input(f"Novo email [{usuario.get_email()}]: ").strip()
                    senha = input("Nova senha (em branco para manter): ").strip()
                    alunos = aluno_repo.listar()
                    idx = alunos.index(usuario)
                    aluno_repo.atualizar(idx, nome or None, email or None, None, None)
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
                    menu_admin(admin_repo, criar_usuario_uc)
                case "2":
                    menu_alunos(
                        aluno_repo, plano_repo, modalidade_repo, 
                        criar_aluno_uc, registrar_frequencia_uc, 
                        sugerir_treino_uc, registrar_treino_uc
                    )
                case "3":
                    menu_planos(plano_repo, criar_plano_uc)
                case "4":
                    menu_modalidades(modalidade_repo, criar_modalidade_uc)
                case "5":
                    from presentation.menus.menu_alunos import listar_alunos
                    listar_alunos(aluno_repo)
                    alunos = aluno_repo.listar()
                    if alunos:
                        try:
                            idx = int(input("ID do aluno: "))
                            ver_historico_treinos(aluno_repo)
                        except (ValueError, IndexError):
                            print("ID inválido.")
                case "6":
                    menu_funcionarios(funcionario_repo, criar_funcionario_uc)
                case "0":
                    print(f"Até logo, {usuario.get_nome()}!")
                    break
                case _:
                    print("Opção inválida.")

        elif eh_funcionario:
            match op:
                case "1":
                    from presentation.menus.menu_alunos import listar_alunos
                    listar_alunos(aluno_repo)
                case "2":
                    from presentation.menus.menu_funcionario import cadastrar_aluno
                    cadastrar_aluno(aluno_repo, plano_repo, modalidade_repo, criar_aluno_uc)
                case "3":
                    from presentation.menus.menu_funcionario import atualizar_aluno
                    atualizar_aluno(aluno_repo, plano_repo)
                case "4":
                    from presentation.menus.menu_funcionario import registrar_frequencia
                    registrar_frequencia(aluno_repo, modalidade_repo, registrar_frequencia_uc)
                case "5":
                    sugestao_treino(sugerir_treino_uc)
                case "6":
                    from presentation.menus.menu_funcionario import gerenciar_pagamentos
                    gerenciar_pagamentos(
                        pagamento_repo, aluno_repo,
                        criar_pagamento_uc, confirmar_pagamento_uc,
                        cancelar_pagamento_uc, marcar_atraso_uc
                    )
                case "7":
                    from presentation.menus.menu_funcionario import gerenciar_treinos_alunos
                    gerenciar_treinos_alunos(aluno_repo)
                case "8":
                    usuario.exibir_info()
                case "0":
                    print(f"Até logo, {usuario.get_nome()}!")
                    break
                case _:
                    print("Opção inválida.")


def main():
    inicializar_dados(usuario_repo, admin_repo, aluno_repo, plano_repo, modalidade_repo, funcionario_repo)
    usuario = tela_login(autenticar_uc)
    if usuario:
        menu_principal(usuario)


if __name__ == "__main__":
    main()
