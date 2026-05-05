from datetime import datetime
from infrastructure.logging import Logger


class AgendarAulaUseCase:
    # Agenda uma aula para o aluno. O aluno deve estar inscrito na modalidade.

    def __init__(self, aluno_repo, modalidade_repo, logger: Logger = None):
        self.aluno_repo = aluno_repo
        self.modalidade_repo = modalidade_repo
        self._logger = logger or Logger()

    def _validar_data(self, data: str) -> bool:
        #Valida se a data está no formato DD/MM/YYYY.
        if not data or len(data) != 10:
            return False
        try:
            partes = data.split('/')
            if len(partes) != 3:
                return False
            dia, mes, ano = int(partes[0]), int(partes[1]), int(partes[2])
            # Valida se a data é válida
            datetime(ano, mes, dia)
            return True
        except (ValueError, IndexError):
            return False

    def _validar_hora(self, hora: str) -> bool:
        # Valida se a hora está no formato HH:MM
        if not hora or len(hora) != 5:
            return False
        try:
            partes = hora.split(':')
            if len(partes) != 2:
                return False
            horas, minutos = int(partes[0]), int(partes[1])
            if not (0 <= horas < 24 and 0 <= minutos < 60):
                return False
            return True
        except (ValueError, IndexError):
            return False

    def _validar_compatibilidade_horario(self, hora_entrada: str, hora_modalidade: str) -> bool:
        # Valida se a hora de entrada é compatível com o horário da modalidade.
        # Considera compatível se a hora de entrada for exatamente igual ou dentro de um intervalo de 30 min.
        try:
            h_ent, m_ent = map(int, hora_entrada.split(':'))
            h_mod, m_mod = map(int, hora_modalidade.split(':'))
            
            # Converte para minutos para facilitar comparação
            minutos_entrada = h_ent * 60 + m_ent
            minutos_modalidade = h_mod * 60 + m_mod
            
            # Permite variação de ±30 minutos
            diferenca = abs(minutos_entrada - minutos_modalidade)
            return diferenca <= 30
        except (ValueError, IndexError):
            return False

    def executar(self, idx_aluno, nome_modalidade, data, hora):
        modalidade = self.modalidade_repo.buscar_por_nome(nome_modalidade)
        if not modalidade:
            return f"Modalidade '{nome_modalidade}' não encontrada."

        alunos = self.aluno_repo.listar()
        aluno = alunos[idx_aluno]
        if modalidade not in aluno.get_modalidades_inscritas():
            return f"Você não está matriculado em '{nome_modalidade}'. Inscreva-se primeiro."

        if not data or not hora:
            return "Data e hora são obrigatórios."

        # Validar formato de data
        if not self._validar_data(data):
            return "Data inválida. Use o formato DD/MM/YYYY."

        # Validar formato de hora
        if not self._validar_hora(hora):
            return "Hora inválida. Use o formato HH:MM."

        # Validar compatibilidade de horário com a modalidade
        if not self._validar_compatibilidade_horario(hora, modalidade.get_horario()):
            return f"Hora incompatível. A modalidade tem aula às {modalidade.get_horario()}."

        ins = self.aluno_repo.agendar_aula(idx_aluno, modalidade, data, hora)
        alunos = self.aluno_repo.listar()
        aluno_nome = alunos[idx_aluno].get_nome()
        self._logger.registrar(aluno_nome, f"Agendamento: {nome_modalidade} em {data} às {hora}")
        return ins
