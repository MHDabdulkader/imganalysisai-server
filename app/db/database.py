from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config.settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

sessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
# Base.metadata.create_all(bind=engine)
Base = declarative_base()


def get_db():
    db = sessionLocal()
    print(" ============= db ================", db)
    try:
        yield db
    finally:
        db.close()
