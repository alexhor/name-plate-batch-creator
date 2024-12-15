from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class LoadedTitleWidget(BoxLayout):
    def __init__(self, title, subtitle, **kwargs):
        self.title = title
        self.subtitle = subtitle

        # Set parameters
        super().__init__(**kwargs)
        self.orientation = kwargs.get('orientation', 'vertical')
        self.size_hint_y = kwargs.get('size_hint_y', None)
        self.height = kwargs.get('height', 70)

        # Add title
        title_label = Label(text=self.title, color="black", font_size=30)
        self.add_widget(title_label)

        # Add subtitle
        subtitle_label = Label(text=self.subtitle, color="black", font_size=20)
        self.add_widget(subtitle_label)
