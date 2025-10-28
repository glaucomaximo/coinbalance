"""
NFT Marketplace para CoinBalance
Implementa marketplace completo para NFTs com funcionalidades avançadas
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal
import time
import hashlib
from datetime import datetime

logger = logging.getLogger(__name__)


class NFTStandard(Enum):
    """Padrões de NFT suportados"""
    ERC721 = "ERC721"
    ERC1155 = "ERC1155"
    ERC4907 = "ERC4907"  # Renting NFTs


class ListingType(Enum):
    """Tipos de listagem"""
    FIXED_PRICE = "fixed_price"
    AUCTION = "auction"
    BUNDLE = "bundle"
    RENTAL = "rental"


class AuctionStatus(Enum):
    """Status de leilão"""
    ACTIVE = "active"
    ENDED = "ended"
    CANCELLED = "cancelled"
    SETTLED = "settled"


@dataclass
class NFTMetadata:
    """Metadados de NFT"""
    name: str
    description: str
    image: str
    animation_url: Optional[str] = None
    external_url: Optional[str] = None
    attributes: List[Dict[str, Any]] = None
    background_color: Optional[str] = None
    youtube_url: Optional[str] = None


@dataclass
class NFT:
    """NFT"""
    token_id: str
    contract_address: str
    owner: str
    creator: str
    metadata: NFTMetadata
    standard: NFTStandard
    royalty_percentage: Decimal
    created_at: float
    last_transfer: float
    is_burned: bool = False


@dataclass
class NFTListing:
    """Listagem de NFT"""
    listing_id: str
    nft: NFT
    seller: str
    listing_type: ListingType
    price: Decimal
    currency: str
    start_time: float
    end_time: Optional[float] = None
    is_active: bool = True
    buyer: Optional[str] = None
    auction_bids: List[Dict[str, Any]] = None


@dataclass
class AuctionBid:
    """Lance de leilão"""
    bidder: str
    amount: Decimal
    timestamp: float
    bid_id: str


class NFTMarketplaceManager:
    """Gerenciador do NFT Marketplace"""
    
    def __init__(self):
        self.nfts: Dict[str, NFT] = {}
        self.listings: Dict[str, NFTListing] = {}
        self.auctions: Dict[str, List[AuctionBid]] = {}
        self.collections: Dict[str, Dict[str, Any]] = {}
        self.royalties: Dict[str, Decimal] = {}
        logger.info("NFTMarketplaceManager inicializado")
    
    def create_nft(self, contract_address: str, token_id: str, owner: str, 
                   creator: str, metadata: NFTMetadata, standard: NFTStandard = NFTStandard.ERC721,
                   royalty_percentage: Decimal = Decimal("2.5")) -> NFT:
        """Cria um novo NFT"""
        try:
            nft = NFT(
                token_id=token_id,
                contract_address=contract_address,
                owner=owner,
                creator=creator,
                metadata=metadata,
                standard=standard,
                royalty_percentage=royalty_percentage,
                created_at=time.time(),
                last_transfer=time.time()
            )
            
            nft_key = f"{contract_address}:{token_id}"
            self.nfts[nft_key] = nft
            
            logger.info(f"NFT criado: {token_id} em {contract_address}")
            return nft
            
        except Exception as e:
            logger.error(f"Erro ao criar NFT: {e}")
            raise
    
    def list_nft(self, nft_key: str, seller: str, listing_type: ListingType,
                 price: Decimal, currency: str = "CNB", duration_hours: int = 168) -> NFTListing:
        """Lista um NFT para venda"""
        try:
            if nft_key not in self.nfts:
                raise ValueError("NFT não encontrado")
            
            nft = self.nfts[nft_key]
            
            if nft.owner != seller:
                raise ValueError("Apenas o proprietário pode listar o NFT")
            
            listing_id = self._generate_listing_id()
            end_time = time.time() + (duration_hours * 3600) if listing_type == ListingType.AUCTION else None
            
            listing = NFTListing(
                listing_id=listing_id,
                nft=nft,
                seller=seller,
                listing_type=listing_type,
                price=price,
                currency=currency,
                start_time=time.time(),
                end_time=end_time,
                auction_bids=[] if listing_type == ListingType.AUCTION else None
            )
            
            self.listings[listing_id] = listing
            
            if listing_type == ListingType.AUCTION:
                self.auctions[listing_id] = []
            
            logger.info(f"NFT listado: {listing_id} por {price} {currency}")
            return listing
            
        except Exception as e:
            logger.error(f"Erro ao listar NFT: {e}")
            raise
    
    def buy_nft(self, listing_id: str, buyer: str, amount: Decimal) -> Dict[str, Any]:
        """Compra um NFT"""
        try:
            if listing_id not in self.listings:
                raise ValueError("Listagem não encontrada")
            
            listing = self.listings[listing_id]
            
            if not listing.is_active:
                raise ValueError("Listagem não está ativa")
            
            if listing.listing_type == ListingType.AUCTION:
                raise ValueError("Use place_bid para leilões")
            
            if amount < listing.price:
                raise ValueError("Valor insuficiente")
            
            # Processar compra
            nft = listing.nft
            seller = listing.seller
            
            # Calcular royalties
            royalty_amount = amount * nft.royalty_percentage / Decimal("100")
            seller_amount = amount - royalty_amount
            
            # Transferir NFT
            nft.owner = buyer
            nft.last_transfer = time.time()
            
            # Finalizar listagem
            listing.is_active = False
            listing.buyer = buyer
            
            logger.info(f"NFT comprado: {listing_id} por {buyer}")
            
            return {
                "success": True,
                "transaction_hash": self._generate_tx_hash(),
                "nft_transferred": True,
                "seller_amount": str(seller_amount),
                "royalty_amount": str(royalty_amount),
                "creator": nft.creator
            }
            
        except Exception as e:
            logger.error(f"Erro ao comprar NFT: {e}")
            raise
    
    def place_bid(self, listing_id: str, bidder: str, amount: Decimal) -> AuctionBid:
        """Coloca um lance em um leilão"""
        try:
            if listing_id not in self.listings:
                raise ValueError("Listagem não encontrada")
            
            listing = self.listings[listing_id]
            
            if listing.listing_type != ListingType.AUCTION:
                raise ValueError("Apenas leilões aceitam lances")
            
            if not listing.is_active:
                raise ValueError("Leilão não está ativo")
            
            if time.time() > listing.end_time:
                raise ValueError("Leilão expirado")
            
            # Verificar lance mínimo
            current_bids = self.auctions.get(listing_id, [])
            if current_bids:
                highest_bid = max(current_bids, key=lambda b: b.amount)
                if amount <= highest_bid.amount:
                    raise ValueError("Lance deve ser maior que o lance atual")
            else:
                if amount < listing.price:
                    raise ValueError("Lance deve ser maior que o preço inicial")
            
            # Criar lance
            bid = AuctionBid(
                bidder=bidder,
                amount=amount,
                timestamp=time.time(),
                bid_id=self._generate_bid_id()
            )
            
            self.auctions[listing_id].append(bid)
            listing.auction_bids.append({
                "bidder": bidder,
                "amount": str(amount),
                "timestamp": bid.timestamp,
                "bid_id": bid.bid_id
            })
            
            logger.info(f"Lance colocado: {amount} por {bidder}")
            return bid
            
        except Exception as e:
            logger.error(f"Erro ao colocar lance: {e}")
            raise
    
    def settle_auction(self, listing_id: str) -> Dict[str, Any]:
        """Finaliza um leilão"""
        try:
            if listing_id not in self.listings:
                raise ValueError("Listagem não encontrada")
            
            listing = self.listings[listing_id]
            
            if listing.listing_type != ListingType.AUCTION:
                raise ValueError("Apenas leilões podem ser finalizados")
            
            if time.time() < listing.end_time:
                raise ValueError("Leilão ainda não expirou")
            
            bids = self.auctions.get(listing_id, [])
            if not bids:
                listing.is_active = False
                return {"success": True, "winner": None, "message": "Nenhum lance recebido"}
            
            # Encontrar vencedor
            winning_bid = max(bids, key=lambda b: b.amount)
            
            # Transferir NFT
            nft = listing.nft
            nft.owner = winning_bid.bidder
            nft.last_transfer = time.time()
            
            # Calcular royalties
            royalty_amount = winning_bid.amount * nft.royalty_percentage / Decimal("100")
            seller_amount = winning_bid.amount - royalty_amount
            
            # Finalizar leilão
            listing.is_active = False
            listing.buyer = winning_bid.bidder
            
            logger.info(f"Leilão finalizado: {listing_id} vencido por {winning_bid.bidder}")
            
            return {
                "success": True,
                "winner": winning_bid.bidder,
                "winning_amount": str(winning_bid.amount),
                "seller_amount": str(seller_amount),
                "royalty_amount": str(royalty_amount),
                "creator": nft.creator
            }
            
        except Exception as e:
            logger.error(f"Erro ao finalizar leilão: {e}")
            raise
    
    def create_collection(self, name: str, description: str, creator: str,
                         contract_address: str, royalty_percentage: Decimal = Decimal("2.5")) -> Dict[str, Any]:
        """Cria uma coleção de NFTs"""
        try:
            collection_id = self._generate_collection_id()
            
            collection = {
                "id": collection_id,
                "name": name,
                "description": description,
                "creator": creator,
                "contract_address": contract_address,
                "royalty_percentage": str(royalty_percentage),
                "created_at": time.time(),
                "nft_count": 0,
                "total_volume": "0",
                "floor_price": None,
                "verified": False
            }
            
            self.collections[collection_id] = collection
            self.royalties[contract_address] = royalty_percentage
            
            logger.info(f"Coleção criada: {name} ({collection_id})")
            return collection
            
        except Exception as e:
            logger.error(f"Erro ao criar coleção: {e}")
            raise
    
    def get_nft_details(self, contract_address: str, token_id: str) -> Optional[NFT]:
        """Obtém detalhes de um NFT"""
        nft_key = f"{contract_address}:{token_id}"
        return self.nfts.get(nft_key)
    
    def search_nfts(self, query: str, filters: Dict[str, Any] = None) -> List[NFT]:
        """Busca NFTs"""
        results = []
        
        for nft in self.nfts.values():
            if nft.is_burned:
                continue
            
            # Busca por nome
            if query.lower() in nft.metadata.name.lower():
                results.append(nft)
                continue
            
            # Busca por descrição
            if query.lower() in nft.metadata.description.lower():
                results.append(nft)
                continue
            
            # Busca por atributos
            if nft.metadata.attributes:
                for attr in nft.metadata.attributes:
                    if query.lower() in str(attr.get("value", "")).lower():
                        results.append(nft)
                        break
        
        # Aplicar filtros
        if filters:
            filtered_results = []
            for nft in results:
                if filters.get("contract_address") and nft.contract_address != filters["contract_address"]:
                    continue
                if filters.get("owner") and nft.owner != filters["owner"]:
                    continue
                if filters.get("standard") and nft.standard.value != filters["standard"]:
                    continue
                filtered_results.append(nft)
            results = filtered_results
        
        return results
    
    def get_trending_nfts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtém NFTs em tendência"""
        # Simular NFTs em tendência baseado em atividade recente
        trending = []
        
        for nft in list(self.nfts.values())[:limit]:
            trending.append({
                "token_id": nft.token_id,
                "contract_address": nft.contract_address,
                "name": nft.metadata.name,
                "image": nft.metadata.image,
                "owner": nft.owner,
                "floor_price": "1.0",  # Simulado
                "volume_24h": "5.2",  # Simulado
                "change_24h": "+12.5%"  # Simulado
            })
        
        return trending
    
    def get_collection_stats(self, collection_id: str) -> Dict[str, Any]:
        """Obtém estatísticas de uma coleção"""
        if collection_id not in self.collections:
            raise ValueError("Coleção não encontrada")
        
        collection = self.collections[collection_id]
        
        # Calcular estatísticas
        nfts_in_collection = [
            nft for nft in self.nfts.values() 
            if nft.contract_address == collection["contract_address"]
        ]
        
        return {
            "collection": collection,
            "nft_count": len(nfts_in_collection),
            "total_volume": collection["total_volume"],
            "floor_price": collection["floor_price"],
            "average_price": "2.5",  # Simulado
            "owners": len(set(nft.owner for nft in nfts_in_collection)),
            "listed": len([nft for nft in nfts_in_collection if any(
                listing.nft.token_id == nft.token_id and listing.is_active 
                for listing in self.listings.values()
            )])
        }
    
    def _generate_listing_id(self) -> str:
        """Gera ID único para listagem"""
        data = f"listing_{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _generate_bid_id(self) -> str:
        """Gera ID único para lance"""
        data = f"bid_{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _generate_collection_id(self) -> str:
        """Gera ID único para coleção"""
        data = f"collection_{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _generate_tx_hash(self) -> str:
        """Gera hash de transação"""
        data = f"tx_{time.time()}"
        return "0x" + hashlib.sha256(data.encode()).hexdigest()


# Instância global
nft_marketplace_manager = NFTMarketplaceManager()
