from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from .models import Shipment

engine =create_engine(
    url="sqlite:///sqlite.db",
    echo=True,
    connect_args={"check_same_thread": False},
)
def create_db_tables():
    SQLModel.metadata.create_all(bind=engine)

session = Session(bind=engine)
session.get(
    Shipment, 1
)
session.add(
    Shipment()
)
session
