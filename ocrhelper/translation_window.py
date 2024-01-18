import tkinter as tk
from time import sleep

import keyboard
from PIL import ImageTk

from ocrhelper.gui_parts.debug_window import DebugWindow


class ResultWindow:
    def __init__(self, gui, debug_window, image, text_related):
        self.gui = gui
        self.debug_window: DebugWindow = debug_window
        self.image = image
        self.width = image.size[0]
        self.recognized_text = text_related['text']
        self.coordinates = text_related['coordinates']

        self._create_transl_window()

        # change window position to the place where the user took a screenshot
        x1, y1 = self.coordinates
        self.window.geometry(f'+{int(x1)}+{int(y1)}')

        self._pack_screenshot()

    def _create_transl_window(self):
        self.window = tk.Toplevel(self.gui)
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)

        self.window.bind('<FocusOut>', lambda event: self.close_window())

        self.window.bind('<ButtonRelease>', lambda event: self.close_window())

        # ensure that translation window is in the focus to make
        # <FocusOut> 100% work
        self.window.after(1, lambda: self.window.focus_force())

        keyboard.add_hotkey('escape', callback=self.close_window)

    def _pack_screenshot(self):
        image_frame = self._pack_frame_with_borders(self.window)
        tkinter_image = ImageTk.PhotoImage(self.image)

        label_image = tk.Label(image_frame, image=tkinter_image)
        label_image.image = tkinter_image
        label_image.pack()

    def _pack_recognized_text(self):
        recognized_text_frame = self._pack_frame_with_borders(self.window)
        recognized_text_label = self.custom_label(
            recognized_text_frame,
            self.recognized_text,
        )
        recognized_text_label.pack(expand=True, fill='x')

    def _pack_second_window_text(self):
        self.translated_text_frame = self._pack_frame_with_borders(self.window)

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

    def close_window(self):
        self.debug_window.clear_text_area()
        self.debug_window.tkinter_withdraw()
        self.window.destroy()

    @staticmethod
    def _pack_frame_with_borders(new_window: tk.Toplevel):
        """Create a new frame with borders inside the given window"""
        frame = tk.Frame(
            new_window,
            bg='#202020',
            highlightbackground='grey',
            highlightthickness=1,
        )
        frame.pack(expand=True, fill='both')
        return frame


class TranslationWindow(ResultWindow):
    """Create a tkinter window for displaying translated text"""

    def __init__(self, gui, debug_window, image, text_related):
        super().__init__(gui, debug_window, image, text_related)
        self.translated_text = text_related['other_text']
        self.use_gpt_stream = text_related['use_gpt_stream']

        self.width = image.size[0] if image.size[0] > 200 else 200
        self._pack_recognized_text()
        self._pack_translated_text()

        if not isinstance(self.translated_text, str):
            self.stream_loop()

    def _pack_translated_text(self):
        translated_text_frame = self._pack_frame_with_borders(self.window)

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

            self.window.update()
            word = ''
        return word


class DictionaryWindow(ResultWindow):
    def __init__(self, gui, debug_window, image, text_related):
        super().__init__(gui, debug_window, image, text_related)
        self.dictionary_text = text_related['other_text']

        self.width = image.size[0] if image.size[0] > 500 else 500
        self._pack_recognized_text()
        self._pack_dictionary_text()

    def _pack_dictionary_text(self):
        dictionary_text_frame = self._pack_frame_with_borders(self.window)

        dictionary_text_label = self.custom_label(
            dictionary_text_frame,
            self.dictionary_text,
        )
        dictionary_text_label.pack(expand=True, fill='x')
