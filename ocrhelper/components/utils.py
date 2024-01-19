import os
import tkinter as tk
from random import randint

import keyring
import openai
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk
import pyperclip

import customtkinter as ctk
from ocrhelper.components import languages, config
from ocrhelper.gui_parts.toast import ToastNotification


def create_stylish_button(master, **kwargs):
    fontsize = kwargs.get('fontsize', 20)
    fg_color = kwargs.get('fg_color', '#5429FE')
    hover_color = kwargs.get('hover_color', '#4a1e9e')
    width = kwargs.get('width', 147)
    height = kwargs.get('height', 89)
    corner_radius = kwargs.get('corner_radius', 12)

    font = kwargs.get('font', 'Consolas')
    if font == 'Consolas' or font == 'Consolas bold':
        fontsize *= 1.15
    return ctk.CTkButton(
        master=master,
        command=kwargs['command'],
        text=kwargs['text'],
        font=(font, fontsize),
        fg_color=fg_color,
        hover_color=hover_color,
        width=width,
        height=height,
        corner_radius=corner_radius,
    )


def change_button_color(button: tk.Button, image: ImageTk):
    button.configure(image=image)
    button.image = image


def bind_button_with_img(type_of_bind, button: tk.Button, image: ImageTk):
    button.bind(
        type_of_bind,
        lambda e: change_button_color(button, image),
    )


def open_tk_img(path_to_image: str):
    image = Image.open(path_to_image)
    image_tk = ImageTk.PhotoImage(image, size=(96, 96))
    return image_tk


def check_path(path):
    if os.path.basename(__file__).rsplit('.', maxsplit=1)[-1] != 'py':
        # This will be the case when the app was compiled via PyInstaller
        return f'ocrhelper/{path}'
    return f'../{path}'


def validate_key(key):
    try:
        openai.ChatCompletion.create(
            model='gpt-3.5-turbo-1106',
            messages=[{'role': 'user', 'content': f'write {randint(1, 100)}'}],
            api_key=key,
        )
        return True
    except openai.error.AuthenticationError:
        return False


def create_ctk_apikey_msg_box(master):
    message = CTkMessagebox(
        title='OCRHelper',
        message=languages.get_string('pls_enter_api'),
        option_1=languages.get_string('create_api_key'),
        option_2='OK',
        font=(config.get_font_name(), 14),
        button_color='#5429FE',
        button_hover_color='#4a1e9e',
        corner_radius=7,
    )
    if message.get() == languages.get_string('create_api_key'):
        pyperclip.copy('https://platform.openai.com/api-keys')
        ToastNotification(
            master,
            message=languages.get_string('url_was_copied'),
            icon_color='#00E81A',
        ).show_toast()


def find_word_in_dictionary(word, to_lang):
    request = (
        f'Please explain what does this word mean.\nWord - {word}\n'
        f'Answer in {to_lang} language. '
        f'In the answer, write given word in the original language. '
    )
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=0.3,
        messages=[{'role': 'user', 'content': request}],
        api_key=keyring.get_password('system', 'GPT_API_KEY'),
        max_tokens=800,
    )
    return response['choices'][0]['message']['content']
