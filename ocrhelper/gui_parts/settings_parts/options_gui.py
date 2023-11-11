import customtkinter as ctk

from ocrhelper.components.utils import create_stylish_button


class OptionsWindow(ctk.CTkToplevel):
    def __init__(self, settings_frame, config):
        self.config = config
        super().__init__(
            settings_frame, width=292, height=280, fg_color='#4a1e9e'
        )

        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_coordinate = int((screen_width / 2) - (292 / 2))
        y_coordinate = int((screen_height / 2) - (280 / 2))

        self.geometry(f'+{x_coordinate}+{y_coordinate}')
        self.overrideredirect(True)
        self.withdraw()

        frame = ctk.CTkFrame(
            self,
            width=292,
            height=280,
            fg_color='#262834',
            border_width=5,
            border_color='#4a1e9e',
        )
        frame.pack()

        self.clipboard_frame = OptionsFrame(
            frame,
            'Добавлять распознанный',
            'текст в буфер обмена',
            var_value=self.config['need_copy_to_clipboard'],
        )
        self.clipboard_frame.place(relx=0.5, rely=0.1875, anchor='center')

        self.debug_frame = OptionsFrame(
            frame,
            'Использовать debug',
            'окно',
            var_value=self.config['use_debug_window'],
        )
        self.debug_frame.place(relx=0.5, rely=0.54, anchor='center')

        save_button = create_stylish_button(
            frame,
            text='Сохранить',
            fontsize=16,
            command=self.withdraw,
            height=45,
        )
        save_button.place(relx=0.5, rely=0.85, anchor='center')

    def get_var_values(self):
        return {
            'need_copy_to_clipboard': self.clipboard_frame.get_var_value(),
            'use_debug_window': self.debug_frame.get_var_value(),
        }


class OptionsFrame(ctk.CTkFrame):
    def __init__(self, settings: ctk.CTkFrame, text1, text2, var_value):
        super().__init__(
            settings,
            bg_color='#262834',
            fg_color='#202020',
            corner_radius=20,
            width=275,
            height=90,
        )

        label = ctk.CTkLabel(
            self,
            text=text1,
            font=("Rubik", 18),
            cursor='hand2',
        )
        label.place(relx=0.5, rely=0.35, anchor='center')

        self.var = ctk.BooleanVar(self, var_value)
        self.checkbox = ctk.CTkCheckBox(
            self,
            font=("Rubik", 18),
            text=text2,
            fg_color='#5429FE',
            hover_color='#4a1e9e',
            variable=self.var,
        )
        self.checkbox.place(relx=0.5, rely=0.59, anchor='center')

        label.bind("<Enter>", self.on_enter)
        label.bind("<Leave>", self.on_leave)
        label.bind(
            "<Button-1>",
            lambda event: self.var.set(False)
            if self.var.get() is True
            else self.var.set(True),
        )

    def get_var_value(self):
        return self.var.get()

    def on_enter(self, _):
        self.checkbox._on_enter()  # noqa

    def on_leave(self, _):
        self.checkbox._on_leave()  # noqa
