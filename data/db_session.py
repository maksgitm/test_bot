from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_name):
    global __factory

    if __factory:
        return

    if not db_name:
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'postgresql+psycopg2://postgres:1923@localhost:5432/{db_name}'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = create_engine(conn_str, echo=False)
    __factory = sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
