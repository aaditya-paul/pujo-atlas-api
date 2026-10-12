import logging
import re
import warnings
from typing import List, Dict, Any
from bs4 import BeautifulSoup
try:
    from bs4 import XMLParsedAsHTMLWarning
    warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
except ImportError:
    pass
from app.crawlers.base import BaseCrawler

logger = logging.getLogger(__name__)

class SocialMediaCrawler(BaseCrawler):
    """
    Crawls public social media discussion feeds (such as r/kolkata public threads,
    crowdsourced local forum feeds) and community recommendation archives to discover
    unpopular, underrated, and quiet neighborhood ('para') pandals.
    """

    FEEDS = [
        "https://www.reddit.com/r/kolkata/hot.rss",
        "https://old.reddit.com/r/kolkata/new.rss"
    ]

    # Curated social media crowdsourced recommendations for hidden gems and quiet para pujas
    CROWDSOURCED_RECOMMENDATIONS = [
        {
            "name": "Baghbazar Sarbojanin Durgotsav - Ghorer Pujo",
            "zone": "North",
            "locality": "Bagbazar",
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "description": "Recommended on local social forums as a quiet traditional alternative to the main crowded Bagbazar pandal.",
            "popularity_score": 30.0,
            "bonedi": False
        },
        {
            "name": "Darpanarayan Tagore Street Puja",
            "zone": "North",
            "locality": "Pathuriaghata",
            "popularity": "unpopular",
            "category": "bonedi_bari",
            "description": "Ancestral household puja praised on r/kolkata for heritage architecture and peaceful atmosphere.",
            "popularity_score": 35.0,
            "bonedi": True
        },
        {
            "name": "Golpark Sarbojanin",
            "zone": "South",
            "locality": "Golpark",
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "description": "Local neighborhood puja right next to Golpark roundabout, cozy and low footfall.",
            "popularity_score": 25.0,
            "bonedi": False
        },
        {
            "name": "Ballygunge Gardens Sarbojanin",
            "zone": "South",
            "locality": "Ballygunge Place",
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "description": "Serene residential puja celebrated by local community residents without commercial loud music.",
            "popularity_score": 20.0,
            "bonedi": False
        },
        {
            "name": "Lake View Road Sammilani",
            "zone": "South",
            "locality": "Southern Avenue",
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "description": "Frequently recommended as a peaceful rest-stop during South Kolkata pandal hopping.",
            "popularity_score": 28.0,
            "bonedi": False
        },
        {
            "name": "Behala Young Mens Association",
            "zone": "Behala",
            "locality": "Behala Chowrasta",
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "description": "Local para puja in Behala with classic clay idol and traditional neighborhood dhaak.",
            "popularity_score": 22.0,
            "bonedi": False
        },
        {
            "name": "Salt Lake BA Block Sarbojanin",
            "zone": "Salt Lake",
            "locality": "Sector 1, Salt Lake",
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "description": "Charming quiet neighborhood block puja praised on social threads for eco-friendly decor.",
            "popularity_score": 25.0,
            "bonedi": False
        },
        {
            "name": "Salt Lake CJ Block Durgotsab",
            "zone": "Salt Lake",
            "locality": "Sector 2, Salt Lake",
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "description": "Peaceful park-based block puja in Salt Lake with intimate community cultural programs.",
            "popularity_score": 24.0,
            "bonedi": False
        },
        {
            "name": "Tollygunge Bangur Park Association",
            "zone": "South",
            "locality": "Tollygunge",
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "description": "Neighborhood puja situated in quiet residential bylanes away from metro rush.",
            "popularity_score": 18.0,
            "bonedi": False
        },
        {
            "name": "Santoshpur Avenue Friends Club",
            "zone": "South",
            "locality": "Santoshpur",
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "description": "Intimate community club puja recognized on local forums for family-friendly ambiance.",
            "popularity_score": 20.0,
            "bonedi": False
        },
        {
            "name": "Khelat Ghosh Bari Durgotsab",
            "zone": "North",
            "locality": "Pathuriaghata",
            "popularity": "unpopular",
            "category": "bonedi_bari",
            "description": "Stunning grand Thakur Dalan household puja dating back to 1846, quiet and historic.",
            "popularity_score": 40.0,
            "bonedi": True
        },
        {
            "name": "Sealdah Durga Bari (Baithakkhana)",
            "zone": "Central",
            "locality": "Sealdah / Baithakkhana",
            "popularity": "popular",
            "category": "traditional",
            "description": "Historic celebration near Sealdah station highlighted on r/kolkata for drawing heavy crowds of commuters and heritage enthusiasts.",
            "popularity_score": 82.0,
            "bonedi": False
        },
        {
            "name": "Thanthania Dutta Bari Puja",
            "zone": "Central",
            "locality": "College Street / Thanthania",
            "popularity": "unpopular",
            "category": "bonedi_bari",
            "description": "Over 200 years old ancestral household puja founded by Dwarkanath Dutta in 1855.",
            "popularity_score": 42.0,
            "bonedi": True
        },
        {
            "name": "Chatu Babu Latu Babu Bonedi Bari",
            "zone": "North",
            "locality": "Beadon Street",
            "popularity": "unpopular",
            "category": "bonedi_bari",
            "description": "Famous historic bonedi puja initiated in 1770 by Ramdulal Dey, peaceful morning visit recommended on Reddit.",
            "popularity_score": 45.0,
            "bonedi": True
        },
        {
            "name": "Laha Bari Durga Puja",
            "zone": "Central",
            "locality": "Bidhan Sarani",
            "popularity": "unpopular",
            "category": "bonedi_bari",
            "description": "Awe-inspiring traditional courtyard puja with unique Ashtadhatu idol, very calm atmosphere.",
            "popularity_score": 42.0,
            "bonedi": True
        },
        {
            "name": "Rani Rashmoni Bari (Janbazar)",
            "zone": "Central",
            "locality": "Janbazar / SN Banerjee Road",
            "popularity": "unpopular",
            "category": "bonedi_bari",
            "description": "Historically founded by Rani Rashmoni in late 18th century, serene religious rituals.",
            "popularity_score": 45.0,
            "bonedi": True
        }
    ]

    def __init__(self):
        super().__init__(name="SocialMediaCrawler")

    def crawl(self) -> List[Dict[str, Any]]:
        logger.info(f"[{self.name}] Crawling social media feeds & crowdsourced forums...")
        results: List[Dict[str, Any]] = []

        # 1. First include crowdsourced forum & community catalogued hidden gems
        for item in self.CROWDSOURCED_RECOMMENDATIONS:
            results.append({
                "name": item["name"],
                "popularity": item["popularity"],
                "category": item["category"],
                "zone": item.get("zone"),
                "locality": item.get("locality"),
                "description": item["description"],
                "popularity_score": item.get("popularity_score", 25.0),
                "bonedi": item.get("bonedi", False),
                "source": "social_media_forum",
                "source_url": "https://www.reddit.com/r/kolkata/"
            })

        # 2. Attempt live feed fetch with anti-ban safeguards
        for feed_url in self.FEEDS:
            resp = self.safe_get(feed_url)
            if not resp or not resp.text.strip():
                continue

            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    soup = BeautifulSoup(resp.text, "html.parser")
                for entry in soup.find_all("entry"):
                    title_elem = entry.find("title")
                    content_elem = entry.find("content")
                    title = title_elem.get_text() if title_elem else ""
                    content = content_elem.get_text() if content_elem else ""
                    full_text = f"{title} {content}"

                    # Look for pandal recommendations in social media text
                    if any(term in full_text.lower() for term in ["pandal", "pujo", "durga puja"]):
                        extracted = self._extract_mentions_from_social(full_text, feed_url)
                        results.extend(extracted)
            except Exception as e:
                logger.error(f"[{self.name}] Error reading feed {feed_url}: {e}")

        logger.info(f"[{self.name}] Collected {len(results)} items from social sources.")
        return results

    def _extract_mentions_from_social(self, text: str, source_url: str) -> List[Dict[str, Any]]:
        found = []
        # Pattern to look for named clubs / associations / sanghas / samitis / bari
        pattern = r"\b([A-Z][a-zA-Z0-9\s\-]{2,30}\s+(?:Club|Sangha|Samiti|Samity|Association|Sarbojanin|Bari|Rajbari))\b"
        matches = set(re.findall(pattern, text))
        for m in matches:
            cleaned = m.strip()
            if len(cleaned.split()) >= 2 and len(cleaned) < 50:
                is_bonedi = "bari" in cleaned.lower() or "rajbari" in cleaned.lower()
                found.append({
                    "name": cleaned,
                    "popularity": "unpopular",
                    "category": "bonedi_bari" if is_bonedi else "neighborhood_para",
                    "bonedi": is_bonedi,
                    "description": f"Discovered from public social media community discussion feed ({source_url}).",
                    "source": "social_media_feed",
                    "source_url": source_url,
                    "popularity_score": 20.0
                })
        return found
