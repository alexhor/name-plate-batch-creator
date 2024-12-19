from enum import Enum
from matplotlib import font_manager
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
        #TOOD: font color is missing
        super().__init__(**kwargs)
        self.orientation = kwargs.get('orientation', 'vertical')
        self.spacing = kwargs.get('spacing', 10)
        self.padding = kwargs.get('padding', 10)

        self.register_event_type('on_settings_updated')
        self.text_formatting_values = TextFormattingValues(**kwargs)

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
            text=self.text_formatting_values.font_family,
            values=self.text_formatting_values.font_families_list,
            size_hint=(None, None), size=(230, 40)
        )
        font_family_spinner.text_size = (font_family_spinner.width-20, font_family_spinner.height)
        font_family_spinner.bind(text=lambda instance, value=None, key="font_family": self._setting_updated(key, value))

        grid_layout.add_widget(font_family_label)
        grid_layout.add_widget(font_family_spinner)

        # Font Size
        font_size_label = AlignLabel(text='Font Size', size_hint=(None, None), size=(label_width, row_height), halign='left', valign='middle', color="black")
        font_size_label.bind(size=font_size_label.setter('text_size'))
        font_size_input = TextInput(text=self.text_formatting_values.font_size, size_hint=(None, None), size=(200, row_height), input_filter='int')
        font_size_input.bind(text=lambda instance, value=None, key="font_size": self._setting_updated(key, value))
        grid_layout.add_widget(font_size_label)
        grid_layout.add_widget(font_size_input)

        # Text Decoration
        text_decoration_label = AlignLabel(text='Text Decoration', size_hint=(None, None),size=(label_width, row_height), halign='left', valign='middle', color="black")
        text_decoration_label.bind(size=text_decoration_label.setter('text_size'))
        text_decoration_layout = BoxLayout(orientation='horizontal', spacing=5)
        ## Text Decoration bold
        bold_btn = ToggleButton(text='[b]B[/b]', markup=True, size_hint=(None, None), size=(row_height, row_height))
        if self.text_formatting_values.bold:
            bold_btn.state = 'down'
        bold_btn.bind(on_press=lambda button, key="bold": self._setting_updated(key, True if button.state == 'down' else False))
        text_decoration_layout.add_widget(bold_btn)
        ## Text Decoration italic
        italic_btn = ToggleButton(text='[i]i[/i]', markup=True, size_hint=(None, None), size=(row_height, row_height))
        if self.text_formatting_values.italic:
            italic_btn.state = 'down'
        italic_btn.bind(on_press=lambda button, key="italic": self._setting_updated(key,  True if button.state == 'down' else False))
        text_decoration_layout.add_widget(italic_btn)
        ## Text Decoration underline
        underline_btn = ToggleButton(text='[u]U[/u]', markup=True, size_hint=(None, None), size=(row_height, row_height))
        if self.text_formatting_values.underline:
            underline_btn.state = 'down'
        underline_btn.bind(on_press=lambda button, key="underline": self._setting_updated(key,  True if button.state == 'down' else False))
        text_decoration_layout.add_widget(underline_btn)
        ## Text Decoration strikethrough
        strikethrough_btn = ToggleButton(text='[s]S[/s]', markup=True, size_hint=(None, None), size=(row_height, row_height))
        if self.text_formatting_values.strikethrough:
            strikethrough_btn.state = 'down'
        strikethrough_btn.bind(on_press=lambda button, key="strikethrough": self._setting_updated(key,  True if button.state == 'down' else False))
        text_decoration_layout.add_widget(strikethrough_btn)
        grid_layout.add_widget(text_decoration_label)
        grid_layout.add_widget(text_decoration_layout)

        # Align
        align_label = AlignLabel(text='Align', size_hint=(None, None), size=(label_width, row_height), halign='left', valign='middle', color="black")
        align_label.bind(size=align_label.setter('text_size'))
        align_layout = BoxLayout(orientation='horizontal', spacing=5)
        ## Align left
        left_align = ToggleButton(text='L', size_hint=(None, None), size=(row_height, row_height), group='align_'+str(self._id))
        if self.text_formatting_values.align == TextFormattingValues.Align.left:
            left_align.state = 'down'
        left_align.bind(on_press=lambda button: self._setting_updated("align",  TextFormattingValues.Align.left))
        ## Align center
        center_align = ToggleButton(text='C', size_hint=(None, None), size=(row_height, row_height), group='align_'+str(self._id))
        if self.text_formatting_values.align == TextFormattingValues.Align.center:
            center_align.state = 'down'
        center_align.bind(on_press=lambda button: self._setting_updated("align",  TextFormattingValues.Align.center))
        ## Align right
        right_align = ToggleButton(text='R', size_hint=(None, None), size=(row_height, row_height), group='align_'+str(self._id))
        if self.text_formatting_values.align == TextFormattingValues.Align.right:
            right_align.state = 'down'
        right_align.bind(on_press=lambda button: self._setting_updated("align",  TextFormattingValues.Align.right))
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
        x_input = TextInput(text=self.text_formatting_values.position_x, size_hint=(None, None), size=(70, row_height), input_filter='int')
        x_input.bind(text=lambda instance, value=None, key="position_x": self._setting_updated(key, value))
        y_label = AlignLabel(text='Y:', size_hint=(None, None), size=(30, row_height), color="black")
        y_input = TextInput(text=self.text_formatting_values.position_y, size_hint=(None, None), size=(70, row_height), input_filter='int')
        y_input.bind(text=lambda instance, value=None, key="position_y": self._setting_updated(key, value))
        position_layout.add_widget(x_label)
        position_layout.add_widget(x_input)
        position_layout.add_widget(y_label)
        position_layout.add_widget(y_input)
        grid_layout.add_widget(position_label)
        grid_layout.add_widget(position_layout)

        # Add grid layout to the main widget
        self.add_widget(grid_layout)

    def on_settings_updated(self, text_formatting_values):
        # Event placeholder
        pass

    def _setting_updated(self, key, value):
        self.text_formatting_values.set(key, value)
        self.dispatch('on_settings_updated', self.text_formatting_values)

