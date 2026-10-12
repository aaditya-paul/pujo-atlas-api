# West Bengal & Kolkata Durga Puja Pandal Web Crawler & REST API 🪔

A modular, anti-ban resilient web crawler and high-performance REST API service designed to crawl, parse, cross-reference, deduplicate, and catalog Durga Puja pandals across **all districts of West Bengal** (Kolkata, Nadia, Hooghly, North/South 24 Parganas, Bardhaman, Birbhum, Bankura, Darjeeling, Siliguri, Cooch Behar, etc.) — distinguishing between **popular** mega-crowd pullers and **unpopular / quiet neighborhood ('para')** & **bonedi bari** celebrations.

---

## Key Features

1. **Multi-Source Autonomous Web Crawler**:
   - **Open Festival Catalogs**: Scrapes open-source community datasets and geo-spatial coordinates (`PujoPoth` / Pujo Atlas datasets).
   - **Wikipedia Heritage Scraper**: Extracts historical barowari pujas, founding dates, and UNESCO heritage context.
   - **Social Media & Community Forums**: Crawls public discussions (such as `r/kolkata` public feeds and community recommendations) to surface hidden gems, calm residential pujas, and local neighborhood favorites.
   - **Cultural & Transit Guides**: Maps pandals to nearest railway confluences and Kolkata Metro stations (e.g. Shyambazar, Sovabazar, Central, Kalighat, Rabindra Sarobar, Sealdah).
   - **Neighborhood Para Directory**: Deeply catalogs local clubs and modest community pujas across North, South, Central, East, Behala, Jadavpur, Kasba, Salt Lake, and Howrah.
   - **West Bengal District Crawler**: Catalogs landmark and quiet pujas across 17+ districts of West Bengal.

2. **Multi-Source Cross-Referencing Consensus**:
   - Aggregates citations across all 6 independent crawlers.
   - Mentions confirmed across multiple sources receive corroboration bonuses (+15 pts for $\ge 2$ sources, +20 pts for $\ge 3$ sources).
   - Ambiguous edge cases (e.g. `Sealdah Durga Bari / Sealdah Railway Athletic Club`) are reconciled through alias canonicalization and transit confluence, accurately classifying them as popular landmarks.
   - Full provenance tracking (`sources: List[str]`, `source_count: int`, `cross_referenced: bool`).

3. **Anti-Ban Resilience**:
   - Realistic browser User-Agent pool rotation.
   - Full browser header emulation (`Accept`, `Accept-Language`, `Sec-Ch-Ua`, `Sec-Fetch-*`).
   - Exponential backoff retry adapter for HTTP 429 (Rate Limit) and 5xx errors.
   - Polite jittered request delays between network requests.
   - Resilient fallback caches so the service remains 100% operational even during external network throttling.

4. **Intelligent Popularity Classification**:
   - **`popular`**: Famous mega-budget themes, award winners, transit hub confluences, and iconic crowd-pullers (e.g., Sreebhumi, Bagbazar, Santosh Mitra Square, College Square, Kumartuli Park, Ekdalia Evergreen, Suruchi Sangha, Maddox Square, Sealdah Durga Bari, Kalyani ITI More).
   - **`unpopular` / `regular`**: Quiet, cozy residential and neighborhood ("para") samitis with minimal commercial queues, authentic dhaak, and intimate community pushpanjali.
   - **`bonedi_bari`**: Historic ancestral household estates (e.g., Sovabazar Rajbari, Sabarna Roy Choudhury, Laha Bari, Thanthania Dutta Bari, Guptipara Barowari, Bishnupur Mrinmoyee).

5. **24-Hour Periodic Scheduler**:
   - Background worker automatically re-crawls, refreshes, and updates the database every 24 hours (configurable via `CRAWL_INTERVAL_HOURS`).
   - Automatic zero-config bootstrap on startup if the database is unpopulated.

6. **FastAPI Endpoints & Interactive Web Dashboard**:
   - Full OpenAPI/Swagger documentation at `/docs`.
   - Rich query filters for `popularity`, `district`, `zone`, `bonedi`, `cross_referenced`, and keyword `search`.
   - Responsive web dashboard served at `/` featuring live KPI counters, district & zone filters, cards with map links, and an on-demand crawl trigger button.

---

## Directory Structure

```
pujo-data-crawler/
├── app/
│   ├── __init__.py
│   ├── config.py                   # Anti-ban headers, timeouts, keywords
│   ├── database.py                 # SQLite/SQLAlchemy connection setup
│   ├── models.py                   # Pandal & CrawlLog database models
│   ├── schemas.py                  # Pydantic validation schemas
│   ├── scheduler.py                # 24-hour background crawler loop
│   ├── main.py                     # FastAPI application setup & lifespan
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py               # REST API endpoints
│   ├── crawlers/
│   │   ├── __init__.py
│   │   ├── base.py                 # Anti-ban BaseCrawler class
│   │   ├── festival_catalog_crawler.py # Geo-spatial catalog crawler
│   │   ├── wikipedia_crawler.py    # Wikipedia history & heritage crawler
│   │   ├── social_media_crawler.py # Social forum & hidden gem crawler
│   │   ├── portal_guide_crawler.py # Tourism & Metro guide crawler
│   │   ├── neighborhood_crawler.py # Local para puja crawler
│   │   └── manager.py              # CrawlerManager orchestrator
│   └── static/
│       └── index.html              # Interactive Pandal Explorer Dashboard
├── tests/
│   ├── test_api.py                 # API endpoints test suite
│   └── test_crawlers.py            # Crawler, classification & deduplication tests
├── requirements.txt
└── README.md
```

---

