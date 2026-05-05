# Use case de criação de plano. Cria novo plano de mensalidade com limite de modalidades.

from domain.entities.models import Plano
from infrastructure.logging import Logger


class CriarPlanoUseCase:
    # Cria um novo plano de academia no sistema.

    def __init__(self, plano_repo, logger: Logger = None):
        self.plano_repo = plano_repo
        self._logger = logger or Logger()

    def executar(self, nome, preco_str, modalidades_str, duracao_str):
        if not nome:
            return None, "Nome do plano é obrigatório."
        
        try:
            preco = float(preco_str.replace(",", "."))
            modalidades = int(modalidades_str)
            duracao = int(duracao_str)
        except ValueError:
            return None, "Preço, modalidades ou duração com valor inválido."

        if preco <= 0:
            return None, "O preço deve ser maior que zero."
        if modalidades <= 0:
            return None, "O número de modalidades deve ser maior que zero."
        if duracao <= 0:
            return None, "A duração deve ser maior que zero."

        plano = Plano(nome, preco, modalidades, duracao)
        self.plano_repo.adicionar(plano)
        self._logger.registrar("SISTEMA", f"Cadastro de plano: {nome} - R$ {preco:.2f} - {modalidades} modalidade(s) - {duracao} mês(es)")
        return plano
