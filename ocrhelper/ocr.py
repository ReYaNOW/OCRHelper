import numpy
from loguru import logger

from ocrhelper.gui_parts.debug_window import DebugWindow


class TextRecognition:
    def __init__(self, image, languages, easyocr_model, debug_window):
        self.image = image
        self.languages = languages
        self.easyocr_model = easyocr_model
        self.debug_window: DebugWindow = debug_window

        self.text = None
        self.current_ocr = None

        self.debug_window.add_message('Начинаю распознавание\n', 'white')

        self.recognition(image)

    def recognition(self, image):
        text = self.easy_ocr(image)
        self.messages(text)
        self.text = text
        return

    def easy_ocr(self, image):
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

    def messages(self, text=None):
        logger.info(f'Результат = \'{text}\'')
        enter = '\n'

        self.debug_window.add_message(
            'Текст успешно распознан\n', 'green', enter=enter
        )

    def get_text(self):
        return self.text
