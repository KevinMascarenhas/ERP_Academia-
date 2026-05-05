# Use case de autenticação. Valida credenciais e devolve o usuário autenticado ou None.

from infrastructure.logging import Logger


class AutenticarUseCase:
    # Valida credenciais e devolve o usuário autenticado ou None.

    def __init__(self, usuario_repo, admin_repo, aluno_repo, funcionario_repo=None, logger: Logger = None):
        self._usuario_repo = usuario_repo
        self._admin_repo = admin_repo
        self._aluno_repo = aluno_repo
        self._funcionario_repo = funcionario_repo
        self._logger = logger or Logger()

    def executar(self, email: str, senha: str):
        repos = (self._usuario_repo, self._admin_repo, self._aluno_repo)
        if self._funcionario_repo:
            repos = repos + (self._funcionario_repo,)
        
        for repo in repos:
            u = repo.buscar_por_email(email)
            if u and u.get_senha() == senha:
                self._logger.registrar(email, f"Login realizado ({u.get_perfil()})")
                return u
        return None