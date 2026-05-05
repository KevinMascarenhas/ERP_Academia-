from infrastructure.logging import Logger


class CancelarAgendamentoUseCase:
    # Cancela um agendamento de aula.

    def __init__(self, aluno_repo, logger: Logger = None):
        self.aluno_repo = aluno_repo
        self._logger = logger or Logger()

    def executar(self, idx_aluno, idx_inscricao):
        ok = self.aluno_repo.cancelar_agendamento(idx_aluno, idx_inscricao)
        if ok:
            alunos = self.aluno_repo.listar()
            aluno_nome = alunos[idx_aluno].get_nome()
            agenda = alunos[idx_aluno].get_agenda()
            inscricao = agenda[idx_inscricao]
            modalidade_nome = inscricao.get_modalidade().get_nome()
            data_hora = f"{inscricao.get_data()} {inscricao.get_hora()}"
            self._logger.registrar(aluno_nome, f"Cancelamento de agendamento: {modalidade_nome} em {data_hora}")
        return None if ok else "Agendamento não encontrado."
