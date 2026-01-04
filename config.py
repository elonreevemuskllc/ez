import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://casino_user:casino_pass_2024@localhost:5432/casino_router')
    
    # Server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Performance Engine
    LAST_N_CLICKS = int(os.getenv('LAST_N_CLICKS', 100))
    EXPLORATION_RATE = float(os.getenv('EXPLORATION_RATE', 0.20))
    CRON_INTERVAL_MINUTES = int(os.getenv('CRON_INTERVAL_MINUTES', 10))
    
    # Postback Authentication
    SHARED_POSTBACK_SECRET = os.getenv('SHARED_POSTBACK_SECRET', 'change-me-in-production')
    
    # Admin Authentication
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    # Rate Limiting
    RATE_LIMIT_CLICK = int(os.getenv('RATE_LIMIT_CLICK', 100))
    RATE_LIMIT_POSTBACK = int(os.getenv('RATE_LIMIT_POSTBACK', 200))