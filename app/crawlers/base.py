import random
import time
import logging
import datetime
import email.utils
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from app.config import settings

logger = logging.getLogger(__name__)

class BaseCrawler(ABC):
    """
    Base crawler equipped with anti-ban resilience:
    - User-Agent pool rotation
    - Full browser header emulation
    - Automatic exponential backoff retries on 429/5xx
    - Jittered rate-limiting delays between calls
    - Graceful error recovery
    """

    def __init__(self, name: str):
        self.name = name
        self.session = self._create_resilient_session()

    def _create_resilient_session(self) -> requests.Session:
        session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=1.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
            respect_retry_after_header=True
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def _get_random_headers(self, referer: Optional[str] = None) -> Dict[str, str]:
        headers = {
            "User-Agent": random.choice(settings.USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8,application/json",
            "Accept-Language": "en-US,en;q=0.9,bn;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site" if referer else "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0"
        }
        if referer:
            headers["Referer"] = referer
        return headers

    @staticmethod
    def _parse_retry_after(header_val: Optional[str], default_delay: float = 3.0) -> float:
        """Parse Retry-After header as either seconds or HTTP-date format."""
        if not header_val:
            return default_delay
        try:
            val = float(header_val.strip())
            return max(0.5, min(val, 60.0))
        except ValueError:
            try:
                dt = email.utils.parsedate_to_datetime(header_val.strip())
                diff = (dt - datetime.datetime.now(datetime.timezone.utc)).total_seconds()
                return max(0.5, min(diff, 60.0))
            except Exception:
                return default_delay

    def safe_get(
        self,
        url: str,
        params: Optional[Dict] = None,
        referer: Optional[str] = None,
        max_attempts: int = 3
    ) -> Optional[requests.Response]:
        """
        Executes an anti-ban HTTP GET request with bounded, idempotency-aware
        throttling, Retry-After header parsing, and exponential backoff with full jitter
        per the api-rate-limit-handler skill.
        """
        for attempt in range(max_attempts):
            # Polite jittered delay
            base_jitter = random.uniform(settings.MIN_REQUEST_DELAY, settings.MAX_REQUEST_DELAY)
            time.sleep(base_jitter)

            headers = self._get_random_headers(referer=referer)
            try:
                resp = self.session.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=settings.REQUEST_TIMEOUT
                )
                if resp.status_code == 200:
                    return resp
                elif resp.status_code in (408, 429):
                    retry_after = self._parse_retry_after(resp.headers.get("Retry-After"))
                    backoff = retry_after if resp.headers.get("Retry-After") else random.uniform(0.5, min(8.0, 1.5 * (2 ** attempt)))
                    logger.warning(
                        f"[{self.name}] Throttled ({resp.status_code}) at {url}. "
                        f"Backing off for {backoff:.2f}s (attempt {attempt + 1}/{max_attempts})."
                    )
                    time.sleep(backoff)
                elif resp.status_code in (500, 502, 503, 504):
                    backoff = random.uniform(0.5, min(6.0, 1.0 * (2 ** attempt)))
                    logger.warning(
                        f"[{self.name}] Server error ({resp.status_code}) at {url}. "
                        f"Backing off for {backoff:.2f}s (attempt {attempt + 1}/{max_attempts})."
                    )
                    time.sleep(backoff)
                else:
                    logger.warning(f"[{self.name}] Terminal HTTP {resp.status_code} for {url}")
                    return None
            except Exception as e:
                logger.error(f"[{self.name}] Request error fetching {url} (attempt {attempt + 1}/{max_attempts}): {e}")
                if attempt == max_attempts - 1:
                    return None
                time.sleep(random.uniform(0.5, 2.0))
        return None

    @abstractmethod
    def crawl(self) -> List[Dict[str, Any]]:
        """
        Execute crawling logic and return a list of pandal dicts.
        """
        pass
