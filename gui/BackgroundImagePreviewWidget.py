from kivy.uix.image import Image

class BackgroundImagePreviewWidget(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = kwargs.get('size_hint', (None, None))
        self.size = kwargs.get('size', (500, 300))
        self.pos = kwargs.get('pos', (0, 0))
        self.allow_stretch = kwargs.get('allow_stretch', True)
        self.keep_ratio = kwargs.get('keep_ratio', True)
        self.bind(source=self.update_position, size=self.update_position)

    @property
    def image_width(self):
        return int(self.norm_image_size[0])
    
    @property
    def image_height(self):
        return int(self.norm_image_size[1])

    def update_position(self, instance, value):
        offset_x = self.size[0] - self.image_width
        if offset_x != 0:
            offset_x = -1*offset_x/2
        offset_y = self.size[1] - self.image_height
        if offset_y != 0:
            offset_y = -1*offset_y/2
        self.pos = (offset_x, offset_y)
