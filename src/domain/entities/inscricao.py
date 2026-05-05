class Inscricao:
    # Representa a inscrição de um aluno em uma modalidade com horário fixo.
    STATUS_PENDENTE    = "pendente"
    STATUS_CONFIRMADO  = "confirmado"
    STATUS_CANCELADO   = "cancelado"

    def __init__(self, modalidade, data, hora):
        self.modalidade = modalidade   # objeto Modalidade
        self.data = data               # string 'DD/MM/AAAA'
        self.hora = hora               # string 'HH:MM'
        self.status = self.STATUS_PENDENTE

    def confirmar(self):
        self.status = self.STATUS_CONFIRMADO

    def cancelar(self):
        self.status = self.STATUS_CANCELADO

    def get_modalidade(self):
        return self.modalidade

    def get_data(self):
        return self.data

    def get_hora(self):
        return self.hora

    def get_status(self):
        return self.status

    def exibir_info(self):
        print(f"  {self.modalidade.get_nome()} | {self.data} às {self.hora} | Status: {self.status}")
