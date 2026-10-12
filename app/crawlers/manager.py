import datetime
import json
import logging
import re
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.config import settings
from app.database import SessionLocal, init_db
from app.models import Pandal, CrawlLog
from app.crawlers.festival_catalog_crawler import FestivalCatalogCrawler
from app.crawlers.wikipedia_crawler import WikipediaCrawler
from app.crawlers.social_media_crawler import SocialMediaCrawler
from app.crawlers.portal_guide_crawler import PortalGuideCrawler
from app.crawlers.neighborhood_crawler import NeighborhoodCrawler
from app.crawlers.west_bengal_district_crawler import WestBengalDistrictCrawler

logger = logging.getLogger(__name__)

class CrawlerManager:
    """
    Coordinates multi-source crawling, data cleaning, fuzzy deduplication,
    popularity classification, cross-referencing, and database persistence.
    """

    def __init__(self):
        self.crawlers = [
            FestivalCatalogCrawler(),
            WikipediaCrawler(),
            SocialMediaCrawler(),
            PortalGuideCrawler(),
            NeighborhoodCrawler(),
            WestBengalDistrictCrawler()
        ]

    @staticmethod
    def slugify(text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[\s_-]+", "-", text)
        return text.strip("-")

    @staticmethod
    def normalize_name(name: str) -> str:
        """Standardize names for deduplication and cross-referencing."""
        cleaned = name.lower().strip()

        # Specific alias canonicalization for multi-source cross-referencing
        if "sealdah" in cleaned and any(k in cleaned for k in ["athletic", "durga bari", "baithakkhana", "railway"]):
            return "sealdah durga bari railway athletic"
        if "kalyani" in cleaned and ("iti" in cleaned or "luminous" in cleaned):
            return "kalyani iti more"
        if "guptipara" in cleaned:
            return "guptipara barowari"
        if "barasat" in cleaned and ("pragati chakra" in cleaned or "pkc" in cleaned):
            return "barasat pragati chakra"
        if "bishnupur" in cleaned and "mrinmoyee" in cleaned:
            return "bishnupur mrinmoyee royal"
        if "cooch behar" in cleaned and ("bada debi" in cleaned or "rajbari" in cleaned):
            return "cooch behar bada debi rajbari"
        if "subrata sangha" in cleaned:
            return "siliguri subrata sangha"
        if "surul" in cleaned and "rajbari" in cleaned:
            return "surul rajbari santiniketan"

        # Remove common formal suffixes
        for suffix in [
            "sarbojanin durgotsav", "sarbojonin durgotsab", "sarbojanin durga puja",
            "sarbajanin durga puja", "sarbojanin", "sarbajanin", "durgotsav", "durgotsab",
            "durga puja committee", "durga puja", "durgapuja", "puja", "pujo"
        ]:
            cleaned = cleaned.replace(suffix, "")
        cleaned = re.sub(r"[^\w\s]", "", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned

    def classify_pandal(self, raw: Dict[str, Any], sources_count: int = 1) -> tuple[str, float, str, bool]:
        """
        Calculates popularity score and assigns:
        (popularity: 'popular'|'unpopular', score: float, category: str, is_bonedi: bool)
        Incorporates multi-source cross-referencing consensus bonuses and transit hubs.
        """
        name = raw.get("name", "")
        desc = raw.get("description", "")
        lower_name = name.lower()
        lower_desc = desc.lower()

        # Check if Bonedi Bari
        is_bonedi = bool(raw.get("bonedi", False)) or any(
            k in lower_name or k in lower_desc
            for k in ["bonedi", "rajbari", "family puja", "ancestral", "bari", "thakur dalan", "roy choudhury", "nabakrishna", "mrinmoyee"]
        )

        score = float(raw.get("popularity_score", 20.0))

        # Check against iconic mega crowd pullers
        for keyword in settings.KNOWN_POPULAR_KEYWORDS:
            if keyword in lower_name or keyword in lower_desc:
                score = max(score, 88.0)
                break

        # Major transit hub and railway confluence (e.g. Sealdah, Howrah station, Shyambazar, Esplanade)
        if any(h in lower_name or h in lower_desc for h in ["sealdah", "howrah station", "shyambazar five-point", "esplanade", "park street"]):
            score = max(score, 75.0)

        # Multi-source cross-referencing consensus bonus:
        # Pandals cited by multiple distinct crawlers earn cross-source credibility
        if sources_count >= 2:
            score += 15.0
        if sources_count >= 3:
            score += 20.0

        # Check description signals
        if any(w in lower_desc for w in ["award", "unesco", "millions", "grand", "towering", "world wonder", "replica", "high-budget", "laser", "monumental"]):
            score += 15.0
        if any(w in lower_desc for w in ["quiet", "intimate", "peaceful", "residential", "local attendance", "no-queue", "modest"]):
            score = min(score, 35.0)

        score = max(5.0, min(100.0, score))

        # Determine popularity
        if score >= 60.0 or raw.get("popularity") == "popular":
            popularity = "popular"
        else:
            popularity = "unpopular"

        # Determine category
        if is_bonedi:
            category = "bonedi_bari"
        elif popularity == "popular":
            category = raw.get("category", "theme")
        else:
            category = "neighborhood_para"

        return popularity, score, category, is_bonedi

    def run_all(self, db: Optional[Session] = None) -> CrawlLog:
        """
        Executes full crawler pipeline across all registered sources,
        deduplicates and cross-references findings, and updates the database.
        """
        owns_db = False
        if db is None:
            init_db()
            db = SessionLocal()
            owns_db = True

        crawl_log = CrawlLog(
            status="running",
            sources_crawled=json.dumps([c.name for c in self.crawlers]),
            started_at=datetime.datetime.now(datetime.timezone.utc)
        )
        db.add(crawl_log)
        db.commit()
        db.refresh(crawl_log)

        try:
            aggregated: Dict[str, Dict[str, Any]] = {}

            # 1. Run all crawlers
            for crawler in self.crawlers:
                try:
                    logger.info(f"[CrawlerManager] Invoking {crawler.name}...")
                    items = crawler.crawl()
                    for item in items:
                        if not item.get("name"):
                            continue
                        
                        norm_key = self.normalize_name(item["name"])
                        if not norm_key:
                            norm_key = item["name"].lower().strip()

                        if norm_key not in aggregated:
                            item["sources"] = [crawler.name]
                            aggregated[norm_key] = item
                        else:
                            # Cross-reference & enrich existing record
                            existing = aggregated[norm_key]
                            existing_sources = existing.setdefault("sources", [existing.get("source", "crawler")])
                            if crawler.name not in existing_sources:
                                existing_sources.append(crawler.name)

                            if len(item.get("name", "")) > len(existing.get("name", "")):
                                existing["name"] = item["name"]

                            if not existing.get("district") and item.get("district"):
                                existing["district"] = item["district"]
                            if not existing.get("state") and item.get("state"):
                                existing["state"] = item["state"]
                            if not existing.get("latitude") and item.get("latitude"):
                                existing["latitude"] = item["latitude"]
                            if not existing.get("longitude") and item.get("longitude"):
                                existing["longitude"] = item["longitude"]
                            if not existing.get("zone") and item.get("zone"):
                                existing["zone"] = item["zone"]
                            if not existing.get("locality") and item.get("locality"):
                                existing["locality"] = item.get("locality")
                            if not existing.get("nearest_metro") and item.get("nearest_metro"):
                                existing["nearest_metro"] = item["nearest_metro"]
                            if not existing.get("year_established") and item.get("year_established"):
                                existing["year_established"] = item["year_established"]
                            if item.get("description") and len(item["description"]) > len(existing.get("description", "")):
                                existing["description"] = item["description"]
                            if item.get("bonedi"):
                                existing["bonedi"] = True
                            
                            # Keep highest popularity score
                            existing["popularity_score"] = max(
                                float(existing.get("popularity_score", 0.0)),
                                float(item.get("popularity_score", 0.0))
                            )

                except Exception as crawler_err:
                    logger.error(f"[CrawlerManager] Error in {crawler.name}: {crawler_err}")

            # 2. Persist to Database
            items_added = 0
            items_updated = 0
            popular_count = 0
            unpopular_count = 0

            existing_pandals = db.query(Pandal).all()
            norm_map: Dict[str, List[Pandal]] = {}
            for ep in existing_pandals:
                nk = self.normalize_name(ep.name)
                norm_map.setdefault(nk, []).append(ep)

            for norm_key, item_data in aggregated.items():
                name = item_data["name"].strip()
                slug = self.slugify(name)
                if not slug:
                    slug = f"pandal-{abs(hash(name))}"

                sources_list = item_data.get("sources", [item_data.get("source", "crawler")])
                source_count = len(sources_list)
                is_cross_referenced = (source_count >= 2)

                popularity, score, category, is_bonedi = self.classify_pandal(item_data, sources_count=source_count)
                if popularity == "popular":
                    popular_count += 1
                else:
                    unpopular_count += 1

                # Query existing pandal by slug, exact name, or normalized key
                existing_pandal = db.query(Pandal).filter(Pandal.slug == slug).first()
                if not existing_pandal:
                    existing_pandal = db.query(Pandal).filter(Pandal.name == name).first()
                if not existing_pandal and norm_key in norm_map and norm_map[norm_key]:
                    existing_pandal = norm_map[norm_key][0]

                # Prune any stale duplicate records in the database with the same normalized key
                matched_records = norm_map.get(norm_key, [])
                for extra in matched_records:
                    if existing_pandal and extra.id != existing_pandal.id:
                        db.delete(extra)
                if matched_records:
                    db.flush()

                district_val = item_data.get("district") or "Kolkata"
                state_val = item_data.get("state") or "West Bengal"

                if existing_pandal:
                    existing_pandal.name = name
                    existing_pandal.slug = slug
                    existing_pandal.popularity = popularity
                    existing_pandal.popularity_score = score
                    existing_pandal.category = category
                    existing_pandal.bonedi = is_bonedi
                    existing_pandal.district = district_val
                    existing_pandal.state = state_val
                    existing_pandal.sources = json.dumps(sources_list)
                    existing_pandal.source_count = source_count
                    existing_pandal.cross_referenced = is_cross_referenced
                    if item_data.get("zone"):
                        existing_pandal.zone = item_data["zone"]
                    if item_data.get("locality"):
                        existing_pandal.locality = item_data["locality"]
                    if item_data.get("latitude"):
                        existing_pandal.latitude = item_data["latitude"]
                    if item_data.get("longitude"):
                        existing_pandal.longitude = item_data["longitude"]
                    if item_data.get("nearest_metro"):
                        existing_pandal.nearest_metro = item_data["nearest_metro"]
                    if item_data.get("description"):
                        existing_pandal.description = item_data["description"]
                    if item_data.get("year_established"):
                        existing_pandal.year_established = item_data["year_established"]
                    existing_pandal.updated_at = datetime.datetime.now(datetime.timezone.utc)
                    items_updated += 1
                else:
                    new_pandal = Pandal(
                        name=name,
                        slug=slug,
                        popularity=popularity,
                        category=category,
                        zone=item_data.get("zone"),
                        district=district_val,
                        state=state_val,
                        locality=item_data.get("locality"),
                        address=item_data.get("address"),
                        latitude=item_data.get("latitude"),
                        longitude=item_data.get("longitude"),
                        nearest_metro=item_data.get("nearest_metro"),
                        description=item_data.get("description"),
                        year_established=item_data.get("year_established"),
                        bonedi=is_bonedi,
                        source=item_data.get("source", "crawler"),
                        source_url=item_data.get("source_url"),
                        sources=json.dumps(sources_list),
                        source_count=source_count,
                        cross_referenced=is_cross_referenced,
                        popularity_score=score,
                        created_at=datetime.datetime.now(datetime.timezone.utc),
                        updated_at=datetime.datetime.now(datetime.timezone.utc)
                    )
                    db.add(new_pandal)
                    items_added += 1

            db.commit()

            # Update log
            crawl_log.status = "success"
            crawl_log.items_found = len(aggregated)
            crawl_log.items_added = items_added
            crawl_log.items_updated = items_updated
            crawl_log.popular_count = popular_count
            crawl_log.unpopular_count = unpopular_count
            crawl_log.completed_at = datetime.datetime.now(datetime.timezone.utc)
            db.commit()
            db.refresh(crawl_log)

            logger.info(
                f"[CrawlerManager] Crawl completed successfully! "
                f"Total: {len(aggregated)}, Added: {items_added}, Updated: {items_updated}, "
                f"Popular: {popular_count}, Unpopular: {unpopular_count}"
            )
            return crawl_log

        except Exception as e:
            logger.exception(f"[CrawlerManager] Fatal crawl error: {e}")
            db.rollback()
            crawl_log.status = "failed"
            crawl_log.error_message = str(e)
            crawl_log.completed_at = datetime.datetime.now(datetime.timezone.utc)
            db.commit()
            return crawl_log

        finally:
            if owns_db:
                db.close()
