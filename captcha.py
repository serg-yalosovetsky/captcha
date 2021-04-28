
import uuid
import PIL
import os, math
from PIL import Image
from PIL import ImageFont, ImageDraw, ImageOps, ImageColor
from numpy import pi, random, sin, cos

fonts = []
captcha_file_path = None
image_size = (1000,1000)
font_size_limit = (70, 70)
offsets={'offset':100, 'x_offset':100, 'y_offset':500}
hsv = {'s_back': (0.1, 0.3),
        'v_back': (0.1, 0.3),
        's_font': (0.65, 0.9),
        'v_font': (0.65, 0.9)
        }

captcha_texts = '''Над седой равниной моря ветер тучи собирает. Между тучами и морем гордо реет Буревестник, черной молнии подобный.
То крылом волны касаясь, то стрелой взмывая к тучам, он кричит, и — тучи слышат радость в смелом крике птицы.
В этом крике — жажда бури! Силу гнева, пламя страсти и уверенность в победе слышат тучи в этом крике.
Чайки стонут перед бурей, — стонут, мечутся над морем и на дно его готовы спрятать ужас свой пред бурей.
И гагары тоже стонут, — им, гагарам, недоступно наслажденье битвой жизни: гром ударов их пугает.
Глупый пингвин робко прячет тело жирное в утесах… Только гордый Буревестник реет смело и свободно над седым от пены морем!
Все мрачней и ниже тучи опускаются над морем, и поют, и рвутся волны к высоте навстречу грому.
Гром грохочет. В пене гнева стонут волны, с ветром споря. Вот охватывает ветер стаи волн объятьем крепким и бросает их с размаху в дикой злобе на утесы, разбивая в пыль и брызги изумрудные громады.
Буревестник с криком реет, черной молнии подобный, как стрела пронзает тучи, пену волн крылом срывает.
Вот он носится, как демон, — гордый, черный демон бури, — и смеется, и рыдает… Он над тучами смеется, он от радости рыдает!
В гневе грома, — чуткий демон, — он давно усталость слышит, он уверен, что не скроют тучи солнца, — нет, не скроют!
Ветер воет… Гром грохочет…
Синим пламенем пылают стаи туч над бездной моря. Море ловит стрелы молний и в своей пучине гасит. Точно огненные змеи, вьются в море, исчезая, отраженья этих молний!
— Буря! Скоро грянет буря!
Это смелый Буревестник гордо реет между молний над ревущим гневно морем; то кричит пророк победы:
— Пусть сильнее грянет буря!..'''

def some_text(songs):
    songs = songs.replace("\n", " ")
    songs = songs.replace("— ", "—")
    texts = songs.split(" ")
    return texts
    
def get_three_words(texts:list, words=3):
    len_ = len(texts)
    rand = random.randint(0,len_ - (words-1))
    return texts[rand:rand + words]


def get_all_fonts(font_dir="cyr_fonts"):
    fonts = []
    for dirpath, dirnames, filenames in os.walk(font_dir):
        # перебрать каталоги
        # for dirname in dirnames:
            # print("Каталог:", os.path.join(dirpath, dirname))
        # перебрать файлы
        for filename in filenames:
            fonts.append(os.path.join(dirpath, filename))
    return fonts    

def create_base_image(name='base.jpg', opacity=255, save=False, imgsize=(250, 250), mode='RGB', inner_сolor = [80, 80, 255], outer_сolor = [0, 0, 80]):
    '''
    Это будет код для круглого градиента:
    Для каждого пикселя он устанавливает значения красного, зеленого и синего где-то между innerColor и outerColor в зависимости от расстояния от пикселя до центра.

    imgsize = (250, 250) #The size of the image
    innerColor = [80, 80, 255] #Color at the center
    outerColor = [0, 0, 80] #Color at the corners

    '''
    image = Image.new(mode, imgsize) #Create the image

    for y in range(imgsize[1]):
        for x in range(imgsize[0]):

            #Find the distance to the center
            distanceToCenter = math.sqrt((x - imgsize[0]/2) ** 2 + (y - imgsize[1]/2) ** 2)

            #Make it on a scale from 0 to 1
            distanceToCenter = float(distanceToCenter) / (math.sqrt(2) * imgsize[0]/2)

            #Calculate r, g, and b values
            r = outer_сolor[0] * distanceToCenter + inner_сolor[0] * (1 - distanceToCenter)
            g = outer_сolor[1] * distanceToCenter + inner_сolor[1] * (1 - distanceToCenter)
            b = outer_сolor[2] * distanceToCenter + inner_сolor[2] * (1 - distanceToCenter)


            #Place the pixel        
            image.putpixel((x, y), (int(r), int(g), int(b), opacity))
    if save:
        image.save(name)
    return image


