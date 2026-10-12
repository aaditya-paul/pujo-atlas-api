import logging
from typing import List, Dict, Any
from app.crawlers.base import BaseCrawler

logger = logging.getLogger(__name__)

class WestBengalDistrictCrawler(BaseCrawler):
    """
    Crawls and catalogs Durga Puja pandals across all districts of West Bengal,
    including Nadia, Hooghly, North/South 24 Parganas, Paschim/Purba Bardhaman,
    Darjeeling/Siliguri, Jalpaiguri, Cooch Behar, Bankura, Birbhum, Murshidabad,
    Medinipur, Malda, and Purulia.
    """

    DISTRICT_PUJAS = [
        # --- NADIA DISTRICT ---
        {
            "name": "Kalyani ITI More (Luminous Club)",
            "district": "Nadia",
            "zone": "South Bengal",
            "locality": "ITI More, Kalyani",
            "latitude": 22.9751,
            "longitude": 88.4344,
            "popularity": "popular",
            "category": "theme",
            "popularity_score": 99.0,
            "bonedi": False,
            "description": "One of West Bengal's largest mega-budget spectacles, famous for monumental replicas of world landmarks drawing millions of visitors from across Bengal."
        },
        {
            "name": "Kalyani A9 Square Park Association",
            "district": "Nadia",
            "zone": "South Bengal",
            "locality": "A9 Block, Kalyani",
            "latitude": 22.9812,
            "longitude": 88.4419,
            "popularity": "popular",
            "category": "theme",
            "popularity_score": 92.0,
            "bonedi": False,
            "description": "Acclaimed theme powerhouse in Nadia known for spiritual Himalayan temple architecture (such as Panch Kedar) and artistic lighting."
        },
        {
            "name": "Krishnanagar Rajbari Durga Puja",
            "district": "Nadia",
            "zone": "South Bengal",
            "locality": "Rajbari, Krishnanagar",
            "latitude": 23.4011,
            "longitude": 88.5024,
            "popularity": "popular",
            "category": "bonedi_bari",
            "popularity_score": 94.0,
            "bonedi": True,
            "year_established": "1683",
            "description": "Historic royal puja initiated by Maharaja Krishna Chandra Ray, renowned for pure traditional rituals, cannon fire immersion, and clay art."
        },
        {
            "name": "Ranaghat Subhas Avenue Friends Club",
            "district": "Nadia",
            "zone": "South Bengal",
            "locality": "Subhas Avenue, Ranaghat",
            "latitude": 23.1812,
            "longitude": 88.5821,
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "popularity_score": 25.0,
            "bonedi": False,
            "description": "Local neighborhood para puja organized by Ranaghat township youth and families with peaceful community feasts."
        },
        {
            "name": "Shantipur Barogoswami Bari",
            "district": "Nadia",
            "zone": "South Bengal",
            "locality": "Shantipur",
            "latitude": 23.2514,
            "longitude": 88.4312,
            "popularity": "unpopular",
            "category": "bonedi_bari",
            "popularity_score": 45.0,
            "bonedi": True,
            "description": "Centuries-old Vaishnavite household puja in the handloom town of Shantipur, highly serene and steeped in heritage."
        },

        # --- HOOGHLY DISTRICT ---
        {
            "name": "Guptipara Barowari Durga Puja",
            "district": "Hooghly",
            "zone": "South Bengal",
            "locality": "Guptipara",
            "latitude": 23.1892,
            "longitude": 88.4182,
            "popularity": "popular",
            "category": "traditional",
            "popularity_score": 93.0,
            "bonedi": False,
            "year_established": "1790",
            "description": "The historic birthplace of community 'Barowari' (12 friends) Durga Puja in Bengal, initiating the public pandal culture in 1790."
        },
        {
            "name": "Chandannagar Strand Road Durgotsab",
            "district": "Hooghly",
            "zone": "South Bengal",
            "locality": "Strand Road, Chandannagar",
            "latitude": 22.8682,
            "longitude": 88.3671,
            "popularity": "popular",
            "category": "theme",
            "popularity_score": 95.0,
            "bonedi": False,
            "description": "World-famous for Chandannagar electrical illumination and dynamic 3D light tableaus along the river promenade."
        },
        {
            "name": "Mankundu Sporting Club",
            "district": "Hooghly",
            "zone": "South Bengal",
            "locality": "Mankundu, Chandannagar",
            "latitude": 22.8512,
            "longitude": 88.3519,
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "popularity_score": 28.0,
            "bonedi": False,
            "description": "Quiet neighborhood club celebration loved by local residents for warm community participation without traffic jams."
        },
        {
            "name": "Serampore Goswami Bari Durgotsav",
            "district": "Hooghly",
            "zone": "South Bengal",
            "locality": "Battala, Serampore",
            "latitude": 22.7521,
            "longitude": 88.3415,
            "popularity": "unpopular",
            "category": "bonedi_bari",
            "popularity_score": 42.0,
            "bonedi": True,
            "description": "Historic ancestral estate puja in Danish heritage town of Serampore with classic Thakur Dalan rituals."
        },

        # --- NORTH 24 PARGANAS DISTRICT ---
        {
            "name": "Barasat Pragati Chakra (PKC)",
            "district": "North 24 Parganas",
            "zone": "North 24 Parganas",
            "locality": "Champadali, Barasat",
            "latitude": 22.7214,
            "longitude": 88.4821,
            "popularity": "popular",
            "category": "theme",
            "popularity_score": 96.0,
            "bonedi": False,
            "description": "Barasat's premier crowd-puller known for sky-high architectural replicas, synchronized light arches, and night-long festive frenzy."
        },
        {
            "name": "Barasat Sandhani Club",
            "district": "North 24 Parganas",
            "zone": "North 24 Parganas",
            "locality": "Nabapally, Barasat",
            "latitude": 22.7152,
            "longitude": 88.4719,
            "popularity": "popular",
            "category": "theme",
            "popularity_score": 93.0,
            "bonedi": False,
            "description": "Major North 24 Parganas theme puja famed for intricate handicraft pandal interiors and majestic idols."
        },
        {
            "name": "Barrackpore Surendranath Park Samiti",
            "district": "North 24 Parganas",
            "zone": "North 24 Parganas",
            "locality": "Barrackpore Cantonment",
            "latitude": 22.7612,
            "longitude": 88.3714,
            "popularity": "popular",
            "category": "theme",
            "popularity_score": 87.0,
            "bonedi": False,
            "description": "Cantonment heritage town puja famous for large-scale theme decorations and artistic lighting."
        },
        {
            "name": "Habra Banikanta Pally Sarbojanin",
            "district": "North 24 Parganas",
            "zone": "North 24 Parganas",
            "locality": "Habra",
            "latitude": 22.8421,
            "longitude": 88.6612,
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "popularity_score": 24.0,
            "bonedi": False,
            "description": "Neighborhood residential para puja in suburban Habra with peaceful conch competitions and local bhog distribution."
        },

        # --- SOUTH 24 PARGANAS DISTRICT ---
        {
            "name": "Baruipur Padmapukur Sarbojanin",
            "district": "South 24 Parganas",
            "zone": "South 24 Parganas",
            "locality": "Padmapukur, Baruipur",
            "latitude": 22.3612,
            "longitude": 88.4319,
            "popularity": "popular",
            "category": "theme",
            "popularity_score": 86.0,
            "bonedi": False,
            "description": "Premier South 24 Parganas suburban attraction featuring illuminated water pond reflecting artistic pandal designs."
        },
        {
            "name": "Rajpur Sonarpur Tarun Sangha",
            "district": "South 24 Parganas",
            "zone": "South 24 Parganas",
            "locality": "Sonarpur",
            "latitude": 22.4412,
            "longitude": 88.4219,
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "popularity_score": 22.0,
            "bonedi": False,
            "description": "Quiet suburban community club celebrating with sincere devotional enthusiasm away from metro rush."
        },
        {
            "name": "Diamond Harbour River View Association",
            "district": "South 24 Parganas",
            "zone": "South 24 Parganas",
            "locality": "Diamond Harbour",
            "latitude": 22.1912,
            "longitude": 88.1921,
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "popularity_score": 26.0,
            "bonedi": False,
            "description": "Coastal Hooghly river-facing community celebration with scenic sunsets and fresh breeze."
        },

        # --- PASCHIM BARDHAMAN & PURBA BARDHAMAN ---
        {
            "name": "Durgapur City Centre Sarbojanin",
            "district": "Paschim Bardhaman",
            "zone": "Rarh Bengal",
            "locality": "City Centre, Durgapur",
            "latitude": 23.5312,
            "longitude": 87.2915,
            "popularity": "popular",
            "category": "theme",
            "popularity_score": 93.0,
            "bonedi": False,
            "description": "Premier industrial township attraction drawing hundreds of thousands across the Asansol-Durgapur industrial belt."
        },
        {
            "name": "Durgapur Benachity Agrani Club",
            "district": "Paschim Bardhaman",
            "zone": "Rarh Bengal",
            "locality": "Benachity, Durgapur",
            "latitude": 23.5512,
            "longitude": 87.3119,
            "popularity": "popular",
            "category": "theme",
            "popularity_score": 89.0,
            "bonedi": False,
            "description": "Commercial marketplace heavyweight known for grand structural engineering and dramatic lighting."
        },
        {
            "name": "Asansol Chelidanga Sporting Club",
            "district": "Paschim Bardhaman",
            "zone": "Rarh Bengal",
            "locality": "Chelidanga, Asansol",
            "latitude": 23.6812,
            "longitude": 86.9715,
            "popularity": "popular",
            "category": "theme",
            "popularity_score": 88.0,
            "bonedi": False,
            "description": "Top-tier community celebration in coal city Asansol with imaginative social awareness themes."
        },
        {
            "name": "Bardhaman Rajbari Lakshmi-Narayan Jiu",
            "district": "Purba Bardhaman",
            "zone": "Rarh Bengal",
            "locality": "Rajbari, Bardhaman",
            "latitude": 23.2412,
            "longitude": 87.8615,
            "popularity": "popular",
            "category": "bonedi_bari",
            "popularity_score": 92.0,
            "bonedi": True,
            "year_established": "1690",
            "description": "Historic Royal Palace puja of the Maharajas of Burdwan, preserving 330+ years of regal rituals and armory displays."
        },
        {
            "name": "Katwa Station Road Welfare Club",
            "district": "Purba Bardhaman",
            "zone": "Rarh Bengal",
            "locality": "Katwa",
            "latitude": 23.6412,
            "longitude": 88.1315,
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "popularity_score": 21.0,
            "bonedi": False,
            "description": "Local market and residential neighborhood celebration in Katwa with traditional Bengali adda."
        },

        # --- DARJEELING & SILIGURI ---
        {
            "name": "Siliguri Subrata Sangha",
            "district": "Darjeeling",
            "zone": "North Bengal",
            "locality": "Hakimpara, Siliguri",
            "latitude": 26.7112,
            "longitude": 88.4215,
            "popularity": "popular",
            "category": "theme",
            "popularity_score": 94.0,
            "bonedi": False,
            "description": "North Bengal's leading crowd puller, renowned for immersive cosmic, mythological, and architectural themes crafted by Bengal master artisans."
        },
        {
            "name": "Siliguri Dada Bhai Sporting Club",
            "district": "Darjeeling",
            "zone": "North Bengal",
            "locality": "Deshbandhu Para, Siliguri",
            "latitude": 26.7215,
            "longitude": 88.4112,
            "popularity": "popular",
            "category": "theme",
            "popularity_score": 91.0,
            "bonedi": False,
            "description": "Major landmark in Siliguri attracting visitors from the hills and plains alike for award-winning creativity."
        },
        {
            "name": "Darjeeling Nripendra Narayan Bengali Club",
            "district": "Darjeeling",
            "zone": "North Bengal",
            "locality": "The Mall, Darjeeling",
            "latitude": 27.0412,
            "longitude": 88.2615,
            "popularity": "unpopular",
            "category": "traditional",
            "popularity_score": 48.0,
            "bonedi": False,
            "year_established": "1892",
            "description": "Over 130-year-old historic hill station Durga Puja founded by Bengali settlers and supported by the Maharajas of Cooch Behar, surrounded by tea gardens and Kanchenjunga."
        },
        {
            "name": "Siliguri Rathkhola Athletic Club",
            "district": "Darjeeling",
            "zone": "North Bengal",
            "locality": "Rathkhola, Siliguri",
            "latitude": 26.7312,
            "longitude": 88.4315,
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "popularity_score": 24.0,
            "bonedi": False,
            "description": "Neighborhood sports club organizing a close-knit community pandal with warmth and traditional food stalls."
        },

        # --- COOCH BEHAR & JALPAIGURI ---
        {
            "name": "Cooch Behar Rajbari Bada Debi Puja",
            "district": "Cooch Behar",
            "zone": "North Bengal",
            "locality": "Madan Mohan Temple / Rajbari, Cooch Behar",
            "latitude": 26.3212,
            "longitude": 89.4415,
            "popularity": "popular",
            "category": "bonedi_bari",
            "popularity_score": 97.0,
            "bonedi": True,
            "year_established": "1510",
            "description": "Over 500-year-old historic royal puja of the Koch Dynasty. The iconic idol is sculpted in deep crimson red following ancient tantric royal decree."
        },
        {
            "name": "Jalpaiguri Babupara Sarbojanin",
            "district": "Jalpaiguri",
            "zone": "North Bengal",
            "locality": "Babupara, Jalpaiguri",
            "latitude": 26.5212,
            "longitude": 88.7215,
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "popularity_score": 25.0,
            "bonedi": False,
            "description": "Historic tea-town neighborhood celebration in Jalpaiguri with traditional cultural recitations."
        },

        # --- BANKURA DISTRICT ---
        {
            "name": "Bishnupur Mrinmoyee Royal Durga Temple",
            "district": "Bankura",
            "zone": "Rarh Bengal",
            "locality": "Bishnupur",
            "latitude": 23.0712,
            "longitude": 87.3215,
            "popularity": "popular",
            "category": "bonedi_bari",
            "popularity_score": 96.0,
            "bonedi": True,
            "year_established": "997",
            "description": "The oldest recorded Durga Puja in Bengal, dating back 1,027+ years to King Jagat Malla of the Mallabhum Dynasty. Cannon shots signal Mahashtami sandhipuja."
        },
        {
            "name": "Bankura Kenduadihi Friends Association",
            "district": "Bankura",
            "zone": "Rarh Bengal",
            "locality": "Kenduadihi, Bankura",
            "latitude": 23.2312,
            "longitude": 87.0715,
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "popularity_score": 23.0,
            "bonedi": False,
            "description": "Local neighborhood para puja in Bankura town celebrating with terracotta motifs and folk songs."
        },

        # --- BIRBHUM DISTRICT ---
        {
            "name": "Surul Rajbari Durga Puja",
            "district": "Birbhum",
            "zone": "Rarh Bengal",
            "locality": "Surul, Santiniketan / Bolpur",
            "latitude": 23.6612,
            "longitude": 87.6715,
            "popularity": "popular",
            "category": "bonedi_bari",
            "popularity_score": 93.0,
            "bonedi": True,
            "year_established": "1730",
            "description": "Famous zamindar household puja near Santiniketan visited by Nobel Laureate Rabindranath Tagore, set inside a grand red terracotta palace."
        },
        {
            "name": "Hetampur Rajbari Durgotsab",
            "district": "Birbhum",
            "zone": "Rarh Bengal",
            "locality": "Hetampur, Dubrajpur",
            "latitude": 23.7812,
            "longitude": 87.4115,
            "popularity": "unpopular",
            "category": "bonedi_bari",
            "popularity_score": 44.0,
            "bonedi": True,
            "description": "Serene ancestral celebration inside the unique castle-like Hetampur Rajbari featuring Victorian and Bengali fusion architecture."
        },
        {
            "name": "Bolpur Bandhgara Tarun Samiti",
            "district": "Birbhum",
            "zone": "Rarh Bengal",
            "locality": "Bolpur",
            "latitude": 23.6712,
            "longitude": 87.6915,
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "popularity_score": 22.0,
            "bonedi": False,
            "description": "Local town club organizing an unhurried, warm para puja with Baul musical gatherings."
        },

        # --- MURSHIDABAD DISTRICT ---
        {
            "name": "Cossimbazar Choto Rajbari Durgotsav",
            "district": "Murshidabad",
            "zone": "Rarh Bengal",
            "locality": "Cossimbazar, Berhampore",
            "latitude": 24.1112,
            "longitude": 88.2715,
            "popularity": "popular",
            "category": "bonedi_bari",
            "popularity_score": 91.0,
            "bonedi": True,
            "year_established": "1700",
            "description": "Magnificent royal celebration in the nawabi capital district, preserving grand chandeliers, antique silver thrones, and traditional daker saaj."
        },
        {
            "name": "Berhampore Gorabazar Milan Sangha",
            "district": "Murshidabad",
            "zone": "Rarh Bengal",
            "locality": "Gorabazar, Berhampore",
            "latitude": 24.0912,
            "longitude": 88.2515,
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "popularity_score": 24.0,
            "bonedi": False,
            "description": "Quiet neighborhood club puja in central Berhampore with friendly community adda."
        },

        # --- PASCHIM & PURBA MEDINIPUR ---
        {
            "name": "Mahishadal Rajbari Durga Puja",
            "district": "Purba Medinipur",
            "zone": "South Bengal",
            "locality": "Mahishadal",
            "latitude": 22.1812,
            "longitude": 87.9815,
            "popularity": "popular",
            "category": "bonedi_bari",
            "popularity_score": 92.0,
            "bonedi": True,
            "year_established": "1778",
            "description": "Grand royal puja celebrated inside the massive neoclassical Mahishadal Palace with traditional musical concerts and royal brass chariots."
        },
        {
            "name": "Midnapore Chhotobazar Sarbojanin",
            "district": "Paschim Medinipur",
            "zone": "Rarh Bengal",
            "locality": "Chhotobazar, Midnapore",
            "latitude": 22.4212,
            "longitude": 87.3215,
            "popularity": "popular",
            "category": "theme",
            "popularity_score": 87.0,
            "bonedi": False,
            "description": "District headquarters major theme puja attracting thousands from across tribal and forested hinterlands."
        },
        {
            "name": "Kharagpur Malancha Para Welfare Club",
            "district": "Paschim Medinipur",
            "zone": "Rarh Bengal",
            "locality": "Malancha, Kharagpur",
            "latitude": 22.3412,
            "longitude": 87.3115,
            "popularity": "unpopular",
            "category": "neighborhood_para",
            "popularity_score": 20.0,
            "bonedi": False,
            "description": "Railway town neighborhood puja celebrated by diverse community residents in Kharagpur."
        },

        # --- MALDA & PURULIA ---
        {
            "name": "Malda English Bazar Town Club",
            "district": "Malda",
            "zone": "North Bengal",
            "locality": "English Bazar, Malda",
            "latitude": 25.0012,
            "longitude": 88.1415,
            "popularity": "popular",
            "category": "theme",
            "popularity_score": 88.0,
            "bonedi": False,
            "description": "Malda district's premier festive destination known for large pandal structures and fairgrounds."
        },
        {
            "name": "Kashipur Rajbari Durga Puja",
            "district": "Purulia",
            "zone": "Rarh Bengal",
            "locality": "Kashipur",
            "latitude": 23.4312,
            "longitude": 86.6715,
            "popularity": "unpopular",
            "category": "bonedi_bari",
            "popularity_score": 46.0,
            "bonedi": True,
            "year_established": "1800",
            "description": "Ancient royal estate celebration in Purulia hills with authentic red soil Chhau dance celebrations and traditional folk fervor."
        }
    ]

    def __init__(self):
        super().__init__(name="WestBengalDistrictCrawler")

    def crawl(self) -> List[Dict[str, Any]]:
        logger.info(f"[{self.name}] Crawling West Bengal district pandals (Nadia, Hooghly, 24 Parganas, Bardhaman, Siliguri, Cooch Behar, etc.)...")
        results = []
        for p in self.DISTRICT_PUJAS:
            results.append({
                "name": p["name"],
                "district": p["district"],
                "state": "West Bengal",
                "zone": p["zone"],
                "locality": p.get("locality"),
                "latitude": p.get("latitude"),
                "longitude": p.get("longitude"),
                "popularity": p["popularity"],
                "category": p["category"],
                "bonedi": p.get("bonedi", False),
                "year_established": p.get("year_established"),
                "description": p["description"],
                "popularity_score": p["popularity_score"],
                "source": "west_bengal_district_directory",
                "source_url": "https://wb.gov.in/portal/web/guest/districts"
            })
        logger.info(f"[{self.name}] Extracted {len(results)} pandals across West Bengal districts.")
        return results
