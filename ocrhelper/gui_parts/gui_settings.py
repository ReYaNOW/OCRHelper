import tkinter as tk
from typing import Callable

from PIL import Image, ImageTk

import customtkinter as ctk


class SettingsFrame(ctk.CTkFrame):
    def __init__(
        self, master, load_ocr: Callable, settings_im, settings_im_dark
    ):
        super().__init__(master, fg_color="#262834", width=670, height=300)
        self.load_ocr = load_ocr
        self.settings_im = settings_im
        self.settings_im_dark = settings_im_dark

        languages_frame = LanguagesFrame(self, load_ocr)
        languages_frame.place(relx=0.2375, rely=0.24, anchor='center')
        self.get_selected_languages = languages_frame.get_selected_languages

        translators_frame = TranslatorsFrame(self)
        translators_frame.place(relx=0.2375, rely=0.638, anchor='center')
        self.get_selected_translator = (
            translators_frame.get_selected_translator
        )

        self.palette_frame = PaletteFrame(self)
        self.palette_frame.place(relx=0.73, rely=0.406, anchor='center')
        self.get_rect_color = self.palette_frame.get_rect_color

        self.options_window = OptionsWindow(self)
        self.addit_sett_button = ctk.CTkButton(
            self,
            font=('Rubik bold', 16),
            text='Дополнительные настройки',
            fg_color='#5429FE',
            hover_color='#4a1e9e',
            command=self.open_option_window,
            height=45,
            corner_radius=20,
        )
        self.addit_sett_button.place(relx=0.2375, rely=0.885, anchor='center')
        self.additional_settings = ctk.CTkFrame(self)

    def open_option_window(self):
        self.options_window.update()
        self.options_window.deiconify()


class LanguagesFrame(ctk.CTkFrame):
    def __init__(self, settings_frame: SettingsFrame, load_ocr: Callable):
        self.load_ocr = load_ocr
        self.button_pressed = None

        super().__init__(
            settings_frame,
            bg_color='#262834',
            fg_color='#202020',
            width=300,
            height=130,
        )

        languages_label = ctk.CTkLabel(
            self,
            text="Языки для распознавания",
            fg_color="#5429FE",
            font=("Rubik bold", 19),
            corner_radius=20,
        )
        languages_label.place(relx=0.5, rely=0.23, anchor='center')

        self.eng_var, eng_option = self.create_lang_option('ENG')
        eng_option.place(relx=0.3, rely=0.525, anchor='center')

        self.rus_var, rus_option = self.create_lang_option('RUS')
        rus_option.place(relx=0.55, rely=0.525, anchor='center')

        self.jap_var, jap_option = self.create_lang_option('JAP')
        jap_option.place(relx=0.80, rely=0.525, anchor='center')

        change_button = ctk.CTkButton(
            self,
            font=('Rubik bold', 16),
            text='Сменить',
            command=self.press_load_ocr_btn,
            fg_color='#5429FE',
            hover_color='#4a1e9e',
            width=65,
            height=30,
            corner_radius=20,
        )
        change_button.place(relx=0.5, rely=0.808, anchor='center')

    def press_load_ocr_btn(self):
        if self.button_pressed:
            return
        self.button_pressed = True
        self.load_ocr()
        self.button_pressed = False

    def create_lang_option(self, language: str):
        lang_var = ctk.StringVar(self, language)
        lang_option = ctk.CTkCheckBox(
            self,
            command=self.validate_lang_var,
            fg_color='#5429FE',
            hover_color='#4a1e9e',
            text=language,
            font=("Rubik", 16),
            variable=lang_var,
            onvalue=language,
            offvalue='',
        )
        if lang_var.get() != 'ENG':
            lang_var.set('')
        return lang_var, lang_option

    def validate_lang_var(self):
        if not self.get_selected_languages():
            self.eng_var.set('ENG')

    def get_selected_languages(self):
        languages = self.eng_var.get(), self.rus_var.get(), self.jap_var.get()
        # change to 2 char version to work with EasyOCR
        return [lang[:-1].lower() for lang in languages if lang != '']


class TranslatorsFrame(ctk.CTkFrame):
    def __init__(self, settings_frame: SettingsFrame):
        super().__init__(
            settings_frame,
            bg_color='#262834',
            fg_color='#202020',
            width=300,
            height=90,
        )

        translator_label = ctk.CTkLabel(
            self,
            text='Переводчик',
            fg_color="#5429FE",
            font=("Rubik bold", 19),
            corner_radius=20,
        )
        translator_label.place(relx=0.5, rely=0.23, anchor='center')

        self.translator_var = ctk.StringVar(self, 'Google')
        translators_segmented_btn = ctk.CTkSegmentedButton(
            self,
            values=["Google", "GPT", 'GPT Stream'],
            variable=self.translator_var,
            font=("Rubik", 17),
            selected_color="#5429FE",
            selected_hover_color="#4a1e9e",
        )
        translators_segmented_btn.place(relx=0.5, rely=0.683, anchor='center')

    def get_selected_translator(self):
        return self.translator_var.get()


