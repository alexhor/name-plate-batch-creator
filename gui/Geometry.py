from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line

class HorizontalLine(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 2
        with self.canvas:
            Color(0, 0, 0, 1)  # Black color
            self.line = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_line, pos=self.update_line)

    def update_line(self, *args):
        self.line.size = self.size
        self.line.pos = self.pos

class VerticalLine(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = None
        self.width = 2
        with self.canvas:
            Color(0, 0, 0, 1)  # Black color
            self.line = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_line, pos=self.update_line)

    def update_line(self, *args):
        self.line.size = self.size
        self.line.pos = self.pos

def widget_add_border(widget, color=(0, 0, 0, 1), border_size=1):
    with widget.canvas:
        Color(color[0], color[1], color[2], color[3])
        border = Line(width=border_size, rectangle=(widget.pos[0], widget.pos[1], widget.width, widget.height))
    
    def update_border(*args):
        border.rectangle = (widget.pos[0], widget.pos[1], widget.width, widget.height)

    widget.bind(size=update_border, pos=update_border)
