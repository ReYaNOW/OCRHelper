import tkinter as tk

from PIL import Image, ImageTk, ImageColor

import customtkinter as ctk


class PaletteFrame(ctk.CTkFrame):
    def __init__(self, settings, rect_color):
        self.rect_color = rect_color

        super().__init__(
            settings,
            bg_color='#262834',
            fg_color='#202020',
            width=342,
            height=230,
        )

        self.rect_color_default = '#b800cf'
        self.rect_color_def_rgb = (184, 0, 207)
        self.rect_color_rgb = ImageColor.getcolor(rect_color, "RGB")

        self.red_var, self.red_slider = self._place_red_widgets()
        self.green_var, self.green_slider = self._place_green_widgets()
        self.blue_var, self.blue_slider = self._place_blue_widgets()

        self._place_example_image()
        self._place_hex_label_and_entry()
        self._place_return_button()
        self._place_change_button()

    def _place_hex_label_and_entry(self):
        hex_label = ctk.CTkLabel(self, text='HEX :', font=("Rubik bold", 15))
        hex_label.place(relx=0.285, rely=0.15, anchor='center')

        self.hex_var = ctk.StringVar(self, self.rect_color)
        self.hex_entry = ctk.CTkEntry(self, textvariable=self.hex_var)
        self.hex_entry.place(relx=0.365, rely=0.09)
        self.hex_entry.bind("<Leave>", lambda event: self.focus())

    def _place_red_widgets(self):
        hex_color = self.rect_color_rgb[0]
        red_widgets = self.create_color_labels_and_slider(
            'Red', 'red', hex_color
        )
        red_label, red_label_value, red_var, red_slider = red_widgets
        red_label.place(relx=0.1, rely=0.35, anchor='center')
        red_label_value.place(relx=0.225, rely=0.35, anchor='center')
        red_slider.place(relx=0.58, rely=0.35, anchor='center')

        return red_var, red_slider

    def _place_green_widgets(self):
        green_widgets = self.create_color_labels_and_slider(
            'Green', '#00E81A', self.rect_color_rgb[1]
        )
        green_label, green_label_value, green_var, green_slider = green_widgets
        green_label.place(relx=0.1, rely=0.5, anchor='center')
        green_label_value.place(relx=0.225, rely=0.5, anchor='center')
        green_slider.place(relx=0.58, rely=0.5, anchor='center')

        return green_var, green_slider

    def _place_blue_widgets(self):
        blue_widgets = self.create_color_labels_and_slider(
            'Blue', '#0376FF', self.rect_color_rgb[2]
        )
        blue_label, blue_label_value, blue_var, blue_slider = blue_widgets
        blue_label.place(relx=0.1, rely=0.65, anchor='center')
        blue_label_value.place(relx=0.225, rely=0.65, anchor='center')
        blue_slider.place(relx=0.58, rely=0.65, anchor='center')

        return blue_var, blue_slider

    def _place_example_image(self):
        self.example_canvas = ctk.CTkCanvas(
            self, width=315, height=55, highlightthickness=0
        )
        self.example_canvas.place(relx=0.5, rely=0.84, anchor='center')

        example_img = Image.open('assets/example_image.png')
        example_img_ctk = ImageTk.PhotoImage(example_img)
        self.example_canvas.image = example_img_ctk
        self.example_canvas.create_image(
            -7, 0, anchor='nw', image=example_img_ctk
        )
        self.rect = self.example_canvas.create_rectangle(
            3, 10, 312, 50, outline=self.rect_color, width=2
        )

        self.red_slider.configure(command=self.change_rect_color)
        self.green_slider.configure(command=self.change_rect_color)
        self.blue_slider.configure(command=self.change_rect_color)

    def _place_return_button(self):
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

    def _place_change_button(self):
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
        self.red_var.set(self.rect_color_def_rgb[0])
        self.green_var.set(self.rect_color_def_rgb[1])
        self.blue_var.set(self.rect_color_def_rgb[2])
        self.hex_var.set(self.rect_color_default)
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
