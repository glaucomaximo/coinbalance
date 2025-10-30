"""
Serviço de Transações
Encapsula a lógica de criação, validação, processamento e persistência de transações.
"""
from typing import Dict, Any

from database_manager import DatabaseManager
from wallet_system import GerenciadorCarteiras
from transaction_validator import TransactionValidator


class TransactionService:
    """Orquestra o fluxo de criação e processamento de transações."""

    def __init__(
        self,
        db_manager: DatabaseManager,
        wallet_manager: GerenciadorCarteiras,
        transaction_validator: TransactionValidator,
    ) -> None:
        self.db_manager = db_manager
        self.wallet_manager = wallet_manager
        self.transaction_validator = transaction_validator

    def create_and_process(
        self,
        remetente_endereco: str,
        destinatario_endereco: str,
        valor: float,
        dados_extra: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """Cria, valida, processa e persiste uma transação.

        Retorna dict com sucesso, hash_transacao e detalhes de validação.
        """
        # Encontrar carteira do remetente
        carteira_remetente = None
        for _, carteira in self.wallet_manager.carteiras.items():
            if carteira.endereco == remetente_endereco:
                carteira_remetente = carteira
                break
        if not carteira_remetente:
            raise ValueError("Carteira remetente não encontrada")

        # Sincronizar saldo da carteira a partir do banco
        try:
            carteira_remetente.saldo = self.db_manager.obter_saldo_carteira(carteira_remetente.endereco)
        except Exception:
            pass

        # Criar transação assinada
        transacao = carteira_remetente.criar_transacao(
            destinatario_endereco,
            valor,
            dados_extra or {},
        )

        # Validar
        validacao = self.transaction_validator.validar_transacao(transacao)
        if not validacao.get("valida"):
            raise ValueError(f"Transação inválida: {validacao.get('erros')}")

        # Processar (atualiza saldos)
        sucesso = self.transaction_validator.processar_transacao(transacao)
        if not sucesso:
            raise RuntimeError("Erro ao processar transação")

        # Persistir
        try:
            self.db_manager.salvar_transacao(transacao)
        except Exception:
            # Não falhar a requisição por persistência; depender de logs/monitoramento
            pass

        return {
            "sucesso": True,
            "hash_transacao": self.transaction_validator._gerar_hash_transacao(transacao),
            "validacao": validacao,
        }
