class Treino:
    def __init__(self, grupo_muscular, exercicios, series, repeticoes, data):
        self.grupo_muscular = grupo_muscular
        self.exercicios = exercicios
        self.series = series
        self.repeticoes = repeticoes
        self.data = data

    def get_grupo_muscular(self):
        return self.grupo_muscular

    def get_exercicios(self):
        return self.exercicios

    def get_series(self):
        return self.series

    def get_repeticoes(self):
        return self.repeticoes

    def get_data(self):
        return self.data

    def exibir_info(self):
        print(f"  Grupo muscular: {self.grupo_muscular}")
        print(f"  Data: {self.data}")
        print(f"  Séries x Repetições: {self.series}x{self.repeticoes}")
        print(f"  Exercícios:")
        for e in self.exercicios:
            print(f" - {e}")
