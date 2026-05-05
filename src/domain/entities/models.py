# camada que define as entidades do sistema. Cada classe tem seus atributos e mÃ©todos para acessar e modificar esses atributos.
# Define as classes de domínio: Usuario (abstrata), Administrador e Aluno.

from abc import ABC, abstractmethod

from .inscricao import Inscricao


class Usuario(ABC):
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

    # Setters
    def set_nome(self, nome):
        if not nome:
            raise ValueError("Nome não pode ser vazio.")
        self.nome = nome

    def set_email(self, email):
        if not email:
            raise ValueError("Email não pode ser vazio.")
        self.email = email

    def set_senha(self, senha):
        if not senha:
            raise ValueError("Senha não pode ser vazia.")
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

    @abstractmethod
    def exibir_info(self):
        pass


class Administrador(Usuario):
    # UsuÃ¡rio com acesso total ao sistema da academia.
    def __init__(self, nome, email, senha):
        super().__init__(nome, email, senha)

    def get_perfil(self):
        return "Administrador"

    def exibir_menu(self):
        return [
            "1 - Gerenciar Administradores",
            "2 - Gerenciar Alunos",
            "3 - Gerenciar Planos",
            "4 - Gerenciar Modalidades",
            "5 - Gerenciar Treinos",
            "6 - Gerenciar Funcionários",
            "0 - Sair"
        ]

    def exibir_info(self):
        print(f"Nome: {self.nome}")
        print(f"Email: {self.email}")
        print(f"Perfil: {self.get_perfil()}")


class Aluno(Usuario):
    def __init__(self, nome, email, senha, cpf, plano, modalidades_inscritas=None):
        super().__init__(nome, email, senha)
        self.cpf = cpf
        self.plano = plano
        self.historico = []                 # registros de frequência (musculação / acesso livre)
        self.historico_treinos = []
        self.modalidades_inscritas = modalidades_inscritas if modalidades_inscritas else []
        self.agenda = []

    def get_perfil(self):
        return "Aluno"

    def exibir_menu(self):
        return [
            "1 - Ver meu perfil e plano",
            "2 - Ver histórico de frequência",
            "3 - Registrar entrada (musculação / acesso livre)",
            "4 - Minhas modalidades e agenda",
            "5 - Ver histórico de treinos",
            "6 - Sugestão de treino",
            "7 - Atualizar meus dados",
            "0 - Sair"
        ]

    # Setters exclusivos
    def set_cpf(self, cpf):
        if not cpf:
            print("CPF não pode ser vazio.")
            return
        self.cpf = cpf

    def set_plano(self, plano):
        self.plano = plano

    # Getters exclusivos
    def get_cpf(self):
        return self.cpf

    def get_plano(self):
        return self.plano

    def get_historico(self):
        return self.historico

    def get_modalidades_inscritas(self):
        return self.modalidades_inscritas

    def inscrever_modalidade(self, modalidade):
        if not self.plano:
            return "O aluno não possui um plano ativo."

        num_modalidades_permitidas = self.plano.get_modalidades_inclusas()
        num_modalidades_inscritas = len(self.modalidades_inscritas)

        if num_modalidades_inscritas >= num_modalidades_permitidas:
            return f"O aluno já atingiu o limite de {num_modalidades_permitidas} modalidade(s) permitida(s) no plano."

        if modalidade not in self.modalidades_inscritas:
            self.modalidades_inscritas.append(modalidade)

        return None  # Sem erro

    def cancelar_inscricao_modalidade(self, modalidade):
        if modalidade in self.modalidades_inscritas:
            self.modalidades_inscritas.remove(modalidade)
            return None  # Sucesso
        return "Aluno não está inscrito nessa modalidade."

    def get_agenda(self):
        return self.agenda

    # Frequência livre (musculação / acesso sem agendamento)

    def frequentar(self, modalidade, data=None, hora=None):
        registro = {"modalidade": modalidade, "data": data, "hora": hora}
        self.historico.append(registro)

    # Agenda (agendamentos com status)

    def agendar(self, modalidade, data, hora):
        # Cria uma inscrição (agendamento) para uma aula específica
        ins = Inscricao(modalidade, data, hora)
        self.agenda.append(ins)
        return ins

    # Treinos

    def get_historico_treinos(self):
        return self.historico_treinos

    def registrar_treino(self, treino):
        self.historico_treinos.append(treino)

    def exibir_info(self):
        nome_plano = self.plano.get_nome_plano() if self.plano else "Sem plano"
        print(f"Nome: {self.nome}")
        print(f"Email: {self.email}")
        print(f"CPF: {self.cpf}")
        print(f"Plano: {nome_plano}")
        if self.modalidades_inscritas:
            print("  Modalidades matriculadas:")
            for m in self.modalidades_inscritas:
                dias = f" ({', '.join(m.get_dias_semana())})" if m.get_dias_semana() else ""
                print(f"    - {m.get_nome()}{dias} | {m.get_horario()}")
        if self.historico:
            print("  Frequências registradas:")
            for reg in self.historico:
                m = reg["modalidade"] if isinstance(reg, dict) else reg
                data = reg.get("data", "") if isinstance(reg, dict) else ""
                hora = reg.get("hora", "") if isinstance(reg, dict) else ""
                info = f"- {m.get_nome()} ({m.get_categoria()})"
                if data:
                    info += f" | {data}"
                if hora:
                    info += f" às {hora}"
                print(info)


__all__ = [
    "Usuario",
    "Administrador",
    "Aluno",
    "Funcionario",
    "Plano",
    "Modalidade",
    "Inscricao",
    "Treino",
    "Pagamento",
]


def __getattr__(name):
    entidades = {
        "Funcionario": ("funcionario", "Funcionario"),
        "Plano": ("plano", "Plano"),
        "Modalidade": ("modalidade", "Modalidade"),
        "Treino": ("treino", "Treino"),
        "Pagamento": ("pagamento", "Pagamento"),
    }

    if name not in entidades:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    modulo_nome, classe_nome = entidades[name]
    modulo = __import__(f"{__package__}.{modulo_nome}", fromlist=[classe_nome])
    classe = getattr(modulo, classe_nome)
    globals()[name] = classe
    return classe
