import logging
import re
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from app.crawlers.base import BaseCrawler

logger = logging.getLogger(__name__)

class WikipediaCrawler(BaseCrawler):
    """
    Crawls Wikipedia entries for Durga Puja in Kolkata to extract
    historically significant barowari pujas, bonedi bari households,
    founding years, and cultural background.
    """

    TARGET_PAGES = [
        "https://en.wikipedia.org/wiki/Durga_Puja_in_Kolkata",
        "https://en.wikipedia.org/wiki/Durga_Puja_in_West_Bengal"
    ]

    def __init__(self):
        super().__init__(name="WikipediaCrawler")

    def crawl(self) -> List[Dict[str, Any]]:
        logger.info(f"[{self.name}] Crawling Wikipedia articles...")
        results: List[Dict[str, Any]] = []

        for url in self.TARGET_PAGES:
            resp = self.safe_get(url)
            if not resp:
                continue

            try:
                soup = BeautifulSoup(resp.text, "html.parser")
                content_div = soup.find("div", {"id": "mw-content-text"})
                if not content_div:
                    continue

                # 1. Parse bullet points and list elements
                for li in content_div.find_all("li"):
                    text = li.get_text()
                    if any(k in text.lower() for k in ["puja", "sarbojanin", "sarbajanin", "rajbari", "durgotsab", "bari"]):
                        pandal_info = self._parse_wiki_bullet(text, url)
                        if pandal_info:
                            results.append(pandal_info)

                # 2. Parse tables (historical overview, awards, locations)
                for table in content_div.find_all("table", class_="wikitable"):
                    for row in table.find_all("tr")[1:]:
                        cols = [td.get_text().strip() for td in row.find_all(["td", "th"])]
                        if len(cols) >= 2:
                            name_candidate = cols[0]
                            desc_candidate = " - ".join(cols[1:])
                            if any(k in name_candidate.lower() for k in ["puja", "club", "association", "samity", "samiti", "sangha", "bari"]):
                                results.append({
                                    "name": name_candidate,
                                    "popularity": "popular",
                                    "category": "traditional" if "bari" not in name_candidate.lower() else "bonedi_bari",
                                    "bonedi": "bari" in name_candidate.lower() or "rajbari" in name_candidate.lower(),
                                    "description": desc_candidate[:300],
                                    "source": "wikipedia",
                                    "source_url": url,
                                    "popularity_score": 90.0
                                })

            except Exception as e:
                logger.error(f"[{self.name}] Error parsing {url}: {e}")

        logger.info(f"[{self.name}] Extracted {len(results)} pandal records from Wikipedia.")
        return results

    def _parse_wiki_bullet(self, text: str, source_url: str) -> Dict[str, Any] | None:
        text = text.strip()
        if len(text) < 10 or len(text) > 400:
            return None

        # Split on colon or dash
        parts = re.split(r"[:–—\-]", text, maxsplit=1)
        name = parts[0].strip()

        # Sanity check name length and terms
        if len(name.split()) > 7 or len(name) < 4:
            return None

        description = parts[1].strip() if len(parts) > 1 else ""
        
        # Check if bonedi
        is_bonedi = any(k in name.lower() or k in description.lower() for k in ["bonedi", "rajbari", "household", "family", "bari", "choudhury", "deb"])
        
        # Extract founding year if mentioned (e.g. 1910, 1757)
        year_match = re.search(r"\b(1[6-9]\d{2}|20\d{2})\b", text)
        year_established = year_match.group(1) if year_match else None

        return {
            "name": name,
            "popularity": "popular" if any(k in name.lower() for k in ["bagbazar", "kumartuli", "college square", "santosh mitra", "mohammad ali", "suruchi", "ekdalia", "maddox"]) else "unpopular",
            "category": "bonedi_bari" if is_bonedi else "traditional",
            "bonedi": is_bonedi,
            "year_established": year_established,
            "description": description or f"Notable Durga Puja mentioned in Wikipedia historical records ({source_url}).",
            "source": "wikipedia",
            "source_url": source_url,
            "popularity_score": 80.0 if not is_bonedi else 75.0
        }
