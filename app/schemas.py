from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict
import datetime

class PandalBase(BaseModel):
    name: str
    popularity: str = "unpopular"
    category: str = "traditional"
    zone: Optional[str] = None
    district: Optional[str] = "Kolkata"
    state: Optional[str] = "West Bengal"
    locality: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    nearest_metro: Optional[str] = None
    description: Optional[str] = None
    year_established: Optional[str] = None
    bonedi: bool = False
    source: str = "crawler"
    source_url: Optional[str] = None
    sources: Optional[str] = "[]"
    source_count: int = 1
    cross_referenced: bool = False
    popularity_score: float = 10.0

class PandalCreate(PandalBase):
    slug: Optional[str] = None

class PandalResponse(PandalBase):
    id: int
    slug: str
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    # Bengali soul — additive easters, populated per-request in routes.
    bengali_tip: Optional[str] = None
    sharodiya_note: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class PandalListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    popular_count: int
    unpopular_count: int
    items: List[PandalResponse]
    # Sharodiya easters on every list response.
    sharodiya_subhechha: str = "শারদীয়া শুভেচ্ছা! পুজো ভালো কাটুক।"
    easter: Optional[str] = None
    proverb: Optional[str] = None

class PandalStats(BaseModel):
    total_pandals: int
    popular_pandals: int
    unpopular_pandals: int
    bonedi_pandals: int
    cross_referenced_pandals: int = 0
    districts: Dict[str, int]
    zones: Dict[str, int]
    categories: Dict[str, int]
    top_popular: List[str]
    # Bengali greetings on stats.
    subhechha: str = "শারদীয়া শুভেচ্ছা! পুজো ভালো কাটুক।"
    proverb: str = "আসছে বছর আবার হবে!"
    easter_note: Optional[str] = "ঢাকে কাঠি পড়েছে — পুজো এসে গেছে!"

class CrawlTriggerResponse(BaseModel):
    message: str
    status: str
    crawl_id: Optional[int] = None
    bengali_message: str = "কুমোরটুলির আলো জ্বলে উঠেছে! Crawler cholche — চা খেয়ে আসুন ☕"
    subhechha: str = "শারদীয়া শুভেচ্ছা! পুজো ভালো কাটুক।"

class CrawlLogResponse(BaseModel):
    id: int
    status: str
    sources_crawled: str
    items_found: int
    items_added: int
    items_updated: int
    popular_count: int
    unpopular_count: int
    started_at: datetime.datetime
    completed_at: Optional[datetime.datetime] = None
    error_message: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
