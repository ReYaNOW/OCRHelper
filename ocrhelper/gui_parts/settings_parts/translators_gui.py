import customtkinter as ctk
from CTkMessagebox import CTkMessagebox


class TranslatorsFrame(ctk.CTkFrame):
    def __init__(self, settings_frame, config):
        self.config = config
        default_transl = config['translator']
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
            # fg_color="#5429FE",
            font=(f"{self.config['font']} bold", 19),
            corner_radius=20,
        )
        translator_label.place(relx=0.5, rely=0.23, anchor='center')

        self.translator_var = ctk.StringVar(self, default_transl)
        translators_segmented_btn = ctk.CTkSegmentedButton(
            self,
            command=self.check_value,
            values=["Google", "GPT", 'GPT Stream'],
            variable=self.translator_var,
            font=(self.config['font'], 17),
            selected_color="#5429FE",
            selected_hover_color="#4a1e9e",
        )
        translators_segmented_btn.place(relx=0.5, rely=0.683, anchor='center')

    def get_selected_translator(self):
        return self.translator_var.get()

    def check_value(self, _):
        if not self.config['api_key_is_set']:
            self.translator_var.set('Google')
            self.update()
            CTkMessagebox(
                title='OCRHelper',
                message='Пожалуйста, введите API-ключ',
                font=(self.config['font'], 14),
                button_color='#5429FE',
                button_hover_color='#4a1e9e',
                corner_radius=7,
            )
            
