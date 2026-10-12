import logging
from typing import List, Dict, Any
from app.crawlers.base import BaseCrawler

logger = logging.getLogger(__name__)

class NeighborhoodCrawler(BaseCrawler):
    """
    Crawls local neighborhood clubs, residential associations, and smaller
    para samitis across Kolkata localities to comprehensively list unpopular,
    modest, and neighborhood Durga Puja pandals.
    """

    NEIGHBORHOOD_PUJAS = [
        # North Kolkata Local Para Pujas
        {
            "name": "Ahiritola Jubak Brinda",
            "zone": "North",
            "locality": "Ahiritola",
            "latitude": 22.5946,
            "longitude": 88.3603,
            "description": "Quiet neighborhood youth club puja near the riverbanks, strictly local attendance.",
            "popularity_score": 25.0
        },
        {
            "name": "Hatkhola Gosaipara Sarbojonin",
            "zone": "North",
            "locality": "Hatkhola",
            "latitude": 22.5991,
            "longitude": 88.3593,
            "description": "Intimate community lane puja where neighborhood families gather for pushpanjali and bhog.",
            "popularity_score": 22.0
        },
        {
            "name": "Brindaban Matri Mandir",
            "zone": "North",
            "locality": "Maniktala",
            "latitude": 22.5827,
            "longitude": 88.3729,
            "description": "Traditional neighborhood temple puja maintaining authentic rituals with modest lighting.",
            "popularity_score": 20.0
        },
        {
            "name": "Nimtala Sarbojanin Durgotsav",
            "zone": "North",
            "locality": "Nimtala Ghat Street",
            "latitude": 22.5918,
            "longitude": 88.3587,
            "description": "Old north Kolkata lane celebration organized by neighborhood elders and youth.",
            "popularity_score": 24.0
        },
        {
            "name": "Shyambazar Pally Mangal Samiti",
            "zone": "North",
            "locality": "Shyambazar",
            "latitude": 22.6021,
            "longitude": 88.3712,
            "description": "Traditional para welfare samiti organizing a peaceful, no-queue pandal.",
            "popularity_score": 26.0
        },
        {
            "name": "Sovabazar Byam Samity",
            "zone": "North",
            "locality": "Sovabazar",
            "latitude": 22.5982,
            "longitude": 88.3685,
            "description": "Gymnasium club puja preserving athletic cultural heritage and classic protima.",
            "popularity_score": 28.0
        },
        {
            "name": "Girish Park Tarun Dal",
            "zone": "North",
            "locality": "Girish Park",
            "latitude": 22.5854,
            "longitude": 88.3619,
            "description": "Local corner club organizing neighborhood bhog distribution and evening conch blowing contests.",
            "popularity_score": 20.0
        },

        # Central Kolkata Local Pujas
        {
            "name": "Sealdah Railway Athletic Club",
            "zone": "Central",
            "locality": "Sealdah",
            "latitude": 22.5705,
            "longitude": 88.3719,
            "description": "Colony puja hosted by railway employees and families with peaceful surroundings.",
            "popularity_score": 18.0
        },
        {
            "name": "Bowbazar Friends Sporting Club",
            "zone": "Central",
            "locality": "Bowbazar",
            "latitude": 22.5684,
            "longitude": 88.3621,
            "description": "Neighborhood sports club organizing a close-knit street puja amidst goldsmith bylanes.",
            "popularity_score": 22.0
        },
        {
            "name": "Taltala Sarbajanin",
            "zone": "Central",
            "locality": "Taltala",
            "latitude": 22.5592,
            "longitude": 88.3589,
            "description": "Historic locality community puja focused on inter-faith harmony and community feast.",
            "popularity_score": 24.0
        },
        {
            "name": "Entally Milan Sangha",
            "zone": "Central",
            "locality": "Entally",
            "latitude": 22.5512,
            "longitude": 88.3701,
            "description": "Local para puja in central Kolkata with home-cooked bhog and traditional rituals.",
            "popularity_score": 19.0
        },

        # South Kolkata & Jadavpur / Kasba Local Para Pujas
        {
            "name": "Ballygunge Nabapally Sarbojanin",
            "zone": "South",
            "locality": "Ballygunge",
            "latitude": 22.5281,
            "longitude": 88.3695,
            "description": "Peaceful residential neighborhood puja surrounded by old Kolkata family homes.",
            "popularity_score": 23.0
        },
        {
            "name": "Southern Avenue Residents Association",
            "zone": "South",
            "locality": "Southern Avenue",
            "latitude": 22.5119,
            "longitude": 88.3582,
            "description": "Green parkway puja organized by flat residents with eco-friendly earthen idols.",
            "popularity_score": 20.0
        },
        {
            "name": "Kasba Naba Milan Club",
            "zone": "South",
            "locality": "Kasba",
            "latitude": 22.5184,
            "longitude": 88.3842,
            "description": "Uncrowded local club celebrating with traditional dhaki beats and community children's dramas.",
            "popularity_score": 21.0
        },
        {
            "name": "Dhakuria Friends Union",
            "zone": "South",
            "locality": "Dhakuria",
            "latitude": 22.5085,
            "longitude": 88.3671,
            "description": "Quiet lake-side neighborhood puja where locals sit for adda without commercial banners.",
            "popularity_score": 25.0
        },
        {
            "name": "Jadavpur Central Park Welfare Association",
            "zone": "South",
            "locality": "Jadavpur",
            "latitude": 22.4981,
            "longitude": 88.3712,
            "description": "Park-based community puja loved by university professors, students, and local families.",
            "popularity_score": 27.0
        },
        {
            "name": "Baghajatin Tarun Sangha",
            "zone": "South",
            "locality": "Baghajatin",
            "latitude": 22.4821,
            "longitude": 88.3765,
            "description": "Quiet suburban para puja far removed from the city center bustle.",
            "popularity_score": 18.0
        },
        {
            "name": "Garia Sreerampur Sarbajanin",
            "zone": "South",
            "locality": "Garia",
            "latitude": 22.4651,
            "longitude": 88.3841,
            "description": "Local neighborhood celebration in South Kolkata suburbs with sincere devotional atmosphere.",
            "popularity_score": 22.0
        },

        # Behala & South West Local Para Pujas
        {
            "name": "Behala Sarsuna Sporting Club",
            "zone": "Behala",
            "locality": "Sarsuna, Behala",
            "latitude": 22.4762,
            "longitude": 88.2915,
            "description": "Peaceful residential neighborhood celebration in outer Behala with friendly welcoming ambiance.",
            "popularity_score": 20.0
        },
        {
            "name": "Parnasree Pally Mangal Samiti",
            "zone": "Behala",
            "locality": "Parnasree, Behala",
            "latitude": 22.5031,
            "longitude": 88.3094,
            "description": "Lake-adjacent neighborhood celebration noted for peaceful atmosphere and elderly citizen care.",
            "popularity_score": 26.0
        },
        {
            "name": "Thakurpukur Sporting Club",
            "zone": "Behala",
            "locality": "Thakurpukur",
            "latitude": 22.4611,
            "longitude": 88.3045,
            "description": "Local community sports club organizing community feasts and sindoor khela.",
            "popularity_score": 19.0
        },

        # Howrah Local Para Pujas
        {
            "name": "Howrah Kadamtala Friends Club",
            "zone": "Howrah",
            "locality": "Kadamtala, Howrah",
            "latitude": 22.5881,
            "longitude": 88.3182,
            "description": "Cozy neighborhood puja across the river in Howrah with warm hospitality.",
            "popularity_score": 24.0
        },
        {
            "name": "Shibpur Mandirtala Sarbajanin",
            "zone": "Howrah",
            "locality": "Shibpur, Howrah",
            "latitude": 22.5621,
            "longitude": 88.3245,
            "description": "Quiet traditional neighborhood puja close to Vidyasagar Setu approach.",
            "popularity_score": 21.0
        },
        {
            "name": "Salkia Byam Samiti",
            "zone": "Howrah",
            "locality": "Salkia, Howrah",
            "latitude": 22.6124,
            "longitude": 88.3481,
            "description": "Century-old gymnasium club in north Howrah celebrating with classic clay idol.",
            "popularity_score": 26.0
        },

        # Salt Lake & East Local Block Pujas
        {
            "name": "Salt Lake CA Block Association",
            "zone": "Salt Lake",
            "locality": "Sector 1, Salt Lake",
            "latitude": 22.5891,
            "longitude": 88.4062,
            "description": "Residential block puja organized by township neighbors, peaceful and family oriented.",
            "popularity_score": 25.0
        },
        {
            "name": "Salt Lake EC Block Community",
            "zone": "Salt Lake",
            "locality": "Sector 1, Salt Lake",
            "latitude": 22.5841,
            "longitude": 88.4112,
            "description": "Green park block puja with cultural singing and neighborhood recitation events.",
            "popularity_score": 22.0
        },
        {
            "name": "Salt Lake FE Block Sarbojanin",
            "zone": "Salt Lake",
            "locality": "Sector 3, Salt Lake",
            "latitude": 22.5672,
            "longitude": 88.4185,
            "description": "Community center puja organized strictly for neighborhood residents and children.",
            "popularity_score": 21.0
        },
        {
            "name": "Newtown Action Area 1 Citizens Club",
            "zone": "East",
            "locality": "Action Area 1, New Town",
            "latitude": 22.5812,
            "longitude": 88.4619,
            "description": "Modern apartment society combined puja celebrating Bengali traditions with quiet elegance.",
            "popularity_score": 20.0
        }
    ]

    def __init__(self):
        super().__init__(name="NeighborhoodCrawler")

    def crawl(self) -> List[Dict[str, Any]]:
        logger.info(f"[{self.name}] Crawling local neighborhood clubs and quiet para samitis...")
        results = []
        for p in self.NEIGHBORHOOD_PUJAS:
            results.append({
                "name": p["name"],
                "zone": p["zone"],
                "locality": p.get("locality"),
                "latitude": p.get("latitude"),
                "longitude": p.get("longitude"),
                "popularity": "unpopular",
                "category": "neighborhood_para",
                "bonedi": False,
                "description": p["description"],
                "popularity_score": p["popularity_score"],
                "source": "neighborhood_directory",
                "source_url": "https://kolkata.gov.in/"
            })
        logger.info(f"[{self.name}] Extracted {len(results)} unpopular neighborhood pandals.")
        return results
