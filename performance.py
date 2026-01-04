import random
from datetime import datetime, timedelta
from sqlalchemy import func
from models import get_session, Offer, Click, FTDEvent, Payout, OfferWeight
from config import Config
from time_restrictions import get_available_offers
from geo_restrictions import filter_offers_by_geo


def calculate_ev(sub1, offer_id, last_n_clicks=None):
    """
    Calculate EV (Expected Value) for a specific sub1 + offer combination using:
    EV = (FTD / clicks) × payout
    
    Args:
        sub1: The tracking code (affiliate/person identifier)
        offer_id: The offer to calculate EV for
        last_n_clicks: Number of recent clicks to consider (default from config)
    
    Returns:
        float: The calculated EV, or 0 if no clicks exist
    """
    if last_n_clicks is None:
        last_n_clicks = Config.LAST_N_CLICKS
    
    session = get_session()
    
    try:
        # Get last N clicks for this sub1 + offer combination
        recent_clicks = session.query(Click).filter(
            Click.sub1 == sub1,
            Click.offer_id == offer_id
        ).order_by(
            Click.timestamp.desc()
        ).limit(last_n_clicks).all()
        
        if not recent_clicks:
            return 0.0
        
        click_ids = [c.click_id for c in recent_clicks]
        total_clicks = len(click_ids)
        
        # Count FTDs from these clicks
        ftd_count = session.query(func.count(FTDEvent.id)).filter(
            FTDEvent.click_id.in_(click_ids)
        ).scalar()
        
        # Get average payout for these FTDs
        avg_payout = session.query(func.avg(Payout.amount)).join(
            FTDEvent
        ).filter(
            FTDEvent.click_id.in_(click_ids)
        ).scalar()
        
        if not avg_payout or ftd_count == 0:
            return 0.0
        
        # Calculate EV
        conversion_rate = ftd_count / total_clicks
        ev = conversion_rate * avg_payout
        
        return round(ev, 4)
    
    finally:
        session.close()


def update_weights_for_sub1(sub1):
    """
    Recalculate and update weights for all active offers for a specific sub1.
    
    Args:
        sub1: The tracking code to update weights for
    """
    session = get_session()
    
    try:
        offers = session.query(Offer).filter(Offer.active == True).all()
        
        if not offers:
            return
        
        # Calculate EV for each offer for this sub1
        ev_data = {}
        for offer in offers:
            ev = calculate_ev(sub1, offer.id)
            ev_data[offer.id] = ev
        
        # Find max EV (for normalization)
        max_ev = max(ev_data.values()) if ev_data else 0
        
        # Update or create weights for each offer
        for offer in offers:
            # Get or create weight record
            weight_record = session.query(OfferWeight).filter(
                OfferWeight.sub1 == sub1,
                OfferWeight.offer_id == offer.id
            ).first()
            
            if not weight_record:
                weight_record = OfferWeight(
                    sub1=sub1,
                    offer_id=offer.id,
                    weight=1.0
                )
                session.add(weight_record)
            
            # Calculate new weight
            if max_ev == 0:
                # Equal weights for exploration
                weight_record.weight = 1.0
            else:
                # Proportional to EV, minimum 0.1 to keep exploring
                normalized_weight = max(0.1, ev_data[offer.id] / max_ev)
                weight_record.weight = round(normalized_weight, 4)
            
            weight_record.updated_at = datetime.utcnow()
        
        session.commit()
        
    except Exception as e:
        session.rollback()
        print(f"✗ Error updating weights for sub1={sub1}: {e}")
        raise
    finally:
        session.close()


def update_all_weights():
    """
    Recalculate and update weights for all sub1 codes that have clicks.
    This is the function called by the cron job.
    """
    session = get_session()
    
    try:
        # Get all unique sub1 codes
        sub1_codes = session.query(Click.sub1).distinct().all()
        sub1_codes = [code[0] for code in sub1_codes]
        
        print(f"Updating weights for {len(sub1_codes)} sub1 codes...")
        
        for sub1 in sub1_codes:
            update_weights_for_sub1(sub1)
            print(f"  ✓ Updated weights for sub1={sub1}")
        
        print(f"✓ Weight update completed for all sub1 codes")
        
    finally:
        session.close()


def select_offer(sub1, ip_address=None, exploration_rate=None):
    """
    Select an offer for a specific sub1 based on weights with exploration traffic.
    
    Args:
        sub1: The tracking code to select an offer for
        ip_address: User's IP address for geo-targeting (optional)
        exploration_rate: Percentage of traffic for exploration (default from config)
    
    Returns:
        Offer: The selected offer object
    """
    if exploration_rate is None:
        exploration_rate = Config.EXPLORATION_RATE
    
    session = get_session()
    
    try:
        # Get all active offers
        all_offers = session.query(Offer).filter(Offer.active == True).all()
        
        if not all_offers:
            raise ValueError("No active offers available")
        
        # Filter offers based on time restrictions
        time_filtered = get_available_offers(all_offers)
        
        # Filter offers based on geo restrictions
        if ip_address:
            offers = filter_offers_by_geo(time_filtered, ip_address)
        else:
            offers = time_filtered
        
        if not offers:
            raise ValueError("No offers available at this time (time restrictions)")
        
        # Get weights for this sub1
        weights_data = session.query(OfferWeight).filter(
            OfferWeight.sub1 == sub1
        ).all()
        
        # Create a mapping of offer_id to weight
        weight_map = {w.offer_id: w.weight for w in weights_data}
        
        # If no weights exist for this sub1, create default weights
        if not weight_map:
            print(f"No weights found for sub1={sub1}, initializing with equal weights")
            for offer in offers:
                new_weight = OfferWeight(
                    sub1=sub1,
                    offer_id=offer.id,
                    weight=1.0
                )
                session.add(new_weight)
                weight_map[offer.id] = 1.0
            session.commit()
        
        # Decide if this is exploration traffic
        is_exploration = random.random() < exploration_rate
        
        if is_exploration:
            # Exploration: random uniform selection
            selected = random.choice(offers)
        else:
            # Exploitation: weighted selection based on performance
            weights = [weight_map.get(offer.id, 1.0) for offer in offers]
            selected = random.choices(offers, weights=weights, k=1)[0]
        
        # Detach from session to avoid issues
        session.expunge(selected)
        return selected
    
    finally:
        session.close()
