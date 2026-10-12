import pytest
from app.crawlers.manager import CrawlerManager
from app.crawlers.festival_catalog_crawler import FestivalCatalogCrawler
from app.crawlers.portal_guide_crawler import PortalGuideCrawler
from app.crawlers.neighborhood_crawler import NeighborhoodCrawler
from app.crawlers.social_media_crawler import SocialMediaCrawler
from app.crawlers.west_bengal_district_crawler import WestBengalDistrictCrawler

def test_slugify():
    cm = CrawlerManager()
    assert cm.slugify("Bagbazar Sarbojanin Durgotsav!") == "bagbazar-sarbojanin-durgotsav"
    assert cm.slugify("Santosh Mitra Square (Sealdah)") == "santosh-mitra-square-sealdah"

def test_normalize_name():
    cm = CrawlerManager()
    assert cm.normalize_name("Bagbazar Sarbojanin Durgotsav") == "bagbazar"
    assert cm.normalize_name("Ahiritola Sarbajanin Durga Puja") == "ahiritola"

def test_classification_popular():
    cm = CrawlerManager()
    raw = {
        "name": "Sreebhumi Sporting Club",
        "description": "Massive mega-budget theme with world wonder replica.",
        "popularity_score": 85.0
    }
    pop, score, cat, is_bonedi = cm.classify_pandal(raw)
    assert pop == "popular"
    assert score >= 60.0
    assert is_bonedi is False

def test_classification_unpopular():
    cm = CrawlerManager()
    raw = {
        "name": "Brindaban Matri Mandir",
        "description": "Quiet neighborhood temple puja maintaining authentic rituals with modest lighting.",
        "popularity_score": 20.0
    }
    pop, score, cat, is_bonedi = cm.classify_pandal(raw)
    assert pop == "unpopular"
    assert score < 60.0
    assert cat == "neighborhood_para"
    assert is_bonedi is False

def test_classification_sealdah_durga_bari():
    cm = CrawlerManager()
    raw = {
        "name": "Sealdah Durga Bari (Railway Athletic Club)",
        "locality": "Sealdah Station Area",
        "description": "Centenary celebration near major railway hub with heavy commuter footfalls."
    }
    # When cross-referenced across 2+ sources
    pop, score, cat, is_bonedi = cm.classify_pandal(raw, sources_count=2)
    assert pop == "popular"
    assert score >= 75.0

def test_cross_referencing_consensus_bonus():
    cm = CrawlerManager()
    raw = {
        "name": "Local Community Samiti",
        "description": "Devotional neighborhood puja",
        "popularity_score": 40.0
    }
    # With 1 source: stays unpopular
    pop1, score1, _, _ = cm.classify_pandal(raw, sources_count=1)
    assert pop1 == "unpopular"

    # With 2 sources: consensus elevates score
    pop2, score2, _, _ = cm.classify_pandal(raw, sources_count=2)
    assert score2 == score1 + 15.0

def test_classification_bonedi_bari():
    cm = CrawlerManager()
    raw = {
        "name": "Sovabazar Rajbari Durga Puja",
        "description": "Historic ancestral household puja founded in 1757.",
        "bonedi": True
    }
    pop, score, cat, is_bonedi = cm.classify_pandal(raw)
    assert is_bonedi is True
    assert cat == "bonedi_bari"

def test_west_bengal_district_crawler():
    crawler = WestBengalDistrictCrawler()
    results = crawler.crawl()
    assert len(results) >= 20
    districts = {r["district"] for r in results}
    assert "Nadia" in districts
    assert "Hooghly" in districts
    assert "Darjeeling" in districts
    assert "Cooch Behar" in districts
    assert "Bankura" in districts

    # Check famous statewide pandals
    names = [r["name"] for r in results]
    assert any("Kalyani ITI" in n for n in names)
    assert any("Guptipara" in n for n in names)
    assert any("Barasat Pragati Chakra" in n for n in names)
    assert any("Bishnupur Mrinmoyee" in n for n in names)

def test_portal_guide_crawler():
    crawler = PortalGuideCrawler()
    results = crawler.crawl()
    assert len(results) > 0
    names = [r["name"] for r in results]
    assert any("Bagbazar" in n for n in names)
    assert any("Santosh Mitra" in n for n in names)
    assert any("Sealdah" in n for n in names)

def test_neighborhood_crawler():
    crawler = NeighborhoodCrawler()
    results = crawler.crawl()
    assert len(results) >= 20
    for r in results:
        assert r["popularity"] == "unpopular"
        assert r["category"] == "neighborhood_para"

def test_social_media_crawler_crowdsourced():
    crawler = SocialMediaCrawler()
    results = crawler.crawl()
    assert len(results) >= 10
    assert any(r["source"] == "social_media_forum" for r in results)
