import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime
from app.database import Base

def get_utc_now():
    return datetime.datetime.now(datetime.timezone.utc)

class Pandal(Base):
    __tablename__ = "pandals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    
    # "popular" vs "unpopular" (or "local")
    popularity = Column(String(50), nullable=False, default="unpopular", index=True)
    
    # "theme", "traditional", "bonedi_bari", "neighborhood_para"
    category = Column(String(100), default="traditional")
    
    # "North", "South", "Central", "East", "Salt Lake", "Howrah", "Behala", etc.
    zone = Column(String(100), nullable=True, index=True)
    
    # Geographic coverage across West Bengal
    district = Column(String(100), default="Kolkata", index=True)
    state = Column(String(100), default="West Bengal", index=True)
    
    locality = Column(String(150), nullable=True)
    address = Column(Text, nullable=True)
    
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    nearest_metro = Column(String(100), nullable=True)
    
    description = Column(Text, nullable=True)
    year_established = Column(String(50), nullable=True)
    bonedi = Column(Boolean, default=False, index=True)
    
    # Primary crawl source provenance and cross-referencing
    source = Column(String(100), default="crawler")
    source_url = Column(String(500), nullable=True)
    sources = Column(Text, default="[]")  # JSON list of all matching sources
    source_count = Column(Integer, default=1)
    cross_referenced = Column(Boolean, default=False, index=True)
    
    # Numeric popularity score from 0.0 to 100.0
    popularity_score = Column(Float, default=10.0)
    
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "popularity": self.popularity,
            "category": self.category,
            "zone": self.zone,
            "district": self.district,
            "state": self.state,
            "locality": self.locality,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "nearest_metro": self.nearest_metro,
            "description": self.description,
            "year_established": self.year_established,
            "bonedi": self.bonedi,
            "source": self.source,
            "source_url": self.source_url,
            "sources": self.sources,
            "source_count": self.source_count,
            "cross_referenced": self.cross_referenced,
            "popularity_score": self.popularity_score,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

class CrawlLog(Base):
    __tablename__ = "crawl_logs"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(50), default="running", index=True)  # running, success, failed
    sources_crawled = Column(Text, default="[]")
    items_found = Column(Integer, default=0)
    items_added = Column(Integer, default=0)
    items_updated = Column(Integer, default=0)
    popular_count = Column(Integer, default=0)
    unpopular_count = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, default=get_utc_now)
    completed_at = Column(DateTime, nullable=True)
