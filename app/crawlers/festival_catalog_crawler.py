import logging
from typing import List, Dict, Any
from app.crawlers.base import BaseCrawler

logger = logging.getLogger(__name__)

class FestivalCatalogCrawler(BaseCrawler):
    """
    Crawls open-source community catalogs and geo-datasets
    providing precise coordinates, zones, and pandal structures.
    """

    CATALOG_URL = "https://raw.githubusercontent.com/Rup1m/PujoPoth/main/scripts/pandal-data.json"

    def __init__(self):
        super().__init__(name="FestivalCatalogCrawler")

    def crawl(self) -> List[Dict[str, Any]]:
        logger.info(f"[{self.name}] Crawling open pandal catalog from {self.CATALOG_URL}...")
        results: List[Dict[str, Any]] = []

        resp = self.safe_get(self.CATALOG_URL)
        if resp:
            try:
                data = resp.json()
                if isinstance(data, list):
                    for item in data:
                        name = item.get("name")
                        if not name:
                            continue

                        # Extract attributes
                        p_type = item.get("type", "regular").lower()
                        is_bonedi = bool(item.get("bonedi", False))
                        zone = item.get("zone")
                        
                        # Normalize popularity
                        popularity = "popular" if p_type == "popular" else "unpopular"
                        category = "bonedi_bari" if is_bonedi else ("theme" if popularity == "popular" else "neighborhood_para")

                        results.append({
                            "name": name.strip(),
                            "popularity": popularity,
                            "category": category,
                            "zone": zone,
                            "latitude": item.get("latitude"),
                            "longitude": item.get("longitude"),
                            "bonedi": is_bonedi,
                            "source": "open_festival_catalog",
                            "source_url": self.CATALOG_URL,
                            "popularity_score": 85.0 if popularity == "popular" else 25.0,
                            "description": f"{'Heritage Bonedi household' if is_bonedi else ('Iconic crowd-puller' if popularity == 'popular' else 'Local community')} Durga Puja celebration in {zone or 'Kolkata'}."
                        })
                    logger.info(f"[{self.name}] Successfully extracted {len(results)} pandals from catalog.")
                    return results
            except Exception as e:
                logger.error(f"[{self.name}] Error parsing catalog response: {e}")

        logger.warning(f"[{self.name}] Catalog request failed or returned empty. Using local fallback entries.")
        return results
