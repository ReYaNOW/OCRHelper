import tkinter as tk
import traceback
from typing import Callable

import keyboard
import pystray
from CTkMessagebox import CTkMessagebox
from PIL import Image
from loguru import logger
from pystray import MenuItem as item

import customtkinter as ctk
from ocrhelper.components import config
from ocrhelper.components import languages
from ocrhelper.components.utils import check_path
from ocrhelper.gui_parts.debug_window import DebugWindow, DebugWindowNullObject
from ocrhelper.gui_parts.main_window_frame import MainFrame
from ocrhelper.gui_parts.snip import SnippingTool
from ocrhelper.gui_parts.toast import ToastNotification

ctk.set_appearance_mode('dark')


class Gui(ctk.CTk):
    def __init__(self, snip_trigger, load_ocr: Callable):
        self.snip_trigger = snip_trigger
        self.load_ocr = load_ocr
        
        self.mode_var = None
        self.use_debug_win = False
        self.errors_counter = 0
        
        super().__init__(fg_color='#262834')
        self.title('OCR Helper')
        self.geometry('670x300')
        
        self.iconbitmap(check_path(r'assets/icon.ico'))
        self.resizable(False, False)
        self.withdraw()
        
        if 'Rubik' not in tk.font.families():
            config.change_value('font', 'Consolas')
        
        self.change_geometry_to_center()
        self._create_system_tray_icon()
        self._create_toast_notifications()
        self.main_window_frame = MainFrame(self, self.load_ocr)
        self.main_window_frame.place(relx=0, rely=0)
        
        self.debug_window = DebugWindow(self)
        self.debug_window_null = DebugWindowNullObject(self)
        self._create_snipping_tool()
        self._add_keyboard_binds()
    
    def _create_system_tray_icon(self):
        image = Image.open(check_path(r'assets/icon.ico'))
        menu = (
            item('Open menu', self.show_window, default=True),
            item('Exit', self.quit_app),
        )
        
        self.tray_icon = pystray.Icon('OCRHelper', image, 'OCRHelper', menu)
        self.tray_icon.run_detached()
        self.protocol('WM_DELETE_WINDOW', self.withdraw)
    
    def _create_toast_notifications(self):
        self.load_ocr_toast = ToastNotification(
            self,
            message=languages.get_string('load_ocr_toast'),
            icon_color='orange',
        )
        self.loaded_ocr_toast = ToastNotification(
            self,
            message=languages.get_string('loaded_ocr_toast'),
            icon_color='#00E81A',
            duration=5000,
        )
        self.already_loaded_toast = ToastNotification(
            self,
            message=languages.get_string('already_loaded_toast'),
            icon_color='#00E81A',
            duration=5000,
        )
    
    def _create_snipping_tool(self):
        additional_methods = {
            'gui_update': self.update,
            'snip_trigger': self.snip_trigger,
            'debug_window': self.debug_window_null,
        }
        self.snipping_tool = SnippingTool(self, additional_methods)
    
    def _add_keyboard_binds(self):
        keyboard.add_hotkey('ctrl + alt + x', callback=self.show_window)
        keyboard.add_hotkey(
            'ctrl + shift + x', callback=self.run_snipping_tool
        )
    
    def change_geometry_to_center(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x_coordinate = int((screen_width / 2) - (670 / 2))
        y_coordinate = int((screen_height / 2) - (300 / 2))
        
        self.geometry(f'+{x_coordinate}+{y_coordinate}')
    
    def run_snipping_tool(self):
        if not config.get_value('ocr_is_loading') and config.get_value(
                'ocr_is_loaded'):
            current_debug_win = self.get_current_debug_win()
            self.snipping_tool.change_debug_win_instance(current_debug_win)
            self.snipping_tool.display_snipping_tool()
    
    def get_current_debug_win(self):
        if config.get_value('use_debug_window') is True:
            return self.debug_window
        else:
            return self.debug_window_null
    
    def change_mode_var(self, mode):
        self.mode_var = mode
    
    def report_callback_exception(self, exc, val, tb):
        if self.errors_counter > 0:
            self.close_window()
            return
        
        self.errors_counter += 1
        tb_lines = [
            str(line) for line in traceback.format_exception(exc, val, tb)
        ]
        logger.error(''.join(tb_lines))
        msg_box = CTkMessagebox(
            title='Error',
            message=f'{exc.__name__}:  {val}',
            button_color='#5429FE',
            button_hover_color='#4a1e9e',
            icon='cancel',
            font=(config.get_font_name(), 16),
        )
        msg_box.bind('<Destroy>', self.close_window)
    
    def show_window(self):
        self.change_geometry_to_center()
        self.iconify()
        self.update()
        self.after(15, self.deiconify)
    
    def close_window(self, _=None):
        self.update()
        config.change_value('font', 'Rubik')
        config.save_config()
        
        self.debug_window.window.destroy()
        self.quit()
        
        self.tray_icon.visible = False
        self.tray_icon.stop()
    
    def quit_app(self, tray_icon):
        self.update()
        config.change_value('font', 'Rubik')
        config.change_value('ocr_is_loaded', False)
        config.change_value('ocr_is_loading', False)
        config.save_config()
        
        self.debug_window.window.destroy()
        self.deiconify()
        self.update()
        self.quit()
        
        tray_icon.visible = False
        tray_icon.stop()
