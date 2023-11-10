import tkinter as tk

import numpy
import pyperclip
from PIL import Image
from loguru import logger
from tkextrafont import Font

from ocr import TextRecognition
from ocrhelper.gui import Gui
from ocrhelper.gui_parts.translation import translation, TranslationWindow


class App:
    """Create a GUI for an OCR (Optical Character Recognition) application."""

    def __init__(self):
        self.easyocr = None
        self.easyocr_model = None
        self.languages = None
        self.use_gpt_stream = False

        self.gui = Gui(self.snip_trigger, self.load_easyocr_with_toast)

        # load font if it is not installed in the system
        if 'Rubik' not in tk.font.families():
            Font(file="Rubik.ttf")

        self.gui.after(15, self.easyocr_first_time_load)
        # run gui
        self.gui.mainloop()

    def easyocr_first_time_load(self):
        self.gui.load_ocr_toast.show_toast()
        self.gui.update()

        import easyocr

        self.easyocr = easyocr
        self.languages = ['en']
        self.load_easyocr_model()

        img = Image.open('load_easyocr.png')
        self.easyocr_model.readtext(numpy.array(img))

        self.gui.loaded_ocr_toast.show_toast()

    def load_easyocr_model(self):
        languages = self.languages
        logger.info(f'Загрузка модели EasyOCR c ' f'{", ".join(languages)}')

        self.easyocr_model = self.easyocr.Reader(languages)
        logger.success('Модель EasyOCR была успешно загружена')

    def load_easyocr_with_toast(self):
        new_languages = self.gui.get_selected_languages()
        if self.languages != new_languages:
            self.languages = new_languages

            self.gui.load_ocr_toast.show_toast()
            self.gui.update()
            self.load_easyocr_model()
            self.gui.loaded_ocr_toast.show_toast()

    def snip_trigger(self, image: Image.Image, coordinates: tuple):
        """Trigger when a screenshot is taken. Performs OCR on the image,
         translates the text, and displays the result.

        Args:
            image: The captured screenshot image.

            coordinates: The coordinates of the captured screenshot.
        """
        self.gui.debug_window.add_message('Скриншот был получен', 'green')

        new_languages = self.gui.get_selected_languages()
        if self.languages != new_languages:
            self.languages = new_languages

            self.gui.load_ocr_toast.show_toast()
            self.gui.update()
            self.load_easyocr_model()
            self.gui.loaded_ocr_toast.show_toast()

        # get recognized text from image via EasyOCR
        recognition_result = TextRecognition(
            image, self.languages, self.easyocr_model, self.gui.debug_window
        )
        text = recognition_result.get_text()

        # get chosen translator from variable and put it on debug window
        translator = self.gui.get_selected_translator()
        self.gui.debug_window.add_message(
            f'Перевод при помощи —\n{translator}\n',
            color='white',
        )

        # get translated text
        translated_text = translation(
            text=text,
            from_lang=self.languages,
            to_lang='russian',
            translator=translator,
        )

        logger.success('Текст успешно переведен')
        logger.info(f'Переведенный текст = {translated_text}')

        if translator == 'GPT Stream':
            self.use_gpt_stream = True

        # add recognized text to clipboard if checkbutton is selected
        if self.gui.get_option_win_values()['need_copy_to_clipboard']:
            pyperclip.copy(text)

        # put translated text on the screen in a new tkinter window
        x1, y1 = coordinates
        TranslationWindow(
            self.gui,
            image,
            {
                'text': text,
                'translated_text': translated_text,
                'coordinates': (x1, y1),
            },
            self.gui.debug_window,
            self.use_gpt_stream,
        )
        self.gui.debug_window.add_message('Перевод прошел успешно!', 'green')
        self.use_gpt_stream = False