class TextFormattingValues:
    def __init__(self, **kwargs):
        self.__font_families_list = None
        self.__font_family_path_mapping = {}
        self.__font_family = kwargs.get('font_name', font_manager.FontProperties().get_name())
        self.__font_size = str(kwargs.get('font_size', '40'))
        self.__bold = kwargs.get('bold', False)
        self.__italic = kwargs.get('italic', False)
        self.__underline = kwargs.get('underline', False)
        self.__strikethrough = kwargs.get('strikethrough', False)
        pos = kwargs.get('pos', ('25', '160'))
        self.__position_x = str(pos[0])
        self.__position_y = str(pos[1])
        self.__align = self.Align[kwargs.get('halign', self.Align.left.name)]
    
    @property
    def font_families_list(self):
        if None is self.__font_families_list:
            font_list = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
            self.__font_families_list = []
            for font_path in font_list:
                try:
                    font = font_manager.FontProperties(fname=font_path)
                    self.__font_families_list.append(font.get_name())
                    self.__font_family_path_mapping[font.get_name()] = font_path
                except:
                    continue
            self.__font_families_list.sort()
        return self.__font_families_list


    @property
    def font_family_file(self):
        #return self.__font_family_path_mapping[self.font_family]
        return font_manager.findfont(self.font_family)
    @property
    def font_family(self):
        return self.__font_family
    @font_family.setter
    def font_family(self, value):
        if value not in self.font_families_list:
            raise ValueError
        self.__font_family = value
    
    @property
    def font_size(self):
        return self.__font_size
    @font_size.setter
    def font_size(self, value):
        if '' == value:
            value = 0
        value = int(value) # This conversion will throw a ValueError itself
        if 0 > value:
            value = -1 * value
        self.__font_size = value
    
    @property
    def bold(self):
        return self.__bold
    @bold.setter
    def bold(self, value):
        self.__bold = bool(value)
    
    @property
    def italic(self):
        return self.__italic
    @italic.setter
    def italic(self, value):
        self.__italic = bool(value)
    
    @property
    def underline(self):
        return self.__underline
    @underline.setter
    def underline(self, value):
        self.__underline = bool(value)
    
    @property
    def strikethrough(self):
        return self.__strikethrough
    @strikethrough.setter
    def strikethrough(self, value):
        self.__strikethrough = bool(value)
    
    @property
    def position_x(self):
        return self.__position_x
    @position_x.setter
    def position_x(self, value):
        if '' == value:
            value = 0
        value = int(value) # This conversion will throw a ValueError itself
        if 0 > value:
            value = -1 * value
        self.__position_x = value
    
    @property
    def position_y(self):
        return self.__position_y
    @position_y.setter
    def position_y(self, value):
        if '' == value:
            value = 0
        value = int(value) # This conversion will throw a ValueError itself
        if 0 > value:
            value = -1 * value
        self.__position_y = value

    class Align(Enum):
        left = 0
        center = 1
        right = 2
    @property
    def align(self):
        return self.__align
    @align.setter
    def align(self, value):
        if not isinstance(value, self.Align):
            raise ValueError
        self.__align = value

    def get(self, key):
        return getattr(self, key)

    def set(self, key, value):
        setattr(self, key, value)
