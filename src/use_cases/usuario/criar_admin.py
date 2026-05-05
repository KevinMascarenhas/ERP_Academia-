from domain.entities.models import Administrador
from infrastructure.logging import Logger


class CriarAdminUseCase:
    # Cria um novo administrador no sistema.

    def __init__(self, usuario_repo, admin_repo, logger: Logger = None):
        self.usuario_repo = usuario_repo
        self.admin_repo = admin_repo
        self._logger = logger or Logger()

    def executar(self, nome, email, senha):
        if not nome or not email or not senha:
            return None, "Todos os campos são obrigatórios."

        if (self.usuario_repo.buscar_por_email(email)
                or self.admin_repo.buscar_por_email(email)):
            return None, f"Email '{email}' já está cadastrado."

        admin = Administrador(nome, email, senha)
        self.admin_repo.adicionar(admin)
        self.usuario_repo.adicionar(admin)
        self._logger.registrar("SISTEMA", f"Cadastro de administrador: {nome}")
        return admin
