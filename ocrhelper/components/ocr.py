import numpy
import pytesseract
from PIL import ImageEnhance

from components.debug_window import DebugWindow

# pytesseract.pytesseract.tesseract_cmd = (
#     r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# )


class TextRecognition:
    def __init__(self, image, languages, easyocr_model, debug_window):
        self.image = image
        self.languages = languages
        self.easyocr_model = easyocr_model
        self.debug_window: DebugWindow = debug_window

        self.text = None
        self.current_ocr = None

        self.debug_window.add_message("Начинаю распознавание\n", "white")

        self.recognition(image, languages)

    def recognition(self, image, pytesser_lang):
        self.current_ocr = "PyTesseract"
        text, conf = self.try_pytesseract(image, pytesser_lang)
        if conf == 1:
            self.text = text
            return

        self.messages("negative", text, conf, "Использую EasyOCR")

        text = self.easy_ocr(image)
        self.messages("positive", text, 1)

        self.text = text
        return

    # Попытка распознать символы с PYTESSERACT
    def try_pytesseract(self, image, lang):
        print("[INFO]Использую PyTesseract")
        self.debug_window.add_message("Использую PyTesseract", "white")

        text, conf = self.pytesseract_ocr(image, lang)

        if conf is not None:
            if conf >= 89 and conf != 95.0 and text:
                self.messages("positive", text, conf)
                text = text.replace("|", "I")
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
            config=f"-l {lang}",
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

    def easy_ocr(self, image):
        reader = self.easyocr_model["model"]
        result = reader.readtext(
            numpy.array(image),
            paragraph=True,
            batch_size=12,
            detail=0,
            decoder="wordbeamsearch",
            beamWidth=15,
        )
        print(result)
        return " ".join(result)

    def messages(self, type_of_operation, text=None, conf=None, nextocr=None):
        info = "[INFO]"
        match type_of_operation:
            case "negative":
                print(f"{info}Не сойдет, conf={conf}")
                print(f"{info}{text}")
                print(f"{info}{nextocr}")

                self.debug_window.add_message(
                    f"{self.current_ocr} не справился\n", "orange"
                )
                self.debug_window.add_message(nextocr, "white")
                self.debug_window.tkinter_update()
            case "positive":
                print(f"{info}Сойдет, conf={conf}")
                print(f"{info}{text}")

                if nextocr == "last":
                    enter = ""
                else:
                    enter = "\n"

                self.debug_window.add_message(
                    "Текст успешно распознан\n", "green", enter=enter
                )
                self.debug_window.tkinter_update()

    def get_text(self):
        return self.text
