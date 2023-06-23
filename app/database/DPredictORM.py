from sqlalchemy import (
    Column,
    DateTime,
    Float,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import (
    BOOLEAN,
    INTEGER,
)

from app.database.database_init import Base

metadata = Base.metadata


class ApiUser(Base):
    __tablename__ = 'api_users'

    id_user = Column(INTEGER, autoincrement=True, primary_key=True)
    login = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    registered_on = Column(DateTime, nullable=True, server_default=text("CURRENT_TIMESTAMP"))
    admin = Column(BOOLEAN, nullable=False, server_default=text("'0'"))

class Products(Base):
    __tablename__ = 'products'

    activity_date = Column(DateTime, nullable=False, index=False, primary_key=True)
    product = Column(INTEGER, nullable=False, index=False, primary_key=True)
    price = Column(Float, nullable=False, index=False, primary_key=True)