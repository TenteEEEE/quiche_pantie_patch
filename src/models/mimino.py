import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb, rgb2gray
from skimage.filters import gaussian


class patcher(patcher):
    def __init__(self, body='./body/body_mimino.png', **options):
        super().__init__('みみの', body=body, pantie_position=[3, 772], **options)
        self.skin = Image.open('./material/mimino_skin.png')
        try:
            self.with_bra = self.options['with_bra']
        except:
            self.with_bra = self.ask(question='With bra?', default=True)
        if self.with_bra:
            self.bra_position = [0, 63]
            self.bra = np.float32(io.imread('./mask/bra_mimino.png') / 255)
            self.bra_center = np.float32(io.imread('./mask/bra_mimino_center.png') / 255)
            self.bra_shade = np.float32(io.imread('./material/bra_mimino_shade.png') / 255)
            self.bra_frill = np.float32(io.imread('./material/bra_mimino_frill.png') / 255)
            self.bra_alpha = self.bra[:, :, 0] > 0
            self.bra_shade_alpha = self.bra_shade[:, :, -1]
            self.bra_frill_mask = self.bra_frill[:, :, -1]

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
        ribbon_shade = pantie[26:30, 12:15, :3] / 255.0
        ribbon_shade_color = pick_color(ribbon_shade)

        # making a center texture
        center = np.float32(pantie[20:170, -200:-15, :3][::-1]) / 255.

        # painting colors
        bra_center = np.copy(self.bra_center)
        bra_center[300:300 + center.shape[0], 310:310 + center.shape[1], :3] = center * np.float32(bra_center[300:300 + center.shape[0], 310:310 + center.shape[1], :3] > 0)
        bra_center[300:300 + center.shape[0], 520:520 + center.shape[1], :3] = center[:, ::-1] * \
            np.float32(bra_center[300:300 + center.shape[0], 520:520 + center.shape[1], :3] > 0)

        bra = self.bra[:, :, :3] * front_color
        bra_shade = (self.bra_shade[:, :, -1])[:, :, None] * front_shade_color
        bra_frill = self.bra_frill[:, :, :3] * ribbon_color

        # overlaying layers
        bra = alpha_brend(bra_center[:, :, :3], bra[:, :, :3], bra_center[:, :, 0] > 0.1)
        bra = alpha_brend(bra_frill, bra, self.bra_frill_mask)
        bra = alpha_brend(bra_shade, bra, self.bra_shade_alpha)
        bra = np.dstack((bra, self.bra_alpha))
        return Image.fromarray(np.uint8(np.clip(bra, 0, 1) * 255))

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-100:-5, 546:, :])
        pantie[-100:, 546:, :] = 0
        patch = skt.resize(patch[::-1, ::-1, :], (patch.shape[0] + 90, patch.shape[1]), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[114:114 + pr, :pc, :] = np.uint8(patch * 255)
        pantie = np.uint8(resize(pantie, [0.82, 0.82]) * 255)
        pantie = pantie[:-70, 5:]
        pantie = np.concatenate([pantie[:, ::-1], pantie], axis=1)
        return Image.fromarray(pantie)

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        patched = self.paste(patched, self.skin, [0, 0])
        if self.with_bra:
            bra = self.gen_bra(image)
            patched = self.paste(patched, bra, self.bra_position)
        patched = self.paste(patched, pantie, self.pantie_position)
        return patched
