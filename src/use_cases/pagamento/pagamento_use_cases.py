# Use cases de pagamento. Gerencia registro, confirmação, cancelamento e atraso de pagamentos.

from domain.entities.models import Pagamento
from infrastructure.logging import Logger


class CriarPagamentoUseCase:
    def __init__(self, pagamento_repo, aluno_repo, logger: Logger = None):
        self.pagamento_repo = pagamento_repo
        self.aluno_repo = aluno_repo
        self._logger = logger or Logger()
    
    def executar(self, idx_aluno, mes_ano, valor):
        if not mes_ano or not valor:
            return None, "Mês/Ano e valor são obrigatórios."
        
        try:
            valor_float = float(valor)
            if valor_float <= 0:
                return None, "O valor deve ser maior que zero."
        except ValueError:
            return None, "Valor inválido."
        
        alunos = self.aluno_repo.listar()
        aluno = alunos[idx_aluno]
        
        # Verifica se já existe pagamento para este mês
        if self.pagamento_repo.buscar_por_aluno_mes(aluno, mes_ano):
            return None, f"Já existe um pagamento registrado para {mes_ano}."
        
        pagamento = Pagamento(aluno, valor_float, mes_ano)
        self.pagamento_repo.adicionar(pagamento)
        self._logger.registrar("SISTEMA", f"Registro de pagamento: {aluno.get_nome()} - {mes_ano} - R$ {valor_float:.2f}")
        return pagamento


class ConfirmarPagamentoUseCase:

    
    def __init__(self, pagamento_repo, aluno_repo, logger: Logger = None):
        self.pagamento_repo = pagamento_repo
        self.aluno_repo = aluno_repo
        self._logger = logger or Logger()
    
    def executar(self, idx_pagamento, data_pagamento=None):
        pagamentos = self.pagamento_repo.listar()
        if not (0 <= idx_pagamento < len(pagamentos)):
            return None, "Pagamento não encontrado."
        
        pagamento = pagamentos[idx_pagamento]
        pagamento.pagar(data_pagamento)
        aluno_nome = pagamento.get_aluno().get_nome()
        self._logger.registrar("SISTEMA", f"Pagamento confirmado: {aluno_nome} - {pagamento.get_mes_ano()}")
        return pagamento


class CancelarPagamentoUseCase:
    def __init__(self, pagamento_repo, aluno_repo, logger: Logger = None):
        self.pagamento_repo = pagamento_repo
        self.aluno_repo = aluno_repo
        self._logger = logger or Logger()
    
    def executar(self, idx_pagamento):
        pagamentos = self.pagamento_repo.listar()
        if not (0 <= idx_pagamento < len(pagamentos)):
            return None, "Pagamento não encontrado."
        
        pagamento = pagamentos[idx_pagamento]
        aluno_nome = pagamento.get_aluno().get_nome()
        mes_ano = pagamento.get_mes_ano()
        
        self.pagamento_repo.remover(idx_pagamento)
        self._logger.registrar("SISTEMA", f"Pagamento cancelado: {aluno_nome} - {mes_ano}")
        return pagamento


class MarcarAtrasoUseCase:
    def __init__(self, pagamento_repo, logger: Logger = None):
        self.pagamento_repo = pagamento_repo
        self._logger = logger or Logger()
    
    def executar(self, idx_pagamento):
        pagamentos = self.pagamento_repo.listar()
        if not (0 <= idx_pagamento < len(pagamentos)):
            return None, "Pagamento não encontrado."
        
        pagamento = pagamentos[idx_pagamento]
        if pagamento.get_status() != Pagamento.STATUS_PENDENTE:
            return None, "Apenas pagamentos pendentes podem ser marcados como atrasados."
        
        pagamento.marcar_atrasado()
        aluno_nome = pagamento.get_aluno().get_nome()
        self._logger.registrar("SISTEMA", f"Pagamento marcado como atrasado: {aluno_nome} - {pagamento.get_mes_ano()}")
        return pagamento
