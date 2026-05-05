class SugerirTreinoUseCase:
    # Sugere exercícios para um grupo muscular específico.

    def executar(self, grupo):
        exercicios = self._exercicios_por_grupo(grupo)
        return exercicios if exercicios else None

    def _exercicios_por_grupo(self, grupo):
        tabela = {
            "Peito":   ["Supino reto", "Supino inclinado", "Crucifixo", "Crossover"],
            "Costas":  ["Puxada frontal", "Remada curvada", "Remada unilateral", "Pulldown"],
            "Pernas":  ["Agachamento", "Leg press", "Cadeira extensora", "Cadeira flexora"],
            "Ombro":   ["Desenvolvimento com halteres", "Elevação lateral", "Elevação frontal", "Encolhimento"],
            "Bíceps":  ["Rosca direta", "Rosca alternada", "Rosca concentrada", "Rosca martelo"],
            "Tríceps": ["Tríceps testa", "Tríceps pulley", "Tríceps francês", "Mergulho no banco"],
            "Abdômen": ["Abdominal crunch", "Prancha", "Abdominal oblíquo", "Elevação de pernas"]
        }
        for chave, exercicios in tabela.items():
            if chave.lower() == grupo.lower():
                return exercicios
        return []
