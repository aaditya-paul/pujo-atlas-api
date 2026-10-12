from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks, Response
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.database import get_db
from app.models import Pandal, CrawlLog
from app.schemas import (
    PandalResponse,
    PandalListResponse,
    PandalStats,
    CrawlTriggerResponse,
    CrawlLogResponse
)
from app.crawlers.manager import CrawlerManager
from app.easters import (
    get_easter_for_search,
    get_subhechha_now,
    get_random_proverb,
    get_pujo_tip,
    get_district_greeting,
    get_header_subhechha,
    get_header_proverb,
    to_ascii_header,
)

router = APIRouter(tags=["Pandals & Crawler"])
crawler_manager = CrawlerManager()

@router.get("/pandals", response_model=PandalListResponse, summary="List and filter all Durga Puja pandals across West Bengal")
def list_pandals(
    response: Response,
    popularity: Optional[str] = Query(None, description="Filter by 'popular' or 'unpopular'"),
    district: Optional[str] = Query(None, description="Filter by district across West Bengal (e.g. 'Kolkata', 'Nadia', 'Hooghly', 'North 24 Parganas', 'Darjeeling', 'Bankura', 'Birbhum')"),
    zone: Optional[str] = Query(None, description="Filter by zone (e.g. 'North', 'South', 'Central', 'North Bengal', 'South Bengal', 'Rarh Bengal')"),
    bonedi: Optional[bool] = Query(None, description="Filter by traditional aristocratic family pujas (true/false)"),
    cross_referenced: Optional[bool] = Query(None, description="Filter pandals verified by 2+ distinct sources (true/false)"),
    search: Optional[str] = Query(None, description="Search term matching pandal name, locality, district, or metro — psst, try 'dhaak', 'kashful', 'bijoya'"),
    limit: int = Query(50, ge=1, le=500, description="Pagination limit"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all Durga Puja pandals across West Bengal with rich filtering capabilities.
    Supports distinguishing between popular mega-crowd pullers and
    unpopular / quiet neighborhood ('para') pandals, with multi-source cross-referencing.
    """
    query = db.query(Pandal)

    if popularity:
        query = query.filter(func.lower(Pandal.popularity) == popularity.lower())

    if district:
        query = query.filter(func.lower(Pandal.district) == district.lower())

    if zone:
        query = query.filter(func.lower(Pandal.zone) == zone.lower())

    if bonedi is not None:
        query = query.filter(Pandal.bonedi == bonedi)

    if cross_referenced is not None:
        query = query.filter(Pandal.cross_referenced == cross_referenced)

    if search:
        search_pattern = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Pandal.name.ilike(search_pattern),
                Pandal.locality.ilike(search_pattern),
                Pandal.district.ilike(search_pattern),
                Pandal.nearest_metro.ilike(search_pattern),
                Pandal.description.ilike(search_pattern)
            )
        )

    total = query.count()
    items = query.order_by(Pandal.popularity_score.desc(), Pandal.name.asc()).offset(offset).limit(limit).all()

    popular_count = sum(1 for p in items if p.popularity == "popular")
    unpopular_count = sum(1 for p in items if p.popularity == "unpopular")

    # ---- Bengali easters (additive, never breaking) ----
    subhechha = get_subhechha_now()
    easter = get_easter_for_search(search)
    district_note = get_district_greeting(district)
    # District greeting takes precedence only when no search easter hit.
    if not easter and district_note:
        easter = district_note
    proverb = get_random_proverb()

    # Per-pandal Bengali tips — attached dynamically for Pydantic from_attributes.
    for p in items:
        try:
            p.bengali_tip = get_pujo_tip(
                popularity=getattr(p, "popularity", ""),
                category=getattr(p, "category", ""),
                bonedi=bool(getattr(p, "bonedi", False)),
                district=getattr(p, "district", ""),
            )
            p.sharodiya_note = subhechha
        except Exception:
            pass

    # Easter headers for curl / API explorers (ASCII-safe; full Bengali in body).
    response.headers["X-Sharodiya-Subhechha"] = get_header_subhechha()
    response.headers["X-Pujo-Proverb"] = get_header_proverb()
    if easter:
        response.headers["X-Pujo-Easter"] = to_ascii_header(easter)

    return PandalListResponse(
        total=total,
        limit=limit,
        offset=offset,
        popular_count=popular_count,
        unpopular_count=unpopular_count,
        items=items,
        sharodiya_subhechha=subhechha,
        easter=easter,
        proverb=proverb,
    )

@router.get("/pandals/{pandal_id}", response_model=PandalResponse, summary="Get pandal details by ID")
def get_pandal(pandal_id: int, response: Response, db: Session = Depends(get_db)):
    """Retrieve detailed information about a single Durga Puja pandal — with a Bengali tip."""
    pandal = db.query(Pandal).filter(Pandal.id == pandal_id).first()
    if not pandal:
        raise HTTPException(status_code=404, detail=f"Pandal with ID {pandal_id} not found — ধুর, কিছু পাওয়া গেল না!")
    subhechha = get_subhechha_now()
    try:
        pandal.bengali_tip = get_pujo_tip(
            popularity=getattr(pandal, "popularity", ""),
            category=getattr(pandal, "category", ""),
            bonedi=bool(getattr(pandal, "bonedi", False)),
            district=getattr(pandal, "district", ""),
        )
        pandal.sharodiya_note = subhechha
    except Exception:
        pass
    response.headers["X-Sharodiya-Subhechha"] = get_header_subhechha()
    response.headers["X-Pujo-Proverb"] = get_header_proverb()
    return pandal

@router.get("/stats", response_model=PandalStats, summary="Aggregated festival statistics across West Bengal")
def get_stats(response: Response, db: Session = Depends(get_db)):
    """
    Retrieve comprehensive statistical metrics on popular vs. unpopular
    pandals, districts, zones distribution, and top popular pandals.
    """
    total = db.query(Pandal).count()
    popular_count = db.query(Pandal).filter(Pandal.popularity == "popular").count()
    unpopular_count = db.query(Pandal).filter(Pandal.popularity == "unpopular").count()
    bonedi_count = db.query(Pandal).filter(Pandal.bonedi == True).count()
    cross_count = db.query(Pandal).filter(Pandal.cross_referenced == True).count()

    # District distribution
    district_rows = db.query(Pandal.district, func.count(Pandal.id)).group_by(Pandal.district).all()
    districts = {dist or "Kolkata": count for dist, count in district_rows}

    # Zone distribution
    zone_rows = db.query(Pandal.zone, func.count(Pandal.id)).group_by(Pandal.zone).all()
    zones = {zone or "Unspecified": count for zone, count in zone_rows}

    # Category distribution
    cat_rows = db.query(Pandal.category, func.count(Pandal.id)).group_by(Pandal.category).all()
    categories = {cat or "other": count for cat, count in cat_rows}

    # Top popular pandals
    top_rows = db.query(Pandal.name).filter(Pandal.popularity == "popular").order_by(Pandal.popularity_score.desc()).limit(10).all()
    top_popular = [row[0] for row in top_rows]

    subhechha = get_subhechha_now()
    proverb = get_random_proverb()
    easter_note = "ঢাকে কাঠি পড়েছে — পুজো এসে গেছে! বলো দুগ্গা মাঈ কী — জয়!"

    response.headers["X-Sharodiya-Subhechha"] = get_header_subhechha()
    response.headers["X-Pujo-Proverb"] = get_header_proverb()

    return PandalStats(
        total_pandals=total,
        popular_pandals=popular_count,
        unpopular_pandals=unpopular_count,
        bonedi_pandals=bonedi_count,
        cross_referenced_pandals=cross_count,
        districts=districts,
        zones=zones,
        categories=categories,
        top_popular=top_popular,
        subhechha=subhechha,
        proverb=proverb,
        easter_note=easter_note,
    )

@router.post("/crawl", response_model=CrawlTriggerResponse, summary="Trigger crawler on-demand")
def trigger_crawl(background_tasks: BackgroundTasks, response: Response, db: Session = Depends(get_db)):
    """
    Manually trigger the web crawler to fetch, classify, and update
    pandals from Wikipedia, Social Media, Open Catalogs, and Neighborhood registries.
    Runs asynchronously in the background.
    """
    # Create initial running record
    crawl_log = CrawlLog(status="queued")
    db.add(crawl_log)
    db.commit()
    db.refresh(crawl_log)

    # Launch task in background
    background_tasks.add_task(crawler_manager.run_all)

    subhechha = get_subhechha_now()
    bengali_message = "কুমোরটুলির আলো জ্বলে উঠেছে! Crawler cholche — চা খেয়ে আসুন ☕"
    response.headers["X-Sharodiya-Subhechha"] = get_header_subhechha()

    return CrawlTriggerResponse(
        message="Web crawler launched in background across all configured sources. কুমোরটুলির আলো জ্বলে উঠেছে!",
        status="running",
        crawl_id=crawl_log.id,
        bengali_message=bengali_message,
        subhechha=subhechha,
    )

@router.get("/crawl/status", response_model=Optional[CrawlLogResponse], summary="Get latest crawl execution status")
def get_crawl_status(db: Session = Depends(get_db)):
    """Retrieve details and metrics of the latest web crawler execution."""
    latest = db.query(CrawlLog).order_by(CrawlLog.id.desc()).first()
    return latest
