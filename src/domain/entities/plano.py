class Plano:
    def __init__(self, nome_plano, preco, modalidades_inclusas, duracao_meses):
        self.nome_plano = nome_plano
        self.preco = preco
        self.modalidades_inclusas = modalidades_inclusas  # quantidade de modalidades permitidas
        self.duracao_meses = duracao_meses

    # Setters
    def set_preco(self, preco):
        self.preco = preco

    def set_modalidades_inclusas(self, modalidades):
        self.modalidades_inclusas = modalidades

    def set_duracao_meses(self, duracao):
        self.duracao_meses = duracao

    # Getters
    def get_nome_plano(self):
        return self.nome_plano

    def get_preco(self):
        return self.preco

    def get_modalidades_inclusas(self):
        return self.modalidades_inclusas

    def get_duracao_meses(self):
        return self.duracao_meses

    def exibir_info(self):
        print(f"Plano: {self.nome_plano}")
        print(f"Preço: R$ {self.preco:.2f}/mês")
        print(f"Modalidades inclusas: {self.modalidades_inclusas}")
        print(f"Duração: {self.duracao_meses} mês(es)")
