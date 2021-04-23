# import os
# import sys
# from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from sqlalchemy import create_engine
# # import databases

# Base = declarative_base()

# class Person(Base):
#     __tablename__ = 'person'
#     # Here we define columns for the table person
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     name = Column(String(250), nullable=False)
#     access_level = Column(Integer)

# class BT_Address(Base):
#     __tablename__ = 'bt_address'
#     # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     address = Column(String(250))
#     person_id = Column(Integer, ForeignKey('person.id'))
#     person = relationship(Person)


# class PIN(Base):
#     __tablename__ = 'pin'
#     # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     number = Column(Integer)
#     person_id = Column(Integer, ForeignKey('person.id'))
#     person = relationship(Person)




# class DatabaseManager():
#     def __init__(self):
#                 ########## DB ###################
#         dbusername = os.environ.get('POSTGRES_USER', None)
#         dbpass = os.environ.get('POSTGRES_PASSWORD', None)
#         dbname = os.environ.get('POSTGRES_DB', None)

#         DATABASE_URI = 'postgresql://'+dbusername+':'+dbpass+'@'+'db'+'/'+dbname
#         self.engine = create_engine(DATABASE_URI, echo = True)
#         ################################

#         Base.metadata.create_all(self.engine)


#     def startup(self):
#         Session = sessionmaker(bind = self.engine)
#         self.session = Session()


# # https://python-dependency-injector.ets-labs.org/examples/fastapi-sqlalchemy.html
# # class Database:

# #     def __init__(self, db_url: str) -> None:
# #         self._engine = create_engine(db_url, echo=True)
# #         self._session_factory = orm.scoped_session(
# #             orm.sessionmaker(
# #                 autocommit=False,
# #                 autoflush=False,
# #                 bind=self._engine,
# #             ),
# #         )

# #     def create_database(self) -> None:
# #         Base.metadata.create_all(self._engine)

# #     @contextmanager
# #     def session(self) -> Callable[..., AbstractContextManager[Session]]:
# #         session: Session = self._session_factory()
# #         try:
# #             yield session
# #         except Exception:
# #             logger.exception('Session rollback because of exception')
# #             session.rollback()
# #             raise
# #         finally:
# #             session.close()