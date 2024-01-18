import numpy
from loguru import logger

from ocrhelper.components import languages
from ocrhelper.gui_parts.debug_window import DebugWindow


class TextRecognition:
    def __init__(self, image, recog_langs, easyocr_model, debug_window):
        self.image = image
        self.languages = recog_langs
        self.easyocr_model = easyocr_model
        self.debug_window: DebugWindow = debug_window

        self.text = None

        self.debug_window.add_message(
            languages.get_string('starting_recog'), 'white'
        )
        self.recognition(image)

    def recognition(self, image):
        text = self.recognize_text(image)
        self.add_messages(text)
        self.text = text
        return

    def recognize_text(self, image):
        reader = self.easyocr_model
        result = reader.readtext(
            numpy.array(image),
            paragraph=True,
            batch_size=12,
            detail=0,
            decoder='wordbeamsearch',
            beamWidth=15,
        )
        return ' '.join(result)

    def add_messages(self, text=None):
        logger.info(f'Result = \'{text}\'')

        self.debug_window.add_message(
            languages.get_string('recog_success'), 'green', enter='\n'
        )

    def get_text(self):
        return self.text
