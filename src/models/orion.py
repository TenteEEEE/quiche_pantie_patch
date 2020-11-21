from PIL import Image, ImageOps
from src.models.cc0 import patcher
import numpy as np
import skimage.io as io
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body='./body/body_orion.png', **options):
        try:
            options = options['options']
        except:
            pass
        options['is_4k'] = True
        options['with_bra'] = True
        super().__init__(options=options)
        self.name = 'オリオン'
        self.body = Image.open(body)
        self.body_size = self.body.size
        self.pantie_position = [407, 838]

        self.frill_position = [361, 1412]
        self.frill_shade = np.float32(io.imread('./material/orion_frill.png')[:, :, -1] / 255)

    def pick_color(self, arr):
        return np.mean(np.mean(arr, axis=0), axis=0)

    def gen_frill(self, image):
        pantie = np.array(image)
        front = pantie[20:100, 30:80, :3] / 255.0
        front_shade = pantie[130:150, 0:40, :3] / 255.0
        front_color = self.pick_color(front)
        front_shade_color = self.pick_color(front_shade)
        r, c = self.frill_shade.shape
        frill = np.ones((r, c, 3), dtype=np.float32) * front_color
        frill_shade = self.frill_shade[:, :, None] * front_shade_color
        frill = alpha_brend(frill_shade, frill, self.frill_shade)
        frill = np.dstack((frill, frill[:, :, 0] > 0))
        return Image.fromarray(np.uint8(np.clip(frill, 0, 1) * 255))

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", (2048, 2048))
        else:
            patched = self.body.copy()
        patched = self.paste(patched, pantie, self.pantie_position)
        bra = self.gen_bra(image)
        patched = self.paste(patched, bra, self.bra_position)
        patched = self.paste(patched, ImageOps.mirror(bra), [self.bra_position[0] - bra.width, self.bra_position[1]])
        patched = self.paste(patched, self.gen_frill(image), self.frill_position)
        return patched
