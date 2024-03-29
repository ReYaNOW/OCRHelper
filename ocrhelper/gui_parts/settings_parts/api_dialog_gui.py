import keyring
import customtkinter as ctk

from ocrhelper.components.utils import create_stylish_button
from ocrhelper.components.utils import validate_key, check_path
from ocrhelper.components import config
from ocrhelper.components import languages


class ApiDialogWindow:
    def __init__(self, settings_frame):
        self.settings_frame = settings_frame

        self.dialog_label = None
        self.dialog_window = None
        self.dialog_ok_btn = None
        self.ok_btn_var = None
        self.dialog_cancel_btn = None
        self.entry_var = None
        self.input_entry = None

        self.create_dialog_window()

    def create_dialog_window(self):
        self.dialog_window = ctk.CTkToplevel(self.settings_frame)
        self.dialog_window.title('OCRHelper')
        self.dialog_window.geometry('343x170')

        # without this icon will not be set on ctk.CTKTopLevel
        self.dialog_window.after(
            200,
            lambda: self.dialog_window.iconbitmap(
                check_path(r'assets/icon.ico')
            ),
        )

        self.dialog_window.attributes('-topmost', True)
        self.dialog_window.resizable(False, False)
        self.dialog_window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.dialog_window.withdraw()

        self.dialog_label = ctk.CTkLabel(
            self.dialog_window,
            text=languages.get_string('pls_enter_api'),
            font=('Rubik', 18),
        )
        self.dialog_label.place(relx=0.5, rely=0.2, anchor='center')

        self.ok_btn_var = ctk.StringVar(self.dialog_window, 'Ok')
        self.dialog_ok_btn = ctk.CTkButton(
            self.dialog_window,
            textvariable=self.ok_btn_var,
            command=self.button_click_event,
            font=('Rubik', 18),
            fg_color='#5429FE',
            hover_color='#4a1e9e',
            width=135,
            height=33,
            corner_radius=7,
        )

        self.dialog_ok_btn.place(relx=0.255, rely=0.8, anchor='center')

        self.dialog_cancel_btn = create_stylish_button(
            self.dialog_window,
            text=languages.get_string('cancel'),
            command=self.close_window,
            font='Rubik',
            fontsize=18,
            width=135,
            height=33,
            corner_radius=7,
        )
        self.dialog_cancel_btn.place(relx=0.745, rely=0.8, anchor='center')

        self.entry_var = ctk.StringVar(self.dialog_window, '')
        self.input_entry = ctk.CTkEntry(
            self.dialog_window, width=305, textvariable=self.entry_var
        )
        self.input_entry.place(relx=0.5, rely=0.5, anchor='center')

    def open_dialog_window(self):
        self.dialog_window.update_idletasks()
        screen_width = self.dialog_window.winfo_screenwidth()
        screen_height = self.dialog_window.winfo_screenheight()

        x_coordinate = int((screen_width / 2) - (343 / 2))
        y_coordinate = int((screen_height / 2) - (170 / 2))

        self.dialog_window.geometry(f'{x_coordinate}+{y_coordinate}')
        self.dialog_window.deiconify()
        self.input_entry.focus_force()

    def button_click_event(self):
        if self.ok_btn_var.get() == languages.get_string('close'):
            self.close_window()
        self.dialog_ok_btn.configure(state='disabled')
        self.dialog_cancel_btn.configure(state='disabled')
        self.dialog_window.update()

        key = self.entry_var.get()
        result = validate_key(key)
        if result is True:
            self.set_api_key(key)
            self.dialog_label.configure(
                text=languages.get_string('api_is_saved')
            )
        else:
            self.dialog_label.configure(
                text=languages.get_string('invalid_api')
            )

        self.dialog_ok_btn.configure(state='normal')
        self.dialog_cancel_btn.configure(state='normal')

    def close_window(self):
        self.dialog_window.destroy()
        self.create_dialog_window()

    def set_api_key(self, key):
        keyring.set_password('system', 'GPT_API_KEY', key)
        config.change_value('api_key_is_set', True)
        self.ok_btn_var.set(languages.get_string('close'))
