import asyncio
import logging
from app.config import settings
from app.crawlers.manager import CrawlerManager
from app.database import SessionLocal
from app.models import Pandal

logger = logging.getLogger(__name__)

class CrawlScheduler:
    """
    Manages periodic background crawling (every 24 hours) and
    initial startup bootstrapping.
    """

    def __init__(self):
        self.crawler_manager = CrawlerManager()
        self.task: asyncio.Task | None = None
        self.is_running = False

    async def _periodic_loop(self):
        interval_seconds = settings.CRAWL_INTERVAL_HOURS * 3600
        logger.info(f"[CrawlScheduler] Periodic crawl worker started (interval: {settings.CRAWL_INTERVAL_HOURS}h / {interval_seconds}s).")
        
        while self.is_running:
            try:
                # Sleep before the next scheduled crawl
                await asyncio.sleep(interval_seconds)
                logger.info("[CrawlScheduler] Triggering scheduled 24-hour Durga Puja crawl run...")
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, self.crawler_manager.run_all)
                logger.info("[CrawlScheduler] Scheduled 24-hour Durga Puja crawl run finished.")
            except asyncio.CancelledError:
                logger.info("[CrawlScheduler] Worker loop cancelled.")
                break
            except Exception as e:
                logger.error(f"[CrawlScheduler] Error during scheduled crawl loop: {e}")
                # Wait 5 minutes before retrying if an unexpected error occurred
                await asyncio.sleep(300)

    def bootstrap_if_empty(self):
        """
        Runs an initial crawl if the database currently has 0 pandals,
        ensuring the API immediately has data on first run.
        """
        db = SessionLocal()
        try:
            count = db.query(Pandal).count()
            if count == 0:
                logger.info("[CrawlScheduler] Database is empty. Bootstrapping initial pandal crawl...")
                self.crawler_manager.run_all(db=db)
                logger.info(f"[CrawlScheduler] Bootstrap completed. Total pandals now in DB: {db.query(Pandal).count()}.")
            else:
                logger.info(f"[CrawlScheduler] Database already populated with {count} pandals.")
        except Exception as e:
            logger.error(f"[CrawlScheduler] Error bootstrapping database: {e}")
        finally:
            db.close()

    def start(self):
        """Start the background scheduler."""
        if not self.is_running:
            self.is_running = True
            # Bootstrap in background executor if needed
            loop = asyncio.get_event_loop()
            loop.run_in_executor(None, self.bootstrap_if_empty)
            self.task = asyncio.create_task(self._periodic_loop())

    def stop(self):
        """Stop the background scheduler gracefully."""
        self.is_running = False
        if self.task and not self.task.done():
            self.task.cancel()
            logger.info("[CrawlScheduler] Background scheduler stopped.")

scheduler = CrawlScheduler()
