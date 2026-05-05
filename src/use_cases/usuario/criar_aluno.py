# Use case de criação de aluno. Cria novo aluno com plano e modalidades iniciais.

from domain.entities.models import Aluno
from infrastructure.logging import Logger


class CriarAlunoUseCase:
    # Cria um novo aluno no sistema com plano e modalidades opcionais.

    def __init__(self, usuario_repo, aluno_repo, plano_repo, modalidade_repo, logger: Logger = None):
        self.usuario_repo = usuario_repo
        self.aluno_repo = aluno_repo
        self.plano_repo = plano_repo
        self.modalidade_repo = modalidade_repo
        self._logger = logger or Logger()

    def executar(self, nome, email, senha, cpf, nome_plano, nomes_modalidades=None):
        if not nome or not email or not senha or not cpf:
            return None

        if (self.usuario_repo.buscar_por_email(email) 
                or self.aluno_repo.buscar_por_email(email)):
            return None, f"Email '{email}' já está cadastrado."

        plano = self.plano_repo.buscar_por_nome(nome_plano)
        if not plano:
            return None, f"Plano '{nome_plano}' não encontrado."

        aluno = Aluno(nome, email, senha, cpf, plano)

        # Inscreve nas modalidades escolhidas, respeitando o limite do plano
        erros_modal = []
        if nomes_modalidades:
            for nm in nomes_modalidades:
                m = self.modalidade_repo.buscar_por_nome(nm)
                if not m:
                    erros_modal.append(f"Modalidade '{nm}' não encontrada.")
                    continue
                ok, err = aluno.inscrever_modalidade(m)
                if not ok:
                    erros_modal.append(err)

        self.aluno_repo.adicionar(aluno)
        self._logger.registrar("SISTEMA", f"Cadastro de aluno: {nome}")
        return aluno
