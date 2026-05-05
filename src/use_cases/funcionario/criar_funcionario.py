from domain.entities.models import Funcionario
from infrastructure.logging import Logger


class CriarFuncionarioUseCase:
    # Cria um novo funcionário no sistema.
    
    def __init__(self, funcionario_repo, usuario_repo, logger: Logger = None):
        self.funcionario_repo = funcionario_repo
        self.usuario_repo = usuario_repo
        self._logger = logger or Logger()
    
    def executar(self, nome, email, senha, id_funcionario):
        if not nome or not email or not senha or not id_funcionario:
            return None, "Todos os campos são obrigatórios."
        
        if self.usuario_repo.buscar_por_email(email) or self.funcionario_repo.buscar_por_email(email):
            return None, f"Email '{email}' já está cadastrado."
        
        if self.funcionario_repo.buscar_por_id(id_funcionario):
            return None, f"ID de funcionário '{id_funcionario}' já está registrado."
        
        funcionario = Funcionario(nome, email, senha, id_funcionario)
        self.funcionario_repo.adicionar(funcionario)
        self.usuario_repo.adicionar(funcionario)
        self._logger.registrar("SISTEMA", f"Cadastro de funcionário: {nome} (ID: {id_funcionario})")
        return funcionario
