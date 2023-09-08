import tkinter as tk
from tkinter import ttk

import easyocr
import keyboard
import numpy
import pyclip
import pystray
from PIL import Image
from pystray import MenuItem as item

from ocrhelper.components.debug_window import DebugWindow
from ocrhelper.components.ocr import TextRecognition
from ocrhelper.components.snip import SnippingTool
from ocrhelper.components.translation import translation, TranslatedWindow


class App(tk.Tk):
    """Create a GUI for an OCR (Optical Character Recognition) application.

    Also load an EasyOCR model upon initialization.
    """

    def __init__(self):
        self.easyocr_lang = ["en"]
        self.faster_gpt_stream = False

        self.easy_ocr = {}
        self.load_easyocr_model()
        img = Image.open("load_easyocr.png")
        self.easy_ocr["model"].readtext(numpy.array(img))

        # create window
        super().__init__()
        self.title("OCR Helper")
        self.geometry("500x400")
        self.iconbitmap(r"assets\icon.ico")

        # Styles
        # self.call("source", r"theme\sv.tcl")
        # self.call("set_theme", "sv-dark")

        # tray
        image = Image.open(r"assets\icon.ico")

        menu = (
            item("Open menu", self.show_window, default=True),
            item("Exit", self.quit_window),
        )

        icon = pystray.Icon("OCRHelper", image, "OCRHelper", menu)
        icon.run_detached()
        self.protocol("WM_DELETE_WINDOW", lambda: self.withdraw())

        # add debug window
        self.debug_window = DebugWindow(self)

        # add snipping tool
        label_text = "Нажми CTRL + Shift + X,\n \
         чтобы запустить окно для перевода"
        hotkey_label = ttk.Label(self, text=label_text, font=("Arial", 18))
        self.snipping_tool = SnippingTool(
            self, self.update, self.snip_trigger, self.debug_window
        )
        hotkey_label.place(
            relx=0.5,
            rely=0.37,
            relheight=0.5,
            anchor="center",
        )

        # add hotkey for snipping tool
        keyboard.add_hotkey(
            "ctrl + shift + x",
            callback=self.snipping_tool.display_snipping_tool,
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
            column=2, row=1, padx=10, pady=3, sticky="nw"
        )

        # add change language buttons
        self.check_eng_var = tk.StringVar(value="eng")
        self.add_check_button(
            text="ENG", onvalue="eng", var=self.check_eng_var
        )

        self.check_rus_var = tk.StringVar()
        self.add_check_button(
            text="RUS", onvalue="rus", var=self.check_rus_var
        )

        # drop down menu for different translators
        translators = [
            "Google Translator",
            "ChatGPT",
            "Faster ChatGPT",
            "Faster ChatGPT streaming",
        ]
        self.translator_var = tk.StringVar(value="Google Translator")

        self.translator_menu = ttk.Combobox(self.config_widgets_frame)
        self.translator_menu.configure(values=translators)
        self.translator_menu.configure(textvariable=self.translator_var)
        self.translator_menu.configure(state="readonly")

        self.translator_menu.grid(column=3, row=1, padx=6, pady=3, sticky="nw")

        # clipboard checkbox
        self.clipboard_var = tk.BooleanVar(value=True)
        self.clipboard_check = ttk.Checkbutton(
            self.config_widgets_frame,
            text="Добавлять считанный текст в буфер обмена",
            variable=self.clipboard_var,
            onvalue=True,
            offvalue=False,
        )

        self.clipboard_check.grid(
            column=0, row=2, columnspan=6, padx=10, sticky="n"
        )

        # add label for loading models status
        self.loading_easyocr_var = tk.StringVar(value="EasyOCR загружен")
        self.loading_easyocr_label = ttk.Label(
            self.config_widgets_frame,
            wraplength=64,
            font=("Arial", 10),
            textvariable=self.loading_easyocr_var,
            anchor="nw",
        )
        self.loading_easyocr_label.grid(column=1, row=1, sticky="n")

        # run
        self.mainloop()

    def add_check_button(self, text: str, onvalue: str, var: tk.StringVar):
        """create a Checkbutton widget with the specified text,
          onvalue and textvariable, and command.
        Args:
           self: Reference to the current object of the class.
           text (str): The text to be displayed next to the checkbutton.
           onvalue: The value to be assigned to the check_var when
            the checkbutton is selected.
           var: The variable to be associated with the Checkbutton and
           store its state.
        Returns:
           None
        """
        check_button = ttk.Checkbutton(
            self.check_buttons_frame,
            text=text,
            variable=var,
            command=self.validate_lang_var,
            onvalue=onvalue,
            offvalue="",
        )
        check_button.pack()

    def load_easyocr_model(self):
        """Loads the EasyOCR model for the specified language.
        Args:
           self: Reference to the current object of the class.
        Returns:
           None
        """
        self.easy_ocr["lang"] = self.easyocr_lang
        self.easy_ocr["model"] = easyocr.Reader(self.easyocr_lang)

    def validate_lang_var(self):
        """Validate the language variables.
        Args:
           self: A reference to the current instance of the class.
        Returns:
           None
        """
        en_var = self.check_eng_var.get()
        ru_var = self.check_rus_var.get()

        if not en_var and not ru_var:
            self.check_eng_var.set("eng")

        # adapt lang variables to work with easyocr by removing third letter
        marked_languages = [lang[:-1] for lang in (en_var, ru_var) if lang]

        if self.easyocr_lang != marked_languages:
            self.easyocr_lang = marked_languages
            self.loading_easyocr_var.set("Загрузка EasyOCR")

            self.update()
            self.load_easyocr_model()
            self.loading_easyocr_var.set("EasyOCR загружен")

    def show_window(self):
        """Deiconify the window, make it visible if it was
           previously hidden.
        Args:
           self: A reference to the App.
        Returns:
           None
        """
        self.after(0, self.deiconify)

    def quit_window(self, icon):
        self.debug_window.window.destroy()
        self.show_window()
        self.quit()

        icon.visible = False
        icon.stop()

    def check_lang_var(self):
        eng_var = self.check_eng_var.get()
        rus_var = self.check_rus_var.get()

        if eng_var and rus_var:
            languages = f"{eng_var}+{rus_var}"

        elif not eng_var and rus_var:
            languages = rus_var

        else:
            languages = eng_var

        return languages

    def snip_trigger(self, image, coordinates):
        # add message to debug window that screenshot is received successfully
        self.debug_window.add_message("Скриншот был получен", "green")
        self.update()

        # get languages from tkinter variables
        languages = self.check_lang_var()

        # get recognized text from image via PyTesseract and EasyOCR
        recognition_result = TextRecognition(
            image, languages, self.easy_ocr, self.debug_window
        )
        text = recognition_result.get_text()

        print(f"[INFO]Исходный текст={text}")

        # get chosen translator from variable and put it on debug window
        translator = self.translator_var.get()
        self.debug_window.add_message(
            f"Перевод при помощи —\n{translator}\n",
            color="white",
        )
        self.update()

        # get translated text
        translated_text = translation(
            text=text,
            from_lang=languages,
            to_lang="russian",
            translator=translator,
        )

        if translator == "Faster ChatGPT streaming":
            self.faster_gpt_stream = True

        # add recognized text to clipboard if checkbutton is selected
        if self.clipboard_var.get():
            pyclip.copy(text)

        # put translated text on the screen in a new tkinter window
        x1, y1 = coordinates
        TranslatedWindow(
            self,
            image,
            {
                "text": text,
                "translated_text": translated_text,
                "coordinates": (x1, y1),
            },
            self.debug_window,
            self.faster_gpt_stream,
        )
        self.debug_window.add_message("Перевод прошел успешно!", "green")
        self.faster_gpt_stream = False


if __name__ == "__main__":
    app = App()
