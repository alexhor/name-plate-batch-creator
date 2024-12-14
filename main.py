from kivy.app import App
from kivy.core.window import Window
from gui.ExportWidget import ExportWidget


class NamePlateBatchCreator(App):
    def build(self):
        Window.clearcolor = (245/255, 245/255, 245/255, 1)
        return ExportWidget()

if __name__ == '__main__':
    NamePlateBatchCreator().run()
