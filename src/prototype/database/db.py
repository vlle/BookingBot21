import nntplib
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///sqlite3.db', echo=True)
Base = declarative_base()


class Object(Base):
    __tablename__ = "Object"
    id = Column(Integer, primary_key=True)  # id object
    type = Column(String)  # type
    name = Column(String)  # uniq name
    campus = Column(String)  # campus name
    floor = Column(Integer)  # floor number
    access = Column(Integer)  # access number


class Booking(Base):
    __tablename__ = "Booking"

    id = Column(Integer, primary_key=True)  # book id
    owner_id = Column(Integer)  # id author
    id_obj = Column(Integer)  # id object
    title = Column(String)  # description(not necessary)
    start_time = Column(String)  # start time
    end_time = Column(String)    # end time
    date = Column(String)  # date


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)  # user id
    tg_id = Column(Integer)  # telegram id
    login = Column(String)  # login
    role = Column(Integer)  # role


engine.connect()
print(engine)

Base.metadata.create_all(engine)
