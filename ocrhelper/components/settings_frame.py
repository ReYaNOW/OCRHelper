import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, settings_im, settings_im_dark):
        super().__init__(master, fg_color="#262834", width=670, height=300)
        self.settings_im = settings_im
        self.settings_im_dark = settings_im_dark

        languages_frame = LanguagesFrame(self)
        languages_frame.place(relx=0.235, rely=0.174, anchor='center')
        self.get_selected_languages = languages_frame.get_selected_languages

        translators_frame = TranslatorsFrame(self)
        translators_frame.place(relx=0.235, rely=0.50, anchor='center')
        self.get_selected_translator = (
            translators_frame.get_selected_translator
        )

        clipboard_frame = ClipboardFrame(self)
        clipboard_frame.place(relx=0.235, rely=0.825, anchor='center')
        self.need_copy_to_clipboard = clipboard_frame.need_copy_to_clipboard

        self.palette_frame = PaletteFrame(self, self.bind_button)
        self.palette_frame.place(relx=0.725, rely=0.406, anchor='center')

    def bind_button(self, type_of_bind, button: tk.Button, image: ImageTk):
        button.bind(
            type_of_bind,
            lambda e: self.change_button_color(button, image),
        )

    @staticmethod
    def change_button_color(button: tk.Button, image: ImageTk):
        button.configure(image=image)
        button.image = image


class LanguagesFrame(ctk.CTkFrame):
    def __init__(self, settings_frame: SettingsFrame):
        super().__init__(
            settings_frame,
            bg_color='#262834',
            fg_color='#202020',
            corner_radius=20,
            width=300,
            height=90,
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
        eng_option.place(relx=0.3, rely=0.685, anchor='center')

        self.rus_var, rus_option = self.create_lang_option('RUS')
        rus_option.place(relx=0.55, rely=0.685, anchor='center')

        self.jap_var, jap_option = self.create_lang_option('JAP')
        jap_option.place(relx=0.80, rely=0.685, anchor='center')

    def create_lang_option(self, language: str):
        lang_var = ctk.StringVar(self, 'ENG')
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
        return lang_var, lang_option

    def validate_lang_var(self):
        if self.get_selected_languages():
            self.eng_var.set('eng')

    def get_selected_languages(self):
        languages = self.eng_var.get(), self.rus_var.get(), self.jap_var.get()
        # change to 2 char version to work with EasyOCR
        return [lang[:-1].lower() for lang in languages]


class TranslatorsFrame(ctk.CTkFrame):
    def __init__(self, settings_frame: SettingsFrame):
        super().__init__(
            settings_frame,
            bg_color='#262834',
            fg_color='#202020',
            corner_radius=20,
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


class ClipboardFrame(ctk.CTkFrame):
    def __init__(self, settings: SettingsFrame):
        super().__init__(
            settings,
            bg_color='#262834',
            fg_color='#202020',
            corner_radius=20,
            width=300,
            height=90,
        )

        clipboard_label = ctk.CTkLabel(
            self,
            text='Добавлять распознанный',
            font=("Rubik", 18),
            cursor='hand2',
        )
        clipboard_label.place(relx=0.5, rely=0.35, anchor='center')

        self.clip_var = ctk.BooleanVar(self, False)
        self.clipboard_option = ctk.CTkCheckBox(
            self,
            font=("Rubik", 18),
            text='текст в буфер обмена',
            fg_color='#5429FE',
            hover_color='#4a1e9e',
            variable=self.clip_var,
        )
        self.clipboard_option.place(relx=0.5, rely=0.59, anchor='center')

        clipboard_label.bind("<Enter>", self.on_enter)
        clipboard_label.bind("<Leave>", self.on_leave)
        clipboard_label.bind(
            "<Button-1>",
            lambda event: self.clip_var.set(False)
            if self.clip_var.get() is True
            else self.clip_var.set(True),
        )

    def need_copy_to_clipboard(self):
        return self.clip_var.get()

    def on_enter(self, _):
        self.clipboard_option._on_enter()  # noqa

    def on_leave(self, _):
        self.clipboard_option._on_leave()  # noqa


class PaletteFrame(ctk.CTkFrame):
    def __init__(self, settings: SettingsFrame, bind_button):
        super().__init__(
            settings,
            bg_color='#262834',
            fg_color='#202020',
            width=342,
            height=230,
        )
        self.bind_button = bind_button

        self.example_canvas = ctk.CTkCanvas(
            self, width=315, height=55, highlightthickness=0
        )
        self.example_canvas.place(relx=0.5, rely=0.84, anchor='center')

        red_widgets = self.create_color_labels_and_slider('Red', 'red', 84)
        red_label, red_label_value, red_var, red_slider = red_widgets
        red_label.place(relx=0.1, rely=0.35, anchor='center')
        red_label_value.place(relx=0.225, rely=0.35, anchor='center')
        red_slider.place(relx=0.58, rely=0.35, anchor='center')

        green_widgets = self.create_color_labels_and_slider(
            'Green', '#00E81A', 41
        )
        green_label, green_label_value, green_var, green_slider = green_widgets
        green_label.place(relx=0.1, rely=0.5, anchor='center')
        green_label_value.place(relx=0.225, rely=0.5, anchor='center')
        green_slider.place(relx=0.58, rely=0.5, anchor='center')

        blue_widgets = self.create_color_labels_and_slider(
            'Blue', '#0376FF', 254
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
            3, 10, 312, 50, outline='#5429FE', width=2
        )

        self.red_var = red_var
        self.green_var = green_var
        self.blue_var = blue_var
        red_slider.configure(command=self.change_rect_color)
        green_slider.configure(command=self.change_rect_color)
        blue_slider.configure(command=self.change_rect_color)

        hex_label = ctk.CTkLabel(self, text='HEX :', font=("Rubik bold", 15))
        hex_label.place(relx=0.285, rely=0.15, anchor='center')

        self.hex_var = ctk.StringVar(self, '#5429FE')
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
        self.example_canvas.itemconfigure(self.rect, outline=hex_color)

    def return_rect_color_to_default(self):
        self.red_var.set(84)
        self.green_var.set(41)
        self.blue_var.set(254)
        self.hex_var.set("#5429FE")
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

    @staticmethod
    def open_tk_img(path_to_image: str):
        image = Image.open(path_to_image)
        image_tk = ImageTk.PhotoImage(image, size=(96, 96))
        return image_tk
