from .models import Usuario


class Funcionario(Usuario):
    # Funcionário da academia com acesso a gerenciamento de alunos, pagamentos e treinos

    def __init__(self, nome, email, senha, id_funcionario):
        super().__init__(nome, email, senha)
        self.id_funcionario = id_funcionario

    def get_perfil(self):
        return "Funcionário"

    def set_id(self, id_funcionario):
        if not id_funcionario:
            raise ValueError("ID do funcionário não pode ser vazio.")
        self.id_funcionario = id_funcionario

    def get_id(self):
        return self.id_funcionario

    def exibir_menu(self):
        return [
            "1 - Listar Alunos",
            "2 - Cadastrar Aluno",
            "3 - Atualizar Aluno",
            "4 - Registrar Frequência",
            "5 - Sugestão de Treino",
            "6 - Gerenciar Pagamentos",
            "7 - Gerenciar Treinos",
            "8 - Ver meu perfil",
            "0 - Sair"
        ]

    def exibir_info(self):
        print(f"Nome: {self.nome}")
        print(f"Email: {self.email}")
        print(f"ID do Funcionário: {self.id_funcionario}")
        print(f"Perfil: {self.get_perfil()}")
