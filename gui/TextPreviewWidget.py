from matplotlib import font_manager
from gui.Label import AlignLabel
from kivy.properties import StringProperty

from gui.TextFormattingWidget import TextFormattingValues

class TextPreviewWidget(AlignLabel):
    _unformatted_text = StringProperty("")

    def __init__(self, text_formatting_values, **kwargs):
        super().__init__(**kwargs)
        #self.size_hint=(None, None)
        #self.size=(500, 300)
        #self.pos_hint={'center_x': 0.5, 'center_y': 0.5}
        self.color="black"
        self.update_text_formatting_values(None, text_formatting_values)
        #self.bind(text=lambda instance, text: self.update_text(text))

    def update_text_formatting_values(self, instance, text_formatting_values):
        self._text_formatting_values = text_formatting_values

        self.bold = self._text_formatting_values.bold
        self.italic = self._text_formatting_values.italic
        self.underline = self._text_formatting_values.underline
        self.strikethrough = self._text_formatting_values.strikethrough

        font_name = self._text_formatting_values.font_family
        self.font_name = font_name
        self.font_size = self._text_formatting_values.font_size

        self.halign = self._text_formatting_values.align.name
        self.pos = (self._text_formatting_values.position_x, self._text_formatting_values.position_y)
        return
