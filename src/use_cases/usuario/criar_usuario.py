from domain.entities.models import Administrador, Funcionario
from infrastructure.logging import Logger


class CriarUsuarioUseCase:
    # Cria um novo usuário no sistema.

    def __init__(self, usuario_repo, admin_repo):
        self.usuario_repo = usuario_repo
        self.admin_repo = admin_repo

    def executar(self, nome, email, senha, perfil):
        if not nome or not email or not senha:
            return None, "Todos os campos são obrigatórios."

        if (self.usuario_repo.buscar_por_email(email)
                or self.admin_repo.buscar_por_email(email)):
            return None, f"Email '{email}' já está cadastrado."

        if perfil.lower() == "Administrador":
            u = Administrador(nome, email, senha)
            self.admin_repo.adicionar(u)
            self.usuario_repo.adicionar(u)
            return u, None
        
        if perfil.lower() == "Funcionário":
            u = Funcionario(nome, email, senha)
            self.usuario_repo.adicionar(u)
            self.funcionario_repo.adicionar(u)
            return u, None

        return None, "Perfil inválido. Use 'Administrador' ou 'Funcionário'."
