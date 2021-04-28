from database import Base 
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class CaptchaTable(Base):
    __tablename__ = 'captcha'
    captcha_uuid = Column(String, primary_key=True)
    font_size = Column(Integer, nullable=False)
    font_name = Column(String, nullable=False)
    text_id = Column(Integer, ForeignKey("Textcaptcha.id"))
    was_used = Column(Integer, nullable=False)
    text = relationship("Textcaptcha", back_populates="captchas")

    def __init__(self, captcha_uuid, font_size, font_name, captcha_id):
        self.captcha_uuid = captcha_uuid
        self.font_size = font_size
        self.font_name = font_name
        self.text_id = captcha_id
        self.was_used = 0

    def __repr__(self):
        return '<captcha %r>' % (self.captcha_text)
    

class TextCaptcha(Base):
    __tablename__ = 'captcha'
    id = Column(String, primary_key=True, index=True)
    captcha_text = Column(String, nullable=False)
    captcha_path = Column(String, nullable=False)
    description = Column(String)
    captchas = relationship("CapthaTable", back_populates="text")

    def __init__(self, captcha_text, captcha_path, description=None):
        self.captcha_text = captcha_text
        self.captcha_path = captcha_path
        if description is not None:
            self.description = description
            

    def __repr__(self):
        return '<captcha %r>' % (self.captcha_text)

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
    description = Column(String, nullable=False)
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