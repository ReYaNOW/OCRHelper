import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from ocrhelper.components.snip import SnipButton
from ocrhelper.components.ocr import TextRecognition
from ocrhelper.components.translation import translation, TranslatedWindow


class App(tk.Tk):
    def __init__(self):
        # create window
        super().__init__()
        self.title("OCR Helper")
        self.geometry("500x400")
        self.iconbitmap("icon.ico")

        # adding snipping tool
        button = SnipButton(self, self)
        button.place(
            relx=0.5,
            rely=0.37,
            relheight=0.5,
            relwidth=0.5,
            anchor="center",
        )

        # frame with configuration widgets
        self.config_widgets_frame = ttk.Frame(self)
        self.config_widgets_frame.place(
            relx=0.5,
            rely=1,
            relheight=0.35,
            relwidth=1,
            anchor="s",
        )
        self.config_widgets_frame.rowconfigure(0, weight=1)
        self.config_widgets_frame.rowconfigure(1, weight=1)
        self.config_widgets_frame.rowconfigure(2, weight=1)
        self.config_widgets_frame.columnconfigure(
            (0, 1, 2, 3, 4, 5),  # noqa cuz its working with tuple flawlesly
            weight=1,
        )

        # label for check button
        self.check_buttons_label = ttk.Label(
            self.config_widgets_frame,
            text="Должен быть выбран хотя бы один язык",
            font=("Arial", 14),
        )
        self.check_buttons_label.grid(column=0, columnspan=6, row=0)

        self.check_buttons_frame = ttk.Frame(self.config_widgets_frame)
        self.check_buttons_frame.grid(
            column=2, row=1, padx=10, pady=3, sticky="ne"
        )

        # add change language buttons
        self.check_eng_var = tk.StringVar(value="en")
        self.add_check_button(
            text="ENG", onvalue="en", check_var=self.check_eng_var
        )

        self.check_rus_var = tk.StringVar()
        self.add_check_button(
            text="RUS", onvalue="ru", check_var=self.check_rus_var
        )

        # drop down menu for different translators
        translators = [
            "Google Translator",
            "ChatGPT",
            "Faster ChatGPT",
            "Faster ChatGPT streaming",
        ]
        self.translation_var = tk.StringVar(value="Faster ChatGPT")

        self.translator_menu = ttk.Combobox(self.config_widgets_frame)
        self.translator_menu.configure(values=translators)
        self.translator_menu.configure(textvariable=self.translation_var)
        self.translator_menu.configure(state="readonly")
        self.translator_menu.grid(
            column=3, row=1, padx=10, pady=3, sticky="nw"
        )

        # run
        self.mainloop()

    def add_check_button(self, text, onvalue, check_var):
        check_button = ttk.Checkbutton(
            self.check_buttons_frame,
            text=text,
            variable=check_var,
            command=self.validate_lang_var,
            onvalue=onvalue,
            offvalue="",
        )
        check_button.pack()

    def validate_lang_var(self):
        print("eng", self.check_eng_var.get(), "rus", self.check_rus_var.get())
        if not self.check_eng_var.get() and not self.check_rus_var.get():
            self.check_eng_var.set("en")

    def trigger_func(self, image, coordinates):
        print(coordinates)
        x1, y1 = coordinates
        image.save("test_img.png")
        eng_var = self.check_eng_var.get()
        rus_var = self.check_rus_var.get()

        if eng_var and rus_var:
            languages = f"{eng_var}+{rus_var}"

        elif not eng_var and rus_var:
            languages = rus_var

        else:
            languages = eng_var

        recognition_result = TextRecognition(image, languages)
        text = recognition_result.get_text()
        print(f"[INFO]Исходный текст={text}")
        translated_text = translation(
            text=text,
            from_lang=languages,
            to_lang="russian",
            translator=self.translation_var.get(),
        )
        print(translated_text)
        TranslatedWindow(image, text, translated_text, (x1, y1))


if __name__ == "__main__":
    app = App()
