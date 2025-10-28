"""
Testes para o sistema de Blockchain
"""

import pytest
from decimal import Decimal
from src.domain.blockchain.entities.blockchain import Blockchain
from src.domain.blockchain.entities.block import Block
from src.domain.blockchain.services.mining_service import MiningService
from src.domain.transaction.entities.transaction import Transaction, TransactionId, TransactionAmount, TransactionFee, TransactionType, TransactionStatus
from src.domain.shared.value_objects.wallet_address import WalletAddress
from src.domain.shared.value_objects.timestamp import Timestamp
from src.domain.shared.value_objects.money import Money


class TestBlockchain:
    """Testes para a entidade Blockchain"""
    
    def test_create_blockchain(self):
        """Testa criação de blockchain"""
        blockchain = Blockchain.create("TestChain", "1.0.0")
        
        assert blockchain.name == "TestChain"
        assert blockchain.version == "1.0.0"
        assert len(blockchain.blocks) == 1  # Bloco gênesis
        assert blockchain.blocks[0].height == 0
    
    def test_genesis_block(self):
        """Testa criação do bloco gênesis"""
        blockchain = Blockchain.create()
        genesis_block = blockchain.blocks[0]
        
        assert genesis_block.height == 0
        assert genesis_block.previous_hash is None
        assert len(genesis_block.transactions) == 1
        assert genesis_block.transactions[0].transaction_type == TransactionType.GENESIS
    
    def test_add_block(self):
        """Testa adição de blocos"""
        blockchain = Blockchain.create()
        
        # Criar transação de teste
        tx = Transaction(
            id=TransactionId.generate(),
            from_address=None,
            to_address=WalletAddress("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"),
            amount=TransactionAmount(Money.from_cnb(Decimal("100"))),
            fee=TransactionFee(Money.from_cnb(Decimal("1"))),
            transaction_type=TransactionType.TRANSFER,
            status=TransactionStatus.PENDING,
            created_at=Timestamp.now()
        )
        
        # Minerar bloco
        mined_block = blockchain.mine_block([tx], "miner_address")
        
        assert mined_block is not None
        assert mined_block.height == 1
        assert mined_block.miner_address == "miner_address"
        assert len(mined_block.transactions) == 1
        assert blockchain.total_blocks_mined == 2  # Gênesis + novo bloco
    
    def test_chain_validation(self):
        """Testa validação da cadeia"""
        blockchain = Blockchain.create()
        
        # Cadeia deve ser válida inicialmente
        assert blockchain.is_chain_valid()
        
        # Adicionar bloco válido
        tx = Transaction(
            id=TransactionId.generate(),
            from_address=None,
            to_address=WalletAddress("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"),
            amount=TransactionAmount(Money.from_cnb(Decimal("50"))),
            fee=TransactionFee(Money.from_cnb(Decimal("0.5"))),
            transaction_type=TransactionType.TRANSFER,
            status=TransactionStatus.PENDING,
            created_at=Timestamp.now()
        )
        
        mined_block = blockchain.mine_block([tx], "miner")
        assert mined_block is not None
        assert blockchain.is_chain_valid()
    
    def test_difficulty_adjustment(self):
        """Testa ajuste automático de dificuldade"""
        blockchain = Blockchain.create()
        initial_difficulty = blockchain.difficulty
        
        # Simular mineração rápida (diferença de tempo pequena)
        tx = Transaction(
            id=TransactionId.generate(),
            from_address=None,
            to_address=WalletAddress("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"),
            amount=TransactionAmount(Money.from_cnb(Decimal("10"))),
            fee=TransactionFee(Money.from_cnb(Decimal("0.1"))),
            transaction_type=TransactionType.TRANSFER,
            status=TransactionStatus.PENDING,
            created_at=Timestamp.now()
        )
        
        blockchain.blocks.append(Block.create_block(
            height=1,
            previous_hash=blockchain.blocks[0].hash,
            transactions=[tx],
            difficulty=initial_difficulty,
            miner_address="test_miner"
        ))
        
        # Dificuldade deve aumentar se blocos forem muito rápidos
        assert blockchain.difficulty >= initial_difficulty
    
    def test_get_block_by_height(self):
        """Testa busca de bloco por altura"""
        blockchain = Blockchain.create()
        
        # Buscar bloco gênesis
        genesis = blockchain.get_block_by_height(0)
        assert genesis is not None
        assert genesis.height == 0
        
        # Buscar bloco inexistente
        non_existent = blockchain.get_block_by_height(999)
        assert non_existent is None
    
    def test_get_block_by_hash(self):
        """Testa busca de bloco por hash"""
        blockchain = Blockchain.create()
        genesis_block = blockchain.blocks[0]
        
        # Buscar por hash válido
        found_block = blockchain.get_block_by_hash(genesis_block.hash.value)
        assert found_block is not None
        assert found_block.height == 0
        
        # Buscar por hash inexistente
        not_found = blockchain.get_block_by_hash("invalid_hash")
        assert not_found is None
    
    def test_get_chain_stats(self):
        """Testa estatísticas da cadeia"""
        blockchain = Blockchain.create()
        stats = blockchain.get_chain_stats()
        
        assert stats["name"] == "CoinBalance"
        assert stats["total_blocks"] == 1
        assert stats["chain_valid"] is True
        assert stats["latest_block_height"] == 0


