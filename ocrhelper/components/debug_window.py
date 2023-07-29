import tkinter as tk

from PIL import Image as im
from PIL import ImageTk

image_path = (
    r"C:\Users\ReYaN\python_projects\OCRHelper\ocrhelper\debug_label.png"
)


class DebugWindow:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.geometry("+0+0")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)

        frame = tk.Frame(self.window, width=300, height=200)
        frame.pack()

        # add label status
        img = ImageTk.PhotoImage(im.open(image_path))
        label = tk.Label(frame, image=img, background="white")
        label.image = img
        label.pack(expand=True, fill="x")

        # add text area for status notifications
        self.text_area = tk.Text(
            frame,
            width=30,
            height=5,
            background="#282a36",
            font=("Verdana", 12),
        )

        self.text_area.bind("<Key>", lambda e: "break")

        self.text_area.tag_config("white", foreground="#F8F8F2")
        self.text_area.tag_config("orange", foreground="#F89580")
        self.text_area.tag_config("green", foreground="#4FF96D")

        self.text_area.pack()
        self.window.withdraw()

    def add_message(self, text, color, enter="\n"):
        self.text_area.insert(tk.END, f"{text}{enter}", color)
        self.text_area.see(tk.END)

    def clear_text_area(self):
        self.text_area.delete("1.0", "end")

    def tkinter_update(self):
        self.window.update()

    def tkinter_withdraw(self):
        self.window.withdraw()
