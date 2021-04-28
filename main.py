import captcha
from starlette.responses import StreamingResponse
from captcha import get_last, init, run
from fastapi import FastAPI,Response
from fastapi.responses import FileResponse

if captcha.use_db:
    from typing import List

    from fastapi import Depends, FastAPI, HTTPException
    from sqlalchemy.orm import Session

    from . import crud, models, schemas
    from .database import SessionLocal, engine

app = FastAPI()

if captcha.use_db:
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

im = None
captcha_prop = None
font_prop = None

fonts_dir="cyr_fonts"

captcha_file_path = None
image_size = (1000,1000)
font_size_limit = (70, 100)
offsets={'offset':100, 'x_offset':100, 'y_offset':500}
hsv = {'s_back': (0.1, 0.3),
        'v_back': (0.1, 0.3),
        's_font': (0.65, 0.9),
        'v_font': (0.65, 0.9)
        }


@app.post("/init")
def init_captcha(fonts_dir='cyr_fonts', use_db=False, captcha_texts='Глупый пингвин робко прячет пузо жирное в утесах', captcha_file_path=None, font_size_limit=font_size_limit, offsets=offsets, hsv=hsv, image_size=image_size):
    '''
    Args:
        fonts_dir (str, optional): папка со шрифтами. Defaults to 'cyr_fonts'.
        font_min (int, optional): минимальный размер шрифта. Defaults to 70.
        font_max (int, optional): максимальный размер шрифта. Defaults to 100.
        fonts ([type], optional): список имен(относительных путей к) шрифтов. Defaults to fonts.
        captcha_texts ([type], optional): большая простыня текста, из которой выбирается случайно номер слова, которое затем идет в капчагенератор. Defaults to songs.
        s_back ([type], optional): сатурация фона из модели картинок hsv, значение - словарь от и до. Defaults to s_back.
        v_back ([type], optional): яркость фона из модели картинок hsv, значение - словарь от и до. Defaults to v_back.
        s_font ([type], optional): сатурация шрифта из модели картинок hsv, значение - словарь от и до. Defaults to s_font.
        v_font ([type], optional): яркость шрифта из модели картинок hsv, значение - словарь от и до. Defaults to v_font.
        im_w ([type], optional): ширина шрифта. Defaults to im_w.
        im_h ([type], optional): высота шрифта. Defaults to im_h.
    ''' 
    _ = init()
    return {'result': _ }

@app.post("/captcha_show")
async def captcha():
    init()
    im, captcha_prop, font_prop = captcha.show_img()
    print(captcha_prop, font_prop)
    return FileResponse("image1.png")

@app.post("/captcha")
async def captcha():
    init()
    im, captcha_prop, font_prop = run()

    return FileResponse("image1.png")

@app.post("/captcha_prop")
async def captcha():
    # init()
    # im, captcha_prop, font_prop = run()
    captcha_prop, font_prop, im = get_last()
    return {'propertis captcha': [*captcha_prop], 'propertis fonts': [*font_prop] }



@app.get("/hello")
async def root():
    return {"message": "Hello World"}
