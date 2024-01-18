import tkinter as tk

import customtkinter as ctk
from ocrhelper.gui_parts.gui_settings import SettingsFrame
from ocrhelper.gui_parts.settings_parts.segmented_gui import (
    TranslationLangFrame,
    LanguageFrame,
)
from ocrhelper.components import config
from ocrhelper.components import languages
from ocrhelper.components.utils import bind_button_with_img, open_tk_img
from ocrhelper.components.utils import check_path
from ocrhelper.gui_parts.animation import AnimateWidget


class MainFrame(ctk.CTkFrame):
    def __init__(self, master, load_ocr):
        super().__init__(master, width=670, height=300, fg_color='#262834')
        self.handler_working = False

        self._place_main_screen_buttons()

        self.langs_frame = self.create_languages_frame()
        self.langs_frame.place(relx=0.1625, rely=1, anchor='nw')

        self.settings_frame = SettingsFrame(self, load_ocr)
        self.settings_frame.place(relx=0, rely=0, anchor='sw')

        self._place_language_button()
        self._place_settings_button()

    def _place_main_screen_buttons(self):
        string = languages.get_string('translation_mode')
        self.transl_mode_button = self.create_mode_button(string)
        self.transl_mode_button.place(relx=0.073, rely=0.300)

        string = languages.get_string('dict_mode')
        self.dict_mode_button = self.create_mode_button(string)
        self.dict_mode_button.place(relx=0.389, rely=0.300)

        string = languages.get_string('decrypt_mode')
        self.decrypt_mode_button = self.create_mode_button(string)
        self.decrypt_mode_button.place(relx=0.705, rely=0.300)

        selected_mode = config.get_value('selected_mode')
        self.change_border_selection(selected_mode)

    def create_mode_button(self, text):
        if text == languages.get_string('translation_mode'):
            mode = 'translation'
        elif text == languages.get_string('dict_mode'):
            mode = 'dict'
        else:
            mode = 'decrypt'

        return ctk.CTkButton(
            self,
            command=lambda: self.change_mode_var(mode),
            font=(f'{config.get_font_name()} bold', 20),
            text=text,
            fg_color='#5429FE',
            hover_color='#4a1e9e',
            border_color='#4bbd55',
            width=147,
            height=89,
            corner_radius=20,
        )

    def change_mode_var(self, selected_mode):
        self.change_border_selection(selected_mode)
        config.change_value('selected_mode', selected_mode)

    def change_border_selection(self, selected_mode):
        self.transl_mode_button.configure(border_width=0)
        self.dict_mode_button.configure(border_width=0)
        self.decrypt_mode_button.configure(border_width=0)
        match selected_mode:
            case 'translation':
                self.transl_mode_button.configure(border_width=3)
            case 'dict':
                self.dict_mode_button.configure(border_width=3)
            case _:
                self.decrypt_mode_button.configure(border_width=3)

    def create_languages_frame(self):
        languages_frame = ctk.CTkFrame(
            self,
            width=470,
            height=100,
            bg_color='#262834',
            fg_color='#262834',
            corner_radius=12,
        )

        interface_language_frame = LanguageFrame(languages_frame, 210, 80)
        interface_language_frame.place(relx=0.25, rely=0.5, anchor='center')

        translation_lang_frame = TranslationLangFrame(languages_frame, 232, 80)
        translation_lang_frame.place(relx=0.75, rely=0.5, anchor='center')
        return languages_frame

    def _place_language_button(self):
        self.langs_im = open_tk_img(check_path('assets/languages.png'))
        self.langs_im_dark = open_tk_img(
            check_path('assets/languages dark.png')
        )

        self.lang_button = self.create_button_from_imgs(
            self.langs_im, self.langs_im_dark
        )
        self.lang_button.place(relx=0.0125, rely=0.825)

        self.languages_animation = AnimateWidget(
            self.langs_frame,
            {
                'relx_pos': 0.1625,
                'rely_pos': 1,
                'rel_start_pos': 0.65,
                'rel_end_pos': 1,
            },
            move_from='bottom',
        )
        self.lang_button.configure(
            command=lambda: self.animation_handler('languages')
        )

    def _place_settings_button(self):
        self.settings_im = open_tk_img(check_path('assets/settings.png'))
        self.settings_im_dark = open_tk_img(
            check_path('assets/settings dark.png')
        )

        self.settings_button = self.create_button_from_imgs(
            self.settings_im, self.settings_im_dark
        )
        self.settings_button.place(relx=0.919, rely=0.825)

        self.settings_animation = AnimateWidget(
            self.settings_frame,
            {
                'relx_pos': 0,
                'rely_pos': 0,
                'rel_start_pos': 1,
                'rel_end_pos': 0,
            },
        )
        self.settings_button.configure(
            command=lambda: self.animation_handler('settings')
        )

    def animation_handler(self, widget_to_move):
        if self.handler_working:
            return
        self.handler_working = True

        match widget_to_move:
            case 'languages':
                if self.settings_animation.widget_on_screen:
                    self.settings_animation.animate()
                self.languages_animation.animate()
            case 'settings':
                if self.languages_animation.widget_on_screen:
                    self.languages_animation.animate()

                self.settings_animation.animate()

        # soft lock to prevent widgets from layering on top of each other
        if widget_to_move == 'languages':
            self.after(300, self.change_handler_status)
        else:
            self.after(500, self.change_handler_status)

    def change_handler_status(self):
        self.handler_working = False

    @staticmethod
    def create_button_from_imgs(img, dark_img):
        button = tk.Button(
            image=img,
            borderwidth=0,
            highlightthickness=0,
            disabledforeground='#262834',
            activebackground='#262834',
            background='#262834',
            width=45,
            height=45,
            relief='flat',
        )

        bind_button_with_img('<Enter>', button, dark_img)
        bind_button_with_img('<Leave>', button, img)
        return button
