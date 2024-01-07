import json

from components.utils import check_path

with open(check_path('additional files/config.json')) as config_file:
    conf = json.load(config_file)


def get_value(key):
    return conf[key]


def change_value(key, new_value):
    conf[key] = new_value


def get_font_name():
    return conf['font']


def save_config():
    with open(check_path('additional files/config.json'), 'w') as conf_file:
        conf_file.write(json.dumps(conf))
