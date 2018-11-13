# coding:utf-8
import sqlite3
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, DateTime, \
    PickleType, Boolean, Date, BigInteger, ForeignKey, Text, event, func, DECIMAL, or_


class Database(object):

    def __init__(self, config=None):
        self.__config = config
        self.__engine= self.__create_engine
        self.__session_factory = sessionmaker(bind=self.__engine)
        self.__base_model = declarative_base()
        self.__db_session = scoped_session(self.__session_factory)

    @property
    def __create_engine(self):
        bind = self.__config.pop("bind", None)
        return create_engine(bind, **self.__config)

    @property
    def Model(self):
        return self.__base_model

    @property
    def session(self):
        return self.__db_session

    @property
    def engine(self):
        return self.__engine

    def create_all(self):
        self.Model.metadata.create_all(self.__engine)

    def drop_all(self):
        self.Model.metadata.drop_all(self.__engine)

BaseModel = declarative_base()

class SalaryEmail(BaseModel):
    __tablename__ = 'salary_email'

    id = Column(Integer, primary_key=True)
    field_name = Column(String(64), unique=True)
    field_value = Column(String(512))
    memo = Column(String(256))


def set_db():
    DB_ROOT = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(DB_ROOT, 'salary.db')

    config = {
        "bind": 'sqlite:///{}'.format(DB_PATH)
    }
    print(config['bind'])


    db = Database(config=config)
    return db


if __name__ == '__main__':
    db = set_db()
    # db.drop_all()
    # db.create_all()
    BaseModel.metadata.create_all(db.engine)