def random_color(op=255, not_this=None):
    diff = 0
    i=0
    while (diff < 30):
        a = random.randint(0, 255)
        b = random.randint(0, 255)
        c = random.randint(0, 255)
        if not_this is not None:    
            diff = abs(a-not_this[0]) + abs(b-not_this[1]) + abs(c-not_this[2])
            if diff < 70:
                print('not now')
            if i>3:
                break
        else:
            break
    return (a,b,c, op)


def rand_float(hue0, hue1):
    r = random.random()
    return r * abs(hue1 - hue0) + min(hue0, hue1)

def random_color_hue(s0, v0, simple=False):
    color = random.randint(0, 360)
    
    s = rand_float(*s0)
    v = rand_float(*v0)
    if simple:
        return (color, s, v)
        
    return f'hsl({color}, {s*100}%, {v*100}%)'

def hsv2rgb(hsv):
    return ImageColor.getrgb(hsv)

def rad(alpha):
    return pi * ((alpha % 180)/180)
    
def normalize(alpha, value=0.25):
    return sin(rad(alpha)) + value


    # {'s_back':s_back, 'v_back':v_back, 's_font':s_font, 'v_font':v_font}
def gen_captcha(save=True, fonts=fonts, captcha_texts=captcha_texts, words=4, offsets=offsets, hsv=hsv, image_size=image_size, font_size_limit=font_size_limit ):    
    """
    генератор капчи


    Args:
        save (bool, optional): указывает, нужно сохранять капчу на диск или показывать в просмотровщике изображений. Defaults to True.
        fonts ([type], optional): список имен(относительных путей к) шрифтов. Defaults to fonts.
        captcha_texts ([type], optional): большая простыня текста, из которой выбирается случайно номер слова, которое затем идет в капчагенератор. Defaults to songs.
        words (int, optional): количество слов в одной капче, выбирается из переменной выше начиная от случайного значения, дальше подряд . Defaults to 4.
        offset (int, optional): смещения для каждого слова. Defaults to 100.
        x_offset (int, optional): смещение картинки по х. Defaults to 100.
        y_offset (int, optional): смещение картинки капчи по у. Defaults to 500.
        s_back ([type], optional): сатурация фона из модели картинок hsv, значение - словарь от и до. Defaults to s_back.
        v_back ([type], optional): яркость фона из модели картинок hsv, значение - словарь от и до. Defaults to v_back.
        s_font ([type], optional): сатурация шрифта из модели картинок hsv, значение - словарь от и до. Defaults to s_font.
        v_font ([type], optional): яркость шрифта из модели картинок hsv, значение - словарь от и до. Defaults to v_font.
        im_w ([type], optional): ширина шрифта. Defaults to im_w.
        im_h ([type], optional): высота шрифта. Defaults to im_h.

    Returns:
        [type]: возвращает объект картинки, словарь параметров шрифта и словарь параметров капчи
    """    
    
    
    # fone = ImageColor.getrgb('white')
    # text_c = (0,0,0,255)
    # im = Image.new('RGB', (im_w, im_h), color=fone) 
    # gr_color1 = random_color()
    font_path = fonts[random.randint(0,len(fonts))]
    font_size = random.randint(*font_size_limit)
    font = ImageFont.truetype(font_path, font_size)
    width, height = font.getsize('Iq')
    
    uu = uuid.uuid4()

    gr_color1 = hsv2rgb(random_color_hue(hsv['s_back'], hsv['v_back']))
    # gr_color1
    gr_color2 = hsv2rgb(random_color_hue(hsv['s_back'], hsv['v_back']))
    im = create_base_image(imgsize=image_size, inner_сolor=gr_color1, outer_сolor=gr_color2)
    song_list = some_text(captcha_texts)
    # song_list
    texts = get_three_words(song_list, words)
    # print(texts)
    draw1 = ImageDraw.Draw(im)
    # draw1.text((0, 0), text='astramariy cerevbor crush', font=font, fill=random_color_hue(s_font, v_font))
    i = 3
    j = 0
    for text in texts:
        # i=1
        for t in text:
            image2 = Image.new('RGBA', (width, height), (255, 255, 255, 0))
            draw2 = ImageDraw.Draw(image2)
            font_color = hsv2rgb(random_color_hue(hsv['s_font'], hsv['v_font']))
            draw2.text((0, 0), text=t, font=font, fill=font_color)
            alpha = 3*i
            image2 = image2.rotate(alpha, expand=1)
            # divided_width = 1.5
            # divided_height = (normalize(alpha))*4
            # divided_by = 9
            # px, py = int( im_w * sin(alpha*pi/180)/divided_width)-1, int(im_h * cos(alpha*pi/180)/divided_height)-200
            px = int( im_w * sin(alpha*pi/180)) - offsets['x_offset'] 
            py = int(im_h * cos(alpha*pi/180)) - offsets['y_offset']
            # px, py = width, height
            sx, sy = image2.size
            # sx =sx//2
            sy =sy
            im.paste(image2, (px, py + j * offsets['offset'], px + sx, py + j * offsets['offset'] + sy), image2)
            i += 1
        j += 1
    if save:
        im.save('image1.png')
    else:
        im.show()
    save_last((texts, uu), (font_path, font_size), im)
    return (im, (texts, uu), (font_path, font_size))