## Installation & Setup

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.13)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
uvicorn app.main:app --reload --port 8000
```

The server starts at `http://localhost:8000`:
- **Web Dashboard**: `http://localhost:8000/`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## API Reference

### 1. List Pandals
`GET /pandals`

**Query Parameters:**
| Parameter | Type | Description |
|---|---|---|
| `popularity` | string | Filter by `"popular"` or `"unpopular"` |
| `district` | string | Filter by district (e.g. `"Kolkata"`, `"Nadia"`, `"Hooghly"`, `"North 24 Parganas"`, `"Birbhum"`, `"Darjeeling"`) |
| `zone` | string | Filter by zone: `"North"`, `"South"`, `"Central"`, `"East"`, `"Salt Lake"`, `"Behala"`, `"Howrah"`, `"North Bengal"`, etc. |
| `bonedi` | boolean | Filter by heritage ancestral estates (`true` / `false`) |
| `cross_referenced` | boolean | Filter for pandals verified across $\ge 2$ independent crawlers (`true` / `false`) |
| `search` | string | Full-text search across name, locality, nearest metro, description |
| `limit` | integer | Number of items per page (default: `50`, max: `500`) |
| `offset` | integer | Pagination offset (default: `0`) |

**Examples:**
```bash
# Get only unpopular / quiet neighborhood pandals
curl "http://localhost:8000/pandals?popularity=unpopular"

# Get pandals in Nadia district (e.g., Kalyani ITI More)
curl "http://localhost:8000/pandals?district=Nadia"

# Get multi-source verified popular pandals (corroborated by 2+ sources)
curl "http://localhost:8000/pandals?popularity=popular&cross_referenced=true"

# Get heritage Bonedi Baris across West Bengal
curl "http://localhost:8000/pandals?bonedi=true"

# Search for pandals near Sealdah
curl "http://localhost:8000/pandals?search=Sealdah"
```

**Response Format:**
```json
{
  "total": 217,
  "limit": 50,
  "offset": 0,
  "popular_count": 127,
  "unpopular_count": 90,
  "items": [
    {
      "id": 14,
      "name": "Sealdah Durga Bari (Railway Athletic Club)",
      "slug": "sealdah-durga-bari-railway-athletic-club",
      "popularity": "popular",
      "category": "bonedi_bari",
      "zone": "Central",
      "district": "Kolkata",
      "state": "West Bengal",
      "locality": "Sealdah / Baithakkhana",
      "nearest_metro": "Sealdah Metro",
      "latitude": 22.5675,
      "longitude": 88.3712,
      "bonedi": true,
      "popularity_score": 100.0,
      "source_count": 4,
      "cross_referenced": true,
      "sources": [
        "FestivalCatalogCrawler",
        "SocialMediaCrawler",
        "PortalGuideCrawler",
        "NeighborhoodCrawler"
      ],
      "description": "Historic celebration near Sealdah station highlighted on r/kolkata for drawing heavy crowds of commuters and heritage enthusiasts."
    }
  ]
}
```

---

### 2. Get Pandal by ID
`GET /pandals/{id}`
```bash
curl "http://localhost:8000/pandals/14"
```

---

### 3. Festival Statistics
`GET /stats`
```bash
curl "http://localhost:8000/stats"
```
**Response Format:**
```json
{
  "total_pandals": 217,
  "popular_pandals": 127,
  "unpopular_pandals": 90,
  "bonedi_pandals": 34,
  "cross_referenced_pandals": 20,
  "districts": {
    "Kolkata": 178,
    "Nadia": 5,
    "Hooghly": 4,
    "North 24 Parganas": 4,
    "Darjeeling": 4,
    "South 24 Parganas": 3,
    "Paschim Bardhaman": 3,
    "Birbhum": 3,
    "Purba Bardhaman": 2,
    "Paschim Medinipur": 2,
    "Murshidabad": 2,
    "Bankura": 2,
    "Purulia": 1,
    "Purba Medinipur": 1,
    "Malda": 1,
    "Jalpaiguri": 1,
    "Cooch Behar": 1
  },
  "top_popular": [
    "Kumartuli Park Sarbojanin Durgotsav",
    "Bagbazar Sarbojanin Durgotsav",
    "Santosh Mitra Square",
    "Ekdalia Evergreen Club",
    "Suruchi Sangha"
  ]
}
```

---

### 4. Trigger Crawler On-Demand
`POST /crawl`
Triggers an immediate background scrape across all sources.
```bash
curl -X POST "http://localhost:8000/crawl"
```

---

### 5. Check Crawler Status
`GET /crawl/status`
```bash
curl "http://localhost:8000/crawl/status"
```

---

## Running Automated Tests

Run the complete test suite with verbose output:
```bash
python -m pytest -v
```

The test suite validates:
- API endpoint status, filtering, and pagination.
- Classification algorithm (popular vs. unpopular vs. bonedi).
- Normalization, slug generation, and deduplication logic.
- Resilient crawling across all sources.

---

## Agentic Awesome Skills (AAS) Integration

This project integrates custom agentic skills powered by [`agentic-awesome-skills`](https://github.com/sickn33/agentic-awesome-skills) (v19.4.0) inside `.agents/skills/`:
- **`api-rate-limit-handler`**: Bounded exponential backoff with full jitter and `Retry-After` header adherence in crawler network operations.
- **`fastapi-pro`** & **`python-fastapi-development`**: High-performance async API patterns and SQLAlchemy 2.0 transaction lifecycle.
- **`python-pro`** & **`systematic-debugging`**: Production Python optimization and defect isolation.
- **`aas-discover`** & **`aas-compose-stack`**: AAS skill catalog discovery and stack management.

---

## License
MIT License.
#   p u j o - a t l a s - a p i  
 