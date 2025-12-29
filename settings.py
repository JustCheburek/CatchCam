try:
    from simplejson import json
except:
    import json


def read_settings():
    with open('settings.json', 'r') as settings_json:
        return json.load(settings_json)


def read_colors():
    with open('colors.json', 'r') as colors_json:
        return json.load(colors_json)


def save(**settings_given):
    for key_setting_given, value_setting_given in settings_given.items():
        settings[key_setting_given] = value_setting_given
        with open('settings.json', 'w') as settings_json:
            json.dump(settings, settings_json)


settings = read_settings()
colors = {}  # ЦВЕТА в BGR (blue green red)
for color in read_colors().items():
    colors[color[0]] = tuple(color[1])
