from domain.entities import Usuario
from domain.interfaces import IUsuarioRepository

class UsuarioRepository(IUsuarioRepository):
    def __init__(self):
        self.usuarios = []

    def adicionar(self, usuario: Usuario):
        self.usuarios.append(usuario)

    def listar(self):
        return list(self.usuarios)

    def buscar_por_email(self, email: str):
        for u in self.usuarios:
            if u.get_email().lower() == email.lower():
                return u
        return None

    def atualizar(self, idx: int, nome=None, email=None, senha=None):
        u = self.usuarios[idx]
        if nome:
            u.set_nome(nome)
        if email:
            u.set_email(email)
        if senha:
            u.set_senha(senha)

    def remover(self, idx: int):
        return self.usuarios.pop(idx)
