import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import DPredictORM
from app.database.database_init import config, get_db
from app.helpers import start_logger
from app.main import app

logger = start_logger(config)
logger.info(msg="Database initialisation!")

connection_string = "postgresql://root:password@pg_test:5433/database2"

engine = create_engine(connection_string)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

DPredictORM.Base.metadata.drop_all(bind=engine)
DPredictORM.Base.metadata.create_all(bind=engine)
logger.info(msg="Create unit tests reference database")


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
