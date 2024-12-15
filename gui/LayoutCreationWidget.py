import os
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.uix.filechooser import FileChooserIconView

from gui.EditTitlesWidget import EditTitlesWidget
from gui.LoadedTitleWidget import LoadedTitleWidget
from gui.ExportWidget import ExportWidget
from gui.Button import BlueButton, GrayButton, LabelButton
from gui.Line import HorizontalLine


class LayoutCreationWidget(BoxLayout):
    panel_background_image = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = kwargs.get('orientation', 'horizontal')
        self.spacing = kwargs.get('spacing', 10)
        self.padding = kwargs.get('padding', 10)

        self.bind(panel_background_image=self.update_panel_background_image)
        
        # Left Section: Loaded Names with ScrollView
        left_section = BoxLayout(orientation='vertical', size_hint=(0.3, 1), spacing=10)
        loaded_titles_label = Label(text='[b]Loaded Names[/b]', markup=True, color="black", size_hint_y=None, height=30)
        
        scroll_view = ScrollView(size_hint=(1, 1))
        self.loaded_titles_list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.loaded_titles_list_layout.bind(minimum_height=self.loaded_titles_list_layout.setter('height'))
        
        self.update_loaded_titles_list()
        
        scroll_view.add_widget(self.loaded_titles_list_layout)
        
        edit_titles_button = BlueButton(text='Edit Titles', size_hint=(1, None))
        edit_titles_button.bind(on_release=self.open_edit_titles_popup)
        
        left_section.add_widget(loaded_titles_label)
        left_section.add_widget(HorizontalLine())
        left_section.add_widget(scroll_view)
        left_section.add_widget(HorizontalLine())
        left_section.add_widget(edit_titles_button)
        
        # Center Section: Background Image & Change Background Button
        center_section = BoxLayout(orientation='vertical', size_hint=(0.7, 1), spacing=10)
        
        # Background Image Placeholder
        preview_container_wrapper = ScrollView(size_hint=(1, 0.6))
        preview_container = FloatLayout()
        preview_container_wrapper.add_widget(preview_container)
        self.panel_background_image_widget = Image(source=self.panel_background_image, size_hint=(None, None), size=(500, 300), pos_hint={'center_x': 0.5, 'center_y': 0.5}, allow_stretch=True, keep_ratio=True)
        preview_container.add_widget(self.panel_background_image_widget)
        
        # Change Background Button
        background_button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        background_button_layout.add_widget(BoxLayout())
        change_background_button = GrayButton(text='Change Background Image', size_hint=(None, None), size=(400, 40))
        change_background_button.bind(on_release=self.show_panel_background_image_file_chooser)
        background_button_layout.add_widget(change_background_button)
        clear_background_button = GrayButton(text='[b]X[/b]', markup=True, size_hint=(None, None), size=(40, 40), background_color=(1, 0, 0, 1))
        clear_background_button.bind(on_release=self.clear_panel_background_image)
        background_button_layout.add_widget(clear_background_button)
        
        # Canvas size
        canvas_size_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5)
        canvas_size_label = Label(text='Canvas Size', size_hint_x=None, width=170, color="black")
        canvas_size_layout.add_widget(canvas_size_label)
        canvas_size_layout.add_widget(BoxLayout(size_hint_x=None, width=30))
        canvas_size_x_label = Label(text='[b]X:[/b]', markup=True, size_hint_x=None, width=50, color="black")
        canvas_size_layout.add_widget(canvas_size_x_label)
        self.canvas_size_x_input = TextInput(text=str(self.panel_background_image_widget.width), size_hint_x=None, width=150, size_hint_y=None, height=50)
        self.canvas_size_x_input.bind(text=lambda instance, value: self.update_canvas_size())
        canvas_size_layout.add_widget(self.canvas_size_x_input)
        canvas_size_layout.add_widget(BoxLayout(size_hint_x=None, width=20))
        canvas_size_y_label = Label(text='[b]Y:[/b]', markup=True, size_hint_x=None, width=50, color="black")
        canvas_size_layout.add_widget(canvas_size_y_label)
        self.canvas_size_y_input = TextInput(text=str(self.panel_background_image_widget.height), size_hint_x=None, width=150, size_hint_y=None, height=50)
        self.canvas_size_y_input.bind(text=lambda instance, value: self.update_canvas_size())
        canvas_size_layout.add_widget(self.canvas_size_y_input)
        canvas_size_layout.add_widget(BoxLayout())

        # Bottom Text Inputs with Titles
        bottom_text_inputs = BoxLayout(orientation='horizontal', size_hint=(1, 0.4), spacing=10)
        title_section = BoxLayout(orientation='vertical')
        title_label = BlueButton(text='Title', size_hint=(None, None), size=(150, 40), font_size=30)
        title_input = TextInput()
        title_section.add_widget(title_label)
        title_section.add_widget(title_input)
        
        subtitle_section = BoxLayout(orientation='vertical')
        subtitle_label = BlueButton(text='Subtitle', size_hint=(None, None), size=(150, 40), font_size=30)
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
        center_section.add_widget(preview_container_wrapper)
        center_section.add_widget(background_button_layout)
        center_section.add_widget(canvas_size_layout)
        center_section.add_widget(bottom_text_inputs)
        center_section.add_widget(export_button_layout)
        
        # Add all sections to main layout
        self.add_widget(left_section)
        self.add_widget(center_section)

    def update_loaded_titles_list(self, loaded_titles_list=[]):
        # Clear previous titles
        self.loaded_titles_list_layout.clear_widgets()

        # Add placeholder titles
        if [] == loaded_titles_list:
            section_label_wrapper = LoadedTitleWidget(f"Placeholder Title", f"Some Subtitle")
            self.loaded_titles_list_layout.add_widget(section_label_wrapper)
        
        # Add all loaded titles
        for loaded_title_data in loaded_titles_list:
            section_label_wrapper = LoadedTitleWidget(loaded_title_data.title, loaded_title_data.subtitle)
            self.loaded_titles_list_layout.add_widget(section_label_wrapper)

    def update_canvas_size(self):
        try:
            x = int(self.canvas_size_x_input.text)
            y = int(self.canvas_size_y_input.text)
        except ValueError:
            print("Only integers allowed as canvas size")
            return
        self.panel_background_image_widget.size = (x, y)
        
    def open_edit_titles_popup(self, instance):
        edit_titles_widget = EditTitlesWidget(popup_size_hint=(0.9, 0.9))
        popup = Popup(title='Edit Titles', content=edit_titles_widget, size_hint=(0.9, 0.9))

        def load_new_titles(popup, new_titles_list):
            self.update_loaded_titles_list(new_titles_list)
            popup.dismiss()

        edit_titles_widget.bind(on_loading_done=lambda instance, new_titles_list, passed_popup=popup: load_new_titles(passed_popup, new_titles_list))
        popup.bind(on_dismiss=self.revert_to_original_window_size_after_popup_dismiss)
        popup.open()

    def open_export_popup(self, instance):
        export_widget = ExportWidget(popup_size_hint=(0.9, 0.9))
        popup = Popup(title='Export', content=export_widget, size_hint=(0.9, 0.9))
        export_widget.bind(on_saving_done=popup.dismiss)
        popup.bind(on_dismiss=self.revert_to_original_window_size_after_popup_dismiss)
        popup.open()

    def revert_to_original_window_size_after_popup_dismiss(self, instance):
        Window.size=(800, 600)#TODO: save actual window size before opening a popup and then restore this state afterwards

    def clear_panel_background_image(self, instance):
        self.panel_background_image = ""

    def show_panel_background_image_file_chooser(self, instance):
        # Popup for file selection
        filechooser = FileChooserIconView()
        filechooser.filters = ["*.jpg", "*.jpeg", "*.png"]
        filechooser.path = str(os.path.expanduser('~'))
        popup_layout = BoxLayout(orientation='vertical')
        popup = Popup(title='Choose Background Image', content=popup_layout, size_hint=(0.9, 0.9))
        popup.bind(on_dismiss=self.revert_to_original_window_size_after_popup_dismiss)
        
        # Add select button
        select_button = BlueButton(text='Select')
        def select_file(_):
            if filechooser.selection:
                self.panel_background_image = filechooser.selection[0]
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

    def update_panel_background_image(self, instance, value):
        print(f"New panel background image is located at \"{value}\"")
        self.panel_background_image_widget.source = value
        #TODO: adjust the background image in the preview

