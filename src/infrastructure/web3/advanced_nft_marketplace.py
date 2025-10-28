"""
Advanced NFT Marketplace - Marketplace Avançado de NFTs
Implementação da Fase 2 do roadmap CoinBalance
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import time
from decimal import Decimal

logger = logging.getLogger(__name__)


class NFTStandard(Enum):
    """Padrões de NFT suportados"""
    ERC721 = "ERC721"
    ERC1155 = "ERC1155"
    ERC4907 = "ERC4907"  # Renting NFTs


class NFTStatus(Enum):
    """Status do NFT"""
    MINTED = "minted"
    LISTED = "listed"
    SOLD = "sold"
    TRANSFERRED = "transferred"
    BURNED = "burned"


class ListingType(Enum):
    """Tipos de listagem"""
    FIXED_PRICE = "fixed_price"
    AUCTION = "auction"
    BUNDLE = "bundle"
    RENTAL = "rental"


@dataclass
class NFTMetadata:
    """Metadados do NFT"""
    name: str
    description: str
    image: str
    attributes: List[Dict[str, Any]] = field(default_factory=list)
    external_url: Optional[str] = None
    animation_url: Optional[str] = None
    background_color: Optional[str] = None
    youtube_url: Optional[str] = None


@dataclass
class NFT:
    """NFT"""
    id: str
    token_id: str
    contract_address: str
    owner: str
    creator: str
    standard: NFTStandard
    metadata: NFTMetadata
    status: NFTStatus
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    royalty_percentage: float = 0.0
    collection_id: Optional[str] = None


@dataclass
class NFTListing:
    """Listagem de NFT"""
    id: str
    nft_id: str
    seller: str
    listing_type: ListingType
    price: Decimal
    currency: str = "CNB"
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    is_active: bool = True
    auction_bids: List[Dict[str, Any]] = field(default_factory=list)
    bundle_items: List[str] = field(default_factory=list)  # Para bundles
    rental_duration: Optional[int] = None  # Para rentals (em dias)


@dataclass
class NFTCollection:
    """Coleção de NFTs"""
    id: str
    name: str
    description: str
    symbol: str
    creator: str
    contract_address: str
    total_supply: int
    minted_count: int = 0
    floor_price: Optional[Decimal] = None
    volume_traded: Decimal = Decimal('0')
    created_at: float = field(default_factory=time.time)
    verified: bool = False
    royalty_percentage: float = 0.0


class AdvancedNFTMarketplace:
    """Marketplace Avançado de NFTs"""
    
    def __init__(self):
        self.nfts: Dict[str, NFT] = {}
        self.listings: Dict[str, NFTListing] = {}
        self.collections: Dict[str, NFTCollection] = {}
        self.bids: Dict[str, List[Dict[str, Any]]] = {}
        self.is_active = False
    
    async def start_marketplace(self):
        """Inicia o marketplace"""
        self.is_active = True
        logger.info("🖼️ NFT Marketplace avançado iniciado")
        
        # Iniciar monitoramento de leilões
        asyncio.create_task(self._monitor_auctions())
        
        # Iniciar monitoramento de rentals
        asyncio.create_task(self._monitor_rentals())
    
    async def stop_marketplace(self):
        """Para o marketplace"""
        self.is_active = False
        logger.info("🛑 NFT Marketplace parado")
    
    async def create_collection(
        self, 
        name: str, 
        description: str, 
        symbol: str, 
        creator: str,
        total_supply: int,
        royalty_percentage: float = 0.0
    ) -> NFTCollection:
        """Cria uma nova coleção de NFTs"""
        collection_id = f"collection_{int(time.time())}"
        contract_address = f"0x{collection_id[:40]}"
        
        collection = NFTCollection(
            id=collection_id,
            name=name,
            description=description,
            symbol=symbol,
            creator=creator,
            contract_address=contract_address,
            total_supply=total_supply,
            royalty_percentage=royalty_percentage
        )
        
        self.collections[collection_id] = collection
        logger.info(f"✅ Coleção criada: {name} ({symbol})")
        
        return collection
    
    async def mint_nft(
        self,
        collection_id: str,
        token_id: str,
        owner: str,
        creator: str,
        metadata: NFTMetadata,
        standard: NFTStandard = NFTStandard.ERC721
    ) -> NFT:
        """Mint um novo NFT"""
        if collection_id not in self.collections:
            raise ValueError(f"Coleção {collection_id} não encontrada")
        
        collection = self.collections[collection_id]
        
        if collection.minted_count >= collection.total_supply:
            raise ValueError("Supply máximo da coleção atingido")
        
        nft_id = f"nft_{collection_id}_{token_id}"
        
        nft = NFT(
            id=nft_id,
            token_id=token_id,
            contract_address=collection.contract_address,
            owner=owner,
            creator=creator,
            standard=standard,
            metadata=metadata,
            status=NFTStatus.MINTED,
            collection_id=collection_id,
            royalty_percentage=collection.royalty_percentage
        )
        
        self.nfts[nft_id] = nft
        collection.minted_count += 1
        
        logger.info(f"✅ NFT mintado: {metadata.name} (ID: {nft_id})")
        
        return nft
    
    async def list_nft(
        self,
        nft_id: str,
        seller: str,
        listing_type: ListingType,
        price: Decimal,
        currency: str = "CNB",
        end_time: Optional[float] = None,
        bundle_items: Optional[List[str]] = None,
        rental_duration: Optional[int] = None
    ) -> NFTListing:
        """Lista um NFT para venda"""
        if nft_id not in self.nfts:
            raise ValueError(f"NFT {nft_id} não encontrado")
        
        nft = self.nfts[nft_id]
        
        if nft.owner != seller:
            raise ValueError("Apenas o proprietário pode listar o NFT")
        
        if nft.status != NFTStatus.MINTED:
            raise ValueError("NFT não pode ser listado")
        
        listing_id = f"listing_{int(time.time())}"
        
        listing = NFTListing(
            id=listing_id,
            nft_id=nft_id,
            seller=seller,
            listing_type=listing_type,
            price=price,
            currency=currency,
            end_time=end_time,
            bundle_items=bundle_items or [],
            rental_duration=rental_duration
        )
        
        self.listings[listing_id] = listing
        nft.status = NFTStatus.LISTED
        
        logger.info(f"✅ NFT listado: {nft.metadata.name} por {price} {currency}")
        
        return listing
    
    async def place_bid(
        self,
        listing_id: str,
        bidder: str,
        amount: Decimal,
        currency: str = "CNB"
    ) -> Dict[str, Any]:
        """Faz um lance em um leilão"""
        if listing_id not in self.listings:
            raise ValueError(f"Listagem {listing_id} não encontrada")
        
        listing = self.listings[listing_id]
        
        if listing.listing_type != ListingType.AUCTION:
            raise ValueError("Apenas leilões aceitam lances")
        
        if not listing.is_active:
            raise ValueError("Leilão não está ativo")
        
        if listing.end_time and time.time() > listing.end_time:
            raise ValueError("Leilão expirado")
        
        # Verificar se o lance é maior que o anterior
        current_bids = self.bids.get(listing_id, [])
        if current_bids:
            highest_bid = max(current_bids, key=lambda x: x['amount'])
            if amount <= highest_bid['amount']:
                raise ValueError("Lance deve ser maior que o lance atual")
        
        bid = {
            "bidder": bidder,
            "amount": amount,
            "currency": currency,
            "timestamp": time.time()
        }
        
        if listing_id not in self.bids:
            self.bids[listing_id] = []
        
        self.bids[listing_id].append(bid)
        listing.auction_bids.append(bid)
        
        logger.info(f"✅ Lance colocado: {bidder} - {amount} {currency}")
        
        return bid
    
    async def buy_nft(
        self,
        listing_id: str,
        buyer: str,
        amount: Optional[Decimal] = None
    ) -> Dict[str, Any]:
        """Compra um NFT"""
        if listing_id not in self.listings:
            raise ValueError(f"Listagem {listing_id} não encontrada")
        
        listing = self.listings[listing_id]
        
        if not listing.is_active:
            raise ValueError("Listagem não está ativa")
        
        if listing.listing_type == ListingType.AUCTION:
            raise ValueError("Use finalize_auction para leilões")
        
        nft = self.nfts[listing.nft_id]
        
        # Verificar preço
        if amount is None:
            amount = listing.price
        elif amount != listing.price:
            raise ValueError("Valor incorreto")
        
        # Processar transferência
        await self._process_transfer(nft, listing.seller, buyer, amount)
        
        # Atualizar status
        listing.is_active = False
        nft.status = NFTStatus.SOLD
        
        # Atualizar estatísticas da coleção
        if nft.collection_id:
            collection = self.collections[nft.collection_id]
            collection.volume_traded += amount
            
            # Atualizar floor price se necessário
            if collection.floor_price is None or amount < collection.floor_price:
                collection.floor_price = amount
        
        logger.info(f"✅ NFT vendido: {nft.metadata.name} por {amount} {listing.currency}")
        
        return {
            "nft_id": nft.id,
            "buyer": buyer,
            "seller": listing.seller,
            "amount": amount,
            "currency": listing.currency
        }
    
    async def finalize_auction(self, listing_id: str) -> Dict[str, Any]:
        """Finaliza um leilão"""
        if listing_id not in self.listings:
            raise ValueError(f"Listagem {listing_id} não encontrada")
        
        listing = self.listings[listing_id]
        
        if listing.listing_type != ListingType.AUCTION:
            raise ValueError("Apenas leilões podem ser finalizados")
        
        if not listing.is_active:
            raise ValueError("Leilão já finalizado")
        
        bids = self.bids.get(listing_id, [])
        if not bids:
            raise ValueError("Nenhum lance encontrado")
        
        # Encontrar o lance vencedor
        winning_bid = max(bids, key=lambda x: x['amount'])
        
        nft = self.nfts[listing.nft_id]
        
        # Processar transferência
        await self._process_transfer(nft, listing.seller, winning_bid['bidder'], winning_bid['amount'])
        
        # Atualizar status
        listing.is_active = False
        nft.status = NFTStatus.SOLD
        
        logger.info(f"✅ Leilão finalizado: {nft.metadata.name} vendido por {winning_bid['amount']}")
        
        return {
            "nft_id": nft.id,
            "winner": winning_bid['bidder'],
            "seller": listing.seller,
            "amount": winning_bid['amount'],
            "currency": winning_bid['currency']
        }
    
    async def rent_nft(
        self,
        listing_id: str,
        renter: str,
        duration_days: int
    ) -> Dict[str, Any]:
        """Aluga um NFT"""
        if listing_id not in self.listings:
            raise ValueError(f"Listagem {listing_id} não encontrada")
        
        listing = self.listings[listing_id]
        
        if listing.listing_type != ListingType.RENTAL:
            raise ValueError("Apenas NFTs de aluguel podem ser alugados")
        
        if not listing.is_active:
            raise ValueError("Listagem não está ativa")
        
        if listing.rental_duration and duration_days > listing.rental_duration:
            raise ValueError("Duração do aluguel excede o máximo permitido")
        
        nft = self.nfts[listing.nft_id]
        
        # Calcular preço do aluguel
        rental_price = listing.price * duration_days
        
        # Processar transferência temporária
        await self._process_rental(nft, listing.seller, renter, rental_price, duration_days)
        
        logger.info(f"✅ NFT alugado: {nft.metadata.name} por {duration_days} dias")
        
        return {
            "nft_id": nft.id,
            "renter": renter,
            "owner": listing.seller,
            "duration_days": duration_days,
            "rental_price": rental_price,
            "currency": listing.currency
        }
    
    async def _process_transfer(self, nft: NFT, from_address: str, to_address: str, amount: Decimal):
        """Processa transferência de NFT"""
        # Simular transferência blockchain
        logger.info(f"🔄 Transferindo NFT {nft.id} de {from_address} para {to_address}")
        
        # Atualizar proprietário
        nft.owner = to_address
        nft.updated_at = time.time()
        
        # Processar royalties se aplicável
        if nft.royalty_percentage > 0:
            royalty_amount = amount * (nft.royalty_percentage / 100)
            logger.info(f"💰 Royalty de {royalty_amount} para {nft.creator}")
    
    async def _process_rental(self, nft: NFT, owner: str, renter: str, rental_price: Decimal, duration_days: int):
        """Processa aluguel de NFT"""
        logger.info(f"🏠 Alugando NFT {nft.id} para {renter} por {duration_days} dias")
        
        try:
            # Verificar se o NFT está disponível para aluguel
            if not nft.is_rentable:
                raise ValueError("NFT não está disponível para aluguel")
            
            # Criar contrato de aluguel
            rental_contract = {
                "nft_id": nft.id,
                "owner": owner,
                "renter": renter,
                "rental_price": float(rental_price),
                "duration_days": duration_days,
                "start_time": time.time(),
                "end_time": time.time() + (duration_days * 24 * 3600),
                "status": "active"
            }
            
            # Registrar contrato
            self.rental_contracts[f"{nft.id}_{renter}"] = rental_contract
            
            # Atualizar status do NFT
            nft.current_renter = renter
            nft.rental_end_time = rental_contract["end_time"]
            
            logger.info(f"✅ Contrato de aluguel criado para NFT {nft.id}")
            
        except Exception as e:
            logger.error(f"Erro ao processar aluguel: {e}")
            raise
    
    async def _monitor_auctions(self):
        """Monitora leilões ativos"""
        while self.is_active:
            try:
                current_time = time.time()
                
                for listing_id, listing in self.listings.items():
                    if (listing.listing_type == ListingType.AUCTION and 
                        listing.is_active and 
                        listing.end_time and 
                        current_time > listing.end_time):
                        
                        try:
                            await self.finalize_auction(listing_id)
                        except Exception as e:
                            logger.error(f"Erro ao finalizar leilão {listing_id}: {e}")
                
                await asyncio.sleep(30)  # Verificar a cada 30 segundos
                
            except Exception as e:
                logger.error(f"Erro no monitoramento de leilões: {e}")
                await asyncio.sleep(60)
    
    async def _monitor_rentals(self):
        """Monitora aluguéis ativos"""
        while self.is_active:
            try:
                # Implementar lógica de monitoramento de aluguéis
                await asyncio.sleep(60)  # Verificar a cada minuto
                
            except Exception as e:
                logger.error(f"Erro no monitoramento de aluguéis: {e}")
                await asyncio.sleep(60)
    
    def get_marketplace_stats(self) -> Dict[str, Any]:
        """Obtém estatísticas do marketplace"""
        total_nfts = len(self.nfts)
        total_listings = len([l for l in self.listings.values() if l.is_active])
        total_collections = len(self.collections)
        total_volume = sum(c.volume_traded for c in self.collections.values())
        
        return {
            "total_nfts": total_nfts,
            "active_listings": total_listings,
            "total_collections": total_collections,
            "total_volume": float(total_volume),
            "floor_prices": {
                c.name: float(c.floor_price) if c.floor_price else None
                for c in self.collections.values()
            }
        }
    
    def get_nft_details(self, nft_id: str) -> Optional[Dict[str, Any]]:
        """Obtém detalhes de um NFT"""
        if nft_id not in self.nfts:
            return None
        
        nft = self.nfts[nft_id]
        
        # Encontrar listagem ativa
        active_listing = None
        for listing in self.listings.values():
            if listing.nft_id == nft_id and listing.is_active:
                active_listing = listing
                break
        
        return {
            "id": nft.id,
            "token_id": nft.token_id,
            "contract_address": nft.contract_address,
            "owner": nft.owner,
            "creator": nft.creator,
            "standard": nft.standard.value,
            "metadata": {
                "name": nft.metadata.name,
                "description": nft.metadata.description,
                "image": nft.metadata.image,
                "attributes": nft.metadata.attributes
            },
            "status": nft.status.value,
            "royalty_percentage": nft.royalty_percentage,
            "collection_id": nft.collection_id,
            "active_listing": {
                "id": active_listing.id,
                "price": float(active_listing.price),
                "currency": active_listing.currency,
                "listing_type": active_listing.listing_type.value
            } if active_listing else None
        }


# Instância global do marketplace
nft_marketplace = AdvancedNFTMarketplace()
