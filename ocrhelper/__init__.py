import tkinter as tk
from ocrhelper.components.snip import SnipButton
from ocrhelper.components.ocr import text_recognition


class App(tk.Tk):
    def __init__(self):
        # create window
        super().__init__()
        self.title("OCR Helper")
        self.geometry("600x400")

        # widgets
        button = SnipButton(self, self.trigger_func)
        button.place(relx=0.5, rely=0.5, anchor="center")

        # run
        self.mainloop()
    
    @staticmethod
    def trigger_func(image):
        image.save('test_img.png')
        text_recognition(image)


if __name__ == "__main__":
    app = App()
