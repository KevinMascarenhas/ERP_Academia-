# camada que define as entidades do sistema. Cada classe tem seus atributos e métodos para acessar e modificar esses atributos.

from abc import ABC, abstractmethod

class Usuario(ABC): 
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha    

    # Setters
    def set_nome(self, nome):
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

    @abstractmethod
    def exibir_info(self):
        pass


class Administrador(Usuario):
    # Usuário com acesso total ao sistema da academia.

    def __init__(self, nome, email, senha):
        super().__init__(nome, email, senha)

    def get_perfil(self):
        return "Administrador"

    def exibir_menu(self):
        return [
            "1 - Gerenciar Usuários",
            "2 - Gerenciar Alunos",
            "3 - Gerenciar Planos",
            "4 - Gerenciar Modalidades",
            "5 - Gerenciar Treinos",
            "0 - Sair"
        ]

    def exibir_info(self):
        print(f"  Nome: {self.nome}")
        print(f"  Email: {self.email}")
        print(f"  Perfil: {self.get_perfil()}")


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
        print(f"  Plano: {self.nome_plano}")
        print(f"  Preço: R$ {self.preco:.2f}/mês")
        print(f"  Modalidades inclusas: {self.modalidades_inclusas}")
        print(f"  Duração: {self.duracao_meses} mês(es)")


class Modalidade:
    # Representa uma modalidade da academia. Para modalidades que não são musculação, dias_semana define
    # os dias fixos em que as aulas ocorrem (ex: ['Terça', 'Quinta']).
    # Musculação tem acesso livre e não usa dias_semana.

    def __init__(self, modalidade_nome, categoria, horario, dias_semana=None):
        self.modalidade_nome = modalidade_nome
        self.categoria = categoria
        self.horario = horario
        # Lista de dias da semana em que a modalidade ocorre.
        # None ou lista vazia = acesso livre (ex: Musculação).
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
        """Retorna True se a modalidade tem aulas em dias/horários fixos."""
        return len(self.dias_semana) > 0

    def exibir_info(self):
        print(f"  Modalidade: {self.modalidade_nome}")
        print(f"  Categoria: {self.categoria}")
        print(f"  Horário: {self.horario}")
        if self.dias_semana:
            print(f"  Dias: {', '.join(self.dias_semana)}")
        else:
            print(f"  Dias: Acesso livre")


class Inscricao:
    # Representa a inscrição de um aluno em uma modalidade com horário fixo.
    
    # Status possíveis:
    # - 'pendente'   : inscrito, ainda não confirmou presença
    # - 'confirmado' : aluno confirmou que vai comparecer
    # - 'cancelado'  : aluno cancelou a inscrição/presença
    
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
        icone = {"pendente": "⏳", "confirmado": "✅", "cancelado": "❌"}.get(self.status, "?")
        print(f"  {icone} {self.modalidade.get_nome()} | {self.data} às {self.hora} | Status: {self.status}")


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

    def get_agenda(self):
        return self.agenda

    # Frequência livre (musculação / acesso sem agendamento)

    def frequentar(self, modalidade, data=None, hora=None):
        registro = {"modalidade": modalidade, "data": data, "hora": hora}
        self.historico.append(registro)

    # Inscrição em modalidades fixas 

    def inscrever_modalidade(self, modalidade):
        if modalidade in self.modalidades_inscritas:
            return False, "Você já está inscrito nessa modalidade."
        limite = self.plano.get_modalidades_inclusas() if self.plano else 0
        if len(self.modalidades_inscritas) >= limite:
            return False, f"Seu plano ({self.plano.get_nome_plano()}) permite apenas {limite} modalidade(s)."
        self.modalidades_inscritas.append(modalidade)
        return True, None

    def cancelar_inscricao_modalidade(self, modalidade):
        if modalidade not in self.modalidades_inscritas:
            return False, "Você não está inscrito nessa modalidade."
        self.modalidades_inscritas.remove(modalidade)
        # Cancela agendamentos pendentes/confirmados desta modalidade
        for ins in self.agenda:
            if ins.get_modalidade() == modalidade and ins.get_status() != Inscricao.STATUS_CANCELADO:
                ins.cancelar()
        return True, None

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