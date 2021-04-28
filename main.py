from io import BytesIO
import PIL

from starlette.responses import StreamingResponse
from captcha import get_last, init, run
from fastapi import FastAPI,Response
from fastapi.responses import FileResponse

app = FastAPI()

im = None
captcha_prop = None
font_prop = None

def init_captcha():
    _ = init()
    return {'result': _ }

@app.post("/captcha_show")
async def captcha():
    init()
    im, captcha_prop, font_prop = show_img()
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


@app.get("/generate")
def generate(data: str):
  img = run()
  print('img=%s' % (img.shape,))
  buf = BytesIO()
  PIL.imsave(buf, img, format='JPEG', quality=100)
  buf.seek(0) # important here!
  return StreamingResponse(buf, media_type="image/jpeg",
    headers={'Content-Disposition': 'inline; filename="%s.jpg"' %(data,)})

@app.get("/hello")
async def root():
    return {"message": "Hello World"}
