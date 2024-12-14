from kivy.uix.button import Button

class BlueButton(Button):
    def __init__(self, **kwargs):
        # Now apply normal button styling
        super().__init__(**kwargs)

        # Set default values for blue button
        self.font_size = kwargs.get('font_size', 30)
        self.bold = kwargs.get('bold', False)
        self.color = kwargs.get('color', (1, 1, 1, 1))
        self.background_normal = kwargs.get('background_normal', '')
        self.background_color = kwargs.get('background_color', (0, 140/255, 255/255, 1))
        self.padding = kwargs.get('padding', (40, 200))
        self.size_hint = kwargs.get('size_hint', (None, None))
        self.size = kwargs.get('size', (300, 80))

class GrayButton(BlueButton):
    def __init__(self, **kwargs):
        # Now apply normal button styling
        super().__init__(**kwargs)

        self.background_color = kwargs.get('background_color', (190/255, 190/255, 190/255, 1))
        self.color = kwargs.get('color', (0, 0, 0, 1))


class LabelButton(Button):
    def __init__(self, **kwargs):
        # Now apply normal button styling
        super().__init__(**kwargs)
        self.background_color = kwargs.get('background_color', (0, 0, 0, 0))
        self.size_hint_y = kwargs.get('size_hint_y', None)
        self.height = kwargs.get('height', 30)