class PaletteFrame(ctk.CTkFrame):
    def __init__(self, settings: SettingsFrame):
        super().__init__(
            settings,
            bg_color='#262834',
            fg_color='#202020',
            width=342,
            height=230,
        )

        self.rect_color = '#b800cf'

        self.example_canvas = ctk.CTkCanvas(
            self, width=315, height=55, highlightthickness=0
        )
        self.example_canvas.place(relx=0.5, rely=0.84, anchor='center')

        red_widgets = self.create_color_labels_and_slider('Red', 'red', 184)
        red_label, red_label_value, red_var, red_slider = red_widgets
        red_label.place(relx=0.1, rely=0.35, anchor='center')
        red_label_value.place(relx=0.225, rely=0.35, anchor='center')
        red_slider.place(relx=0.58, rely=0.35, anchor='center')

        green_widgets = self.create_color_labels_and_slider(
            'Green', '#00E81A', 0
        )
        green_label, green_label_value, green_var, green_slider = green_widgets
        green_label.place(relx=0.1, rely=0.5, anchor='center')
        green_label_value.place(relx=0.225, rely=0.5, anchor='center')
        green_slider.place(relx=0.58, rely=0.5, anchor='center')

        blue_widgets = self.create_color_labels_and_slider(
            'Blue', '#0376FF', 207
        )
        blue_label, blue_label_value, blue_var, blue_slider = blue_widgets
        blue_label.place(relx=0.1, rely=0.65, anchor='center')
        blue_label_value.place(relx=0.225, rely=0.65, anchor='center')
        blue_slider.place(relx=0.58, rely=0.65, anchor='center')

        example_img = Image.open('assets/example_image.png')
        example_img_ctk = ImageTk.PhotoImage(example_img)
        self.example_canvas.image = example_img_ctk
        self.example_canvas.create_image(
            -7, 0, anchor='nw', image=example_img_ctk
        )
        self.rect = self.example_canvas.create_rectangle(
            3, 10, 312, 50, outline='#b800cf', width=2
        )

        self.red_var = red_var
        self.green_var = green_var
        self.blue_var = blue_var
        red_slider.configure(command=self.change_rect_color)
        green_slider.configure(command=self.change_rect_color)
        blue_slider.configure(command=self.change_rect_color)

        hex_label = ctk.CTkLabel(self, text='HEX :', font=("Rubik bold", 15))
        hex_label.place(relx=0.285, rely=0.15, anchor='center')

        self.hex_var = ctk.StringVar(self, '#b800cf')
        self.hex_entry = ctk.CTkEntry(self, textvariable=self.hex_var)
        self.hex_entry.place(relx=0.365, rely=0.09)
        self.hex_entry.bind("<Leave>", lambda event: self.focus())

        self.return_im = self.open_tk_img(r'assets/return default.png')
        self.return_im_dark = self.open_tk_img(
            r'assets/return default dark.png'
        )

        self.return_button = self.create_button_with_preset(
            self.return_im, self.return_rect_color_to_default
        )
        self.return_button.place(relx=0.04, rely=0.05)

        self.bind_button('<Enter>', self.return_button, self.return_im_dark)
        self.bind_button('<Leave>', self.return_button, self.return_im)

        self.change_im = self.open_tk_img(r'assets/change color.png')
        self.change_im_dark = self.open_tk_img(r'assets/change color dark.png')

        self.change_button = self.create_button_with_preset(
            self.change_im, command=self.change_color_from_entry
        )
        self.change_button.place(relx=0.825, rely=0.05)

        self.bind_button('<Enter>', self.change_button, self.change_im_dark)
        self.bind_button('<Leave>', self.change_button, self.change_im)

    def create_color_labels_and_slider(self, color_name: str, color, start_v):
        color_label = ctk.CTkLabel(
            self,
            text=color_name,
            text_color=color,
            font=("Rubik bold", 15),
        )

        color_var = ctk.IntVar(self, start_v)
        color_label_value = ctk.CTkLabel(
            self,
            text_color=color,
            font=("Rubik", 15),
            textvariable=color_var,
        )

        color_slider = ctk.CTkSlider(
            self,
            from_=0,
            to=255,
            progress_color=color,
            button_color='#5429FE',
            button_hover_color='#4a1e9e',
            variable=color_var,
        )
        return color_label, color_label_value, color_var, color_slider

    def change_rect_color(self, _=None):
        r, g, b = self.red_var.get(), self.green_var.get(), self.blue_var.get()
        hex_color = f'#{r:02x}{g:02x}{b:02x}'

        self.rect_color = hex_color
        self.example_canvas.itemconfigure(self.rect, outline=hex_color)

    def return_rect_color_to_default(self):
        self.red_var.set(184)
        self.green_var.set(0)
        self.blue_var.set(207)
        self.hex_var.set("#b800cf")
        self.change_rect_color()

    def change_color_from_entry(self):
        if len(self.hex_var.get()) == 7:
            hex_color = self.hex_entry.get()
            red_hex = hex_color[1:3]
            green_hex = hex_color[3:5]
            blue_hex = hex_color[5:7]

            self.red_var.set(int(red_hex, base=16))
            self.green_var.set(int(green_hex, base=16))
            self.blue_var.set(int(blue_hex, base=16))
            self.change_rect_color()

    def create_button_with_preset(self, image, command):
        return tk.Button(
            self,
            image=image,
            command=command,
            borderwidth=0,
            highlightthickness=0,
            activebackground='#202020',
            background='#202020',
            width=48,
            height=48,
            relief="flat",
        )

    def bind_button(self, type_of_bind, button: tk.Button, image: ImageTk):
        button.bind(
            type_of_bind,
            lambda e: self.change_button_color(button, image),
        )

    def get_rect_color(self):
        return self.rect_color

    @staticmethod
    def change_button_color(button: tk.Button, image: ImageTk):
        button.configure(image=image)
        button.image = image

    @staticmethod
    def open_tk_img(path_to_image: str):
        image = Image.open(path_to_image)
        image_tk = ImageTk.PhotoImage(image, size=(96, 96))
        return image_tk


