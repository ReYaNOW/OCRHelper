from typing import Callable

import customtkinter as ctk

from ocrhelper.components.utils import create_stylish_button
from ocrhelper.components import config
from ocrhelper.components import languages

from ocrhelper.gui_parts.settings_parts.language_frames import LanguagesFrame
from ocrhelper.gui_parts.settings_parts.options_gui import OptionsWindow
from ocrhelper.gui_parts.settings_parts.palette_gui import PaletteFrame
from ocrhelper.gui_parts.settings_parts.segmented_gui import TranslatorsFrame
from ocrhelper.gui_parts.settings_parts.api_dialog_gui import ApiDialogWindow


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, load_ocr: Callable):
        super().__init__(master, fg_color='#262834', width=670, height=300)
        self.load_ocr = load_ocr

        self._place_lang_frame()
        self._place_transl_frame()
        self._place_palette_frame()

        self.api_window = ApiDialogWindow(self)
        self.api_button = create_stylish_button(
            self,
            text=languages.get_string('enter_api'),
            font=f'{config.get_font_name()}',
            fontsize=16,
            command=self.api_window.open_dialog_window,
            height=45,
            corner_radius=11,
        )
        self.api_button.place(relx=0.46, rely=0.815, anchor='ne')

        self.options_window = OptionsWindow(self)
        self.addit_sett_button = create_stylish_button(
            self,
            text=languages.get_string('additional_settings'),
            font=f'{config.get_font_name()}',
            fontsize=16,
            command=self.options_window.open_option_window,
            height=45,
            corner_radius=11,
        )
        self.addit_sett_button.place(relx=0.475, rely=0.815)

    def _place_lang_frame(self):
        languages_frame = LanguagesFrame(self, self.load_ocr)
        languages_frame.place(relx=0.2375, rely=0.24, anchor='center')

    def _place_transl_frame(self):
        translators_frame = TranslatorsFrame(self)
        translators_frame.place(relx=0.2375, rely=0.638, anchor='center')

    def _place_palette_frame(self):
        self.palette_frame = PaletteFrame(self)
        self.palette_frame.place(relx=0.73, rely=0.406, anchor='center')
