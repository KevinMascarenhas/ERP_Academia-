# Use case de registro de frequência. Registra presença do aluno em uma modalidade ou aula.

from infrastructure.logging import Logger


class RegistrarFrequenciaUseCase:
    # Registra frequência livre do aluno (musculação ou modalidade sem agendamento).

    def __init__(self, aluno_repo, modalidade_repo, logger: Logger = None):
        self.aluno_repo = aluno_repo
        self.modalidade_repo = modalidade_repo
        self._logger = logger or Logger()

    def executar(self, idx_aluno, nome_modalidade, data=None, hora=None):
        modalidade = self.modalidade_repo.buscar_por_nome(nome_modalidade)
        if not modalidade:
            return f"Modalidade '{nome_modalidade}' não encontrada."
        
        self.aluno_repo.registrar_frequencia(idx_aluno, modalidade, data, hora)
        alunos = self.aluno_repo.listar()
        aluno_nome = alunos[idx_aluno].get_nome()
        data_hora = f"{data} {hora}" if data and hora else (data or hora or "sem data/hora")
        self._logger.registrar(aluno_nome, f"Registro de freqüência: {nome_modalidade} em {data_hora}")
        return modalidade
