from paddleocr import PaddleOCR
import pytesseract
import easyocr

import numpy
from PIL import ImageEnhance


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


class TextRecognition:
    def __init__(self, image, languages):
        self.text = None

        match languages:
            case "ru":
                self.recognition(image, "ru", "rus", use_paddle=False)

            case "en+ru":
                lang = ("en", "ru")
                pytesser_lang = "eng+rus"
                self.recognition(image, lang, pytesser_lang, use_paddle=False)

            case _:
                lang = ("en",)
                self.recognition(image, lang, "eng", use_paddle=True)

    def recognition(self, image, lang, pytesser_lang, use_paddle=False):
        text, conf = self.try_pytesseract(image, pytesser_lang)
        if conf == 1:
            self.text = text
            return

        if isinstance(lang, tuple | list) and use_paddle is True:
            self.messages("negative", conf, text, "Использую Paddle")

            text, conf = self.try_paddle(image, lang[0])
            if conf == 1:
                self.text = text
                return

        self.messages("negative", text, conf, "Использую EasyOCR")
        text = self.easy_ocr(image, lang)

        self.text = text
        return

    # Попытка распознать символы с PYTESSERACT
    def try_pytesseract(self, image, lang):
        print("[INFO]Использую PyTesseract")
        text, conf = self.pytesseract_ocr(image, lang)

        if conf is not None:
            if conf >= 89:
                self.messages("positive", text, conf)
                return text, 1
        return text, conf

    # Попытка распознать символы с PADDLE
    def try_paddle(self, image, lang):
        text, conf = self.paddle_ocr(image, lang=lang)
        if conf >= 0.8:
            self.messages("positive", text, conf)
            return text, 1

        return text, conf

    @staticmethod
    def pytesseract_ocr(image, lang):
        enhancer = ImageEnhance.Contrast(image)
        img = enhancer.enhance(2)

        # Преобразуем в черно-белый рисунок:
        thresh = 200
        res = img.convert("L").point(
            lambda x: 255 if x > thresh else 0, mode="1"
        )
        result = pytesseract.image_to_data(
            res,
            config=f"--oem 3  --psm 7 -l {lang}",
            output_type="data.frame",
        )
        result = result[result.conf != -1]
        lines = result.groupby("block_num")["text"].apply(list)

        if lines.empty:
            print("Пусто")
            return None, 0

        # getting simple list
        line = next(iter(lines))

        text = " ".join(line)
        conf = result.groupby(["block_num"])["conf"].mean()[1]
        return text, conf

    @staticmethod
    def paddle_ocr(image, lang):
        print(lang)
        ocr = PaddleOCR(use_angle_cls=True, lang=lang)
        result = ocr.ocr(numpy.array(image), cls=True, det=False)

        text, conf = None, None
        for i in range(len(result)):
            res = result[i]
            for line in res:
                text, conf = line
        return text, conf

    @staticmethod
    def easy_ocr(image, lang):
        reader = easyocr.Reader(lang)
        result = reader.readtext(
            numpy.array(image), paragraph=True, batch_size=16, detail=0
        )
        return " ".join(result)

    @staticmethod
    def messages(type_of_operation, text=None, conf=None, nextocr=None):
        info = "[INFO]"
        match type_of_operation:
            case "negative":
                print(f"{info}Не сойдет, conf={conf}")
                print(f"{info}{text}")
                print(f"{info}{nextocr}")
            case "positive":
                print(f"{info}Сойдет, conf={conf}")
                print(f"{info}{text}")

    def get_text(self):
        return self.text
