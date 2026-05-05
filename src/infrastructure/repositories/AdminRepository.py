from domain.entities import Administrador
from domain.interfaces import IAdminRepository

class AdminRepository(IAdminRepository):
    def __init__(self):
        self.administradores = []

    def adicionar(self, admin: Administrador):
        self.administradores.append(admin)

    def listar(self):
        return list(self.administradores)

    def buscar_por_email(self, email: str):
        for a in self.administradores:
            if a.get_email().lower() == email.lower():
                return a
        return None

    def atualizar(self, idx: int, nome=None, email=None, senha=None):
        a = self.administradores[idx]
        if nome:
            a.set_nome(nome)
        if email:
            a.set_email(email)
        if senha:
            a.set_senha(senha)

    def remover(self, idx: int):
        return self.administradores.pop(idx)