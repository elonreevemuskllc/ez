from apscheduler.schedulers.background import BackgroundScheduler
from performance import update_all_weights
from config import Config
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def scheduled_weight_update():
    """Wrapper function for scheduled weight updates with logging"""
    try:
        logger.info("Starting scheduled weight update...")
        update_all_weights()
        logger.info("✓ Scheduled weight update completed")
    except Exception as e:
        logger.error(f"✗ Scheduled weight update failed: {e}")


def start_scheduler():
    """Start the background scheduler for periodic weight updates"""
    scheduler = BackgroundScheduler()
    
    # Schedule weight updates every N minutes
    scheduler.add_job(
        scheduled_weight_update,
        'interval',
        minutes=Config.CRON_INTERVAL_MINUTES,
        id='weight_update_job',
        name='Update offer weights based on EV per sub1',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info(f"✓ Scheduler started - weight updates every {Config.CRON_INTERVAL_MINUTES} minutes")
    
    return scheduler
