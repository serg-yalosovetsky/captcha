from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import desc

from . import models


def get_captcha(db: Session, id: int):
    return db.query(models.CaptchaTable).filter(models.CaptchaTable.captcha_uuid == id).first()


def get_text(db: Session, id: int):
    return db.query(models.TextCaptcha).filter(models.TextCaptcha.id == id).first()


def get_config(db: Session, id: int):
    return db.query(models.CaptchaInit).filter(models.CaptchaInit.id == id).first()
    

def get_config_last(db: Session):
    return db.query(models.CaptchaInit).order_by(desc(models.CaptchaInit.id)).first()
    

def get_config_by_name(db: Session, description: str):
    return db.query(models.CaptchaInit).filter(models.CaptchaInit.description == description).first()
    


def get_texts(db: Session):
    return db.query(models.TextCaptcha).all()


def get_random_not_used(db: Session, captcha_id: int):
    return db.query(models.User).filter(models.CaptchaTable.text_id == captcha_id).filter(models.CaptchaTable.was_used == 0).first()


def get_captchas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CaptchaTable).offset(skip).limit(limit).all()


def create_config(db: Session, offsets, hsv, image_size, fonts_dir, captcha_texts, captcha_file_path, font_size_limit):
    ini = models.CaptchaInit(offsets, hsv, image_size, fonts_dir, captcha_texts, captcha_file_path, font_size_limit)
    
    db.add(ini)
    db.commit()
    db.refresh(ini)
    return ini


def create_captcha_text(db: Session,  text: str, path: str ):
    db_text = models.TextCaptcha(text, path)
    db.add(db_text)
    db.commit()
    db.refresh(db_text)
    return db_text


def create_captcha(db: Session,   captcha_uuid, font_size, font_name, captcha_id: int):
    db_captcha = models.CaptchaTable(captcha_uuid=captcha_uuid, font_size=font_size, font_name=font_name, captcha_id=captcha_id)
    db.add(db_captcha)
    db.commit()
    db.refresh(db_captcha)
    return db_captcha