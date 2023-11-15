import os
import tkinter as tk
from time import sleep

import keyboard
import openai
from PIL import ImageTk

from ocrhelper.gui_parts.debug_window import DebugWindow

api_key = os.getenv('GPT_API_KEY')
openai.api_key = api_key


class TranslationWindow:
    """Create a tkinter window for displaying translated text"""

    def __init__(self, gui, debug_window, image, text_related):
        self.gui = gui
        self.debug_window: DebugWindow = debug_window
        self.image = image
        self.original_text = text_related['text']
        self.translated_text = text_related['translated_text']
        self.coordinates = text_related['coordinates']
        self.use_gpt_stream = text_related['use_gpt_stream']

        self._create_transl_window()

        # change window position to the place where user took a screenshot
        x1, y1 = self.coordinates
        self.transl_window.geometry(f'+{int(x1)}+{int(y1)}')

        self._pack_screenshot()

        # get width for both labels, so they adapt to the width of image
        self.width = image.size[0]

        self._pack_recognized_text()
        self._pack_translated_text()

        if not isinstance(self.translated_text, str):
            self.stream_loop()

    def _create_transl_window(self):
        self.transl_window = tk.Toplevel(self.gui)
        self.transl_window.overrideredirect(True)
        self.transl_window.attributes('-topmost', True)

        self.transl_window.bind(
            '<FocusOut>', lambda event: self.close_transl_window()
        )

        self.transl_window.bind(
            '<ButtonRelease>', lambda event: self.close_transl_window()
        )

        # ensure that translation window is in the focus to make
        # <FocusOut> 100% work
        self.transl_window.after(1, lambda: self.transl_window.focus_force())

        keyboard.add_hotkey('escape', callback=self.close_transl_window)

    def _pack_screenshot(self):
        image_frame = self.frame_with_borders(self.transl_window)
        tkinter_image = ImageTk.PhotoImage(self.image)

        label_image = tk.Label(image_frame, image=tkinter_image)
        label_image.image = tkinter_image
        label_image.pack()

    def _pack_recognized_text(self):
        recognized_text_frame = self.frame_with_borders(self.transl_window)
        recognized_text_label = self.custom_label(
            recognized_text_frame,
            self.original_text,
        )
        recognized_text_label.pack(expand=True, fill='x')

    def _pack_translated_text(self):
        translated_text_frame = self.frame_with_borders(self.transl_window)

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

        translated_text_label.pack(expand=True, fill='x')

    def custom_label(self, frame, text: str | tk.StringVar, is_variable=False):
        """Create a custom label with specified parameters"""
        arguments = {
            'master': frame,
            'background': 'light grey',
            'wraplength': self.width,
            'font': ('Arial', 12),
            'anchor': 'center',
        }
        if is_variable:
            arguments['textvariable'] = text
        else:
            arguments['text'] = text

        return tk.Label(**arguments)

    def close_transl_window(self):
        self.debug_window.clear_text_area()
        self.debug_window.tkinter_withdraw()
        self.transl_window.destroy()

    def stream_loop(self):
        """Display translated text in real-time if GPT stream is used"""
        word = ''
        for chunk in self.translated_text:
            sleep(0.07)
            delta: dict = chunk['choices'][0]['delta']
            try:
                for char in delta['content']:
                    word = self.extend_stream_string(char, word)
            except KeyError:
                break

    def extend_stream_string(self, char, word):
        if char.isalpha():
            word += char
        else:
            current_text = self.translation_var.get()
            self.translation_var.set(current_text + word + char)

            self.transl_window.update()
            word = ''
        return word

    @staticmethod
    def frame_with_borders(new_window: tk.Toplevel):
        """Create a new lg_frames with borders inside the given window"""
        image_frame = tk.Frame(
            new_window,
            highlightbackground='grey',
            highlightthickness=1,
        )
        image_frame.pack(expand=True, fill='both')
        return image_frame
