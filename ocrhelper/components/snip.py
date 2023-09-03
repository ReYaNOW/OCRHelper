import tkinter as tk

import keyboard
from PIL import ImageTk, ImageGrab

from components.debug_window import DebugWindow


class SnippingTool:
    def __init__(self, master, app_update, snip_trigger, debug_window):
        self.master = master
        self.app_update = app_update
        self.snip_trigger = snip_trigger
        self.debug_window: DebugWindow = debug_window
        self.snip_surface = None
        self.canvas_on_screen = False
        self.screenshot_window = None
        self.screenshot_label = None
        self.screenshot = None

        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None

        self.master_screen = tk.Toplevel(self.master)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "maroon3")
        self.picture_frame = tk.Frame(self.master_screen)
        self.picture_frame.pack(fill="both", expand=True)

        self.create_screenshot_window()

    def display_snipping_tool(self):
        if self.canvas_on_screen:
            return

        self.canvas_on_screen = True

        self.display_screenshot_window()
        self.master_screen.deiconify()

        self.snip_surface = tk.Canvas(
            self.picture_frame,
            cursor="crosshair",
            bg="grey11",
        )

        self.snip_surface.pack(fill="both", expand=True)

        self.snip_surface.bind("<ButtonPress-1>", self.on_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_button_release)
        self.snip_surface.bind(
            "<ButtonRelease-3>", self.destroy_screenshot_mode
        )

        # add hotkey to stop process of recognition and translation
        keyboard.add_hotkey("escape", callback=self.destroy_screenshot_mode)

        self.master_screen.attributes("-fullscreen", True)
        self.master_screen.attributes("-alpha", 0.3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

        self.display_debug_window()

    def display_debug_window(self):
        self.debug_window.window.deiconify()
        self.debug_window.add_message("Ожидание скриншота", "white")
        self.app_update()

    def on_button_press(self, event):
        print(event)
        # save mouse drag start position
        self.start_x = self.snip_surface.canvasx(event.x)
        self.start_y = self.snip_surface.canvasy(event.y)
        self.snip_surface.create_rectangle(
            0, 0, 1, 1, outline="red", width=3, fill="maroon3"
        )
        self.debug_window.window.lift()

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
            return self.destroy_screenshot_mode()

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

    def on_snip_drag(self, event):
        self.current_x, self.current_y = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.snip_surface.coords(
            1,
            self.start_x,
            self.start_y,
            self.current_x,
            self.current_y,
        )

    def display_rectangle_position(self):
        print(
            "координаты:",
            self.start_x,
            self.start_y,
            self.current_x,
            self.current_y,
        )

    def exit_screenshot_mode(self, _=None):
        self.screenshot_window.withdraw()

        self.canvas_on_screen = False
        self.snip_surface.destroy()
        self.master_screen.withdraw()

    def destroy_screenshot_mode(self, _=None):
        self.exit_screenshot_mode()
        self.debug_window.clear_text_area()
        self.debug_window.window.withdraw()

    def create_screenshot_window(self):
        self.screenshot_window = tk.Toplevel(master=self.master)
        self.screenshot_window.attributes("-fullscreen", True)
        self.screenshot_window.attributes("-topmost", True)

        self.screenshot_label = tk.Label(self.screenshot_window)
        self.screenshot_label.pack()

        self.screenshot_window.withdraw()

    def display_screenshot_window(self):
        self.screenshot = ImageGrab.grab()
        tkinter_image = ImageTk.PhotoImage(self.screenshot)

        self.screenshot_label.image = tkinter_image
        self.screenshot_label.configure(image=tkinter_image)
        self.screenshot_window.deiconify()

    @staticmethod
    def coordinates_validator(x1, y1, x2, y2):
        if not all((x1, y1, x2, y2)):
            return False
        if abs(x1 - x2) < 10 and abs(y1 - y2) < 10:
            return False
        return True

    def take_bounded_screenshot(self, x1, y1, x2, y2):
        self.canvas_on_screen = False

        # convert coords to Pillow "version"
        pillow_x2 = x1 + x2
        pillow_y2 = y1 + y2

        # add this so that the translation window will appear in the same place
        # where the snipping tool used
        correction = 3

        image = self.screenshot.crop(
            (
                x1 + correction,
                y1 + correction,
                pillow_x2 + correction,
                pillow_y2 + correction,
            ),
        )
        # image = pyautogui.screenshot(region=(x1+3, y1+3, x2+3, y2+3))
        print("размер изображения:", image.size)
        image.save("test_image.png")

        self.snip_trigger(image, (x1, y1))
