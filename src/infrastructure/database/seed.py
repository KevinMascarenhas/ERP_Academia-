# Dados iniciais de exemplo — injetados nos repositórios concretos. Popula o banco com usuários, planos e modalidades padrão.

from domain.entities.models import Administrador, Aluno, Plano, Modalidade, Funcionario


def inicializar_dados(usuario_repo, admin_repo, aluno_repo, plano_repo, modalidade_repo, funcionario_repo=None):
    # Administrador padrão
    admin = Administrador("Admin", "admin@academia.com", "1234")
    admin_repo.adicionar(admin)
    usuario_repo.adicionar(admin)

    # Planos - Cada plano disponível em 3 durações (1 mês, 3 meses, 1 ano)
    # Musculação é obrigatória em todos os planos
    # Descontos: 10% para 3 meses, 20% para 1 ano
    
    # BÁSICO: 1 modalidade (+ musculação obrigatória)
    plano_repo.adicionar(Plano("Básico - 1 mês",    65.00, 1, 1))
    plano_repo.adicionar(Plano("Básico - 3 meses",  58.50, 1, 3))   # 10% desconto
    plano_repo.adicionar(Plano("Básico - 1 ano",    52.00, 1, 12))  # 20% desconto
    
    # STANDARD: 3 modalidades (+ musculação obrigatória)
    plano_repo.adicionar(Plano("Standard - 1 mês",  89.90, 3, 1))
    plano_repo.adicionar(Plano("Standard - 3 meses", 80.91, 3, 3))  # 10% desconto
    plano_repo.adicionar(Plano("Standard - 1 ano",  71.92, 3, 12))  # 20% desconto
    
    # PREMIUM: 5 modalidades (+ musculação obrigatória)
    plano_repo.adicionar(Plano("Premium - 1 mês",   125.00, 5, 1))
    plano_repo.adicionar(Plano("Premium - 3 meses", 112.50, 5, 3))  # 10% desconto
    plano_repo.adicionar(Plano("Premium - 1 ano",   100.00, 5, 12)) # 20% desconto

    # Modalidades
    modalidade_repo.adicionar(Modalidade("Musculação", "Força",       "06:00 - 22:00"))
    modalidade_repo.adicionar(Modalidade("Natação",    "Aquática",    "07:00 - 08:00", ["Terça", "Quinta"]))
    modalidade_repo.adicionar(Modalidade("Yoga",       "Relaxamento", "08:00 - 09:00", ["Segunda", "Quarta", "Sexta"]))
    modalidade_repo.adicionar(Modalidade("Muay Thai",  "Luta",        "19:00 - 20:30", ["Segunda", "Quarta"]))

    # Aluno de exemplo — plano Standard (1 mês)
    plano_standard = plano_repo.buscar_por_nome("Standard - 1 mês")
    modalidades = modalidade_repo.listar()

    joao = Aluno("João Silva", "joao@email.com", "1234", "111.111.111-11", plano_standard, [modalidades[0], modalidades[3]])

    ins1 = joao.agendar(modalidades[3], "15/04/2026", "19:00")   # pendente
    ins2 = joao.agendar(modalidades[3], "20/04/2026", "20:00")
    ins2.confirmar()

    aluno_repo.adicionar(joao)

    # Aluno sem plano
    aluno_repo.adicionar(Aluno("Kevin Mascarenhas", "kevin@gmail.com", "1234", "123.456.789-00", None))

    # Funcionário de exemplo
    if funcionario_repo:
        funcionario = Funcionario("Maria Silva", "maria@academia.com", "1234", "F001")
        funcionario_repo.adicionar(funcionario)
        usuario_repo.adicionar(funcionario)