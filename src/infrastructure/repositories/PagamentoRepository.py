from domain.entities import Pagamento, Aluno
from domain.interfaces import IPagamentoRepository

class PagamentoRepository(IPagamentoRepository):
    # Repositório para gerenciar pagamentos dos alunos.
    
    def __init__(self):
        self.pagamentos = []
    
    def adicionar(self, pagamento: Pagamento):
        self.pagamentos.append(pagamento)
    
    def listar(self):
        return list(self.pagamentos)
    
    def listar_por_aluno(self, aluno: Aluno):
        # Lista todos os pagamentos de um aluno específico.
        return [p for p in self.pagamentos if p.get_aluno() == aluno]
    
    def listar_pendentes(self):
        # Lista todos os pagamentos pendentes.
        return [p for p in self.pagamentos if p.get_status() == Pagamento.STATUS_PENDENTE]
    
    def listar_atrasados(self):
        # Lista todos os pagamentos atrasados.
        return [p for p in self.pagamentos if p.get_status() == Pagamento.STATUS_ATRASADO]
    
    def buscar_por_aluno_mes(self, aluno: Aluno, mes_ano: str):
        # Busca o pagamento de um aluno em um mês específico.
        for p in self.pagamentos:
            if p.get_aluno() == aluno and p.get_mes_ano() == mes_ano:
                return p
        return None
    
    def atualizar_status(self, idx: int, novo_status: str, data_pagamento=None):
        # Atualiza o status de um pagamento.
        p = self.pagamentos[idx]
        if novo_status == Pagamento.STATUS_PAGO:
            p.pagar(data_pagamento)
        elif novo_status == Pagamento.STATUS_ATRASADO:
            p.marcar_atrasado()
    
    def remover(self, idx: int):
        return self.pagamentos.pop(idx)
