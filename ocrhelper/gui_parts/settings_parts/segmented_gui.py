import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from ocrhelper.components import config
from ocrhelper.components import languages
from ocrhelper.gui_parts.toast import ToastNotification


class SegmentedFrame(ctk.CTkFrame):
    def __init__(self, master, def_value, frame_width=None, frame_height=None):
        super().__init__(
            master,
            bg_color='#262834',
            fg_color='#202020',
            width=300 if frame_width is None else frame_width,
            height=90 if frame_height is None else frame_height,
        )

        self.label = ctk.CTkLabel(
            self, font=(f'{config.get_font_name()} bold', 19), corner_radius=20
        )
        self.label.place(relx=0.5, rely=0.23, anchor='center')

        self.var = ctk.StringVar(self, def_value)
        self.segmented_btn = ctk.CTkSegmentedButton(
            self,
            variable=self.var,
            font=(config.get_font_name(), 17),
            selected_color='#5429FE',
            selected_hover_color='#4a1e9e',
        )
        self.segmented_btn.place(relx=0.5, rely=0.683, anchor='center')


class TranslatorsFrame(SegmentedFrame):
    def __init__(self, master):
        default_transl = config.get_value('translator')
        super().__init__(master, def_value=default_transl)

        self.label.configure(text=languages.get_string('translator'))
        self.segmented_btn.configure(values=['Google', 'GPT', 'GPT Stream'])
        self.segmented_btn.configure(command=self.check_value)

    def check_value(self, _):
        if not config.get_value('api_key_is_set'):
            self.var.set('Google')
            self.update()
            CTkMessagebox(
                title='OCRHelper',
                message=languages.get_string('pls_enter_api'),
                font=(config.get_font_name(), 14),
                button_color='#5429FE',
                button_hover_color='#4a1e9e',
                corner_radius=7,
            )
        else:
            config.change_value('translator', self.var.get())


class LanguageFrame(SegmentedFrame):
    def __init__(self, master, frame_width, frame_height):
        default_lang = config.get_value('interface_language')
        super().__init__(master, default_lang, frame_width, frame_height)

        self.toast_was_shown = False

        self.configure(border_width=2, border_color='#5429FE')
        self.label.configure(text=languages.get_string('interface_lang'))
        self.segmented_btn.configure(values=['ENG', 'RUS'])
        self.segmented_btn.configure(command=self.change_interface_lang)

    def change_interface_lang(self, _):
        lang = self.var.get()
        if lang != config.get_value('interface_language'):
            config.change_value('interface_language', lang)

            if self.toast_was_shown:
                return

            toast = ToastNotification(
                self,
                message=languages.get_string('need_restart_lang'),
                icon_color='#0377fc',
            )
            toast.show_toast()
            self.toast_was_shown = True


class TranslationLangFrame(SegmentedFrame):
    def __init__(self, master, frame_width=None, frame_height=None):
        default_lang = config.get_value('translation_language')
        super().__init__(master, default_lang, frame_width, frame_height)

        self.configure(border_width=2, border_color='#5429FE')
        self.label.configure(text=languages.get_string('translation_lang'))
        self.segmented_btn.configure(values=['ENG', 'RUS', 'JAP'])
        self.segmented_btn.configure(command=self.change_translation_lang)

    def change_translation_lang(self, _):
        lang = self.var.get()
        if lang != config.get_value('translation_language'):
            config.change_value('translation_language', lang)
