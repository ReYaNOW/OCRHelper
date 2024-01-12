class AnimateWidget:
    def __init__(self, widget, position_related, move_from='top'):
        self.widget = widget
        self.rel_x_pos = position_related['relx_pos']
        self.pos = position_related['rely_pos']
        self.start_pos = position_related['rel_start_pos']
        self.end_pos = position_related['rel_end_pos']
        self.move_from = move_from

        self.animation_started = False
        self.widget_on_screen = False

    def animate(self):
        if not self.animation_started:
            self.animation_started = True
            if not self.widget_on_screen:
                self.widget.lift()
                self.animate_forward()
            else:
                self.animate_backwards()

    def animate_forward(self):
        if self.move_from == 'top' and self.pos < self.start_pos:
            self.pos += 0.035
            self.widget.place(relx=self.rel_x_pos, rely=self.pos, anchor='sw')
            self.widget.after(15, self.animate_forward)
            self.widget_on_screen = True
        elif self.move_from == 'bottom' and self.pos > self.start_pos:
            self.pos -= 0.035
            self.widget.place(relx=self.rel_x_pos, rely=self.pos, anchor='nw')
            self.widget.after(15, self.animate_forward)
            self.widget_on_screen = True
        else:
            self.animation_started = False
            self.widget_on_screen = True

    def animate_backwards(self):
        if self.move_from == 'top' and self.pos > self.end_pos:
            self.pos -= 0.035
            self.widget.place(relx=self.rel_x_pos, rely=self.pos, anchor='sw')
            self.widget.after(15, self.animate_backwards)
            self.widget_on_screen = False
        elif self.move_from == 'bottom' and self.pos < self.end_pos:
            self.pos += 0.035
            self.widget.place(relx=self.rel_x_pos, rely=self.pos, anchor='nw')
            self.widget.after(15, self.animate_backwards)
            self.widget_on_screen = False
        else:
            self.animation_started = False
            self.widget_on_screen = False