class OptionsWindow(ctk.CTkToplevel):
    def __init__(self, settings_frame):
        super().__init__(
            settings_frame, width=292, height=280, fg_color='#4a1e9e'
        )

        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_coordinate = int((screen_width / 2) - (292 / 2))
        y_coordinate = int((screen_height / 2) - (280 / 2))

        self.geometry(f'+{x_coordinate}+{y_coordinate}')
        self.overrideredirect(True)
        self.withdraw()

        frame = ctk.CTkFrame(
            self,
            width=292,
            height=280,
            fg_color='#262834',
            border_width=5,
            border_color='#4a1e9e',
        )
        frame.pack()

        self.clipboard_frame = OptionsFrame(
            frame, 'Добавлять распознанный', 'текст в буфер обмена'
        )
        self.clipboard_frame.place(relx=0.5, rely=0.1875, anchor='center')

        self.debug_frame = OptionsFrame(frame, 'Использовать debug', 'окно')
        self.debug_frame.place(relx=0.5, rely=0.54, anchor='center')

        save_button = ctk.CTkButton(
            frame,
            font=('Rubik bold', 16),
            text='Сохранить',
            fg_color='#5429FE',
            hover_color='#4a1e9e',
            command=self.withdraw,
            height=45,
            corner_radius=20,
        )
        save_button.place(relx=0.5, rely=0.85, anchor='center')

    def get_var_values(self):
        return {
            'need_copy_to_clipboard': self.clipboard_frame.get_var_value(),
            'use_debug_window': self.debug_frame.get_var_value(),
        }


class OptionsFrame(ctk.CTkFrame):
    def __init__(self, settings: ctk.CTkFrame, text1, text2):
        super().__init__(
            settings,
            bg_color='#262834',
            fg_color='#202020',
            corner_radius=20,
            width=275,
            height=90,
        )

        label = ctk.CTkLabel(
            self,
            text=text1,
            font=("Rubik", 18),
            cursor='hand2',
        )
        label.place(relx=0.5, rely=0.35, anchor='center')

        self.var = ctk.BooleanVar(self, False)
        self.checkbox = ctk.CTkCheckBox(
            self,
            font=("Rubik", 18),
            text=text2,
            fg_color='#5429FE',
            hover_color='#4a1e9e',
            variable=self.var,
        )
        self.checkbox.place(relx=0.5, rely=0.59, anchor='center')

        label.bind("<Enter>", self.on_enter)
        label.bind("<Leave>", self.on_leave)
        label.bind(
            "<Button-1>",
            lambda event: self.var.set(False)
            if self.var.get() is True
            else self.var.set(True),
        )

    def get_var_value(self):
        return self.var.get()

    def on_enter(self, _):
        self.checkbox._on_enter()  # noqa

    def on_leave(self, _):
        self.checkbox._on_leave()  # noqa
