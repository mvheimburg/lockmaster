"""Database module."""

from contextlib import contextmanager, AbstractContextManager
from typing import Callable
import logging
from os import environ

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database():

    def __init__(self) -> None:

        dbusername = environ.get('POSTGRES_USER', None)
        dbpass = environ.get('POSTGRES_PASSWORD', None)
        dbname = environ.get('POSTGRES_DB', None)

        DATABASE_URI = 'postgresql://'+dbusername+':'+dbpass+'@'+'db'+'/'+dbname

        self._engine = create_engine(DATABASE_URI, echo=True)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)


    @contextmanager
    # def session(self) -> Callable[..., AbstractContextManager[Session]]:
    def session(self) -> Callable:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception('Session rollback because of exception')
            session.rollback()
            raise
        finally:
            session.close()