import customtkinter as ctk


class TranslatorsFrame(ctk.CTkFrame):
    def __init__(self, settings_frame, default_transl):
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
            fg_color="#5429FE",
            font=("Rubik bold", 19),
            corner_radius=20,
        )
        translator_label.place(relx=0.5, rely=0.23, anchor='center')

        self.translator_var = ctk.StringVar(self, default_transl)
        translators_segmented_btn = ctk.CTkSegmentedButton(
            self,
            values=["Google", "GPT", 'GPT Stream'],
            variable=self.translator_var,
            font=("Rubik", 17),
            selected_color="#5429FE",
            selected_hover_color="#4a1e9e",
        )
        translators_segmented_btn.place(relx=0.5, rely=0.683, anchor='center')

    def get_selected_translator(self):
        return self.translator_var.get()
