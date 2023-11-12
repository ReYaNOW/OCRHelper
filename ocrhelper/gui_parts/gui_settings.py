from typing import Callable

import customtkinter as ctk

from ocrhelper.components.utils import create_stylish_button

from ocrhelper.gui_parts.settings_parts.languages_gui import LanguagesFrame
from ocrhelper.gui_parts.settings_parts.options_gui import OptionsWindow
from ocrhelper.gui_parts.settings_parts.palette_gui import PaletteFrame
from ocrhelper.gui_parts.settings_parts.translators_gui import TranslatorsFrame


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
            fontsize=16,
            command=self.open_option_window,
            height=45,
        )
        self.addit_sett_button.place(relx=0.2375, rely=0.885, anchor='center')
        self.additional_settings = ctk.CTkFrame(self)

    def _place_lang_frame(self):
        languages_frame = LanguagesFrame(self, self.config, self.load_ocr)
        languages_frame.place(relx=0.2375, rely=0.24, anchor='center')
        self.get_selected_languages = languages_frame.get_selected_languages

    def _place_transl_frame(self):
        translators_frame = TranslatorsFrame(self, self.config['translator'])
        translators_frame.place(relx=0.2375, rely=0.638, anchor='center')
        self.get_selected_translator = (
            translators_frame.get_selected_translator
        )

    def _place_palette_frame(self):
        self.palette_frame = PaletteFrame(self, self.config['rect_color'])
        self.palette_frame.place(relx=0.73, rely=0.406, anchor='center')
        self.get_rect_color = self.palette_frame.get_rect_color

    def open_option_window(self):
        self.options_window.update()
        self.options_window.deiconify()
