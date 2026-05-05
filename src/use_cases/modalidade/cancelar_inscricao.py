from infrastructure.logging import Logger


class CancelarInscricaoModalidadeUseCase:
    # Remove o aluno de uma modalidade fixa.

    def __init__(self, aluno_repo, modalidade_repo, logger: Logger = None):
        self.aluno_repo = aluno_repo
        self.modalidade_repo = modalidade_repo
        self._logger = logger or Logger()

    def executar(self, idx_aluno, nome_modalidade):
        modalidade = self.modalidade_repo.buscar_por_nome(nome_modalidade)
        if not modalidade:
            return f"Modalidade '{nome_modalidade}' não encontrada."
        
        resultado = self.aluno_repo.cancelar_inscricao_modalidade(idx_aluno, modalidade)
        if resultado:
            alunos = self.aluno_repo.listar()
            aluno_nome = alunos[idx_aluno].get_nome()
            self._logger.registrar(aluno_nome, f"Cancelamento de inscrição: {nome_modalidade}")
            return modalidade
        return None
