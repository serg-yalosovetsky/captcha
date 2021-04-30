

import database
count = 0

def run_once():
    count = globals()['count']
    if not count:
        database.init_db()
        count += 1
        
def create_config(offsets, hsv, image_size, fonts_dir, captcha_texts, captcha_file_path, font_size_limit):
    run_once()
    res = database.create_config(database.db_session, offsets, hsv, image_size, fonts_dir, captcha_texts, captcha_file_path, font_size_limit)
    return res

def get_config_last():
    res = database.get_config_last(database.db_session)
    return res