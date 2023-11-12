class AnimateWidget:
    def __init__(self, frame, button):
        self.frame = frame
        self.button = button
        self.animation_started = False
        self.settings_on_screen = False
        self.pos = 0
        self.start_pos = 1
        self.end_pos = 0

    def animate(self):
        if not self.animation_started:
            self.animation_started = True
            if not self.settings_on_screen:
                self.animate_forward()
            else:
                self.animate_backwards()

    def animate_forward(self):
        if self.pos < self.start_pos:
            self.pos += 0.035
            self.frame.place(relx=0, rely=self.pos, anchor='sw')
            self.button.lift()
            self.frame.after(15, self.animate_forward)
        else:
            self.animation_started = False
            self.settings_on_screen = True

    def animate_backwards(self):
        if self.pos > self.end_pos:
            self.pos -= 0.035
            self.frame.place(relx=0, rely=self.pos, anchor='sw')
            self.button.lift()
            self.frame.after(15, self.animate_backwards)
        else:
            self.animation_started = False
            self.settings_on_screen = False
