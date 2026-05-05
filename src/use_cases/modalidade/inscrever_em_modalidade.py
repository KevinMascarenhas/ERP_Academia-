# Use case de inscrição em modalidade. Inscreve aluno em uma modalidade/turma com horário fixo.

from infrastructure.logging import Logger


class InscreverEmModalidadeUseCase:
    # Inscreve o aluno em uma modalidade com horário fixo.

    def __init__(self, aluno_repo, modalidade_repo, logger: Logger = None):
        self.aluno_repo = aluno_repo
        self.modalidade_repo = modalidade_repo
        self._logger = logger or Logger()

    def executar(self, idx_aluno, nome_modalidade):
        modalidade = self.modalidade_repo.buscar_por_nome(nome_modalidade)
        if not modalidade:
            return f"Modalidade '{nome_modalidade}' não encontrada."
        
        resultado = self.aluno_repo.inscrever_em_modalidade(idx_aluno, modalidade)
        if resultado:
            alunos = self.aluno_repo.listar()
            aluno_nome = alunos[idx_aluno].get_nome()
            self._logger.registrar(aluno_nome, f"Inscrição em modalidade: {nome_modalidade}")
            return modalidade
        return None
