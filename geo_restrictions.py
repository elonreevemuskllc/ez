"""
Geo-targeting module for country-specific offers.
Uses ipapi.co to detect user's country from their IP address.
"""
import requests
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

# Configuration
IPAPI_KEY = "M3ZmorMRHUNe7BNL3Feg2Y4DJ4k5RMYZvyi5m7kf0ul7MlJPDq"
IPAPI_URL = "https://ipapi.co/{ip}/country/"

# Geo restrictions configuration
# Format: offer_id -> dict with 'countries' and 'exclusive' flag
GEO_RESTRICTIONS = {
    8: {  # 7ladies - EXCLUSIF pour ces pays
        "countries": ["BE", "CH", "IT", "DE", "CA"],
        "exclusive": True  # Si True, les autres offres sont bloquées pour ces pays
    }
}


def get_country_from_ip(ip_address: str) -> Optional[str]:
    """
    Get country code from IP address using ipapi.co
    
    Args:
        ip_address: The IP address to lookup
        
    Returns:
        str: Two-letter country code (e.g., "US", "FR") or None if lookup fails
    """
    try:
        # Skip localhost/private IPs
        if ip_address in ["127.0.0.1", "localhost", "::1"] or ip_address.startswith("192.168.") or ip_address.startswith("10."):
            logger.info(f"Skipping geo lookup for local IP: {ip_address}")
            return None
        
        # Call ipapi.co with API key
        url = f"https://ipapi.co/{ip_address}/country/"
        headers = {"User-Agent": "ipapi.co/#ipapi-python/1.0.4"}
        params = {"key": IPAPI_KEY}
        
        response = requests.get(url, headers=headers, params=params, timeout=2)
        
        if response.status_code == 200:
            country_code = response.text.strip()
            logger.info(f"IP {ip_address} → Country: {country_code}")
            return country_code
        else:
            logger.warning(f"ipapi.co returned status {response.status_code} for IP {ip_address}")
            return None
            
    except requests.Timeout:
        logger.warning(f"Timeout while looking up IP {ip_address}")
        return None
    except Exception as e:
        logger.error(f"Error looking up IP {ip_address}: {e}")
        return None


def is_offer_available_for_country(offer_id: int, country_code: Optional[str]) -> bool:
    """
    Check if an offer is available for a specific country.
    Handles exclusive offers that block other offers in their countries.
    
    Args:
        offer_id: The offer ID to check
        country_code: Two-letter country code (e.g., "US") or None
        
    Returns:
        bool: True if offer is available for this country, False otherwise
    """
    # If we couldn't determine country, don't show geo-restricted offers
    if country_code is None:
        # Only show offers without geo restrictions
        return offer_id not in GEO_RESTRICTIONS
    
    # Check if this offer has geo restrictions
    if offer_id in GEO_RESTRICTIONS:
        config = GEO_RESTRICTIONS[offer_id]
        allowed_countries = config.get("countries", [])
        
        # This offer is restricted, check if country is allowed
        if country_code not in allowed_countries:
            return False
    
    # Check if another EXCLUSIVE offer claims this country
    for other_offer_id, config in GEO_RESTRICTIONS.items():
        if other_offer_id == offer_id:
            continue
        
        # If another offer is exclusive for this country, block this offer
        if config.get("exclusive", False):
            if country_code in config.get("countries", []):
                logger.info(f"Offer {offer_id} blocked by exclusive offer {other_offer_id} for country {country_code}")
                return False
    
    return True


def filter_offers_by_geo(offers: List, ip_address: str) -> List:
    """
    Filter a list of offers to only include those available for the user's country.
    
    Args:
        offers: List of Offer objects
        ip_address: User's IP address
        
    Returns:
        list: Filtered list of available offers
    """
    # Get user's country
    country_code = get_country_from_ip(ip_address)
    
    # Filter offers
    available_offers = [
        offer for offer in offers 
        if is_offer_available_for_country(offer.id, country_code)
    ]
    
    logger.info(f"Geo-filtering: {len(offers)} offers → {len(available_offers)} available for country {country_code or 'UNKNOWN'}")
    
    return available_offers


def get_geo_info(offer_id: int) -> str:
    """
    Get human-readable information about an offer's geo restrictions.
    
    Args:
        offer_id: The offer ID
        
    Returns:
        str: Description of restrictions, or "Worldwide" if none
    """
    if offer_id not in GEO_RESTRICTIONS:
        return "Worldwide 🌍"
    
    config = GEO_RESTRICTIONS[offer_id]
    countries = config.get("countries", [])
    is_exclusive = config.get("exclusive", False)
    
    country_names = {
        "BE": "Belgium",
        "CH": "Switzerland", 
        "IT": "Italy",
        "DE": "Germany",
        "CA": "Canada"
    }
    
    names = [country_names.get(code, code) for code in countries]
    exclusive_text = " (EXCLUSIVE)" if is_exclusive else ""
    return f"Only: {', '.join(names)}{exclusive_text} 🎯"


if __name__ == "__main__":
    # Test the geo detection
    print("Testing ipapi.co geo detection...")
    
    # Test with a known IP (Google DNS)
    test_ip = "8.8.8.8"
    country = get_country_from_ip(test_ip)
    print(f"IP {test_ip} → Country: {country}")
    
    # Test offer availability with EXCLUSIVE logic
    print(f"\n=== OFFER 8 (7ladies) ===")
    print(f"Restrictions: {get_geo_info(8)}")
    print(f"Available for US? {is_offer_available_for_country(8, 'US')}")
    print(f"Available for CH? {is_offer_available_for_country(8, 'CH')}")
    
    print(f"\n=== OTHER OFFERS (should be BLOCKED for BE/CH/IT/DE/CA) ===")
    print(f"Offer 5 (MyStake) available for CH? {is_offer_available_for_country(5, 'CH')}")
    print(f"Offer 5 (MyStake) available for FR? {is_offer_available_for_country(5, 'FR')}")
    print(f"Offer 6 (iCE) available for DE? {is_offer_available_for_country(6, 'DE')}")
    print(f"Offer 7 (SpinGranny) available for BE? {is_offer_available_for_country(7, 'BE')}")

