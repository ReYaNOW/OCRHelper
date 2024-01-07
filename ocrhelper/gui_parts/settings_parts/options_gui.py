import customtkinter as ctk

from ocrhelper.components import config
from ocrhelper.components.utils import check_path
from ocrhelper.components.utils import create_stylish_button


class OptionsWindow:
    def __init__(self, settings_frame):
        self.settings_frame = settings_frame
        self.font_name = config.get_value('font')

        self.option_window = None
        self.clipboard_frame = None
        self.debug_frame = None

        self.create_option_window()

    def create_option_window(self):
        self.option_window = ctk.CTkToplevel(
            self.settings_frame, width=292, height=280
        )

        # without this icon will not be set on ctk.CTKTopLevel
        self.option_window.after(
            200,
            lambda: self.option_window.iconbitmap(
                check_path(r'assets/icon.ico')
            ),
        )

        self.option_window.attributes('-topmost', True)
        self.option_window.resizable(False, False)
        self.option_window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.option_window.withdraw()

        self.clipboard_frame = OptionsFrame(
            self.option_window,
            ('Добавлять распознанный', 'текст в буфер обмена'),
            type_='clipboard',
        )
        self.clipboard_frame.place(relx=0.5, rely=0.1875, anchor='center')

        self.debug_frame = OptionsFrame(
            self.option_window,
            ('Использовать debug', 'окно'),
            type_='debug',
        )
        self.debug_frame.place(relx=0.5, rely=0.54, anchor='center')

        save_button = create_stylish_button(
            self.option_window,
            text='Ok',
            font=self.font_name,
            fontsize=16,
            command=self.close_window,
            height=45,
        )
        save_button.place(relx=0.5, rely=0.85, anchor='center')

    def open_option_window(self):
        screen_width = self.settings_frame.winfo_screenwidth()
        screen_height = self.settings_frame.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (343 / 2))
        y_coordinate = int((screen_height / 2) - (170 / 2))

        self.option_window.update_idletasks()
        self.option_window.geometry(f'+{x_coordinate}+{y_coordinate}')
        self.option_window.deiconify()

    def close_window(self):
        self.option_window.destroy()
        self.create_option_window()


class OptionsFrame(ctk.CTkFrame):
    def __init__(self, settings: ctk.CTkToplevel, texts, type_):
        self.type_ = type_
        font = config.get_value('font')
        text1, text2 = texts
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
            font=(font, 18),
            cursor='hand2',
        )
        label.place(relx=0.5, rely=0.35, anchor='center')

        var_value = config.get_value(self.get_config_key())
        self.var = ctk.BooleanVar(self, var_value)
        self.checkbox = ctk.CTkCheckBox(
            self,
            font=(font, 18),
            text=text2,
            command=self.change_val_in_config,
            fg_color='#5429FE',
            hover_color='#4a1e9e',
            variable=self.var,
        )
        self.checkbox.place(relx=0.5, rely=0.59, anchor='center')

        label.bind('<Enter>', self.on_enter)
        label.bind('<Leave>', self.on_leave)
        label.bind(
            '<Button-1>',
            lambda event: self.var.set(False)
            if self.var.get() is True
            else self.var.set(True),
        )

    def get_config_key(self):
        if self.type_ == 'clipboard':
            return 'need_copy_to_clipboard'
        else:
            return 'use_debug_window'

    def change_val_in_config(self):
        key = self.get_config_key()
        value = self.var.get()
        config.change_value(key, value)

    def on_enter(self, _):
        self.checkbox._on_enter()  # noqa

    def on_leave(self, _):
        self.checkbox._on_leave()  # noqa
