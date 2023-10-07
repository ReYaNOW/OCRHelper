import tkinter as tk
from tkinter import ttk

import customtkinter as ctk
from tkextrafont import Font
from loguru import logger
import easyocr
import keyboard
import numpy
import pyperclip
import pystray
from PIL import Image, ImageTk
from pystray import MenuItem as item

from ocrhelper.components.debug_window import DebugWindow
from ocrhelper.components.ocr import TextRecognition
from ocrhelper.components.snip import SnippingTool
from ocrhelper.components.translation import translation, TranslatedWindow
from ocrhelper.components.settings_frame import SettingsFrame


class App(ctk.CTk):
    """Create a GUI for an OCR (Optical Character Recognition) application.

    Also load an EasyOCR model upon initialization.
    """

    def __init__(self):
        self.easyocr_model = None
        self.faster_gpt_stream = False

        super().__init__(fg_color="#262834")
        self.title('OCR Helper')
        self.geometry("670x300")
        self.iconbitmap(r'assets\icon.ico')
        
        self.withdraw()

        # Styles
        # self.call("source", r"theme\sv.tcl")
        # self.call("set_theme", "sv-dark")

        # tray
        image = Image.open(r'assets\icon.ico')

        menu = (
            item('Open menu', self.show_window, default=True),
            item('Exit', self.quit_window),
        )

        icon = pystray.Icon('OCRHelper', image, 'OCRHelper', menu)
        icon.run_detached()
        self.protocol('WM_DELETE_WINDOW', lambda: self.withdraw())

        # add debug window
        self.debug_window = DebugWindow(self)

        self.snipping_tool = SnippingTool(
            self, self.update, self.snip_trigger, self.debug_window
        )
        
        keyboard.add_hotkey(
            'ctrl + shift + x',
            callback=self.snipping_tool.display_snipping_tool,
        )

        # load font if it is not installed in the system
        if 'Rubik' not in tk.font.families():
            Font(file="Rubik.ttf")

        self.mode_var = ctk.StringVar(self, 'translation')
        translator_mode_button = self.create_mode_button(
            'Перевод', 'translation'
        )
        translator_mode_button.place(relx=0.073, rely=0.353)

        dict_mode_button = self.create_mode_button('Словарь', 'dict')
        dict_mode_button.place(relx=0.389, rely=0.353)

        decrypt_mode_button = self.create_mode_button('Decrypt', 'decrypt')
        decrypt_mode_button.place(relx=0.705, rely=0.353)

        self.settings_im = self.open_tk_img('assets/settings.png')
        self.settings_im_dark = self.open_tk_img('assets/settings dark.png')

        self.settings_button = tk.Button(
            image=self.settings_im,
            command=self.animate,
            borderwidth=0,
            highlightthickness=0,
            disabledforeground='#262834',
            activebackground='#262834',
            background='#262834',
            width=45,
            height=45,
            relief="flat",
        )
        self.settings_button.place(relx=0.919, rely=0.825)

        self.bind_button(
            '<Enter>', self.settings_button, self.settings_im_dark
        )
        self.bind_button('<Leave>', self.settings_button, self.settings_im)

        self.settings_frame = SettingsFrame(
            self,
            settings_im=self.settings_im,
            settings_im_dark=self.settings_im_dark,
        )
        self.settings_frame.place(relx=0, rely=0, anchor='sw')
        self.get_selected_languages = (
            self.settings_frame.get_selected_languages
        )
        self.get_selected_translator = (
            self.settings_frame.get_selected_translator
        )
        self.need_copy_to_clipboard = (
            self.settings_frame.need_copy_to_clipboard
        )

        self.animation_started = False
        self.settings_on_screen = False
        self.pos = 0
        self.start_pos = 1
        self.end_pos = 0

        self.after(20, self.easyocr_first_time_load)
        # run
        self.mainloop()

    def easyocr_first_time_load(self):
        
        self.load_easyocr_model()
        img = Image.open('load_easyocr.png')
        # self.easy_ocr['model'].readtext(numpy.array(img))
        self.easyocr_model.readtext(numpy.array(img))
        
        self.update()
        self.deiconify()

    def animate(self):
        if not self.animation_started:
            self.animation_started = True
            if not self.settings_on_screen:
                self.animate_forward()
            else:
                self.animate_backwards()

    def animate_forward(self):
        if self.pos < self.start_pos:
            self.pos += 0.035
            self.settings_frame.place(relx=0, rely=self.pos, anchor='sw')
            self.settings_button.lift()
            self.after(15, self.animate_forward)
        else:
            self.animation_started = False
            self.settings_on_screen = True

    def animate_backwards(self):
        if self.pos > self.end_pos:
            self.pos -= 0.035
            self.settings_frame.place(relx=0, rely=self.pos, anchor='sw')
            self.settings_button.lift()
            self.after(15, self.animate_backwards)
        else:
            self.animation_started = False
            self.settings_on_screen = False

    def create_mode_button(self, text, mode):
        return ctk.CTkButton(
            self,
            command=lambda: self.change_mode_var(mode),
            font=('Rubik bold', 20),
            text=text,
            fg_color='#5429FE',
            hover_color='#4a1e9e',
            width=147,
            height=89,
            corner_radius=20,
        )

    def bind_button(self, type_of_bind, button: tk.Button, image: ImageTk):
        button.bind(
            type_of_bind,
            lambda e: self.change_button_color(button, image),
        )

    def change_mode_var(self, mode):
        self.mode_var = mode

    @staticmethod
    def change_button_color(button: tk.Button, image: ImageTk):
        button.configure(image=image)
        button.image = image

    @staticmethod
    def open_tk_img(path_to_image: str):
        image = Image.open(path_to_image)
        image_tk = ImageTk.PhotoImage(image, size=(96, 96))
        return image_tk


    def load_easyocr_model(self, first_time_load = False):
        # self.easy_ocr['lang'] = self.easyocr_langs
        # logger.info(
        #     f'Загрузка модели EasyOCR c {", ".join(self.easyocr_langs)}'
        # )
        if first_time_load:
            languages = ['en']
        else:
            languages = self.get_selected_languages()
        logger.info(f'Загрузка модели EasyOCR c ' f'{", ".join(languages)}')

        # self.easy_ocr['model'] = easyocr.Reader(self.easyocr_langs)
        self.easyocr_model = easyocr.Reader(languages)
        logger.success('Модель EasyOCR была успешно загружена')

    def show_window(self):
        """Deiconify the window, make it visible if it was
        previously hidden.
        """
        self.after(0, self.deiconify)

    def quit_window(self, icon):
        self.debug_window.window.destroy()
        self.show_window()
        self.quit()

        icon.visible = False
        icon.stop()

    def snip_trigger(self, image: Image.Image, coordinates: tuple):
        """Trigger when a screenshot is taken. Performs OCR on the image,
         translates the text, and displays the result.

        Args:
            image: The captured screenshot image.

            coordinates: The coordinates of the captured screenshot.
        """
        # add message to debug window that screenshot is received successfully
        self.debug_window.add_message('Скриншот был получен', 'green')
        self.update()

        # get languages from tkinter variables
        # languages = self.check_lang_var()
        languages = self.get_selected_languages()

        # get recognized text from image via PyTesseract and EasyOCR
        recognition_result = TextRecognition(
            image, languages, self.easyocr_model, self.debug_window
        )
        text = recognition_result.get_text()

        # get chosen translator from variable and put it on debug window
        translator = self.get_selected_translator()
        self.debug_window.add_message(
            f'Перевод при помощи —\n{translator}\n',
            color='white',
        )
        self.update()

        # get translated text
        translated_text = translation(
            text=text,
            from_lang=languages,
            to_lang='russian',
            translator=translator,
        )

        logger.success('Текст успешно переведен')
        logger.info(f'Переведенный текст = {translated_text}')

        if translator == 'Faster ChatGPT streaming':
            self.faster_gpt_stream = True

        # add recognized text to clipboard if checkbutton is selected
        if self.need_copy_to_clipboard():
            pyperclip.copy(text)

        # put translated text on the screen in a new tkinter window
        x1, y1 = coordinates
        TranslatedWindow(
            self,
            image,
            {
                'text': text,
                'translated_text': translated_text,
                'coordinates': (x1, y1),
            },
            self.debug_window,
            self.faster_gpt_stream,
        )
        self.debug_window.add_message('Перевод прошел успешно!', 'green')
        self.faster_gpt_stream = False


if __name__ == "__main__":
    app = App()
