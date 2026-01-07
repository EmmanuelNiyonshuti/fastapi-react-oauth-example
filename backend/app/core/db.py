from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine

from .config import settings

engine = create_engine(str(settings.DATABASE_URL))

metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column("uid", Integer, primary_key=True),
    Column("username", String, nullable=True),
    Column("email", String, unique=True, nullable=False),
    Column("password_hash", String, nullable=True),
)
