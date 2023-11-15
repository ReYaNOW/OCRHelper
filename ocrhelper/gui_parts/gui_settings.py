from typing import Callable

import customtkinter as ctk

from ocrhelper.components.utils import create_stylish_button

from ocrhelper.gui_parts.settings_parts.languages_gui import LanguagesFrame
from ocrhelper.gui_parts.settings_parts.options_gui import OptionsWindow
from ocrhelper.gui_parts.settings_parts.palette_gui import PaletteFrame
from ocrhelper.gui_parts.settings_parts.translators_gui import TranslatorsFrame
from ocrhelper.gui_parts.settings_parts.api_dialog_gui import ApiDialogWindow


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, config, load_ocr: Callable):
        super().__init__(master, fg_color="#262834", width=670, height=300)
        self.config = config
        self.load_ocr = load_ocr

        self._place_lang_frame()
        self._place_transl_frame()
        self._place_palette_frame()

        self.options_window = OptionsWindow(self, config)
        self.addit_sett_button = create_stylish_button(
            self,
            text='Дополнительные настройки',
            font=f"{self.config['font']}",
            fontsize=16,
            command=self.options_window.open_option_window,
            height=45,
        )
        self.addit_sett_button.place(relx=0.2375, rely=0.885, anchor='center')

        self.api_window = ApiDialogWindow(self, config)
        self.api_button = create_stylish_button(
            self,
            text='Ввести API-ключ',
            font=f"{self.config['font']}",
            fontsize=16,
            command=self.api_window.open_dialog_window,
            height=45,
        )
        self.api_button.place(relx=0.725, rely=0.885, anchor='center')

    def _place_lang_frame(self):
        languages_frame = LanguagesFrame(self, self.config, self.load_ocr)
        languages_frame.place(relx=0.2375, rely=0.24, anchor='center')

    def _place_transl_frame(self):
        translators_frame = TranslatorsFrame(self, self.config)
        translators_frame.place(relx=0.2375, rely=0.638, anchor='center')

    def _place_palette_frame(self):
        self.palette_frame = PaletteFrame(self, self.config)
        self.palette_frame.place(relx=0.73, rely=0.406, anchor='center')

