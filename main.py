from kivy.app import App
from kivy.core.window import Window
from gui.LayoutCreationWidget import LayoutCreationWidget


class NamePlateBatchCreator(App):
    def build(self):
        Window.clearcolor = (245/255, 245/255, 245/255, 1)
        return LayoutCreationWidget()

if __name__ == '__main__':
    NamePlateBatchCreator().run()
