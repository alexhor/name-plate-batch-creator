from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from gui.Geometry import HorizontalLine

class LoadedTitleWidget(BoxLayout):
    def __init__(self, text_list, **kwargs):
        self._text_list = text_list

        # Set parameters
        super().__init__(**kwargs)
        self.orientation = kwargs.get('orientation', 'vertical')
        self.size_hint_y = kwargs.get('size_hint_y', None)
        self.height = kwargs.get('height', 70)

        # Add Labels
        for text in self._text_list:
            self.add_widget(Label(text=text, color="black", font_size=25))
        self.add_widget(HorizontalLine(size_hint_x=0.5, pos_hint={"center_x": 0.5}))

    def get_text(self, i):
        try:
            return self._text_list[i]
        except IndexError:
            return ""
