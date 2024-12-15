import os, csv
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

class EditTitlesWidget(BoxLayout, EventDispatcher):
    def __init__(self, popup_size_hint=None, **kwargs):
        self.register_event_type('on_loading_done')

        self.popup_size_hint = popup_size_hint
        self._set_fixed_window_size()
        super().__init__(orientation='vertical', padding=40, spacing=10, **kwargs)
        
        # Choose file
        choose_file_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        self.file_input = TextInput(text=str(os.path.expanduser('~')), size_hint_y=None, height=80, font_size=30, padding_y=20, padding_x=10)
        self.file_input.pos_hint = {'top': 2, 'x': 0}
        choose_file_btn = GrayButton(text='Choose CSV File', size=(350, 80))
        choose_file_btn.bind(on_release=self.show_file_chooser)
        choose_file_layout.add_widget(self.file_input)
        choose_file_layout.add_widget(choose_file_btn)
        self.add_widget(choose_file_layout)
        ## Seperator
        csv_seperator_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.add_widget(csv_seperator_layout)
        csv_seperator_label = Label(text="Seperator", size_hint_x=None, width=300)
        self.csv_seperator_input = TextInput(text=";", size_hint=(None, None), size=(50, 50), halign="center")
        csv_seperator_layout.add_widget(csv_seperator_label)
        csv_seperator_layout.add_widget(BoxLayout(size_hint_x=None, width=20))
        csv_seperator_layout.add_widget(self.csv_seperator_input)
        csv_seperator_layout.add_widget(BoxLayout())
        ## Title column number
        title_column_number_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.add_widget(title_column_number_layout)
        title_column_number_label = Label(text="Title column number", size_hint_x=None, width=300)
        self.title_column_number_input = TextInput(text="1", size_hint=(None, None), size=(50, 50), halign="center")
        title_column_number_layout.add_widget(title_column_number_label)
        title_column_number_layout.add_widget(BoxLayout(size_hint_x=None, width=20))
        title_column_number_layout.add_widget(self.title_column_number_input)
        title_column_number_layout.add_widget(BoxLayout())
        ## Subtitle column number
        subtitle_column_number_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.add_widget(subtitle_column_number_layout)
        subtitle_column_number_label = Label(text="Subtitle column number", size_hint_x=None, width=300)
        self.subtitle_column_number_input = TextInput(text="2", size_hint=(None, None), size=(50, 50), halign="center")
        subtitle_column_number_layout.add_widget(subtitle_column_number_label)
        subtitle_column_number_layout.add_widget(BoxLayout(size_hint_x=None, width=20))
        subtitle_column_number_layout.add_widget(self.subtitle_column_number_input)
        subtitle_column_number_layout.add_widget(BoxLayout())
        # Title row switch
        title_row_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), height=50, spacing=10)
        self.add_widget(title_row_layout)
        self.title_row_switch = Switch(active=True, size_hint_x=None, width=160)
        switch_label = Label(text='File has title row', valign='middle', size_hint_x=None, width=300)
        title_row_layout.add_widget(self.title_row_switch)
        title_row_layout.add_widget(switch_label)
        
        # Save button
        save_button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        save_button = BlueButton(text='Load')
        save_button.bind(on_release=self.on_loading)
        save_button_layout.add_widget(BoxLayout())  # Expandable spacer
        save_button_layout.add_widget(save_button)
        self.add_widget(save_button_layout)

    def _set_fixed_window_size(self, size_x=600, size_y=200):
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
        filechooser.filters = ['*.csv']
        filechooser.path = str(os.path.expanduser('~'))
        popup_layout = BoxLayout(orientation='vertical')
        popup = Popup(title='Choose Export Location', content=popup_layout, size_hint=(0.9, 0.9))
        popup.bind(on_dismiss=lambda instance: self._set_fixed_window_size())
        
        # Add select button
        select_button = BlueButton(text='Select')
        def select_file(_):
            if filechooser.selection:
                self.file_input.text = filechooser.selection[0]
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

    def on_loading_done(self, laded_titles_list):
        # This placeholder method allows binding to saving_done event
        pass

    def on_loading(self, instance):
        loaded_titles_list = []
        # Parse (sub)title indexes
        try:
            title_index = int(self.title_column_number_input.text) - 1
            subtitle_index = int(self.subtitle_column_number_input.text) - 1
        except ValueError:
            print("Invalid title or subtitle index")
            return
        # Read CSV file
        try:
            with open(self.file_input.text, mode='r') as file:
                csv_reader = csv.reader(file, delimiter=self.csv_seperator_input.text)
        
                i = 0
                # Skip title row if this CSV has one
                if self.title_row_switch.active:
                    next(csv_reader)
                    i += 1
            
                # Iterate through the titles
                for row in csv_reader:
                    i += 1
                    try:
                        loaded_titles_list.append(LoadedTitle(row[title_index], row[subtitle_index]))
                    except IndexError:
                        print("Index error on row", i)
                        continue
        except IOError:
            print("CSV file not readable")
            return
        
        # Dispatch save event with loaded titles list
        self.dispatch('on_loading_done', loaded_titles_list)

class LoadedTitle:
    def __init__(self, title, subtitle):
        self.title = title
        self.subtitle = subtitle
