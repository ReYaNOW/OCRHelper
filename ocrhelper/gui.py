import json
import tkinter as tk
from typing import Callable

import keyboard
import pystray
from PIL import Image
from pystray import MenuItem as item

import customtkinter as ctk
from ocrhelper.components.utils import bind_button_with_img, open_tk_img
from ocrhelper.components.utils import create_stylish_button
from ocrhelper.components.utils import check_path
from ocrhelper.gui_parts.animation import AnimateWidget
from ocrhelper.gui_parts.debug_window import DebugWindow, DebugWindowNullObject
from ocrhelper.gui_parts.gui_settings import SettingsFrame
from ocrhelper.gui_parts.snip import SnippingTool
from ocrhelper.gui_parts.toast import ToastNotification


class Gui(ctk.CTk):
    def __init__(self, config, snip_trigger, load_ocr: Callable):
        self.config = config
        self.snip_trigger = snip_trigger
        self.load_ocr = load_ocr

        self.mode_var = None
        self.use_debug_win = False

        super().__init__(fg_color="#262834")
        self.title('OCR Helper')
        self.geometry("670x300")
        self.iconbitmap(check_path(r'assets/icon.ico'))
        self.withdraw()

        self._change_geometry_to_center()
        self._create_system_tray_icon()
        self._create_toast_notifications()
        self._place_mode_buttons()
        self._place_settings_button()

        self.settings_frame = SettingsFrame(self, self.config, self.load_ocr)
        self.settings_frame.place(relx=0, rely=0, anchor='sw')
        self.animated_widget = AnimateWidget(
            self.settings_frame, self.settings_button
        )

        self.debug_window = DebugWindow(self)
        self.debug_window_null = DebugWindowNullObject(self)
        self._create_snipping_tool()
        self._add_keyboard_binds()

    def _change_geometry_to_center(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_coordinate = int((screen_width / 2) - (670 / 2))
        y_coordinate = int((screen_height / 2) - (300 / 2))

        self.geometry(f'+{x_coordinate}+{y_coordinate}')

    def _create_system_tray_icon(self):
        image = Image.open(check_path(r'assets/icon.ico'))
        menu = (
            item('Open menu', self.show_window, default=True),
            item('Exit', self.quit_window),
        )

        tray_icon = pystray.Icon('OCRHelper', image, 'OCRHelper', menu)
        tray_icon.run_detached()
        self.protocol('WM_DELETE_WINDOW', lambda: self.withdraw())

    def _place_settings_button(self):
        self.settings_im = open_tk_img(check_path('assets/settings.png'))
        self.settings_im_dark = open_tk_img(
            check_path('assets/settings dark.png')
        )

        self.settings_button = tk.Button(
            image=self.settings_im,
            command=lambda: self.animated_widget.animate(),
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
        bind_button_with_img(
            '<Enter>', self.settings_button, self.settings_im_dark
        )
        bind_button_with_img('<Leave>', self.settings_button, self.settings_im)

    def _place_mode_buttons(self):
        self.mode_var = ctk.StringVar(self, 'translation')
        translator_mode_button = create_stylish_button(
            self, 'Перевод', lambda: self.change_mode_var('translation')
        )
        translator_mode_button.place(relx=0.073, rely=0.353)

        dict_mode_button = create_stylish_button(
            self, 'Словарь', lambda: self.change_mode_var('dict')
        )
        dict_mode_button.place(relx=0.389, rely=0.353)

        decrypt_mode_button = create_stylish_button(
            self, 'Decrypt', lambda: self.change_mode_var('decrypt')
        )
        decrypt_mode_button.place(relx=0.705, rely=0.353)

    def _create_toast_notifications(self):
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

    def _create_snipping_tool(self):
        additional_methods = {
            'gui_update': self.update,
            'snip_trigger': self.snip_trigger,
            'debug_window': self.debug_window_null,
            'get_rect_color': self.get_rect_color,
        }
        self.snipping_tool = SnippingTool(self, additional_methods)

    def _add_keyboard_binds(self):
        keyboard.add_hotkey('ctrl + alt + x', callback=self.deiconify)
        keyboard.add_hotkey(
            'ctrl + shift + x', callback=self.run_snipping_tool
        )

    def run_snipping_tool(self):
        current_debug_win = self.get_current_debug_win()
        self.snipping_tool.change_debug_win_instance(current_debug_win)
        self.snipping_tool.display_snipping_tool()

    def get_option_window_values(self) -> dict:
        return self.settings_frame.options_window.get_var_values()

    def get_current_debug_win(self):
        option_val = self.get_option_window_values()
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

    def change_mode_var(self, mode):
        self.mode_var = mode

    def show_window(self):
        self.iconify()
        self.deiconify()

    def quit_window(self, tray_icon):
        self.config['recognition_languages'] = self.get_selected_languages()
        self.config['translator'] = self.get_selected_translator()
        self.config['rect_color'] = self.get_rect_color()
        self.config.update(self.get_option_window_values())

        with open(check_path('additional files/config.json'), 'w') as config:
            config.write(json.dumps(self.config))

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
