class Modalidade:
    # Representa uma modalidade da academia. Para modalidades que nÃ£o sÃ£o musculação, dias_semana define
    # os dias fixos em que as aulas ocorrem (ex: ['Terça', 'Quinta']).
    # Musculação tem acesso livre e não usa dias_semana.

    def __init__(self, modalidade_nome, categoria, horario, dias_semana=None):
        self.modalidade_nome = modalidade_nome
        self.categoria = categoria
        self.horario = horario
        # Lista de dias da semana em que a modalidade ocorre.
        # None ou lista vazia = acesso livre (ex: MusculaÃ§Ã£o).
        self.dias_semana = dias_semana if dias_semana else []

    # Setters
    def set_nome(self, nome):
        self.modalidade_nome = nome

    def set_categoria(self, categoria):
        self.categoria = categoria

    def set_horario(self, horario):
        self.horario = horario

    def set_dias_semana(self, dias):
        self.dias_semana = dias

    # Getters
    def get_nome(self):
        return self.modalidade_nome

    def get_categoria(self):
        return self.categoria

    def get_horario(self):
        return self.horario

    def get_dias_semana(self):
        return self.dias_semana

    def tem_horario_fixo(self):
        return len(self.dias_semana) > 0

    def exibir_info(self):
        print(f"  Modalidade: {self.modalidade_nome}")
        print(f"  Categoria: {self.categoria}")
        print(f"  Horário: {self.horario}")
        if self.dias_semana:
            print(f"  Dias: {', '.join(self.dias_semana)}")
        else:
            print(f"  Dias: Acesso livre")
