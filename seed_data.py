from models import init_db, get_session, Offer

def seed_data():
    """Seed the database with example casino offers"""
    
    print("Initializing database...")
    init_db()
    
    session = get_session()
    
    try:
        # Check if offers already exist
        existing_count = session.query(Offer).count()
        
        if existing_count > 0:
            print(f"⚠ Database already contains {existing_count} offers. Skipping seed.")
            return
        
        # Create example offers (no postback_secret needed - using shared secret)
        offers_data = [
            {
                "name": "Casino Alpha",
                "casino_url": "https://casino-alpha.example.com/register",
                "active": True
            },
            {
                "name": "Casino Beta",
                "casino_url": "https://casino-beta.example.com/signup",
                "active": True
            },
            {
                "name": "Casino Gamma",
                "casino_url": "https://casino-gamma.example.com/join",
                "active": True
            },
            {
                "name": "Casino Delta",
                "casino_url": "https://casino-delta.example.com/start",
                "active": True
            }
        ]
        
        for offer_data in offers_data:
            offer = Offer(**offer_data)
            session.add(offer)
            print(f"  + {offer_data['name']}")
            print(f"    URL: {offer_data['casino_url']}")
            print()
        
        session.commit()
        print("✓ Seed data created successfully")
        print(f"✓ {len(offers_data)} offers added to database")
        print()
        print("=" * 60)
        print("IMPORTANT: Configure your shared postback secret")
        print("=" * 60)
        print("Set SHARED_POSTBACK_SECRET in your .env file or environment")
        print("Casino platforms should use this shared secret for all postbacks")
        print("=" * 60)
        
    except Exception as e:
        session.rollback()
        print(f"✗ Error seeding data: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_data()
