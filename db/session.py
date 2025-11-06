from sqlmodel import Session, SQLModel, create_engine

from .engine import engine


def get_session() -> Session:
    with Session(engine) as session:
        yield session
