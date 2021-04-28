from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
engine = create_engine('sqlite:///./sql_app.db', echo=True, connect_args={"check_same_thread": False})
db_session = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)
Base = declarative_base()
Base.query = db_session.query_property()


        

def init_db():
    # Здесь нужно импортировать все модули, где могут быть определены модели,
    # которые необходимым образом могут зарегистрироваться в метаданных.
    # В противном случае их нужно будет импортировать до вызова init_db()
    Base.metadata.create_all(bind=engine)

def shutdown_session(exception=None):
    db_session.remove()
    