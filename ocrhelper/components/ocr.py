import easyocr
import numpy


def text_recognition(image):
    reader = easyocr.Reader(["en"])
    result = reader.readtext(
        numpy.array(image),
        paragraph=True,
        detail=0,
        batch_size=16,
    )
    print(result)
