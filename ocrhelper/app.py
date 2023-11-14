import json

import numpy
import pyperclip
from PIL import Image
from loguru import logger

from ocrhelper.components.translation import translation
from ocrhelper.components.utils import check_path
from ocrhelper.gui import Gui
from ocrhelper.ocr import TextRecognition
from ocrhelper.translation_window import TranslationWindow


class App:
    """Create a GUI for an OCR (Optical Character Recognition) application."""

    def __init__(self):
        self.easyocr = None
        self.easyocr_model = None
        self.languages = None
        self.use_gpt_stream = False

        with open(check_path('additional files/config.json')) as config_file:
            self.config = json.load(config_file)

        self.gui = Gui(
            self.config, self.snip_trigger, self.load_easyocr_with_toast
        )

        self.gui.after(15, self.easyocr_first_time_load)
        # run gui
        self.gui.mainloop()

    def easyocr_first_time_load(self):
        self.gui.load_ocr_toast.show_toast()
        self.gui.update()

        import easyocr

        self.easyocr = easyocr
        self.languages = self.config['recognition_languages']
        self.load_easyocr_model()

        img = Image.open(check_path('additional files/load_easyocr.png'))
        self.easyocr_model.readtext(numpy.array(img))

        self.gui.load_ocr_toast.hide_toast_immediately()
        self.gui.loaded_ocr_toast.show_toast()

    def load_easyocr_model(self):
        languages = self.languages

        logger.info(f'Загрузка модели EasyOCR c ' f'{", ".join(languages)}')
        self.easyocr_model = self.easyocr.Reader(languages)
        logger.success('Модель EasyOCR была успешно загружена')

    def load_easyocr_with_toast(self):
        """Load EasyOCR with some languages
        if they are changed from a previous load"""
        new_languages = self.gui.get_selected_languages()
        if self.languages != new_languages:
            self.languages = new_languages

            self.gui.load_ocr_toast.show_toast()
            self.gui.update()
            self.load_easyocr_model()
            self.gui.load_ocr_toast.hide_toast_immediately()
            self.gui.loaded_ocr_toast.show_toast()

    def snip_trigger(self, image: Image.Image, coordinates: tuple):
        """Trigger when a screenshot is taken. Performs OCR on the image,
         translates the text, and displays the result.

        Args:
            image: The captured screenshot image.
            coordinates: The coordinates of the captured screenshot.
        """
        self.gui.debug_window.add_message('Скриншот был получен', 'green')
        self.load_easyocr_with_toast()

        text = TextRecognition(
            image, self.languages, self.easyocr_model, self.gui.debug_window
        ).get_text()

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
        if self.gui.get_option_window_values()['need_copy_to_clipboard']:
            pyperclip.copy(text)

        # put translated text on the screen in a new tkinter window
        x1, y1 = coordinates
        text_related = {
            'text': text,
            'translated_text': translated_text,
            'coordinates': (x1, y1),
            'use_gpt_stream': self.use_gpt_stream,
        }
        TranslationWindow(
            self.gui,
            self.gui.debug_window,
            image,
            text_related,
        )
        self.gui.debug_window.add_message('Перевод прошел успешно!', 'green')
        self.use_gpt_stream = False