class TestBlock:
    """Testes para a entidade Block"""
    
    def test_create_genesis_block(self):
        """Testa criação do bloco gênesis"""
        genesis = Block.create_genesis_block()
        
        assert genesis.height == 0
        assert genesis.previous_hash is None
        assert genesis.nonce == 0
        assert genesis.difficulty == 1
        assert len(genesis.transactions) == 1
    
    def test_create_block(self):
        """Testa criação de bloco normal"""
        from src.domain.shared.value_objects.hash_value import HashValue
        
        # Criar transação
        tx = Transaction(
            id=TransactionId.generate(),
            from_address=None,
            to_address=WalletAddress("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"),
            amount=TransactionAmount(Money.from_cnb(Decimal("100"))),
            fee=TransactionFee(Money.from_cnb(Decimal("1"))),
            transaction_type=TransactionType.TRANSFER,
            status=TransactionStatus.PENDING,
            created_at=Timestamp.now()
        )
        
        # Criar bloco
        previous_hash = HashValue.create("0" * 64)
        block = Block.create_block(
            height=1,
            previous_hash=previous_hash,
            transactions=[tx],
            difficulty=1,
            miner_address="test_miner"
        )
        
        assert block.height == 1
        assert block.previous_hash == previous_hash
        assert block.miner_address == "test_miner"
        assert len(block.transactions) == 1
        assert block.is_valid()
    
    def test_block_validation(self):
        """Testa validação de bloco"""
        genesis = Block.create_genesis_block()
        
        # Bloco gênesis deve ser válido
        assert genesis.is_valid()
        
        # Verificar hash
        assert genesis.hash.value.startswith("0" * genesis.difficulty)
    
    def test_merkle_root_calculation(self):
        """Testa cálculo da raiz Merkle"""
        # Bloco com uma transação
        tx1 = Transaction(
            id=TransactionId.generate(),
            from_address=None,
            to_address=WalletAddress("1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2"),
            amount=TransactionAmount(Money.from_cnb(Decimal("100"))),
            fee=TransactionFee(Money.from_cnb(Decimal("1"))),
            transaction_type=TransactionType.TRANSFER,
            status=TransactionStatus.PENDING,
            created_at=Timestamp.now()
        )
        
        from src.domain.shared.value_objects.hash_value import HashValue
        previous_hash = HashValue.create("0" * 64)
        
        block = Block.create_block(
            height=1,
            previous_hash=previous_hash,
            transactions=[tx1],
            difficulty=1
        )
        
        # Raiz Merkle deve ser calculada corretamente
        assert block.merkle_root is not None
        assert len(block.merkle_root.value) == 64  # SHA-256


class TestMiningService:
    """Testes para o serviço de mineração"""
    
    def test_create_mining_service(self):
        """Testa criação do serviço de mineração"""
        blockchain = Blockchain.create()
        mining_service = MiningService(blockchain)
        
        assert mining_service.blockchain == blockchain
        assert len(mining_service.transaction_pool) == 0
    
    def test_add_transaction_to_pool(self):
        """Testa adição de transação ao pool"""
        blockchain = Blockchain.create()
        mining_service = MiningService(blockchain)
        
        tx = Transaction(
            id=TransactionId.generate(),
            from_address=None,
            to_address=WalletAddress("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"),
            amount=TransactionAmount(Money.from_cnb(Decimal("100"))),
            fee=TransactionFee(Money.from_cnb(Decimal("1"))),
            transaction_type=TransactionType.TRANSFER,
            status=TransactionStatus.PENDING,
            created_at=Timestamp.now()
        )
        
        # Adicionar ao pool
        success = mining_service.add_transaction_to_pool(tx)
        assert success is True
        assert len(mining_service.transaction_pool) == 1
        
        # Tentar adicionar a mesma transação novamente
        success = mining_service.add_transaction_to_pool(tx)
        assert success is False  # Não deve permitir duplicatas
    
    def test_mine_block(self):
        """Testa mineração de bloco"""
        blockchain = Blockchain.create()
        mining_service = MiningService(blockchain)
        
        # Adicionar transação ao pool
        tx = Transaction(
            id=TransactionId.generate(),
            from_address=None,
            to_address=WalletAddress("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"),
            amount=TransactionAmount(Money.from_cnb(Decimal("100"))),
            fee=TransactionFee(Money.from_cnb(Decimal("1"))),
            transaction_type=TransactionType.TRANSFER,
            status=TransactionStatus.PENDING,
            created_at=Timestamp.now()
        )
        
        mining_service.add_transaction_to_pool(tx)
        
        # Minerar bloco
        mined_block = mining_service.mine_block("test_miner")
        
        assert mined_block is not None
        assert mined_block.miner_address == "test_miner"
        assert len(mined_block.transactions) == 1
        assert len(mining_service.transaction_pool) == 0  # Pool deve ser esvaziado
    
    def test_mining_stats(self):
        """Testa estatísticas de mineração"""
        blockchain = Blockchain.create()
        mining_service = MiningService(blockchain)
        
        stats = mining_service.get_mining_stats()
        
        assert "blocks_mined" in stats
        assert "current_difficulty" in stats
        assert "current_reward" in stats
        assert "pool_size" in stats
        assert stats["pool_size"] == 0
    
    def test_simulate_mining(self):
        """Testa simulação de mineração"""
        blockchain = Blockchain.create()
        mining_service = MiningService(blockchain)
        
        # Simular mineração com dificuldade baixa
        result = mining_service.simulate_mining(difficulty=1, max_time=1.0)
        
        assert "success" in result
        assert "attempts" in result
        assert "mining_time" in result
        assert result["difficulty"] == 1
