from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import scoped_session, sessionmaker
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True, connect_args={"check_same_thread": False})
db_session = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)
Base = declarative_base()
Base.query = db_session.query_property()


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    captcha_uuid = Column(String, primary_key=True)
    font_size = Column(Integer, nullable=False)
    font_name = Column(String, nullable=False)
    captcha_text = Column(String, nullable=False)
    captcha_path = Column(String, nullable=False)

class CaptchaTable(Base):
    __tablename__ = 'captcha'
    captcha_uuid = Column(String, primary_key=True)
    font_size = Column(Integer, nullable=False)
    font_name = Column(String, nullable=False)
    captcha_text = Column(String, nullable=False)
    captcha_path = Column(String, nullable=False)


    def __init__(self, captcha_uuid, font_size, font_name, captcha_text, captcha_path):
        self.captcha_uuid = captcha_uuid
        self.font_size = font_size
        self.font_name = font_name
        self.captcha_text = captcha_text
        self.captcha_path = captcha_path

    def __repr__(self):
        return '<CAptcha %r>' % (self.captcha_text)

class CaptchaInit(Base):
    __tablename__ = 'captcha_init'
    config_id = Column(Integer, primary_key=True)
    offset = Column(Integer, nullable=False)
    x_offset = Column(Integer, nullable=False)
    y_offset = Column(Integer, nullable=False)
    v_back0 = Column(Integer, nullable=False)
    s_back0 = Column(Integer, nullable=False)
    s_back1 = Column(Integer, nullable=False)
    v_back1 = Column(Integer, nullable=False)
    v_font0 = Column(Integer, nullable=False)
    v_font1 = Column(Integer, nullable=False)
    s_font0 = Column(Integer, nullable=False)
    s_font1 = Column(Integer, nullable=False)
    font_min = Column(Integer, nullable=False)
    font_max = Column(Integer, nullable=False)
    im_w = Column(Integer, nullable=False)
    im_h = Column(Integer, nullable=False)
    fonts_dir = Column(String, nullable=False)
    captcha_texts = Column(String)
    captcha_file_path = Column(String)
    
    def __init__(self, offsets, hsv, image_size, fonts_dir, captcha_texts, captcha_file_path, font_size_limit):

        self.offset = offsets['offset']
        self.x_offset = offsets['x_offset']
        self.y_offset = offsets['y_offset']
        self.v_back0 = hsv['v_back'][0]
        self.s_back0 = hsv['s_back'][0]
        self.v_back1 = hsv['v_back'][1]
        self.s_back1 = hsv['s_back'][1]
        self.v_font0 = hsv['v_font'][0]
        self.v_font1 = hsv['v_font'][1]
        self.s_font0 = hsv['s_font'][0]
        self.s_font1 = hsv['s_font'][1]
        self.font_min = font_size_limit[0]
        self.font_max = font_size_limit[1]
        self.im_w = image_size[1]
        self.im_h = image_size[0]
        self.fonts_dir = fonts_dir
        self.captcha_texts = captcha_texts
        self.captcha_file_path = captcha_file_path
        

def init_db():
    # Здесь нужно импортировать все модули, где могут быть определены модели,
    # которые необходимым образом могут зарегистрироваться в метаданных.
    # В противном случае их нужно будет импортировать до вызова init_db()
    Base.metadata.create_all(bind=engine)

def shutdown_session(exception=None):
    db_session.remove()
    