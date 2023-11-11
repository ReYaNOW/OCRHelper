"""This module was borrowed from the project
https://github.com/israel-dryer/ttkbootstrap

from the module
https://github.com/israel-dryer/ttkbootstrap/blob/master/src/ttkbootstrap/toast.py

and modified by me"""
import customtkinter as ctk
from tkinter import TclError

DEFAULT_ICON_WIN32 = "\ue154"
DEFAULT_ICON = "\u25f0"
BASELINE = 1.33398982438864281


class ToastNotification:
    """A semi-transparent popup window for temporary alerts or messages.
    You may choose to display the toast for a specified period of time,
    otherwise you must click the toast to close it.
    """

    def __init__(
        self, master, title=None, message=None, icon_color=None, duration=3500
    ):
        """
        Parameters:

            title (str):
                The toast title.

            message (str):
                The toast message.

            icon_color (str):
                Change color of icon to custom.

            duration (int):
                The number of milliseconds to show the toast. If None
                (default), then you must click the toast to close it.

        """
        self.master = master
        self.title = title
        self.message = message
        self.duration = duration

        self.toplevel = None
        self.position = None

        self.icon = None
        self.icon_color = icon_color
        self.iconfont = None
        self.titlefont = None

        if title is None:
            self.title = 'OCR Helper'
        if message is None:
            self.message = 'This is the actual message'
        if icon_color is None:
            self.icon_color = 'white'

    def show_toast(self):
        self.hide_toast_immediately()
        
        self.toplevel = ctk.CTkToplevel(self.master)
        self.toplevel.overrideredirect(True)
        self.toplevel.wm_attributes("-toolwindow", True)
        self.toplevel.attributes('-alpha', 0.95)
        self.toplevel.attributes('-topmost', True)

        self._setup()

        ctk.CTkLabel(
            self.toplevel,
            text=self.icon,
            font=self.iconfont,
            text_color=self.icon_color,
            anchor='nw',
        ).grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(5, 0))
        ctk.CTkLabel(
            self.toplevel,
            text=self.title,
            font=self.titlefont,
            anchor='nw',
        ).grid(row=0, column=1, sticky='nsew', padx=10, pady=(5, 0))
        ctk.CTkLabel(
            self.toplevel,
            text=self.message,
            justify='left',
            wraplength=200,
            anchor='nw',
        ).grid(row=1, column=1, sticky='nsew', padx=10, pady=(0, 5))

        self.toplevel.bind("<ButtonPress>", self.hide_toast)

        # specified duration to close
        if self.duration:
            self.toplevel.after(self.duration, self.hide_toast)

    def hide_toast(self, *_):
        """Destroy and close the toast window."""
        try:
            alpha = float(self.toplevel.attributes("-alpha"))
            if alpha <= 0.1:
                self.toplevel.destroy()
            else:
                self.toplevel.attributes("-alpha", alpha - 0.1)
                self.toplevel.after(25, self.hide_toast)
        except TclError:
            if self.toplevel:
                self.toplevel.destroy()
    
    def hide_toast_immediately(self):
        if self.toplevel:
            if self.toplevel.winfo_exists():
                self.toplevel.destroy()

    def _setup(self):
        winsys = self.toplevel.tk.call("tk", "windowingsystem")

        # minsize
        w, h = scale_size(self.toplevel, [300, 75])
        self.toplevel.minsize(w, h)

        # heading font
        _font = ctk.CTkFont("TkDefaultFont")
        self.titlefont = ctk.CTkFont(
            family=_font["family"],
            size=_font["size"] + 1,
            weight="bold",
        )
        # symbol font
        self.iconfont = ctk.CTkFont(size=43, weight="bold")
        match winsys:
            case "win32":
                self.iconfont["family"] = "Segoe UI Symbol"
                self.icon = DEFAULT_ICON_WIN32
                if self.position is None:
                    x, y = scale_size(self.toplevel, [5, 50])
                    self.position = (x, y, 'se')
            case "x11":
                self.iconfont["family"] = "FreeSerif"
                self.icon = DEFAULT_ICON if self.icon is None else self.icon
                if self.position is None:
                    x, y = scale_size(self.toplevel, [0, 0])
                    self.position = (x, y, 'se')
            case _:
                self.iconfont["family"] = "Apple Symbols"
                self.toplevel.update_idletasks()
                self.icon = DEFAULT_ICON if self.icon is None else self.icon
                if self.position is None:
                    x, y = scale_size(self.toplevel, [50, 50])
                    self.position = (x, y, 'ne')

        self.set_geometry()

    def set_geometry(self):
        self.toplevel.update_idletasks()  # actualize geometry

        screen_w = self.toplevel.winfo_screenwidth()
        screen_h = self.toplevel.winfo_screenheight()
        self.toplevel.geometry(f"+{screen_w - 299}+{screen_h - 122}")


def scale_size(widget, size):
    """Scale the size based on the scaling factor of tkinter.
    This is used most frequently to adjust the assets for
    image-based widget layouts and font sizes.

    Parameters:

        widget (Widget):
            The widget object.

        size (Union[int, List, Tuple]):
            A single integer or an iterable of integers

    Returns:

        Union[int, List]:
            An integer or list of integers representing the new size.
    """

    scaling = widget.tk.call('tk', 'scaling')
    factor = scaling / BASELINE

    if isinstance(size, int):
        return int(size * factor)
    elif isinstance(size, tuple) or isinstance(size, list):
        return [int(x * factor) for x in size]


if __name__ == '__main__':
    window = ctk.CTk()
    window.geometry('300x300')

    toast = ToastNotification(window)
    toast_button = ctk.CTkButton(
        window, text='Show toast', command=toast.show_toast
    )
    toast_button.place(relx=0.5, rely=0.5, anchor='center')

    window.mainloop()
