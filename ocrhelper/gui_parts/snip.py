import tkinter as tk

from loguru import logger
import keyboard
from PIL import ImageTk, ImageGrab

from gui_parts.debug_window import DebugWindow


class SnippingTool:
    def __init__(self, master, additional_methods):
        self.master = master
        self.app_update = additional_methods['gui_update']
        self.snip_trigger = additional_methods['snip_trigger']
        self.debug_window: DebugWindow = additional_methods['debug_window']
        self.get_rect_color = additional_methods['get_rect_color']
        self.master_screen = None
        self.snip_surface = None
        self.canvas_on_screen = False
        self.screenshot = None
        self.rect = None

        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None

        self.master_screen = tk.Toplevel(self.master)
        self.master_screen.withdraw()
        self.master_screen.overrideredirect(True)

        self.w = self.master.winfo_screenwidth()
        self.h = self.master.winfo_screenheight()
        self.master_screen.geometry(f'{self.w}x{self.h}+0+0')

        # add hotkey to stop process of recognition and translation
        keyboard.add_hotkey('escape', callback=self.destroy_screenshot_mode)

    def display_snipping_tool(self):
        if self.canvas_on_screen:
            return

        self.snip_surface = self.create_canvas()
        self.canvas_on_screen = True

        self.screenshot = ImageGrab.grab()
        image = ImageTk.PhotoImage(self.screenshot)
        self.snip_surface.create_image(self.w / 2, self.h / 2, image=image)
        self.snip_surface.image = image

        self.master_screen.attributes('-topmost', True)
        self.master_screen.deiconify()
        self.display_debug_window()

    def create_canvas(self):
        # general canvas settings
        canvas = tk.Canvas(self.master_screen, width=self.w, height=self.h)
        canvas.pack()
        canvas.configure(highlightthickness=0)
        canvas.configure(cursor='crosshair')
        canvas.configure(background='black')

        # set events
        canvas.bind('<ButtonPress-1>', self.on_button_press)
        canvas.bind('<B1-Motion>', self.on_snip_drag)
        canvas.bind('<ButtonRelease-1>', self.on_button_release)
        canvas.bind(
            '<ButtonPress-3>', lambda e: self.debug_window.tkinter_withdraw()
        )
        canvas.bind('<ButtonRelease-3>', self.destroy_screenshot_mode)
        return canvas

    def display_debug_window(self):
        self.debug_window.tkinter_deiconify()
        self.debug_window.add_message('Ожидание скриншота', 'white')
    
    def change_debug_win_instance(self, instance):
        self.debug_window = instance

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.snip_surface.canvasx(event.x)
        self.start_y = self.snip_surface.canvasy(event.y)
        
        rect_color = self.get_rect_color()
        self.rect = self.snip_surface.create_rectangle(
            0, 0, 1, 1, outline=rect_color, width=2
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
            logger.warning(
                'Была выбрана слишком маленькая область, '
                'распознавание отменено'
            )
            return self.destroy_screenshot_mode()

        if self.start_x <= self.current_x and self.start_y <= self.current_y:
            self.exit_screenshot_mode()
            self.take_bounded_screenshot(
                self.start_x,
                self.start_y,
                self.current_x - self.start_x,
                self.current_y - self.start_y,
            )

        elif self.start_x >= self.current_x and self.start_y <= self.current_y:
            self.exit_screenshot_mode()
            self.take_bounded_screenshot(
                self.current_x,
                self.start_y,
                self.start_x - self.current_x,
                self.current_y - self.start_y,
            )

        elif self.start_x <= self.current_x and self.start_y >= self.current_y:
            self.exit_screenshot_mode()
            self.take_bounded_screenshot(
                self.start_x,
                self.current_y,
                self.current_x - self.start_x,
                self.start_y - self.current_y,
            )

        elif self.start_x >= self.current_x and self.start_y >= self.current_y:
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
            self.rect,
            self.start_x,
            self.start_y,
            self.current_x,
            self.current_y,
        )

    def display_rectangle_position(self):
        logger.debug(
            f'координаты: {self.start_x} {self.start_y} {self.current_x}'
            f'{self.current_y}'
        )

    def exit_screenshot_mode(self, _=None):
        if not self.canvas_on_screen:
            return
        self.canvas_on_screen = False
        self.snip_surface.destroy()
        self.master_screen.update()
        self.master_screen.withdraw()

    def destroy_screenshot_mode(self, _=None):
        self.exit_screenshot_mode()
        self.app_update()
        self.debug_window.tkinter_withdraw()
        self.debug_window.clear_text_area()

    @staticmethod
    def coordinates_validator(x1, y1, x2, y2):
        if not all((x1, y1, x2, y2)):
            return False
        if abs(x1 - x2) < 10 and abs(y1 - y2) < 10:
            return False
        return True

    def take_bounded_screenshot(self, x1, y1, x2, y2):
        self.start_x = self.start_y = self.current_x = self.current_y = None
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
        # logger.debug(f'размер изображения: {image.size}')

        self.snip_trigger(image, (x1, y1))
