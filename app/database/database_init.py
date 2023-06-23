import os
import re

from app.helpers import (
    load_yaml_file,
    start_logger,
)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuration file reading
config = load_yaml_file(
    file_path=os.path.realpath("app/configuration/config.yaml"),
)

# set logging
logger = start_logger(config)
logger.info(msg="Database initialisation!")


ALGORITHM = config.get("algorithm")
environment = config.get("log").get("environment")

SQLALCHEMY_DATABASE_URL = config["database_connection_string"]

# extract the password part to mask it
# matches after // until @
# res = [(username, password)]
# so one matching tuple
# and we want the second element
DATABASE_PASSWORD = re.findall(
    r"\/\/(.*):(.*)@",
    SQLALCHEMY_DATABASE_URL
)[0][1]

# we log the url but we hide the password
logger.info(
    msg=f"SQLALCHEMY_DATABASE_URL : "
    f"{SQLALCHEMY_DATABASE_URL.replace(DATABASE_PASSWORD,'****')}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
