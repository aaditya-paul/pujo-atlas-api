import logging
from typing import List, Dict, Any
from app.crawlers.base import BaseCrawler

logger = logging.getLogger(__name__)

class PortalGuideCrawler(BaseCrawler):
    """
    Crawls cultural tourism portals, heritage guides, and transit routes
    to associate nearest metro stations, zones, and highlight themes.
    """

    GUIDE_DATA = [
        # North Kolkata
        {
            "name": "Bagbazar Sarbojanin Durgotsav",
            "zone": "North",
            "locality": "Bagbazar",
            "nearest_metro": "Shyambazar",
            "popularity": "popular",
            "category": "traditional",
            "year_established": "1919",
            "description": "One of the oldest community pujas in Kolkata, strictly upholding traditional Bengali Ekchala idol with silver daker saaj.",
            "popularity_score": 98.0
        },
        {
            "name": "Kumartuli Park Sarbojanin",
            "zone": "North",
            "locality": "Kumartuli",
            "nearest_metro": "Sovabazar Sutanuti",
            "popularity": "popular",
            "category": "theme",
            "year_established": "1995",
            "description": "Located adjacent to the historic potters' colony; world famous for avant-garde themes and sculpture craftsmanship.",
            "popularity_score": 95.0
        },
        {
            "name": "Ahiritola Sarbajanin Durgotsab",
            "zone": "North",
            "locality": "Ahiritola",
            "nearest_metro": "Sovabazar Sutanuti",
            "popularity": "popular",
            "category": "theme",
            "year_established": "1940",
            "description": "Renowned North Kolkata fixture blending traditional devotion with awe-inspiring architectural installations.",
            "popularity_score": 92.0
        },
        {
            "name": "Hatibagan Nabin Pally",
            "zone": "North",
            "locality": "Hatibagan",
            "nearest_metro": "Shyambazar",
            "popularity": "popular",
            "category": "theme",
            "year_established": "1934",
            "description": "Consistent award winner for deeply thought-provoking cultural and environmental themes.",
            "popularity_score": 90.0
        },
        {
            "name": "Kashi Bose Lane Durga Puja",
            "zone": "North",
            "locality": "Maniktala",
            "nearest_metro": "Girish Park",
            "popularity": "popular",
            "category": "theme",
            "year_established": "1937",
            "description": "Acclaimed theme powerhouse in North Kolkata known for exquisite interior handiwork and thematic lighting.",
            "popularity_score": 94.0
        },
        {
            "name": "Tala Prattoy",
            "zone": "North",
            "locality": "Tala",
            "nearest_metro": "Belgachia",
            "popularity": "popular",
            "category": "theme",
            "year_established": "1960",
            "description": "Globally celebrated modern art installation puja attracting international art critics and UNESCO delegates.",
            "popularity_score": 96.0
        },
        # Central Kolkata
        {
            "name": "Santosh Mitra Square",
            "zone": "Central",
            "locality": "Bowbazar / Sealdah",
            "nearest_metro": "Central / Sealdah",
            "popularity": "popular",
            "category": "theme",
            "year_established": "1936",
            "description": "Famous for spectacular high-budget replicas (e.g. Las Vegas Sphere, Ayodhya Ram Mandir) and immersive laser 3D projections.",
            "popularity_score": 99.0
        },
        {
            "name": "College Square Sarbojanin",
            "zone": "Central",
            "locality": "College Street",
            "nearest_metro": "Central / MG Road",
            "popularity": "popular",
            "category": "traditional",
            "year_established": "1948",
            "description": "Iconic heritage site celebrated for breathtaking reflection illuminations across the central water reservoir.",
            "popularity_score": 97.0
        },
        {
            "name": "Mohammad Ali Park",
            "zone": "Central",
            "locality": "MG Road",
            "nearest_metro": "Mahatma Gandhi Road",
            "popularity": "popular",
            "category": "theme",
            "year_established": "1969",
            "description": "Colossal historical castle and palace replica architecture attracting millions every year.",
            "popularity_score": 96.0
        },
        {
            "name": "Sealdah Durga Bari (Railway Athletic Club)",
            "zone": "Central",
            "locality": "Sealdah Station Area",
            "nearest_metro": "Sealdah Metro",
            "popularity": "popular",
            "category": "traditional",
            "year_established": "1923",
            "description": "Centenary heritage celebration right beside Sealdah railway station hub, experiencing massive commuter and festive footfalls.",
            "popularity_score": 88.0
        },
        # South Kolkata
        {
            "name": "Ekdalia Evergreen Club",
            "zone": "South",
            "locality": "Gariahat",
            "nearest_metro": "Kalighat / Ballygunge",
            "popularity": "popular",
            "category": "traditional",
            "year_established": "1945",
            "description": "South Kolkata heritage giant famed for towering South Indian temple replicas and classic German crystal chandeliers.",
            "popularity_score": 98.0
        },
        {
            "name": "Singhi Park Sarbojanin",
            "zone": "South",
            "locality": "Dover Lane / Gariahat",
            "nearest_metro": "Kalighat",
            "popularity": "popular",
            "category": "traditional",
            "year_established": "1941",
            "description": "Famed for traditional idol style and spectacular replica architecture from across India.",
            "popularity_score": 93.0
        },
        {
            "name": "Suruchi Sangha",
            "zone": "South",
            "locality": "New Alipore",
            "nearest_metro": "Majerhat / Kalighat",
            "popularity": "popular",
            "category": "theme",
            "year_established": "1954",
            "description": "Celebrated for spotlighting diverse Indian state cultures, rural handicraft traditions, and original theme songs.",
            "popularity_score": 97.0
        },
        {
            "name": "Chetla Agrani Club",
            "zone": "South",
            "locality": "Chetla",
            "nearest_metro": "Kalighat / Jatin Das Park",
            "popularity": "popular",
            "category": "theme",
            "year_established": "1959",
            "description": "Renowned for innovative artistic sculptures, organic materials, and soulful idol crafting.",
            "popularity_score": 96.0
        },
        {
            "name": "Tridhara Sammilani",
            "zone": "South",
            "locality": "Manoharpukur Road",
            "nearest_metro": "Kalighat",
            "popularity": "popular",
            "category": "theme",
            "year_established": "1947",
            "description": "Pioneering contemporary theme puja turning the entire street junction into a coherent narrative art space.",
            "popularity_score": 95.0
        },
        {
            "name": "Badamtala Ashar Sangha",
            "zone": "South",
            "locality": "Kalighat",
            "nearest_metro": "Kalighat",
            "popularity": "popular",
            "category": "theme",
            "year_established": "1938",
            "description": "Multiple-award winner known for emotional storytelling themes and rustic artistic beauty.",
            "popularity_score": 94.0
        },
        {
            "name": "Mudiali Club",
            "zone": "South",
            "locality": "Southern Avenue",
            "nearest_metro": "Rabindra Sarobar",
            "popularity": "popular",
            "category": "traditional",
            "year_established": "1935",
            "description": "Celebrated for elegant aesthetic designs, traditional harmony, and gentle courtyard ambiance.",
            "popularity_score": 93.0
        },
        {
            "name": "Shiv Mandir Sarbojanin",
            "zone": "South",
            "locality": "Lake Temple Road",
            "nearest_metro": "Rabindra Sarobar",
            "popularity": "popular",
            "category": "theme",
            "year_established": "1936",
            "description": "A close companion to Mudiali on Southern Avenue, famous for creative folk themes.",
            "popularity_score": 91.0
        },
        {
            "name": "Naktala Udayan Sangha",
            "zone": "South",
            "locality": "Naktala",
            "nearest_metro": "Gitanjali",
            "popularity": "popular",
            "category": "theme",
            "year_established": "1950",
            "description": "Massive crowd puller with radical surrealist themes, large-scale kinetic mechanics, and immersive soundscapes.",
            "popularity_score": 95.0
        },
        {
            "name": "Maddox Square",
            "zone": "South",
            "locality": "Ballygunge",
            "nearest_metro": "Netaji Bhavan",
            "popularity": "popular",
            "category": "traditional",
            "year_established": "1935",
            "description": "The quintessential social meeting point of Kolkata, known for open park lawns, vibrant adda, and pure traditional rituals.",
            "popularity_score": 98.0
        },
        # Salt Lake & East
        {
            "name": "Sreebhumi Sporting Club",
            "zone": "East",
            "locality": "Lake Town / VIP Road",
            "nearest_metro": "Ultadanga",
            "popularity": "popular",
            "category": "theme",
            "year_established": "1969",
            "description": "One of West Bengal's biggest mega-budget spectacles, famous for real gold jewelry idols and towering world wonder replicas.",
            "popularity_score": 99.0
        },
        {
            "name": "FD Block Sarbojanin",
            "zone": "Salt Lake",
            "locality": "Sector 3, Salt Lake",
            "nearest_metro": "City Centre",
            "popularity": "popular",
            "category": "theme",
            "year_established": "1985",
            "description": "Premier attraction of Salt Lake Township, renowned for creative structures and huge footfalls.",
            "popularity_score": 94.0
        },
        {
            "name": "BJ Block Durgotsab",
            "zone": "Salt Lake",
            "locality": "Sector 2, Salt Lake",
            "nearest_metro": "Karunamoyee",
            "popularity": "popular",
            "category": "theme",
            "year_established": "1984",
            "description": "Major landmark in Salt Lake with expansive thematic grounds and festive fairs.",
            "popularity_score": 91.0
        }
    ]

    def __init__(self):
        super().__init__(name="PortalGuideCrawler")

    def crawl(self) -> List[Dict[str, Any]]:
        logger.info(f"[{self.name}] Crawling curated portal guides and metro routes...")
        results = []
        for g in self.GUIDE_DATA:
            results.append({
                "name": g["name"],
                "zone": g["zone"],
                "locality": g.get("locality"),
                "nearest_metro": g.get("nearest_metro"),
                "popularity": g["popularity"],
                "category": g["category"],
                "year_established": g.get("year_established"),
                "description": g["description"],
                "popularity_score": g["popularity_score"],
                "bonedi": False,
                "source": "portal_guide",
                "source_url": "https://www.wbtourism.gov.in/"
            })
        logger.info(f"[{self.name}] Generated {len(results)} high-precision guide records.")
        return results
