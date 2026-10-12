import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import Pandal, CrawlLog
from app.crawlers import manager as crawler_manager_module

# Shared in-memory test SQLite DB using StaticPool
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
crawler_manager_module.SessionLocal = TestingSessionLocal

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    # Insert sample seed data
    p1 = Pandal(
        name="Bagbazar Sarbojanin Durgotsav",
        slug="bagbazar-sarbojanin-durgotsav",
        popularity="popular",
        category="traditional",
        zone="North",
        district="Kolkata",
        locality="Bagbazar",
        nearest_metro="Shyambazar",
        latitude=22.6044,
        longitude=88.3656,
        description="Historic sabeki puja",
        bonedi=False,
        source_count=3,
        cross_referenced=True,
        popularity_score=95.0
    )
    p2 = Pandal(
        name="Hatkhola Gosaipara Sarbojonin",
        slug="hatkhola-gosaipara-sarbojonin",
        popularity="unpopular",
        category="neighborhood_para",
        zone="North",
        district="Kolkata",
        locality="Hatkhola",
        nearest_metro="Sovabazar",
        latitude=22.5991,
        longitude=88.3593,
        description="Quiet local lane celebration",
        bonedi=False,
        source_count=1,
        cross_referenced=False,
        popularity_score=22.0
    )
    p3 = Pandal(
        name="Sovabazar Rajbari Durga Puja",
        slug="sovabazar-rajbari-durga-puja",
        popularity="popular",
        category="bonedi_bari",
        zone="North",
        district="Kolkata",
        locality="Sovabazar",
        nearest_metro="Sovabazar Sutanuti",
        latitude=22.5962,
        longitude=88.3674,
        description="Aristocratic household celebration founded in 1757",
        bonedi=True,
        source_count=2,
        cross_referenced=True,
        popularity_score=88.0
    )
    p4 = Pandal(
        name="Suruchi Sangha",
        slug="suruchi-sangha",
        popularity="popular",
        category="theme",
        zone="South",
        district="Kolkata",
        locality="New Alipore",
        nearest_metro="Majerhat",
        latitude=22.5152,
        longitude=88.3248,
        description="Folk art and cultural themes",
        bonedi=False,
        source_count=2,
        cross_referenced=True,
        popularity_score=96.0
    )
    p5 = Pandal(
        name="Kalyani ITI More (Luminous Club)",
        slug="kalyani-iti-more-luminous-club",
        popularity="popular",
        category="theme",
        zone="South Bengal",
        district="Nadia",
        locality="ITI More, Kalyani",
        nearest_metro=None,
        latitude=22.9751,
        longitude=88.4344,
        description="Massive mega theme in Nadia district",
        bonedi=False,
        source_count=3,
        cross_referenced=True,
        popularity_score=99.0
    )
    db.add_all([p1, p2, p3, p4, p5])
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_list_all_pandals(client):
    response = client.get("/pandals")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["items"]) == 5

def test_filter_by_popularity(client):
    # Filter popular
    resp_pop = client.get("/pandals?popularity=popular")
    assert resp_pop.status_code == 200
    data_pop = resp_pop.json()
    assert data_pop["total"] == 4
    for item in data_pop["items"]:
        assert item["popularity"] == "popular"

    # Filter unpopular
    resp_unpop = client.get("/pandals?popularity=unpopular")
    assert resp_unpop.status_code == 200
    data_unpop = resp_unpop.json()
    assert data_unpop["total"] == 1
    assert data_unpop["items"][0]["name"] == "Hatkhola Gosaipara Sarbojonin"

def test_filter_by_district(client):
    resp = client.get("/pandals?district=Nadia")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert "Kalyani ITI More" in data["items"][0]["name"]

def test_filter_by_cross_referenced(client):
    resp = client.get("/pandals?cross_referenced=true")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 4
    for item in data["items"]:
        assert item["cross_referenced"] is True

def test_filter_by_zone(client):
    resp = client.get("/pandals?zone=South")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["name"] == "Suruchi Sangha"

def test_filter_by_bonedi(client):
    resp = client.get("/pandals?bonedi=true")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["name"] == "Sovabazar Rajbari Durga Puja"

def test_search_filter(client):
    resp = client.get("/pandals?search=Shyambazar")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert "Bagbazar" in data["items"][0]["name"]

def test_get_pandal_by_id(client):
    resp = client.get("/pandals/1")
    assert resp.status_code == 200
    assert resp.json()["id"] == 1

def test_get_pandal_not_found(client):
    resp = client.get("/pandals/9999")
    assert resp.status_code == 404

def test_stats_endpoint(client):
    resp = client.get("/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_pandals"] == 5
    assert data["popular_pandals"] == 4
    assert data["unpopular_pandals"] == 1
    assert data["bonedi_pandals"] == 1
    assert data["cross_referenced_pandals"] == 4
    assert "Kolkata" in data["districts"]
    assert "Nadia" in data["districts"]
    assert "North" in data["zones"]

def test_trigger_crawl(client):
    resp = client.post("/crawl")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data
    assert data["status"] == "running"
