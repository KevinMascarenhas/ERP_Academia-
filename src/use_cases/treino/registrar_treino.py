from domain.entities.models import Treino


class RegistrarTreinoUseCase:
    # Registra um treino para o aluno.

    def __init__(self, aluno_repo):
        self.aluno_repo = aluno_repo

    def executar(self, idx_aluno, grupo_muscular, series, repeticoes, data):
        if not grupo_muscular or not data:
            return None
        
        exercicios = self._exercicios_por_grupo(grupo_muscular)
        if not exercicios:
            return None, f"Grupo muscular '{grupo_muscular}' não reconhecido."
        
        treino = Treino(grupo_muscular, exercicios, series, repeticoes, data)
        self.aluno_repo.registrar_treino(idx_aluno, treino)
        return treino

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
