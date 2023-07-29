import os
import tkinter as tk
from time import sleep
from tkinter import ttk

import g4f
import keyboard
from PIL import ImageTk
from deep_translator import GoogleTranslator, ChatGptTranslator

from components.debug_window import DebugWindow


def translation(text, from_lang, to_lang, translator="google"):
    print(f"[INFO]using {translator}")
    match translator:
        case "Google Translator":
            if from_lang not in ("ru", "en"):
                from_lang_checked = "auto"
            else:
                from_lang_checked = from_lang

            translator_obj = GoogleTranslator(
                source=from_lang_checked,
                target=to_lang,
            )
            return translator_obj.translate(text=text)

        case "ChatGPT":
            translator_obj = ChatGptTranslator(
                api_key=os.environ["GPT_API_KEY"],
                target=gpt_lang_convert(to_lang),
            )

            return translator_obj.translate(text=text)

        case "Faster ChatGPT":
            from_lang_conv = gpt_lang_convert(from_lang)
            to_lang_conv = gpt_lang_convert(to_lang)
            return better_gpt(text, from_lang_conv, to_lang_conv)

        case "Faster ChatGPT streaming":
            from_lang_conv = gpt_lang_convert(from_lang)
            to_lang_conv = gpt_lang_convert(to_lang)
            return better_gpt(
                text, from_lang_conv, to_lang_conv, use_stream=True
            )


def better_gpt(text, from_lang, to_lang, use_stream=False):
    request = f"Please translate the user message from {from_lang} to\
     {to_lang}. Make the translation sound as natural as possible.\
      In answer write only translation.\n\n {text}"

    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        provider=g4f.Provider.GetGpt,
        messages=[{"role": "user", "content": request}],
        stream=use_stream,
    )
    return response


def gpt_lang_convert(language):
    print("gpt_lang_convert", language)
    match language:
        case "eng":
            return "english"
        case "rus":
            return "russian"
        case "eng+rus":
            return "english and russian"
        case _:
            return language


class TranslatedWindow:
    """Create a tkinter window for displaying translated text"""
    def __init__(self, app, image, text_related, debug_window, use_gpt_stream):
        self.image = image
        self.original_text = text_related["text"]
        self.translated_text = text_related["translated_text"]
        self.coordinates = text_related["coordinates"]
        self.use_gpt_stream = use_gpt_stream
        self.debug_window: DebugWindow = debug_window

        # create new window to display recognized and translated text
        self.new_window = tk.Toplevel(app)
        self.new_window.overrideredirect(True)
        self.new_window.attributes("-topmost", True)

        # ensure that translation window is in the focus to make
        # <FocusOut> 100% work
        self.new_window.after(1, lambda: self.new_window.focus_force())
        self.new_window.bind("<FocusOut>", lambda event: self.window_trigger())

        self.new_window.bind(
            "<ButtonRelease>", lambda event: self.window_trigger()
        )

        # add hotkey to close this window if needed
        keyboard.add_hotkey("escape", callback=self.window_trigger)

        # change window position to the place where user took a screenshot
        x1, y1 = self.coordinates
        self.new_window.geometry(f"+{int(x1)}+{int(y1)}")

        # pack frame with image
        image_frame = self.frame_with_borders(self.new_window)

        tkinter_image = ImageTk.PhotoImage(image)
        label_image = tk.Label(image_frame, image=tkinter_image)
        label_image.image = tkinter_image
        label_image.pack()

        # get width for both labels, so they adapt to the width of image
        self.width = image.size[0]

        # create and pack label with Recognized text
        recognized_text_frame = self.frame_with_borders(self.new_window)
        recognized_text_label = self.custom_label(
            recognized_text_frame,
            self.original_text,
        )

        recognized_text_label.pack(expand=True, fill="x")

        # create and pack label with Translated text
        translated_text_frame = self.frame_with_borders(self.new_window)

        if self.use_gpt_stream:
            self.translation_var = tk.StringVar()

            translated_text_label = self.custom_label(
                translated_text_frame,
                self.translation_var,
                is_variable=True,
            )
        else:
            translated_text_label = self.custom_label(
                translated_text_frame,
                self.translated_text,
            )

        translated_text_label.pack(expand=True, fill="x")

        # start loop if translated text is not a str, but generator
        if self.use_gpt_stream:
            self.stream_loop()

    @staticmethod
    def frame_with_borders(new_window: tk.Toplevel):
        """Create a new frame with borders inside the given window"""
        image_frame = tk.Frame(
            new_window,
            highlightbackground="black",
            highlightthickness=1,
        )
        image_frame.pack(expand=True, fill="both")
        return image_frame

    def custom_label(self, frame, text: str | tk.StringVar, is_variable=False):
        """Create a custom label with specified parameters"""
        arguments = {
            "master": frame,
            "background": "light grey",
            "wraplength": self.width,
            "font": ("Arial", 12),
            "anchor": "center",
        }
        if is_variable:
            arguments["textvariable"] = text
        else:
            arguments["text"] = text

        return ttk.Label(**arguments)

    def window_trigger(self):
        self.debug_window.clear_text_area()
        self.debug_window.tkinter_withdraw()
        self.new_window.destroy()

    def stream_loop(self):
        """Display translated text in real-time if GPT stream is used"""
        word = ""
        for elem in self.translated_text:
            sleep(0.07)
            for char in elem:
                if char.isalpha():
                    word += char
                else:
                    current_text = self.translation_var.get()
                    self.translation_var.set(current_text + word + char)

                    self.new_window.update()
                    word = ""
