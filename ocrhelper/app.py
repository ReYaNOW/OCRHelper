import threading

import numpy
import pyperclip
from PIL import Image
from loguru import logger

from components import languages
from ocrhelper.components import config
from ocrhelper.components.translation import translation
from ocrhelper.components.utils import check_path
from ocrhelper.components.utils import find_word_in_dictionary
from ocrhelper.gui import Gui
from ocrhelper.ocr import TextRecognition
from ocrhelper.result_window import TranslationWindow, DictionaryWindow
from ocrhelper.result_window import RecognitionWindow

class App:
    """Create a GUI for an OCR (Optical Character Recognition) application."""

    def __init__(self):
        self.easyocr = None
        self.easyocr_model = None
        self.ocr_is_loaded = False
        self.languages = None

        self.gui = Gui(self.snip_trigger, self.load_easyocr_with_toast)
        self.load_ocr_threading(first_time=True)

        self.gui.mainloop()

    def load_ocr_threading(self, first_time=False):
        self.gui.load_ocr_toast.show_toast()
        self.gui.update()
        self.ocr_is_loaded = False

        if first_time:
            target = self.easyocr_first_time_load
        else:
            target = self.load_easyocr_model
        thread = threading.Thread(target=target)
        thread.start()
        self.check_thread(thread)

    def check_thread(self, thread):
        if thread.is_alive():
            self.gui.after(100, lambda: self.check_thread(thread))
        else:
            self.gui.load_ocr_toast.hide_toast_immediately()
            self.gui.loaded_ocr_toast.show_toast()
            self.ocr_is_loaded = True

    def easyocr_first_time_load(self):
        logger.info('Importing EasyOCR module')
        import easyocr

        logger.success('EasyOCR import was successful')

        self.easyocr = easyocr
        self.languages = config.get_value('recognition_languages')
        self.load_easyocr_model()

        img = Image.open(check_path('additional files/load_easyocr.png'))
        self.easyocr_model.readtext(numpy.array(img))
        config.change_value('ocr_is_loaded', True)

    def load_easyocr_model(self):
        config.change_value('ocr_is_loading', True)
        languages = self.languages

        logger.info(
            f'Loading the EasyOCR model with ' f'{", ".join(languages)}'
        )
        self.easyocr_model = self.easyocr.Reader(languages)
        logger.success('The EasyOCR model was successfully loaded')
        config.change_value('ocr_is_loading', False)

    def load_easyocr_with_toast(self):
        """Load EasyOCR with some languages
        if they are changed from a previous load"""
        new_languages = config.get_value('recognition_languages')
        if self.languages != new_languages:
            self.languages = new_languages
            self.load_ocr_threading()
        else:
            self.gui.already_loaded_toast.show_toast()

    def display_translated_text(self, text, image, coordinates: tuple):
        translator = config.get_value('translator')
        self.gui.debug_window.add_message(
            f'{languages.get_string("translation_with")} —\n{translator}\n',
            color='white',
        )

        translated_text = translation(text=text)
        logger.success('Text successfully translated')
        logger.info(f'Translated text: {translated_text}')

        text_related = {
            'text': text,
            'other_text': translated_text,
            'coordinates': coordinates,
            'use_gpt_stream': translator == 'GPT Stream',
        }

        TranslationWindow(
            self.gui,
            self.gui.debug_window,
            image,
            text_related,
        )

        self.gui.debug_window.add_message(
            languages.get_string('transl_succeed'), 'green'
        )

    def display_dictionary_text(self, text, image, coordinates: tuple):
        if len(text.split()) > 1:
            self.gui.dict_only_one_word_toast.show_toast()
            return

        self.gui.debug_window.add_message(
            languages.get_string("analysis_with"),
            color='white',
        )
        output_lang = config.get_value('translation_language')
        string_found_in_dict = find_word_in_dictionary(text, output_lang)
        logger.success('Word successfully analyzed')
        logger.info(f'Analyzed word: {string_found_in_dict}')

        text_related = {
            'text': text,
            'other_text': string_found_in_dict,
            'coordinates': coordinates,
        }
        DictionaryWindow(
            self.gui,
            self.gui.debug_window,
            image,
            text_related,
        )

        self.gui.debug_window.add_message(
            languages.get_string('dict_succeed'), 'green'
        )

    def display_only_recogn_text(self, text, image, coordinates):
        text_related = {
            'text': text,
            'coordinates': coordinates,
        }
        RecognitionWindow(
            self.gui,
            self.gui.debug_window,
            image,
            text_related,
        )

    def snip_trigger(self, image: Image.Image, coordinates: tuple):
        """Trigger when a screenshot is taken.
        Performs OCR on the image,
         translates the text, and displays the result.

        Args:
            image: The captured screenshot image.
            coordinates: The coordinates of the captured screenshot.
        """
        self.gui.debug_window.add_message(
            languages.get_string('received_screenshot'), 'green'
        )

        text = TextRecognition(
            image, self.languages, self.easyocr_model, self.gui.debug_window
        ).get_text()

        if config.get_value('need_copy_to_clipboard'):
            pyperclip.copy(text)

        match config.get_value('selected_mode'):
            case 'translation':
                self.display_translated_text(text, image, coordinates)
            case 'dict':
                self.display_dictionary_text(text, image, coordinates)
            case _:
                self.display_only_recogn_text(text, image, coordinates)
