from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency that yields a database session and closes it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create all tables and auto-migrate any new columns if they don't exist."""
    import app.models  # ensure models are registered
    Base.metadata.create_all(bind=engine)

    # Auto-migration for SQLite to add newly introduced columns to existing tables
    with engine.connect() as conn:
        try:
            result = conn.exec_driver_sql("PRAGMA table_info(pandals)")
            existing_cols = {row[1] for row in result.fetchall()}
            
            migrations = [
                ("district", "ALTER TABLE pandals ADD COLUMN district VARCHAR(100) DEFAULT 'Kolkata'"),
                ("state", "ALTER TABLE pandals ADD COLUMN state VARCHAR(100) DEFAULT 'West Bengal'"),
                ("sources", "ALTER TABLE pandals ADD COLUMN sources TEXT DEFAULT '[]'"),
                ("source_count", "ALTER TABLE pandals ADD COLUMN source_count INTEGER DEFAULT 1"),
                ("cross_referenced", "ALTER TABLE pandals ADD COLUMN cross_referenced BOOLEAN DEFAULT 0")
            ]
            for col_name, sql in migrations:
                if col_name not in existing_cols:
                    conn.exec_driver_sql(sql)
            conn.commit()
        except Exception:
            pass
