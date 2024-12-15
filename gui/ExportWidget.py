import os
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.event import EventDispatcher

from gui.Button import BlueButton, GrayButton, LabelButton

class ExportWidget(BoxLayout, EventDispatcher):
    def __init__(self, popup_size_hint=None, **kwargs):
        self.register_event_type('on_saving_done')

        self.popup_size_hint = popup_size_hint
        self._set_fixed_window_size()
        super().__init__(orientation='vertical', padding=40, spacing=50, **kwargs)
        self.pos_hint = {'top': 1, 'x': 0}
        
        # Choose folder
        choose_folder_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        self.file_input = TextInput(text=str(os.path.expanduser('~')), size_hint_y=None, height=80, font_size=30, padding_y=20, padding_x=10)
        self.file_input.pos_hint = {'top': 2, 'x': 0}
        choose_file_btn = GrayButton(text='Choose Export Folder', size=(350, 80))
        choose_file_btn.bind(on_release=self.show_file_chooser)
        choose_folder_layout.add_widget(self.file_input)
        choose_folder_layout.add_widget(choose_file_btn)

        # Output file name
        output_file_name_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        output_file_name_label = Label(text='Output file name', valign='middle', color=(0/255, 0/255, 0/255, 1), size_hint=(None, None), width=250, height=80)
        self.output_file_input = TextInput(text='NamePlateBatch.pdf', size_hint_y=None, height=80, font_size=30, padding_y=20, padding_x=10)
        output_file_name_layout.add_widget(output_file_name_label)
        output_file_name_layout.add_widget(self.output_file_input)
        
        # Double sided switch
        double_sided_layout = BoxLayout(orientation='vertical')
        left_aligned_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), height=50, spacing=10)
        left_aligned_layout.pos_hint = {'x': 0}
        self.switch = Switch(active=True, size_hint_x=None, width=160)
        switch_label = Label(text='Double sided', valign='middle', color=(0/255, 0/255, 0/255, 1), size_hint_x=None, width=200)
        left_aligned_layout.add_widget(self.switch)
        left_aligned_layout.add_widget(switch_label)
        double_sided_layout.add_widget(left_aligned_layout)
        
        # Save button
        save_button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        save_button = BlueButton(text='Save')
        save_button.bind(on_release=self.on_save)
        
        save_button_layout.add_widget(BoxLayout())  # Expandable spacer
        save_button_layout.add_widget(save_button)
        
        # Add layouts to main widget
        self.add_widget(choose_folder_layout)
        self.add_widget(output_file_name_layout)
        self.add_widget(double_sided_layout)
        self.add_widget(save_button_layout)

    def _set_fixed_window_size(self, size_x=600, size_y=180):
        if None is not self.popup_size_hint:
            size_x = (1 + (1 - self.popup_size_hint[0])*2) * size_x
            size_y = (1 + (1 - self.popup_size_hint[1])*2) * size_y + 70
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
        filechooser.filters = ['*/']
        filechooser.path = str(os.path.expanduser('~'))
        popup_layout = BoxLayout(orientation='vertical')
        popup = Popup(title='Choose Export Location', content=popup_layout, size_hint=(0.9, 0.9))
        popup.bind(on_dismiss=lambda instance: self._set_fixed_window_size())
        
        # Add select button
        select_button = BlueButton(text='Select')
        def select_file(_):
            self.file_input.text = filechooser.path
            self.file_input.cursor = (0, len(self.file_input.text))
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

    def on_saving_done(self):
        # This placeholder method allows binding to saving_done event
        pass

    def on_save(self, instance):
        print(f"File: {self.file_input.text}/{self.output_file_input.text}")
        print(f"Double Sided: {'ON' if self.switch.active else 'OFF'}")
        self.dispatch('on_saving_done')
