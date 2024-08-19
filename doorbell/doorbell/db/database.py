"""Database module."""

from contextlib import contextmanager, AbstractContextManager
from typing import Generator, Any
import logging
from os import environ, remove

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database, drop_database

from doorbell.config.db import DBSettings

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database():

    def __init__(self, settings: DBSettings = DBSettings()) -> None:

        self._settings = settings

        self._engine = create_engine(self._settings.URI, echo=True)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )
        # self.delete_db()
        self.create_database()

        print("databasefactory!")

    def create_database(self) -> None:
        if not database_exists(self._settings.URI):
            create_database(self._settings.URI)

        Base.metadata.create_all(self._engine)

    def delete_db(self) -> None:
        if database_exists(self._settings.URI):
            drop_database(self._settings.URI)

    @contextmanager
    def session(self) -> Generator[Session, Any, Any]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception('Session rollback because of exception')
            session.rollback()
            raise
        finally:
            session.close()