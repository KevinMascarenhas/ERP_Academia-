# Use case de criação de modalidade. Cria nova modalidade (turma) com horário e dias da semana.

from infrastructure.logging import Logger


class CriarModalidadeUseCase:
    # Cria uma nova modalidade no sistema.

    def __init__(self, modalidade_repo, logger: Logger = None):
        self.modalidade_repo = modalidade_repo
        self._logger = logger or Logger()

    def executar(self, nome, categoria, horario, dias_semana=None):
        if not nome or not categoria or not horario:
            return None, "Todos os campos são obrigatórios."
        
        if self.modalidade_repo.buscar_por_nome(nome):
            return None, f"Modalidade '{nome}' já existe."
        
        from domain.entities.models import Modalidade
        modalidade = Modalidade(nome, categoria, horario, dias_semana)
        self.modalidade_repo.adicionar(modalidade)
        dias_info = f"Dias: {', '.join(dias_semana)}" if dias_semana else "Acesso livre"
        self._logger.registrar("SISTEMA", f"Cadastro de modalidade: {nome} ({categoria}) - {horario} - {dias_info}")
        return modalidade
