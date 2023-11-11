import os

import openai
from deep_translator import GoogleTranslator
from loguru import logger

api_key = os.getenv('GPT_API_KEY')
openai.api_key = api_key


def translation(text, from_lang, to_lang, translator='Google Translator'):
    logger.info(f'Перевод при помощи {translator}')
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
            from_lang_conv = lang_convert(from_lang)
            to_lang_conv = lang_convert(to_lang)
            return gpt_request(text, from_lang_conv, to_lang_conv)

        case 'GPT Stream':
            from_lang_conv = lang_convert(from_lang)
            to_lang_conv = lang_convert(to_lang)
            return gpt_request(
                text, from_lang_conv, to_lang_conv, use_stream=True
            )


def gpt_request(text, from_lang, to_lang, use_stream=False):
    request = f'Please translate the user message from {from_lang} to\
     {to_lang}. Make the translation sound as natural as possible.\
      In answer write only translation.\n\n {text}'

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-1106',
        messages=[{'role': 'user', 'content': request}],
        stream=use_stream,
    )
    if use_stream:
        return response
    return response['choices'][0]['message']['content']


def lang_convert(language):
    match language:
        case 'eng':
            return 'english'
        case 'rus':
            return 'russian'
        case 'eng+rus':
            return 'english and russian'
        case _:
            return language
