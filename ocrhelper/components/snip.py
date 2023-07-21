import tkinter as tk
from tkinter import ttk
import pyautogui


class SnipButton(ttk.Frame):
    def __init__(self, master: tk.Tk, app):
        super().__init__()
        self.snip_surface = None
        self.master: tk.Tk = master
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None
        self.app = app

        self.snipButton = ttk.Button(
            self,
            command=self.create_screen_canvas,
            text="Нажми для перевода",
        )
        self.snipButton.pack(expand=True, fill="both")

        self.master_screen = tk.Toplevel(self.master)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "maroon3")
        self.picture_frame = tk.Frame(self.master_screen)
        self.picture_frame.pack(fill="both", expand=True)

    def create_screen_canvas(self):
        self.master_screen.deiconify()
        self.master.withdraw()

        self.snip_surface = tk.Canvas(
            self.picture_frame, cursor="cross", bg="grey11"
        )
        self.snip_surface.pack(fill="both", expand=True)

        self.snip_surface.bind("<ButtonPress-1>", self.on_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes("-fullscreen", True)
        self.master_screen.attributes("-alpha", 0.3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.snip_surface.canvasx(event.x)
        self.start_y = self.snip_surface.canvasy(event.y)
        self.snip_surface.create_rectangle(
            0, 0, 1, 1, outline="red", width=3, fill="maroon3"
        )

    def on_button_release(self, _):
        self.display_rectangle_position()

        if (
            self.coordinates_validator(
                self.start_x,
                self.current_x,
                self.start_y,
                self.current_y,
            )
            is False
        ):
            return self.exit_screenshot_mode()

        if self.start_x <= self.current_x and self.start_y <= self.current_y:
            print("right down")
            self.exit_screenshot_mode()
            self.take_bounded_screenshot(
                self.start_x,
                self.start_y,
                self.current_x - self.start_x,
                self.current_y - self.start_y,
            )

        elif self.start_x >= self.current_x and self.start_y <= self.current_y:
            print("left down")
            self.exit_screenshot_mode()
            self.take_bounded_screenshot(
                self.current_x,
                self.start_y,
                self.start_x - self.current_x,
                self.current_y - self.start_y,
            )

        elif self.start_x <= self.current_x and self.start_y >= self.current_y:
            print("right up")
            self.exit_screenshot_mode()
            self.take_bounded_screenshot(
                self.start_x,
                self.current_y,
                self.current_x - self.start_x,
                self.start_y - self.current_y,
            )

        elif self.start_x >= self.current_x and self.start_y >= self.current_y:
            print("left up")
            self.exit_screenshot_mode()
            self.take_bounded_screenshot(
                self.current_x,
                self.current_y,
                self.start_x - self.current_x,
                self.start_y - self.current_y,
            )

    def exit_screenshot_mode(self):
        self.snip_surface.destroy()
        self.master_screen.withdraw()
        self.master.deiconify()

    def on_snip_drag(self, event):
        self.current_x, self.current_y = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.snip_surface.coords(
            1, self.start_x, self.start_y, self.current_x, self.current_y
        )

    @staticmethod
    def coordinates_validator(x1, y1, x2, y2):
        if not all((x1, y1, x2, y2)):
            return False
        if abs(x1 - x2) < 10 and abs(y1 - y2) < 10:
            return False
        return True

    def display_rectangle_position(self):
        print(
            "координаты:",
            self.start_x,
            self.start_y,
            self.current_x,
            self.current_y,
        )

    def take_bounded_screenshot(self, x1, y1, x2, y2):
        image = pyautogui.screenshot(region=(x1, y1, x2, y2))
        print("размер изображения:", image.size)
        image.save("test_img.png")
        self.app.trigger_func(image, (x1, y1))
