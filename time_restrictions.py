"""
Time-based offer restrictions module.
Allows offers to be available only during specific time windows.
"""
from datetime import datetime
import pytz


# Time restrictions configuration
# Format: offer_id -> list of time rules
TIME_RESTRICTIONS = {
    7: {  # SpinGranny
        "timezone": "Europe/Paris",
        "rules": [
            {
                "days": [5, 6],  # Saturday=5, Sunday=6 (ISO weekday: Monday=0, Sunday=6)
                "start_hour": 0,
                "end_hour": 24,
                "description": "Weekend - All day"
            },
            {
                "days": [0, 1, 2, 3, 4],  # Monday to Friday
                "start_hour": 19,
                "end_hour": 24,
                "description": "Weekdays - Evening (19h-00h)"
            },
            {
                "days": [0, 1, 2, 3, 4],  # Monday to Friday
                "start_hour": 0,
                "end_hour": 6,
                "description": "Weekdays - Night (00h-06h)"
            }
        ]
    }
}


def is_offer_available(offer_id):
    """
    Check if an offer is available at the current time based on its restrictions.
    
    Args:
        offer_id: The offer ID to check
        
    Returns:
        bool: True if offer is available now, False otherwise
    """
    # If no restrictions defined, offer is always available
    if offer_id not in TIME_RESTRICTIONS:
        return True
    
    config = TIME_RESTRICTIONS[offer_id]
    tz = pytz.timezone(config["timezone"])
    now = datetime.now(tz)
    
    current_day = now.weekday()  # Monday=0, Sunday=6
    current_hour = now.hour
    
    # Check each rule
    for rule in config["rules"]:
        # Check if current day matches
        if current_day in rule["days"]:
            # Check if current hour is within range
            start = rule["start_hour"]
            end = rule["end_hour"]
            
            # Handle time range (e.g., 19-24 or 0-6)
            if start < end:
                if start <= current_hour < end:
                    return True
            else:
                # Handle ranges that cross midnight (e.g., 22-02)
                if current_hour >= start or current_hour < end:
                    return True
    
    return False


def get_available_offers(offers):
    """
    Filter a list of offers to only include those available at current time.
    
    Args:
        offers: List of Offer objects
        
    Returns:
        list: Filtered list of available offers
    """
    return [offer for offer in offers if is_offer_available(offer.id)]


def get_restriction_info(offer_id):
    """
    Get human-readable information about an offer's time restrictions.
    
    Args:
        offer_id: The offer ID
        
    Returns:
        str: Description of restrictions, or "Always available" if none
    """
    if offer_id not in TIME_RESTRICTIONS:
        return "Always available"
    
    config = TIME_RESTRICTIONS[offer_id]
    rules_desc = [rule["description"] for rule in config["rules"]]
    
    return f"Available: {', '.join(rules_desc)} ({config['timezone']})"


if __name__ == "__main__":
    # Test the restrictions
    print("Testing SpinGranny (ID: 7) availability...")
    print(f"Current time: {datetime.now(pytz.timezone('Europe/Paris')).strftime('%A %H:%M %Z')}")
    print(f"Is available: {is_offer_available(7)}")
    print(f"Restrictions: {get_restriction_info(7)}")

