from fastapi import APIRouter, HTTPException, status, Query, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from models import get_session, Offer, Click, FTDEvent, Payout, OfferWeight
from performance import calculate_ev, update_weights_for_sub1, update_all_weights
from security import verify_admin
from sqlalchemy import func

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(verify_admin)]  # Protection globale des endpoints admin
)


# Pydantic models
class OfferCreate(BaseModel):
    name: str = Field(..., description="Casino offer name")
    casino_url: str = Field(..., description="Casino destination URL")
    active: bool = Field(True, description="Whether offer is active")


class OfferUpdate(BaseModel):
    name: Optional[str] = None
    casino_url: Optional[str] = None
    active: Optional[bool] = None


class OfferResponse(BaseModel):
    id: int
    name: str
    casino_url: str
    active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Sub1StatsResponse(BaseModel):
    sub1: str
    offer_id: int
    offer_name: str
    total_clicks: int
    total_ftds: int
    total_payout: float
    conversion_rate: float
    ev: float
    weight: float


class OfferStatsResponse(BaseModel):
    id: int
    name: str
    total_clicks: int
    total_ftds: int
    total_payout: float
    active: bool


@router.post("/offers", response_model=OfferResponse, status_code=status.HTTP_201_CREATED)
async def create_offer(offer: OfferCreate):
    """Create a new casino offer"""
    session = get_session()
    
    try:
        new_offer = Offer(
            name=offer.name,
            casino_url=offer.casino_url,
            active=offer.active
        )
        
        session.add(new_offer)
        session.commit()
        session.refresh(new_offer)
        
        return new_offer
        
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating offer: {str(e)}"
        )
    finally:
        session.close()


@router.get("/offers", response_model=List[OfferResponse])
async def list_offers(active_only: bool = Query(False, description="Filter for active offers only")):
    """List all offers"""
    session = get_session()
    
    try:
        query = session.query(Offer)
        
        if active_only:
            query = query.filter(Offer.active == True)
        
        offers = query.all()
        return offers
        
    finally:
        session.close()


@router.get("/offers/{offer_id}", response_model=OfferResponse)
async def get_offer(offer_id: int):
    """Get a specific offer by ID"""
    session = get_session()
    
    try:
        offer = session.query(Offer).filter(Offer.id == offer_id).first()
        
        if not offer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Offer not found"
            )
        
        return offer
        
    finally:
        session.close()


@router.put("/offers/{offer_id}", response_model=OfferResponse)
async def update_offer(offer_id: int, offer_update: OfferUpdate):
    """Update an existing offer"""
    session = get_session()
    
    try:
        offer = session.query(Offer).filter(Offer.id == offer_id).first()
        
        if not offer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Offer not found"
            )
        
        # Update fields if provided
        if offer_update.name is not None:
            offer.name = offer_update.name
        if offer_update.casino_url is not None:
            offer.casino_url = offer_update.casino_url
        if offer_update.active is not None:
            offer.active = offer_update.active
        
        session.commit()
        session.refresh(offer)
        
        return offer
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating offer: {str(e)}"
        )
    finally:
        session.close()


@router.delete("/offers/{offer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_offer(offer_id: int):
    """Delete an offer"""
    session = get_session()
    
    try:
        offer = session.query(Offer).filter(Offer.id == offer_id).first()
        
        if not offer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Offer not found"
            )
        
        session.delete(offer)
        session.commit()
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting offer: {str(e)}"
        )
    finally:
        session.close()


@router.get("/stats", response_model=List[OfferStatsResponse])
async def get_global_stats():
    """Get global performance statistics for all offers (aggregated across all sub1)"""
    session = get_session()
    
    try:
        offers = session.query(Offer).all()
        stats = []
        
        for offer in offers:
            # Total clicks
            total_clicks = session.query(func.count(Click.id)).filter(
                Click.offer_id == offer.id
            ).scalar()
            
            # Total FTDs
            total_ftds = session.query(func.count(FTDEvent.id)).filter(
                FTDEvent.offer_id == offer.id
            ).scalar()
            
            # Total payout
            total_payout = session.query(func.sum(Payout.amount)).join(
                FTDEvent
            ).filter(
                FTDEvent.offer_id == offer.id
            ).scalar() or 0.0
            
            stats.append(OfferStatsResponse(
                id=offer.id,
                name=offer.name,
                total_clicks=total_clicks or 0,
                total_ftds=total_ftds or 0,
                total_payout=total_payout,
                active=offer.active
            ))
        
        return stats
        
    finally:
        session.close()


@router.get("/stats/sub1/{sub1}", response_model=List[Sub1StatsResponse])
async def get_sub1_stats(sub1: str):
    """Get performance statistics for a specific sub1 across all offers"""
    session = get_session()
    
    try:
        offers = session.query(Offer).all()
        stats = []
        
        for offer in offers:
            # Total clicks for this sub1 + offer
            total_clicks = session.query(func.count(Click.id)).filter(
                Click.sub1 == sub1,
                Click.offer_id == offer.id
            ).scalar() or 0
            
            if total_clicks == 0:
                continue  # Skip offers with no clicks for this sub1
            
            # Get click IDs for this sub1 + offer
            click_ids = [c.click_id for c in session.query(Click.click_id).filter(
                Click.sub1 == sub1,
                Click.offer_id == offer.id
            ).all()]
            
            # Total FTDs
            total_ftds = session.query(func.count(FTDEvent.id)).filter(
                FTDEvent.click_id.in_(click_ids)
            ).scalar() or 0
            
            # Total payout
            total_payout = session.query(func.sum(Payout.amount)).join(
                FTDEvent
            ).filter(
                FTDEvent.click_id.in_(click_ids)
            ).scalar() or 0.0
            
            # Conversion rate
            conversion_rate = (total_ftds / total_clicks * 100) if total_clicks > 0 else 0.0
            
            # EV
            ev = calculate_ev(sub1, offer.id)
            
            # Get weight
            weight_record = session.query(OfferWeight).filter(
                OfferWeight.sub1 == sub1,
                OfferWeight.offer_id == offer.id
            ).first()
            
            weight = weight_record.weight if weight_record else 1.0
            
            stats.append(Sub1StatsResponse(
                sub1=sub1,
                offer_id=offer.id,
                offer_name=offer.name,
                total_clicks=total_clicks,
                total_ftds=total_ftds,
                total_payout=total_payout,
                conversion_rate=round(conversion_rate, 2),
                ev=ev,
                weight=weight
            ))
        
        return stats
        
    finally:
        session.close()


@router.get("/stats/sub1")
async def list_all_sub1():
    """List all unique sub1 codes that have clicks"""
    session = get_session()
    
    try:
        sub1_codes = session.query(Click.sub1).distinct().all()
        sub1_list = [code[0] for code in sub1_codes]
        
        return {"sub1_codes": sub1_list, "total": len(sub1_list)}
        
    finally:
        session.close()


@router.post("/update-weights", status_code=status.HTTP_200_OK)
async def trigger_weight_update(sub1: Optional[str] = Query(None, description="Update weights for specific sub1, or all if not provided")):
    """Manually trigger weight recalculation"""
    try:
        if sub1:
            update_weights_for_sub1(sub1)
            return {"status": "success", "message": f"Weights updated for sub1={sub1}"}
        else:
            update_all_weights()
            return {"status": "success", "message": "Weights updated for all sub1 codes"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating weights: {str(e)}"
        )
