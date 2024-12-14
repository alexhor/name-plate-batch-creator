from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

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
