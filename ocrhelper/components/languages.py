import json

from ocrhelper.components import config
from ocrhelper.components.utils import check_path

with open(
    check_path('additional files/languages.json'), encoding='utf-8'
) as language_file:
    language_dict = json.load(language_file)


def get_string(key):
    language = config.get_value('interface_language')
    return language_dict[language][key]
