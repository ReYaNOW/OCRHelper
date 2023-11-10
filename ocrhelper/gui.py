import tkinter as tk
from typing import Callable

import keyboard
import pystray
from PIL import Image, ImageTk
from pystray import MenuItem as item

import customtkinter as ctk
from ocrhelper.gui_parts.debug_window import DebugWindow, DebugWindowNullObject
from ocrhelper.gui_parts.gui_settings import SettingsFrame
from ocrhelper.gui_parts.snip import SnippingTool
from ocrhelper.gui_parts.toast import ToastNotification


class Gui(ctk.CTk):
    def __init__(self, snip_trigger, load_ocr: Callable):
        self.snip_trigger = snip_trigger
        self.load_ocr = load_ocr
        self.use_debug_win = False

        super().__init__(fg_color="#262834")
        self.title('OCR Helper')
        self.geometry("670x300")
        self.iconbitmap(r'assets\icon.ico')
        self.withdraw()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_coordinate = int((screen_width / 2) - (670 / 2))
        y_coordinate = int((screen_height / 2) - (300 / 2))

        self.geometry(f'+{x_coordinate}+{y_coordinate}')

        # tray
        image = Image.open(r'assets\icon.ico')
        menu = (
            item('Open menu', self.show_window, default=True),
            item('Exit', self.quit_window),
        )

        tray_icon = pystray.Icon('OCRHelper', image, 'OCRHelper', menu)
        tray_icon.run_detached()
        self.protocol('WM_DELETE_WINDOW', lambda: self.withdraw())

        self.mode_var = ctk.StringVar(self, 'translation')
        translator_mode_button = self.create_mode_button(
            'Перевод', 'translation'
        )
        translator_mode_button.place(relx=0.073, rely=0.353)

        dict_mode_button = self.create_mode_button('Словарь', 'dict')
        dict_mode_button.place(relx=0.389, rely=0.353)

        decrypt_mode_button = self.create_mode_button('Decrypt', 'decrypt')
        decrypt_mode_button.place(relx=0.705, rely=0.353)

        self.settings_im = self.open_tk_img('assets/settings.png')
        self.settings_im_dark = self.open_tk_img('assets/settings dark.png')

        self.settings_button = tk.Button(
            image=self.settings_im,
            command=self.animate,
            borderwidth=0,
            highlightthickness=0,
            disabledforeground='#262834',
            activebackground='#262834',
            background='#262834',
            width=45,
            height=45,
            relief="flat",
        )
        self.settings_button.place(relx=0.919, rely=0.825)

        self.bind_button(
            '<Enter>', self.settings_button, self.settings_im_dark
        )
        self.bind_button('<Leave>', self.settings_button, self.settings_im)

        self.settings_frame = SettingsFrame(
            self,
            self.load_ocr,
            settings_im=self.settings_im,
            settings_im_dark=self.settings_im_dark,
        )
        self.settings_frame.place(relx=0, rely=0, anchor='sw')

        self.load_ocr_toast = ToastNotification(
            self,
            message='Загрузка модели EasyOCR с выбранными языками',
            icon_color='orange',
        )
        self.loaded_ocr_toast = ToastNotification(
            self,
            message='Модель EasyOCR загружена, программа готова к работе',
            icon_color='#00E81A',
            duration=5000,
        )
        self.debug_window = DebugWindow(self)
        self.debug_window_null = DebugWindowNullObject(self)

        additional_methods = {
            'gui_update': self.update,
            'snip_trigger': self.snip_trigger,
            'debug_window': self.debug_window_null,
            'get_rect_color': self.get_rect_color,
        }
        self.snipping_tool = SnippingTool(self, additional_methods)

        keyboard.add_hotkey(
            'ctrl + shift + x', callback=self.run_snipping_tool
        )

        self.animation_started = False
        self.settings_on_screen = False
        self.pos = 0
        self.start_pos = 1
        self.end_pos = 0

    def animate(self):
        if not self.animation_started:
            self.animation_started = True
            if not self.settings_on_screen:
                self.animate_forward()
            else:
                self.animate_backwards()

    def animate_forward(self):
        if self.pos < self.start_pos:
            self.pos += 0.035
            self.settings_frame.place(relx=0, rely=self.pos, anchor='sw')
            self.settings_button.lift()
            self.after(15, self.animate_forward)
        else:
            self.animation_started = False
            self.settings_on_screen = True

    def animate_backwards(self):
        if self.pos > self.end_pos:
            self.pos -= 0.035
            self.settings_frame.place(relx=0, rely=self.pos, anchor='sw')
            self.settings_button.lift()
            self.after(15, self.animate_backwards)
        else:
            self.animation_started = False
            self.settings_on_screen = False

    def run_snipping_tool(self):
        current_debug_win = self.get_current_debug_win()
        self.snipping_tool.change_debug_win_instance(current_debug_win)
        self.snipping_tool.display_snipping_tool()

    def get_option_win_values(self) -> dict:
        return self.settings_frame.options_window.get_var_values()

    def get_current_debug_win(self):
        option_val = self.get_option_win_values()
        if option_val['use_debug_window'] is True:
            return self.debug_window
        else:
            return self.debug_window_null

    def create_mode_button(self, text, mode):
        return ctk.CTkButton(
            self,
            command=lambda: self.change_mode_var(mode),
            font=('Rubik bold', 20),
            text=text,
            fg_color='#5429FE',
            hover_color='#4a1e9e',
            width=147,
            height=89,
            corner_radius=20,
        )

    def bind_button(self, type_of_bind, button: tk.Button, image: ImageTk):
        button.bind(
            type_of_bind,
            lambda e: self.change_button_color(button, image),
        )

    def change_mode_var(self, mode):
        self.mode_var = mode

    def show_window(self):
        self.iconify()
        self.deiconify()

    def quit_window(self, tray_icon):
        self.debug_window.window.destroy()
        self.deiconify()
        self.update()
        self.quit()

        tray_icon.visible = False
        tray_icon.stop()

    def get_selected_languages(self):
        return self.settings_frame.get_selected_languages()

    def get_selected_translator(self):
        return self.settings_frame.get_selected_translator()

    def get_rect_color(self):
        return self.settings_frame.get_rect_color()

    @staticmethod
    def change_button_color(button: tk.Button, image: ImageTk):
        button.configure(image=image)
        button.image = image

    @staticmethod
    def open_tk_img(path_to_image: str):
        image = Image.open(path_to_image)
        image_tk = ImageTk.PhotoImage(image, size=(96, 96))
        return image_tk
