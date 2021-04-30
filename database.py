from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import desc




# engine = create_engine('sqlite:///./sql_app.db', echo=True, connect_args={"check_same_thread": False})
engine = create_engine('sqlite:///./sql_app.db', echo=True)
db_session = sessionmaker(bind=engine)
Base = declarative_base()
# Base.query = db_session.query_property()



class CaptchaTable(Base):
    __tablename__ = 'CaptchaTable'
    captcha_uuid = Column(String, primary_key=True)
    font_size = Column(Integer, nullable=False)
    font_name = Column(String, nullable=False)
    text_id = Column(Integer, ForeignKey("TextCaptcha.id"))
    was_used = Column(Integer, nullable=False)
    text = relationship("TextCaptcha", back_populates="captchas")

    def __init__(self, captcha_uuid, font_size, font_name, captcha_id):
        self.captcha_uuid = captcha_uuid
        self.font_size = font_size
        self.font_name = font_name
        self.text_id = captcha_id
        self.was_used = 0

    def __repr__(self):
        return '<captcha %r>' % (self.captcha_text)
    

class TextCaptcha(Base):
    __tablename__ = 'TextCaptcha'
    id = Column(String, primary_key=True, index=True)
    captcha_text = Column(String, nullable=False)
    captcha_path = Column(String, nullable=False)
    description = Column(String)
    captchas = relationship("CaptchaTable", back_populates="text")

    def __init__(self, captcha_text, captcha_path, description=None):
        self.captcha_text = captcha_text
        self.captcha_path = captcha_path
        if description is not None:
            self.description = description
            

    def __repr__(self):
        return '<captcha %r>' % (self.captcha_text)

class CaptchaInit(Base):
    __tablename__ = 'CaptchaInit'
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
    description = Column(String, nullable=False)
    captcha_texts = Column(String)
    captcha_file_path = Column(String)
    
    def __init__(self, offsets, hsv, image_size, fonts_dir, captcha_texts, captcha_file_path, font_size_limit):
        if type(offsets) == dict:   
            for i,j in offsets.items():
                print(i,j)
        if type(hsv) == str:   
            for i in offsets:
                print(i,j)
        
        x = int(offsets['offset'])
        
        self.offset = x
        self.offset = 100 #int(offsets['offset'])
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
    
    
    
def get_captcha(db: Session, id: int):
    return db.query(CaptchaTable).filter(CaptchaTable.captcha_uuid == id).first()


def get_text(db: Session, id: int):
    return db.query(TextCaptcha).filter(TextCaptcha.id == id).first()


def get_config(db: Session, id: int):
    return db.query(CaptchaInit).filter(CaptchaInit.id == id).first()
    

def get_config_last(db: Session):
    return db.query(CaptchaInit).order_by(desc(CaptchaInit.id)).first()
    

def get_config_by_name(db: Session, description: str):
    return db.query(CaptchaInit).filter(CaptchaInit.description == description).first()
    


def get_texts(db: Session):
    return db.query(TextCaptcha).all()


def get_random_not_used(db: Session, captcha_id: int):
    return db.query(CaptchaTable).filter(CaptchaTable.text_id == captcha_id).filter(CaptchaTable.was_used == 0).first()


def get_captchas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CaptchaTable).offset(skip).limit(limit).all()


def create_config(db: Session, offsets, hsv, image_size, fonts_dir, captcha_texts, captcha_file_path, font_size_limit):
    ini = CaptchaInit(offsets, hsv, image_size, fonts_dir, captcha_texts, captcha_file_path, font_size_limit)
    print(offsets)
    db.add(ini)
    db.commit()
    db.refresh(ini)
    return ini


def create_captcha_text(db: Session,  text: str, path: str ):
    db_text = TextCaptcha(text, path)
    db.add(db_text)
    db.commit()
    db.refresh(db_text)
    return db_text


def create_captcha(db: Session,   captcha_uuid, font_size, font_name, captcha_id: int):
    db_captcha = CaptchaTable(captcha_uuid=captcha_uuid, font_size=font_size, font_name=font_name, captcha_id=captcha_id)
    db.add(db_captcha)
    db.commit()
    db.refresh(db_captcha)
    return db_captcha
