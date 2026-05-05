# Exceções personalizadas do domínio. Define erros de validação e negócio específicos da Academia Winner.

class DomainError(Exception):
    pass

class CampoObrigatorioError(DomainError):
    def __init__(self, campo: str):
        super().__init__(f"Campo obrigatório ausente: {campo}")


class EmailJaCadastradoError(DomainError):
    def __init__(self, email: str):
        super().__init__(f"Email '{email}' já está cadastrado.")


class PlanoNaoEncontradoError(DomainError):
    def __init__(self, nome: str):
        super().__init__(f"Plano '{nome}' não encontrado.")


class ModalidadeNaoEncontradaError(DomainError):
    def __init__(self, nome: str):
        super().__init__(f"Modalidade '{nome}' não encontrada.")


class LimitePlanoAtingidoError(DomainError):
    def __init__(self, nome_plano: str, limite: int):
        super().__init__(
            f"Plano '{nome_plano}' permite apenas {limite} modalidade(s)."
        )


class AlunoJaInscritoError(DomainError):
    def __init__(self, modalidade: str):
        super().__init__(f"Aluno já está inscrito em '{modalidade}'.")


class AlunoNaoInscritoError(DomainError):
    def __init__(self, modalidade: str):
        super().__init__(f"Aluno não está inscrito em '{modalidade}'.")


class AgendamentoNaoEncontradoError(DomainError):
    pass


class PerfilInvalidoError(DomainError):
    def __init__(self, perfil: str):
        super().__init__(f"Perfil inválido: '{perfil}'. Use 'Administrador'.")


class GrupoMuscularInvalidoError(DomainError):
    def __init__(self, grupo: str):
        super().__init__(f"Grupo muscular '{grupo}' não reconhecido.")


class ValorInvalidoError(DomainError):
    pass