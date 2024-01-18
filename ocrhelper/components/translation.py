import openai
from deep_translator import GoogleTranslator
from loguru import logger
import keyring

from ocrhelper.components import config


def translation(text, from_lang, translator='Google'):
    logger.info(f'Translation using {translator}')
    to_lang = to_lang_convert(config.get_value('translation_language'))
    match translator:
        case 'Google':
            if len(from_lang) == 1 or from_lang not in ('ru', 'en'):
                from_lang_checked = 'auto'
            else:
                from_lang_checked = from_lang[0]

            translator_obj = GoogleTranslator(
                source=from_lang_checked,
                target=to_lang,
            )
            return translator_obj.translate(text=text)

        case 'GPT':
            from_lang_conv = langs_convert_gpt(from_lang)
            return gpt_request(text, from_lang_conv, to_lang)

        case 'GPT Stream':
            from_lang_conv = langs_convert_gpt(from_lang)
            return gpt_request(text, from_lang_conv, to_lang, use_stream=True)


def gpt_request(text, from_lang, to_lang, use_stream=False):
    if from_lang == to_lang and not use_stream:
        return text

    request = f'Please translate the user message from {from_lang} to\
     {to_lang}. Make the translation sound as natural as possible.\
      In answer write ONLY translation.\n\n {text}'

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=0.3,
        messages=[{'role': 'user', 'content': request}],
        stream=use_stream,
        api_key=keyring.get_password('system', 'GPT_API_KEY'),
    )
    if use_stream:
        return response
    return response['choices'][0]['message']['content']


def to_lang_convert(language):
    match language:
        case 'ENG':
            return 'english'
        case 'RUS':
            return 'russian'
        case 'JAP':
            return 'japanese'


def langs_convert_gpt(languages):
    for lang in languages:
        match lang:
            case 'en':
                return 'english'
            case 'ru':
                return 'russian'
            case 'ja':
                return 'japanese'