def init(fonts_dir='cyr_fonts', use_db=False, captcha_texts=None, captcha_file_path=None, offsets=offsets, hsv=hsv, image_size=image_size):
    """инициализатор

    Args:
        font_dir (str, optional): папка со шрифтами. Defaults to 'cyr_fonts'.
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
    """    
    if captcha_texts is not None:
        globals()['captcha_texts']  = captcha_texts
        
    globals()['fonts']  = get_all_fonts(fonts_dir)
    globals()['image_size'] = image_size
    globals()['font_size_limit'] = font_size_limit
    globals()['hsv'] = hsv
    globals()['captcha_file_path'] = captcha_file_path
    
    if use_db:
        pass
        import db_init
        ini = db_init.CaptchaInit(offsets, hsv, image_size, fonts_dir, captcha_texts, captcha_file_path, font_size_limit)
        db_init.db_session.add(ini)
        db_init.db_session.commit()


def save_last(captcha_prop, font_prop, im):
    globals()['captcha_prop'] = captcha_prop
    globals()['font_prop'] = font_prop
    globals()['im'] = im
    
def get_last():
    captcha_prop = globals()['captcha_prop']
    font_prop =  globals()['font_prop']
    im = globals()['im'] 
    return captcha_prop, font_prop, im
    

def show_img():
    y_off, x_off, gen_off = offsets['y_offset'], offsets['x_offset'], offsets['offset']
    ofssets0 = {'y_offset': 400, 'x_offset': x_off, 'offset': gen_off}
    
    im, captcha_prop, font_prop = gen_captcha(save=False, fonts=fonts, captcha_texts=captcha_texts, offsets=ofssets0 )
    return im, captcha_prop, font_prop


def run():
    y_off, x_off, gen_off = offsets['y_offset'], offsets['x_offset'], offsets['offset']
    ofssets0 = {'y_offset': 400, 'x_offset': x_off, 'offset': gen_off}
    
    im, captcha_prop, font_prop = gen_captcha(save=True, fonts=fonts, captcha_texts=captcha_texts, offsets=ofssets0 )
    # im, captcha_prop, font_prop = gen_captcha(save=True, fonts=fonts, captcha_texts=songs, words=4, offset = 100, s_back=s_back, x_offset=100, y_offset=500, v_back=v_back, s_font=s_font, v_font=v_font, im_w=im_w, im_h=im_h )
    return im, captcha_prop, font_prop

init()
    