import os

from sqlalchemy import create_engine, column, Integer, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import decl_base

#database_type#+#db_driver#://#user_name#: #password#@#host#: #port#/#db_name#
CONNECTION_STRING = f'postgresql+psycopgg2://yoana:{os.getenv('DB_PASSWORD')}@localhost::5432/sql_alchemy_lab'
engine = create_engine(CONNECTION_STRING)

Base = declarative_base()

class Worked(Base):
    __tablename__ = 'workers'
    id = column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=False, default='Mitko')
    last_name = Column(String(30), nullable=False, default='Mitkov')
    age = Column(Integer)
    salary = Column(Integer)

Base.metadata.create_all(engine) #this will migrate but no migration file, no going back