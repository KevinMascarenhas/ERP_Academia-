from domain.entities import Funcionario
from domain.interfaces import IFuncionarioRepository

class FuncionarioRepository(IFuncionarioRepository):
    # Repositório para gerenciar funcionários da academia.
    
    def __init__(self):
        self.funcionarios = []

    def adicionar(self, funcionario: Funcionario):
        self.funcionarios.append(funcionario)

    def listar(self):
        return list(self.funcionarios)

    def buscar_por_email(self, email: str):
        for f in self.funcionarios:
            if f.get_email().lower() == email.lower():
                return f
        return None

    def buscar_por_id(self, id_funcionario: str):
        for f in self.funcionarios:
            if f.get_id() == id_funcionario:
                return f
        return None

    def atualizar(self, idx: int, nome=None, email=None, senha=None):
        f = self.funcionarios[idx]
        if nome:
            f.set_nome(nome)
        if email:
            f.set_email(email)
        if senha:
            f.set_senha(senha)

    def remover(self, idx: int):
        return self.funcionarios.pop(idx)
