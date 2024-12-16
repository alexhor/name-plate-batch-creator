from kivy.uix.label import Label

class AlignLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text_size = self.size
        self.bind(size=self.setter('text_size'))
