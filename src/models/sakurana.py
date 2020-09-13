from PIL import Image
from src.models.cc0 import patcher
import numpy as np
import skimage.io as io
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body='./body/body_sakurana.png', **options):
        try:
            options = options['options']
        except:
            pass
        options['is_4k'] = False
        super().__init__(options=options)
        self.name = 'サクラナ'
        self.body = Image.open(body)
        self.body_size = self.body.size
        self.pantie_position = [3433, 1782]
        try:
            self.with_bra = options['with_bra']
        except:
            self.with_bra = self.ask(question='With bra?', default=True)
        if self.with_bra:
            self.bra_position = [2017, 1491]
            self.bra = np.float32(io.imread('./mask/bra_sakurana.png') / 255)
            self.bra_center = np.float32(io.imread('./mask/bra_sakurana_center.png') / 255)
            self.bra_shade = np.float32(io.imread('./material/bra_sakurana_shade.png') / 255)
            self.bra_frill = np.float32(io.imread('./material/bra_sakurana_frill.png') / 255)
            self.bra_shade_alpha = self.bra_shade[:, :, -1]
            self.bra_frill_mask = self.bra_frill[:, :, -1] > 0.5

    def gen_bra(self, image):
        def pick_color(arr):
            return np.mean(np.mean(arr, axis=0), axis=0)
        pantie = np.array(image)

        # pickup colors
        front = pantie[20:100, 30:80, :3] / 255.0
        front_shade = pantie[130:150, 0:40, :3] / 255.0
        front_color = pick_color(front)
        front_shade_color = pick_color(front_shade)
        front_shade_color = rgb2hsv(front_shade_color[None, None])
        front_shade_color[0, 0, 1] *= front_shade_color[0, 0, 2] / 0.3
        if front_shade_color[0, 0, 1] > 0.7:
            front_shade_color[0, 0, 1] *= 0.7
        front_shade_color[0, 0, 2] *= front_shade_color[0, 0, 2] / 0.4
        front_shade_color = np.clip(hsv2rgb(front_shade_color)[0, 0], 0, 1)
        ribbon = pantie[24:32, 15:27, :3] / 255.0
        ribbon_color = pick_color(ribbon)

        # making a center texture
        center = pantie[20:170, -200:-15, :3][:, ::-1]
        center = resize(center, [2.3, 2.5])

        bra_center = np.copy(self.bra_center)
        bra_center[:center.shape[0], :center.shape[1], :3] = center * np.float32(bra_center[:center.shape[0], :center.shape[1], :3] > 0)
        bra = self.bra[:, :, :3] * front_color
        bra_shade = (self.bra_shade[:, :, -1])[:, :, None] * front_shade_color
        bra_frill = self.bra_frill[:, :, :3] * ribbon_color

        # overlaying layers
        bra = alpha_brend(bra_center[:, :, :3], bra[:, :, :3], bra_center[:, :, 0] > 0.1)
        bra = alpha_brend(bra_frill, bra, self.bra_frill_mask)
        bra = alpha_brend(bra_shade, bra, self.bra_shade_alpha)
        bra = np.dstack((bra, self.bra[:, :, 0] > 0))
        return Image.fromarray(np.uint8(np.clip(bra, 0, 1) * 255))

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", (4096, 4096))
        else:
            patched = self.body.copy()
        pantie = pantie.resize((int(pantie.width * .75), int(pantie.height * .77)), resample=Image.BICUBIC)
        pantie = pantie.rotate(-90, expand=True)
        patched = self.paste(patched, pantie, self.pantie_position)
        if self.with_bra:
            patched = self.paste(patched, self.gen_bra(image), self.bra_position)
        return patched
