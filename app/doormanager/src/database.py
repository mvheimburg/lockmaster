"""Database module."""

from contextlib import contextmanager, AbstractContextManager
from typing import Callable
import logging
from os import environ, remove

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database, drop_database

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database():

    def __init__(self) -> None:

        dbusername = environ.get('POSTGRES_USER', None)
        dbpass = environ.get('POSTGRES_PASSWORD', None)
        dbname = environ.get('POSTGRES_DB', None)

        build_type = environ.get('BUILD_TYPE', None)    
        if build_type == 'release':
            dbserver = environ.get('POSTGRES_SERVER', None)
        else:
            dbserver = 'localhost'

        self.DATABASE_URI = 'postgresql://'+dbusername+':'+dbpass+'@'+dbserver+'/'+dbname

        self._engine = create_engine(self.DATABASE_URI, echo=True)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

        self.delete_db()
        self.create_database()

        print("databasefactory!")



    def create_database(self) -> None:
        if not database_exists(self.DATABASE_URI):
            create_database(self.DATABASE_URI)

        Base.metadata.create_all(self._engine)

    def delete_db(self) -> None:
        if database_exists(self.DATABASE_URI):
            drop_database(self.DATABASE_URI)

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