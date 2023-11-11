from typing import Callable

import customtkinter as ctk
from ocrhelper.components.utils import create_stylish_button


class LanguagesFrame(ctk.CTkFrame):
    def __init__(self, settings_frame, config, load_ocr: Callable):
        self.config = config
        self.load_ocr = load_ocr
        self.button_pressed = None

        super().__init__(
            settings_frame,
            bg_color='#262834',
            fg_color='#202020',
            width=300,
            height=130,
        )

        languages_label = ctk.CTkLabel(
            self,
            text="Языки для распознавания",
            fg_color="#5429FE",
            font=("Rubik bold", 19),
            corner_radius=20,
        )
        languages_label.place(relx=0.5, rely=0.23, anchor='center')

        self.eng_var, eng_option = self.create_lang_option('ENG')
        eng_option.place(relx=0.3, rely=0.525, anchor='center')

        self.rus_var, rus_option = self.create_lang_option('RUS')
        rus_option.place(relx=0.55, rely=0.525, anchor='center')

        self.jap_var, jap_option = self.create_lang_option('JAP')
        jap_option.place(relx=0.80, rely=0.525, anchor='center')

        change_button = create_stylish_button(
            self,
            text='Сменить',
            fontsize=16,
            command=self.press_load_ocr_btn,
            width=65,
            height=30,
        )
        change_button.place(relx=0.5, rely=0.808, anchor='center')
        
        self.load_langs_from_config()

    def press_load_ocr_btn(self):
        if self.button_pressed:
            return
        self.button_pressed = True
        self.load_ocr()
        self.button_pressed = False

    def create_lang_option(self, language: str):
        lang_var = ctk.StringVar(self, language)
        lang_option = ctk.CTkCheckBox(
            self,
            command=self.validate_lang_var,
            fg_color='#5429FE',
            hover_color='#4a1e9e',
            text=language,
            font=("Rubik", 16),
            variable=lang_var,
            onvalue=language,
            offvalue='',
        )
        if lang_var.get() != 'ENG':
            lang_var.set('')
        return lang_var, lang_option

    def validate_lang_var(self):
        if not self.get_selected_languages():
            self.eng_var.set('ENG')

    def get_selected_languages(self):
        languages = self.eng_var.get(), self.rus_var.get(), self.jap_var.get()
        # change to 2 char versions to work with EasyOCR
        return [lang[:-1].lower() for lang in languages if lang != '']

    def load_langs_from_config(self):
        for lang in self.config['recognition_languages']:
            match lang:
                case 'en':
                    self.eng_var.set('ENG')
                case 'ru':
                    self.rus_var.set('RUS')
                case 'ja':
                    self.jap_var.set('JAP')
