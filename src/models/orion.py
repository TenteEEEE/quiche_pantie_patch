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
        super().__init__(options=options)
        self.name = 'オリオン'
        self.body = Image.open(body)
        self.body_size = self.body.size
        self.pantie_position = [407, 838]

        self.bra_position = [1023, 0]
        self.bra = np.float32(io.imread('./mask/bra_orion.png') / 255)
        self.bra_center = np.float32(io.imread('./mask/bra_orion_center.png') / 255)
        self.bra_shade = np.float32(io.imread('./material/bra_orion_shade.png') / 255)
        self.bra_component = np.float32(io.imread('./material/bra_orion_component.png') / 255)
        self.bra_shade_alpha = self.bra_shade[:, :, -1]
        self.bra_component_mask = self.bra_component[:, :, -1] > 0.5

        self.frill_position = [361, 1412]
        self.frill_shade = np.float32(io.imread('./material/orion_frill.png')[:, :, -1] / 255)

    def pick_color(self, arr):
        return np.mean(np.mean(arr, axis=0), axis=0)

    def gen_bra(self, image):
        pantie = np.array(image)

        # pickup colors
        front = pantie[20:100, 30:80, :3] / 255.0
        front_shade = pantie[130:150, 0:40, :3] / 255.0
        front_color = self.pick_color(front)
        front_shade_color = self.pick_color(front_shade)
        front_shade_color = rgb2hsv(front_shade_color[None, None])
        front_shade_color[0, 0, 1] *= front_shade_color[0, 0, 2] / 0.3
        if front_shade_color[0, 0, 1] > 0.7:
            front_shade_color[0, 0, 1] *= 0.7
        front_shade_color[0, 0, 2] *= front_shade_color[0, 0, 2] / 0.4
        front_shade_color = np.clip(hsv2rgb(front_shade_color)[0, 0], 0, 1)
        ribbon = pantie[24:32, 15:27, :3] / 255.0
        ribbon_color = self.pick_color(ribbon)

        # making a center texture
        center = pantie[20:170, -200:-15, :3][:, ::-1]
        center = resize(center, [2.42, 2.42])

        bra_center = np.copy(self.bra_center)
        bra_center[225:225 + center.shape[0], 25:25 + center.shape[1], :3] = center * np.float32(bra_center[225:225 + center.shape[0], 25:25 + center.shape[1], :3] > 0)
        bra = self.bra[:, :, :3] * front_color
        bra_shade = (self.bra_shade[:, :, -1])[:, :, None] * front_shade_color
        bra_component = self.bra_component[:, :, :3] * ribbon_color

        # overlaying layers
        bra = alpha_brend(bra_center[:, :, :3], bra[:, :, :3], bra_center[:, :, 0] > 0.1)
        bra = alpha_brend(bra_component, bra, self.bra_component_mask)
        bra = alpha_brend(bra_shade, bra, self.bra_shade_alpha)
        bra = np.dstack((bra, self.bra[:, :, 0] > 0.8))
        return Image.fromarray(np.uint8(np.clip(bra, 0, 1) * 255))

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
