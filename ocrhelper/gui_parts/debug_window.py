import tkinter as tk

from PIL import Image as im
from PIL import ImageTk

from ocrhelper.components import config
from ocrhelper.components.utils import check_path


class DebugWindow:
    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.withdraw()
        self.window.update()
        self.window.geometry('+0+0')
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)

        frame = tk.Frame(self.window, width=300, height=200)
        frame.pack()

        if config.get_value('interface_language') == 'ENG':
            img_path = r'assets/debug_label_eng.png'
        else:
            img_path = r'assets/debug_label.png'
        img = ImageTk.PhotoImage(im.open(check_path(img_path)))

        label = tk.Label(frame, image=img, background='white')
        label.image = img
        label.pack(expand=True, fill='x')

        self.text_area = tk.Text(
            frame,
            width=30,
            height=5,
            background='#282a36',
            font=('Verdana', 12),
        )

        # make text area read-only
        self.text_area.bind('<Key>', lambda event: 'break')

        self.text_area.tag_config('white', foreground='#F8F8F2')
        self.text_area.tag_config('orange', foreground='#F89580')
        self.text_area.tag_config('green', foreground='#4FF96D')
        self.text_area.pack()

    def add_message(self, text, color, enter='\n'):
        self.text_area.insert('end', f'{text}{enter}', color)
        self.text_area.see('end')
        self.master.update()

    def clear_text_area(self):
        self.text_area.delete('1.0', 'end')

    def tkinter_withdraw(self):
        self.window.withdraw()

    def tkinter_deiconify(self):
        self.window.deiconify()


class DebugWindowNullObject:
    """NullObject version of DebugWindow that will be used when usage
     of debug window is not selected"""
    def __init__(self, master):
        self.master = master

    def add_message(self, text, color, enter='\n'):
        pass

    def clear_text_area(self):
        pass

    def tkinter_withdraw(self):
        pass

    def tkinter_deiconify(self):
        pass
