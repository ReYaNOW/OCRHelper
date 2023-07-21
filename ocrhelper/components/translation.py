from deep_translator import GoogleTranslator, ChatGptTranslator
from PIL import ImageTk
from tkinter import ttk
import tkinter as tk
import g4f
import os


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
    match language:
        case "en":
            return "english"
        case "ru":
            return "russian"
        case "en+ru":
            return "english and russian"
        case _:
            return language


class TranslatedWindow:
    def __init__(self, image, original_text, translated_text, coordinates):
        self.image = image
        self.original_text = original_text
        self.translated_text = translated_text
        self.coordinates = coordinates

        new_window = tk.Toplevel()
        new_window.overrideredirect(True)
        new_window.attributes("-topmost", True)

        new_window.after(1, lambda: new_window.focus_force())
        new_window.bind("<FocusOut>", lambda event: new_window.destroy())
        new_window.bind("<ButtonRelease>", lambda event: new_window.destroy())

        self.width = image.size[0]
        x1, y1 = coordinates
        new_window.geometry(f"+{int(x1)}+{int(y1)}")

        # frame with image
        image_frame = self.frame_with_borders(new_window)

        tkinter_image = ImageTk.PhotoImage(image)
        label_image = tk.Label(image_frame, image=tkinter_image)
        label_image.pack()

        # frame with recognized text
        recognized_text_frame = self.frame_with_borders(new_window)
        recognized_text_label = self.custom_label(
            recognized_text_frame,
            original_text,
        )

        recognized_text_label.pack(expand=True, fill="x")

        # frame with translated text
        translated_text_frame = self.frame_with_borders(new_window)
        translated_text_label = self.custom_label(
            translated_text_frame,
            translated_text,
        )
        translated_text_label.pack(expand=True, fill="x")

        new_window.mainloop()

    @staticmethod
    def frame_with_borders(new_window):
        image_frame = tk.Frame(
            new_window,
            highlightbackground="black",
            highlightthickness=1,
        )
        image_frame.pack(expand=True, fill="both")
        return image_frame

    def custom_label(self, frame, text):
        return ttk.Label(
            frame,
            text=text,
            background="light grey",
            wraplength=self.width,
            font=("Arial", 12),
            anchor="center",
        )
