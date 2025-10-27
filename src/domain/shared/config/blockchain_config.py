"""
Configurações centralizadas da blockchain CNB
"""

from decimal import Decimal

class BlockchainConfig:
    """
    Configurações centralizadas para a blockchain CNB.
    
    Todas as configurações relacionadas a tempo de blocos,
    política monetária e parâmetros de consenso estão aqui.
    """
    
    # ========== CONFIGURAÇÕES DE TEMPO ==========
    
    # Tempo entre blocos (em segundos)
    BLOCK_TIME_SECONDS = 5  # 5 segundos por bloco
    
    # Blocos por ano (baseado no tempo de bloco)
    BLOCKS_PER_YEAR = int(365.25 * 24 * 3600 / BLOCK_TIME_SECONDS)  # ~6,307,200 blocos
    
    # Tempo alvo para ajuste de dificuldade (em segundos)
    TARGET_BLOCK_TIME_SECONDS = BLOCK_TIME_SECONDS
    
    # ========== CONFIGURAÇÕES MONETÁRIAS ==========
    
    # Supply inicial de CNB
    INITIAL_SUPPLY = Decimal("21000000")  # 21M CNB (como Bitcoin)
    
    # Taxa de inflação anual
    ANNUAL_INFLATION_RATE = Decimal("0.02")  # 2% ao ano
    
    # Taxa de recompensa para stakers
    STAKING_REWARD_RATE = Decimal("0.15")  # 15% para stakers
    
    # Intervalo de halving (em anos)
    HALVING_INTERVAL_YEARS = 10  # Halving a cada 10 anos
    
    # Recompensa inicial por bloco (será calculada dinamicamente)
    INITIAL_BLOCK_REWARD = INITIAL_SUPPLY * ANNUAL_INFLATION_RATE / Decimal(BLOCKS_PER_YEAR)
    
    # ========== CONFIGURAÇÕES DE MINERAÇÃO ==========
    
    # Dificuldade inicial
    INITIAL_DIFFICULTY = 1
    
    # Intervalo para ajuste de dificuldade (em blocos)
    DIFFICULTY_ADJUSTMENT_INTERVAL = 2016  # Ajustar a cada ~2.8 horas
    
    # Taxa mínima de transação
    MIN_TRANSACTION_FEE = Decimal("0.00000001")  # 1 satoshi
    
    # Máximo de transações por bloco
    MAX_TRANSACTIONS_PER_BLOCK = 1000
    
    # ========== CONFIGURAÇÕES DE CONSENSO ==========
    
    # Stake mínimo para validação
    MIN_STAKE_FOR_VALIDATION = Decimal("1000")  # 1000 CNB
    
    # Número máximo de validadores ativos
    MAX_ACTIVE_VALIDATORS = 100
    
    # Tempo de votação para propostas de governança (em segundos)
    GOVERNANCE_VOTING_DURATION_SECONDS = 604800  # 7 dias
    
    # Quorum mínimo para propostas (percentual)
    MIN_GOVERNANCE_QUORUM = Decimal("0.1")  # 10%
    
    # Taxa de aprovação mínima (percentual)
    MIN_APPROVAL_RATE = Decimal("0.6")  # 60%
    
    # ========== MÉTODOS DE CÁLCULO ==========
    
    @classmethod
    def get_blocks_per_year(cls) -> int:
        """Retorna número de blocos por ano"""
        return cls.BLOCKS_PER_YEAR
    
    @classmethod
    def get_block_time_seconds(cls) -> float:
        """Retorna tempo entre blocos em segundos"""
        return cls.BLOCK_TIME_SECONDS
    
    @classmethod
    def calculate_current_supply(cls, block_height: int) -> Decimal:
        """
        Calcula o supply atual baseado na altura do bloco.
        
        Args:
            block_height: Altura atual do bloco
            
        Returns:
            Supply atual em CNB
        """
        years_passed = Decimal(block_height) / Decimal(cls.BLOCKS_PER_YEAR)
        
        if years_passed <= cls.HALVING_INTERVAL_YEARS:
            # Primeiros 10 anos: inflação de 2% ao ano
            supply = cls.INITIAL_SUPPLY * (Decimal("1") + cls.ANNUAL_INFLATION_RATE) ** years_passed
        else:
            # Após 10 anos: deflação gradual
            base_supply = cls.INITIAL_SUPPLY * (Decimal("1") + cls.ANNUAL_INFLATION_RATE) ** Decimal(str(cls.HALVING_INTERVAL_YEARS))
            halving_cycles = (years_passed - Decimal(str(cls.HALVING_INTERVAL_YEARS))) // Decimal(str(cls.HALVING_INTERVAL_YEARS))
            supply = base_supply / (Decimal("2") ** halving_cycles)
        
        return supply
    
    @classmethod
    def calculate_block_reward(cls, block_height: int) -> Decimal:
        """
        Calcula a recompensa por bloco baseada na altura.
        
        Args:
            block_height: Altura do bloco
            
        Returns:
            Recompensa do bloco em CNB
        """
        years_passed = Decimal(block_height) / Decimal(cls.BLOCKS_PER_YEAR)
        
        if years_passed <= cls.HALVING_INTERVAL_YEARS:
            # Primeiros 10 anos: recompensa baseada na inflação
            annual_reward = cls.INITIAL_SUPPLY * cls.ANNUAL_INFLATION_RATE
            block_reward = annual_reward / Decimal(cls.BLOCKS_PER_YEAR)
        else:
            # Após 10 anos: recompensa reduzida pela metade a cada 10 anos
            halving_cycles = (years_passed - Decimal(str(cls.HALVING_INTERVAL_YEARS))) // Decimal(str(cls.HALVING_INTERVAL_YEARS))
            base_reward = cls.INITIAL_SUPPLY * cls.ANNUAL_INFLATION_RATE / Decimal(cls.BLOCKS_PER_YEAR)
            block_reward = base_reward / (Decimal("2") ** halving_cycles)
        
        return block_reward
    
    @classmethod
    def calculate_staking_reward(cls, block_height: int) -> Decimal:
        """
        Calcula a recompensa para stakers.
        
        Args:
            block_height: Altura do bloco
            
        Returns:
            Recompensa para stakers em CNB
        """
        block_reward = cls.calculate_block_reward(block_height)
        return block_reward * cls.STAKING_REWARD_RATE
