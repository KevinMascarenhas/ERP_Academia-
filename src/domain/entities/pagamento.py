class Pagamento:
    # Representa um pagamento de mensalidade de um aluno
    STATUS_PENDENTE = "pendente"
    STATUS_PAGO = "pago"
    STATUS_ATRASADO = "atrasado"

    def __init__(self, aluno, valor, mes_ano, status=STATUS_PENDENTE):
        self.aluno = aluno
        self.valor = valor
        self.mes_ano = mes_ano
        self.status = status
        self.data_pagamento = None

    def pagar(self, data_pagamento=None):
        self.status = self.STATUS_PAGO
        self.data_pagamento = data_pagamento

    def marcar_atrasado(self):
        # Marca o pagamento como atrasado.
        if self.status == self.STATUS_PENDENTE:
            self.status = self.STATUS_ATRASADO

    def get_aluno(self):
        return self.aluno

    def get_valor(self):
        return self.valor

    def get_mes_ano(self):
        return self.mes_ano

    def get_status(self):
        return self.status

    def get_data_pagamento(self):
        return self.data_pagamento

    def exibir_info(self):
        aluno_nome = self.aluno.get_nome() if hasattr(self.aluno, 'get_nome') else str(self.aluno)
        print(f"  Aluno: {aluno_nome}")
        print(f"  Mês/Ano: {self.mes_ano}")
        print(f"  Valor: R$ {self.valor:.2f}")
        print(f"  Status: {self.status}")
        if self.data_pagamento:
            print(f"  Data do pagamento: {self.data_pagamento}")
