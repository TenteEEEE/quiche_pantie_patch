from PIL import Image
from src.models.cc0 import patcher


class patcher(patcher):
    def __init__(self, body='./body/body_sepina.png', **options):
        try:
            options = options['options']
        except:
            pass
        options['is_4k'] = True
        super().__init__(options=options)
        self.name = 'セピナ'
        self.body = Image.open(body)
        self.body_size = self.body.size
        self.pantie_position = [824, 3154]

    def patch(self, image, transparent=False):
        image = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", (4096, 4096))
        else:
            patched = self.body.copy()
        image = image.resize((int(image.width * 1.85), int(image.height * 1.85)), resample=Image.BICUBIC)
        patched = self.paste(patched, image, self.pantie_position)
        return patched
