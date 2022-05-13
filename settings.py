try:
    from simplejson import json
except:
    import json


def read():
    with open('settings.json', 'r') as settings_json:
        return json.load(settings_json)


def save():
    with open('settings.json', 'w') as settings_json:
        json.dump(settings, settings_json)


settings = read()
HANDS = settings['HANDS']  # работа с руками
FACE = settings['FACE']  # работа с лицом
BLUR = settings['BLUR']  # уровень размазывания
show_number_fingers = settings['show_number_fingers']
RECORDING = settings['RECORDING']  # работа с видео
modules_installing = settings['modules_installing']  # установка модулей
