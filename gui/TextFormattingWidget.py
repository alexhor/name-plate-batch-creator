from random import random
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

from gui.Geometry import widget_add_border
from gui.Label import AlignLabel

class TextFormattingWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = kwargs.get('orientation', 'vertical')
        self.spacing = kwargs.get('spacing', 10)
        self.padding = kwargs.get('padding', 10)

        # Parameters
        label_width = 250
        row_height = 40
        self._id = int(random()*1000000)
        
        # Main layout grid
        grid_layout = GridLayout(cols=2, spacing=10, size_hint=(1, 1), padding=(10, 30))
        widget_add_border(grid_layout)

        # Font Family
        font_family_label = AlignLabel(text='Font Family', size_hint_x=None, width=label_width, halign='left', valign='middle', color="black")
        font_family_label.bind(size=font_family_label.setter('text_size'))
        font_family_spinner = Spinner(
            text='Option 1',
            values=['Option 1', 'Option 2', 'Option 3'],
            size_hint=(None, None), size=(200, 40)
        )
        grid_layout.add_widget(font_family_label)
        grid_layout.add_widget(font_family_spinner)

        # Font Size
        font_size_label = AlignLabel(text='Font Size', size_hint=(None, None), size=(label_width, row_height), halign='left', valign='middle', color="black")
        font_size_label.bind(size=font_size_label.setter('text_size'))
        font_size_input = TextInput(text='100', size_hint=(None, None), size=(200, row_height), input_filter='int')
        grid_layout.add_widget(font_size_label)
        grid_layout.add_widget(font_size_input)

        # Text Decoration
        text_decoration_label = AlignLabel(text='Text Decoration', size_hint=(None, None),size=(label_width, row_height), halign='left', valign='middle', color="black")
        text_decoration_label.bind(size=text_decoration_label.setter('text_size'))
        text_decoration_layout = BoxLayout(orientation='horizontal', spacing=5)
        bold_btn = ToggleButton(text='B', size_hint=(None, None), size=(row_height, row_height))
        italic_btn = ToggleButton(text='I', size_hint=(None, None), size=(row_height, row_height))
        underline_btn = ToggleButton(text='U', size_hint=(None, None), size=(row_height, row_height))
        text_decoration_layout.add_widget(bold_btn)
        text_decoration_layout.add_widget(italic_btn)
        text_decoration_layout.add_widget(underline_btn)
        grid_layout.add_widget(text_decoration_label)
        grid_layout.add_widget(text_decoration_layout)

        # Align
        align_label = AlignLabel(text='Align', size_hint=(None, None), size=(label_width, row_height), halign='left', valign='middle', color="black")
        align_label.bind(size=align_label.setter('text_size'))
        align_layout = BoxLayout(orientation='horizontal', spacing=5)
        left_align = ToggleButton(text='L', size_hint=(None, None), size=(row_height, row_height), group='align_'+str(self._id))
        center_align = ToggleButton(text='C', size_hint=(None, None), size=(row_height, row_height), group='align_'+str(self._id), state='down')
        right_align = ToggleButton(text='R', size_hint=(None, None), size=(row_height, row_height), group='align_'+str(self._id))
        align_layout.add_widget(left_align)
        align_layout.add_widget(center_align)
        align_layout.add_widget(right_align)
        grid_layout.add_widget(align_label)
        grid_layout.add_widget(align_layout)

        # Position
        position_label = AlignLabel(text='Position', size_hint=(None, None), size=(label_width, row_height), halign='left', valign='middle', color="black")
        position_label.bind(size=position_label.setter('text_size'))
        position_layout = BoxLayout(orientation='horizontal', spacing=5)
        x_label = AlignLabel(text='X:', size_hint=(None, None), size=(30, row_height), color="black")
        x_input = TextInput(text='100', size_hint=(None, None), size=(70, row_height), input_filter='int')
        y_label = AlignLabel(text='Y:', size_hint=(None, None), size=(30, row_height), color="black")
        y_input = TextInput(text='100', size_hint=(None, None), size=(70, row_height), input_filter='int')
        position_layout.add_widget(x_label)
        position_layout.add_widget(x_input)
        position_layout.add_widget(y_label)
        position_layout.add_widget(y_input)
        grid_layout.add_widget(position_label)
        grid_layout.add_widget(position_layout)

        # Add grid layout to the main widget
        self.add_widget(grid_layout)
