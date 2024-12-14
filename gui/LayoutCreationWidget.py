from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from gui.ExportWidget import ExportWidget
from gui.Button import BlueButton
from gui.Line import HorizontalLine


class LayoutCreationWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='horizontal', spacing=10, padding=10, **kwargs)
        
        # Left Section: Loaded Names with ScrollView
        left_section = BoxLayout(orientation='vertical', size_hint=(0.3, 1), spacing=10)
        loaded_names_label = Label(text='[b]Loaded Names[/b]', markup=True, color="black", size_hint_y=None, height=30)
        
        scroll_view = ScrollView(size_hint=(1, 1))
        self.loaded_names_list = GridLayout(cols=1, size_hint_y=None, spacing=5, width=scroll_view.width)
        self.loaded_names_list.bind(minimum_height=self.loaded_names_list.setter('height'))
        
        # Add placeholder sections to the list
        for i in range(1, 100):
            section_label = Label(text=f'Section {i}', color="black", size_hint_y=None, height=50)
            self.loaded_names_list.add_widget(section_label)
        
        scroll_view.add_widget(self.loaded_names_list)
        
        edit_names_button = BlueButton(text='Edit names', size_hint=(1, None))
        
        left_section.add_widget(loaded_names_label)
        left_section.add_widget(HorizontalLine())
        left_section.add_widget(scroll_view)
        left_section.add_widget(HorizontalLine())
        left_section.add_widget(edit_names_button)
        
        # Center Section: Background Image & Change Background Button
        center_section = BoxLayout(orientation='vertical', size_hint=(0.7, 1), spacing=10)
        
        # Background Image Placeholder
        background_image = Image(source='', size_hint=(1, 0.6), allow_stretch=True, keep_ratio=False)
        
        # Change Background Button
        background_button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        change_background_button = BlueButton(text='Change Background Image', size_hint=(None, None), size=(200, 40))
        background_icon = Button(text='✎', size_hint=(None, None), size=(40, 40))
        
        background_button_layout.add_widget(change_background_button)
        background_button_layout.add_widget(background_icon)
        
        # Bottom Text Inputs with Titles
        bottom_text_inputs = BoxLayout(orientation='horizontal', size_hint=(1, 0.4), spacing=10)
        title_section = BoxLayout(orientation='vertical')
        title_label = BlueButton(text='Title', height=30)
        title_input = TextInput()
        title_section.add_widget(title_label)
        title_section.add_widget(title_input)
        
        subtitle_section = BoxLayout(orientation='vertical')
        subtitle_label = BlueButton(text='Subtitle', height=30)
        subtitle_input = TextInput()
        subtitle_section.add_widget(subtitle_label)
        subtitle_section.add_widget(subtitle_input)
        
        bottom_text_inputs.add_widget(title_section)
        bottom_text_inputs.add_widget(subtitle_section)
        
        # Export Button aligned right
        export_button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=80)
        export_button = BlueButton(text='Export')
        export_button.bind(on_release=self.open_export_popup)
        export_button_layout.add_widget(BoxLayout())  # Spacer to push Export to the right
        export_button_layout.add_widget(export_button)
        
        # Add to center section
        center_section.add_widget(background_image)
        center_section.add_widget(background_button_layout)
        center_section.add_widget(bottom_text_inputs)
        center_section.add_widget(export_button_layout)
        
        # Add all sections to main layout
        self.add_widget(left_section)
        self.add_widget(center_section)

    def open_export_popup(self, instance):
        export_widget = ExportWidget(popup_size_hint=(0.9, 0.9))
        popup = Popup(title='Export', content=export_widget, size_hint=(0.9, 0.9))
        export_widget.bind(on_saving_done=popup.dismiss)
        popup.bind(on_dismiss=self.close_export_popup)
        popup.open()

    def close_export_popup(self, instance):
        Window.size=(800, 600)
        

"""
import os
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from gui.Button import BlueButton, LabelButton

class LayoutCreationWidget(BoxLayout):
    def __init__(self, **kwargs):
        self._set_fixed_window_size()
        super().__init__(orientation='vertical', padding=40, spacing=50, **kwargs)
        self.pos_hint = {'top': 1, 'x': 0}
    
    def _set_fixed_window_size(self, size_x=600, size_y=180):
        Window.size = (size_x, size_y)
        Window.minimum_width = size_x
        Window.minimum_height = size_y
        Window.maximum_width = size_x
        Window.maximum_height = size_y
        Window.resizable = False

    def show_file_chooser(self, instance):
        self._set_fixed_window_size(700, 500)
        # Popup for file selection
        filechooser = FileChooserIconView()
        filechooser.filters = []
        filechooser.path = str(os.path.expanduser('~'))
        popup_layout = BoxLayout(orientation='vertical')
        popup = Popup(title='Choose File', content=popup_layout, size_hint=(0.9, 0.9))
        popup.bind(on_dismiss=lambda instance: self._set_fixed_window_size())
        
        # Add select button
        select_button = BlueButton(text='Select')
        def select_file(_):
            if filechooser.selection:
                self.file_input.text = os.path.basename(filechooser.selection[0])
                self.file_input.cursor = (0, 0)
            popup.dismiss()
        select_button.bind(on_release=select_file)

        def navigate_to(path):
            # Update the filechooser path to the clicked directory
            filechooser.path = path
        
        breadcrumbs_layout_scroll_view = ScrollView(size_hint_y=None, height=40, bar_width=0)

        # Update breadcrumbs
        def update_breadcrumbs(instance=None, current_path=filechooser.path):
            # Create a layout for the breadcrumbs at the top
            breadcrumbs_layout = BoxLayout(orientation='horizontal', size_hint_x=None)
            breadcrumbs_layout.bind(minimum_width = breadcrumbs_layout.setter("width"))

            # Split the current path into directories
            if "/" == current_path:
                directories = ['']
            else:
                directories = current_path.split(os.sep)
            
            # Create a label for each directory in the path
            for index, directory in enumerate(directories):
                button_text = directory + "/"
                breadcrumb_label = LabelButton(text=button_text, font_name='Courier New', size_hint_x=None, width=len(button_text) * 18)

                # If it's not the last breadcrumb, add a clickable event to navigate
                if index < len(directories) - 1:
                    path_to_navigate = os.path.sep.join(directories[:index+1])
                    if path_to_navigate == "":
                        path_to_navigate = "/"
                    breadcrumb_label.bind(on_release=lambda instance, path=path_to_navigate: navigate_to(path))
                    breadcrumb_label.color = (0, 140/255, 1, 1)  # Blue color for clickable breadcrumbs

                # Add the label to the breadcrumb layout
                breadcrumbs_layout.add_widget(breadcrumb_label)
            # Clear current breadcrumbs
            breadcrumbs_layout_scroll_view.clear_widgets()
            breadcrumbs_layout_scroll_view.add_widget(breadcrumbs_layout)
        filechooser.bind(path=update_breadcrumbs)

        # Add the filechooser and breadcrumbs to the main layout
        popup_layout.add_widget(breadcrumbs_layout_scroll_view)
        popup_layout.add_widget(filechooser)
        popup_layout.add_widget(select_button)
        update_breadcrumbs()
        popup.open()

    def on_save(self, instance):
        print(f"File: {self.file_input.text}")
        print(f"Double Sided: {'ON' if self.switch.active else 'OFF'}")
"""
