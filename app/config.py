import os
from typing import List

class Settings:
    PROJECT_NAME: str = "Durga Puja Pandal Data Crawler & API"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./pujo_data.db")
    
    # Automatic background crawl interval in hours
    CRAWL_INTERVAL_HOURS: int = int(os.getenv("CRAWL_INTERVAL_HOURS", "24"))
    
    # Crawler rate limiting and timeouts (anti-ban resilience)
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "15"))
    MIN_REQUEST_DELAY: float = float(os.getenv("MIN_REQUEST_DELAY", "0.5"))
    MAX_REQUEST_DELAY: float = float(os.getenv("MAX_REQUEST_DELAY", "1.5"))
    
    # User-Agent rotation pool to prevent anti-scraping blocks
    USER_AGENTS: List[str] = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1"
    ]

    # Renowned popular pandals / mega-crowd pullers for scoring
    KNOWN_POPULAR_KEYWORDS: List[str] = [
        "sreebhumi", "santosh mitra", "college square", "bagbazar", "kumartuli park",
        "ekdalia", "singhi park", "suruchi sangha", "chetla agrani", "maddox square",
        "mohammad ali park", "badamtala", "hindusthan park", "samaj sebi", "naktala",
        "tridhara", "deshapriya", "ballygunge cultural", "mudiali", "shiv mandir",
        "fd block", "bj block", "labony", "bosepukur", "babubagan", "jodhpur park",
        "chaltabagan", "ahiritola sarbojanin", "hatibagan nabin pally", "dum dum park tarun dal",
        "dum dum park bharat chakra", "tala prattoy", "kashi bose lane", "barisha club",
        "haridevpur ajeyo sangha", "behala club", "41 pally", "behala natun dal",
        "sealdah durga bari", "sealdah railway", "kalyani iti", "kalyani a9", "luminous club",
        "subrata sangha", "dada bhai", "chandannagar strand", "barasat", "pragati chakra",
        "durgapur city centre", "bishnupur mrinmoyee", "cooch behar rajbari", "bada debi"
    ]

settings = Settings()
