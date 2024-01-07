import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from ocrhelper.components import config


class TranslatorsFrame(ctk.CTkFrame):
    def __init__(self, settings_frame):
        default_transl = config.get_value('translator')
        super().__init__(
            settings_frame,
            bg_color='#262834',
            fg_color='#202020',
            width=300,
            height=90,
        )

        translator_label = ctk.CTkLabel(
            self,
            text='Переводчик',
            font=(f'{config.get_font_name()} bold', 19),
            corner_radius=20,
        )
        translator_label.place(relx=0.5, rely=0.23, anchor='center')

        self.translator_var = ctk.StringVar(self, default_transl)
        translators_segmented_btn = ctk.CTkSegmentedButton(
            self,
            command=self.check_value,
            values=['Google', 'GPT', 'GPT Stream'],
            variable=self.translator_var,
            font=(config.get_font_name(), 17),
            selected_color='#5429FE',
            selected_hover_color='#4a1e9e',
        )
        translators_segmented_btn.place(relx=0.5, rely=0.683, anchor='center')

    def check_value(self, _):
        if not config.get_value('api_key_is_set'):
            self.translator_var.set('Google')
            self.update()
            CTkMessagebox(
                title='OCRHelper',
                message='Пожалуйста, введите API-ключ',
                font=(config.get_font_name(), 14),
                button_color='#5429FE',
                button_hover_color='#4a1e9e',
                corner_radius=7,
            )
        else:
            config.change_value('translator', self.translator_var.get())
