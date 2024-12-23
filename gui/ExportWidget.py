import os
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.event import EventDispatcher
import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import landscape, portrait, A4

from gui.BackgroundImagePreviewWidget import BackgroundImagePreviewWidget
from gui.Button import BlueButton, GrayButton, LabelButton
from gui.TextFormattingWidget import TextFormattingValues
from gui.TextPreviewWidget import TextPreviewWidget

class ExportWidget(BoxLayout, EventDispatcher):
    def __init__(self, loaded_texts_list, text_formatting_values_list, background_image_source, canvas_size, background_image_size, popup_size_hint=None, **kwargs):
        self.register_event_type('on_saving_done')
        self._loaded_texts_list = loaded_texts_list
        self._text_formatting_values_list = text_formatting_values_list
        self._background_image_source = background_image_source
        self._canvas_size = canvas_size
        self._background_image_size = background_image_size

        self.popup_size_hint = popup_size_hint
        self._set_fixed_window_size()
        super().__init__(orientation='vertical', padding=40, spacing=50, **kwargs)
        self.pos_hint = {'top': 1, 'x': 0}
        
        # Choose folder
        choose_folder_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        self.add_widget(choose_folder_layout)
        self.file_input = TextInput(text=str(os.path.expanduser('~')), size_hint_y=None, height=80, font_size=30, padding_y=20, padding_x=10)
        self.file_input.pos_hint = {'top': 2, 'x': 0}
        choose_file_btn = GrayButton(text='Choose Export Folder', size=(350, 80))
        choose_file_btn.bind(on_release=self.show_file_chooser)
        choose_folder_layout.add_widget(self.file_input)
        choose_folder_layout.add_widget(choose_file_btn)

        # Output file name
        output_file_name_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        self.add_widget(output_file_name_layout)
        output_file_name_label = Label(text='Output file name', valign='middle', color="white", size_hint=(None, None), width=250, height=80)
        self.output_file_input = TextInput(text='NamePlateBatch.pdf', size_hint_y=None, height=80, font_size=30, padding_y=20, padding_x=10)
        output_file_name_layout.add_widget(output_file_name_label)
        output_file_name_layout.add_widget(self.output_file_input)
        
        # Double sided switch
        left_aligned_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), height=50, spacing=10)
        left_aligned_layout.pos_hint = {'x': 0}
        self.switch = Switch(active=True, size_hint_x=None, width=160)
        switch_label = Label(text='Double sided', valign='middle', color="white", size_hint_x=None, width=200)
        left_aligned_layout.add_widget(switch_label)
        left_aligned_layout.add_widget(self.switch)
        self.add_widget(left_aligned_layout)

        # Double sided offset
        double_sided_offset_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5)
        self.add_widget(double_sided_offset_layout)
        double_sided_offset_label = Label(text='Double sided offset', size_hint_x=None, width=200, color="white")
        double_sided_offset_layout.add_widget(double_sided_offset_label)
        double_sided_offset_layout.add_widget(BoxLayout(size_hint_x=None, width=30))
        double_sided_offset_x_label = Label(text='[b]X:[/b]', markup=True, size_hint_x=None, width=50, color="white")
        double_sided_offset_layout.add_widget(double_sided_offset_x_label)
        self.double_sided_offset_x_input = TextInput(text='0', size_hint_x=None, width=150, size_hint_y=None, height=50, input_filter='int')
        self.double_sided_offset_x_input.bind(text=lambda instance, value: self.update_double_sided_offset())
        double_sided_offset_layout.add_widget(self.double_sided_offset_x_input)
        double_sided_offset_layout.add_widget(BoxLayout(size_hint_x=None, width=20))
        double_sided_offset_y_label = Label(text='[b]Y:[/b]', markup=True, size_hint_x=None, width=50, color="white")
        double_sided_offset_layout.add_widget(double_sided_offset_y_label)
        self.double_sided_offset_y_input = TextInput(text='0', size_hint_x=None, width=150, size_hint_y=None, height=50, input_filter='int')
        self.double_sided_offset_y_input.bind(text=lambda instance, value: self.update_double_sided_offset())
        double_sided_offset_layout.add_widget(self.double_sided_offset_y_input)

        # Save button
        save_button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.add_widget(save_button_layout)
        save_button = BlueButton(text='Save')
        save_button.bind(on_release=self.on_save)
        
        save_button_layout.add_widget(save_button)
        

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
        pdf = canvas.Canvas(f"{self.file_input.text}/{self.output_file_input.text}")
        page_size = A4
        pdf.setPageSize(page_size)
        #pdf.setTitle(documentTitle)

        # Load title font
        for text_formatting_values in self._text_formatting_values_list:
            self.__text_formatting_load_font(text_formatting_values)


        offset = 550/1885

        # TODO: add border around whole pdf page

        # TODO: make badge spacing adjustable in export widget
        spacing_x = 50
        spacing_y = 100

        # Calculate maximum number of badges per page
        page_size_x, page_size_y = page_size
        canvas_size_x, canvas_size_y = self._canvas_size
        max_batches_per_row = (page_size_x-canvas_size_x*offset) // (canvas_size_x*offset + spacing_x*offset) + 1
        max_batches_per_col = (page_size_y-canvas_size_y*offset) // (canvas_size_y*offset + spacing_y*offset) + 1

        page = 0
        row = max_batches_per_col - 1
        col = 0
        # Draw badges
        for i in range(len(self._loaded_texts_list)):
            text_list = self._loaded_texts_list[i]
            ## Calculate batch anchor
            batch_anchor_x = col * (canvas_size_x*offset + spacing_x*offset)
            batch_anchor_y = row * (canvas_size_y*offset + spacing_y*offset)

            self.__draw_badge(pdf, self._background_image_source, self._background_image_size, text_list, self._text_formatting_values_list, (batch_anchor_x, batch_anchor_y), offset)

            ## Calculate next batch page, row and col
            col += 1
            if col == max_batches_per_row:
                col = 0
                row -= 1
                if 0 > row:
                    row = max_batches_per_col - 1
                    pdf.showPage()
                    if self.switch.active:
                        self.__draw_backside(pdf, page, max_batches_per_row, max_batches_per_col, offset, (spacing_x, spacing_y), page_size)
                    page += 1
        pdf.showPage()
        # Draw the last double sided page
        if self.switch.active:
            self.__draw_backside(pdf, page, max_batches_per_row, max_batches_per_col, offset, (spacing_x, spacing_y), page_size)
        pdf.save()
        self.dispatch('on_saving_done')

    def __draw_backside(self, pdf, page, max_batches_per_row, max_batches_per_col, offset, spacing, page_size):
        canvas_size_x, canvas_size_y = self._canvas_size
        page_size_x_mm, page_size_y_mm = page_size
        spacing_x, spacing_y = spacing
        batches_to_skip = int(page * max_batches_per_row * max_batches_per_col)
        backside_offset_x = page_size_x_mm - (max_batches_per_row - 1) * (canvas_size_x*offset + spacing_x*offset) - canvas_size_x*offset + int(self.double_sided_offset_x_input.text)
        backside_offset_y = int(self.double_sided_offset_y_input.text)

        row = max_batches_per_col - 1
        col = max_batches_per_row - 1

        for i in range(batches_to_skip, batches_to_skip+int(max_batches_per_row * max_batches_per_col)):
            batch_anchor_x = col * (canvas_size_x*offset + spacing_x*offset) + backside_offset_x
            batch_anchor_y = row * (canvas_size_y*offset + spacing_y*offset) + backside_offset_y
            if i >= len(self._loaded_texts_list):
                break
            text_list = self._loaded_texts_list[i]
            self.__draw_badge(pdf, self._background_image_source, self._background_image_size, text_list, self._text_formatting_values_list, (batch_anchor_x, batch_anchor_y), offset)

            ## Calculate next batch page, row and col
            col -= 1
            if 0 > col:
                col = max_batches_per_row - 1
                row -= 1
                if 0 > row:
                    row = max_batches_per_col - 1
                    pdf.showPage()

    def __text_formatting_load_font(self, text_formatting_values):
        reportlab.rl_config.TTFSearchPath.append(text_formatting_values.font_folder)
        # TODO: convert OTF to TTF before registering
        pdfmetrics.registerFont(TTFont(text_formatting_values.font_file_name, text_formatting_values.font_file_name))

    def __draw_badge(self, pdf, background_image_source, background_image_size, text_list, text_formatting_values_list, anchor, offset):
        canvas_size_x, canvas_size_y = self._canvas_size
        batch_anchor_x, batch_anchor_y = anchor
        ## Background Image
        if '' != background_image_source:
            pdf.drawImage(background_image_source, batch_anchor_x, batch_anchor_y, width=background_image_size[0]*offset, height=background_image_size[1]*offset)
        ## Texts
        for i in range(len(text_formatting_values_list)):
            text_formatting_values = text_formatting_values_list[i]
            if i >= len(text_list):
                break
            text = text_list[i]
            pdf.setFont(text_formatting_values.font_file_name, int(text_formatting_values.font_size)*offset)
            ### Calc position
            x = int(text_formatting_values.position_x)*offset+batch_anchor_x
            y = int(text_formatting_values.position_y)*offset+batch_anchor_y

            ### Draw text according to align
            if TextFormattingValues.Align.left == text_formatting_values.align:
                pdf.drawString(x, y, text)
            elif TextFormattingValues.Align.center == text_formatting_values.align:
                pdf.drawCentredString(x + (canvas_size_x/2)*offset, y, text)
            elif TextFormattingValues.Align.right == text_formatting_values.align:
                pdf.drawRightString(x + canvas_size_x*offset, y, text)
            #TODO: text formattings missing: underline, strikethrough
