
# camada que define as entidades do sistema. Cada classe tem seus atributos e métodos para acessar e modificar esses atributos.


from abc import ABC, abstractmethod

class Usuario(ABC): 
    @abstractmethod
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha    

    # Setters

    def set_nome(self, nome):           # Os Setters apenas recebem e validam o valor
        if not nome:
            print("Nome não pode ser vazio.")
            return
        self.nome = nome

    def set_email(self, email):
        if not email:
            print("Email não pode ser vazio.")
            return
        self.email = email

    def set_senha(self, senha):
        if not senha:
            print("Senha não pode ser vazia.")
            return
        self.senha = senha

    # Getters
    def get_nome(self):
        return self.nome

    def get_email(self):
        return self.email

    def get_senha(self):
        return self.senha

    @abstractmethod
    def get_perfil(self):
        pass

    @abstractmethod
    def exibir_menu(self):
        pass

    def exibir_info(self):
        pass


class Administrador(Usuario):
    # Usuário com acesso total ao sistema da academia. Gerencia alunos, planos, modalidades e outros usuários.

    def __init__(self, nome, email, senha):
        super().__init__(nome, email, senha,)

    def get_perfil(self):
        return "Administrador"

    def exibir_menu(self):
        return [
            "1 - Gerenciar Usuários",
            "2 - Gerenciar Planos",
            "3 - Gerenciar Modalidades",
            "4 - Gerenciar Treinos",
            "5 - Ver Histórico do Aluno",
            "0 - Sair"
        ]

    def exibir_info(self):
        print(f"  Nome: {self.nome}")
        print(f"  Usuário: {self.nome_usuario}")
        print(f"  Email: {self.email}")
        print(f"  Perfil: {self.get_perfil()}")

class Plano:
    def __init__(self, nome_plano, preco, modalidades_inclusas, duracao_meses):
        self.nome_plano = nome_plano
        self.preco = preco
        self.modalidades_inclusas = modalidades_inclusas  # ex: 1, 2 ou ilimitado
        self.duracao_meses = duracao_meses           # ex: 1, 3, 6, 12

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
        return self._modalidades_inclusas

    def get_duracao_meses(self):
        return self._duracao_meses

    def exibir_info(self):
        print(f"  Plano: {self.nome_plano}")
        print(f"  Preço: R$ {self.preco:.2f}/mês")
        print(f"  Modalidades inclusas: {self.modalidades_inclusas}")
        print(f"  Duração: {self.duracao_meses} mês(es)")

class Modalidade:
    # Representa uma modalidade oferecida pela academia. Ex: Musculação, Natação, Yoga, Spinning.
    def __init__(self, nome, categoria, horario):
        self.nome = nome
        self.categoria = categoria  # ex: "Luta", "Aquática", "Funcional"
        self.horario = horario    # ex: "07:00 - 08:00"

    # Setters
    def set_nome(self, nome):
        self._nome = nome

    def set_categoria(self, categoria):
        self._categoria = categoria

    def set_horario(self, horario):
        self._horario = horario

    # Getters
    def get_nome(self):
        return self.nome

    def get_categoria(self):
        return self.categoria

    def get_horario(self):
        return self.horario

    def exibir_info(self):
        print(f"  Modalidade: {self.nome}")
        print(f"  Categoria: {self.categoria}")
        print(f"  Horário: {self.horario}")

class Aluno(Usuario):
    def __init__(self, nome, email, senha, cpf, plano):
        super().__init__(nome, email, senha)
        self.cpf = cpf
        self.plano = plano    # objeto da classe Plano
        self.historico = []      # lista de objetos Modalidade frequentados

    def get_perfil(self):
        return "Aluno"

    def exibir_menu(self):
        return [
            "1 - Ver meu perfil e plano",
            "2 - Ver minhas modalidades frequentadas",
            "3 - Registrar frequência em modalidade",
            "4 - Atualizar meus dados",
            "5 - Ver histórico de treinos",
            "0 - Sair"
        ]

    # Setters exclusivos da classe Aluno
    def set_cpf(self, cpf):
        if not cpf:
            print("CPF não pode ser vazio.")
            return
        self.cpf = cpf

    def set_plano(self, plano):
        self.plano = plano

    # Getters exclusivos da classe Aluno
    def get_cpf(self):
        return self.cpf

    def get_plano(self):
        return self.plano

    def get_historico(self):
        return self.historico

    def frequentar(self, modalidade):
        self.historico.append(modalidade)

    def exibir_info(self):
        nome_plano = self.plano.get_nome() if self.plano else "Sem plano"
        print(f"  Nome: {self.nome}")
        print(f"  Usuário: {self.nome_usuario}")
        print(f"  Email: {self.email}")
        print(f"  CPF: {self.cpf}")
        print(f"  Plano: {nome_plano}")
        if self.historico:
            print("  Modalidades frequentadas:")
            for m in self.historico:
                print(f"- {m.get_nome()} ({m.get_categoria()})")

class Treino: 
    # Representa uma sessão de treino de musculação realizada pelo aluno.
    # Armazena o grupo muscular trabalhado, os exercícios, séries e repetições.
    # Separado de Modalidade porque é específico de musculação e tem estrutura própria de exercícios.

    def __init__(self, grupo_muscular, exercicios, series, repeticoes, data):
        self.grupo_muscular = grupo_muscular  # ex: "Peito", "Costas", "Pernas"
        self.exercicios = exercicios     # lista de strings com os nomes dos exercícios
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
            print(f"    - {e}")
 

