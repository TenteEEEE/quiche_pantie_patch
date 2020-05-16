import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body='./body/body_shaon.png', **options):
        super().__init__('シャオン', body=body, pantie_position=[1312, 1435], **options)
        self.mask = io.imread('./mask/mask_shaon.png')
        try:
            self.with_bra = self.options['with_bra']
        except:
            self.with_bra = self.ask(question='With bra?', default=True)
        if self.with_bra:
            self.bra_position = [1289, 0]
            self.bra = np.float32(io.imread('./mask/bra_shaon.png') / 255)
            self.bra_center = np.float32(io.imread('./mask/bra_shaon_center.png') / 255)
            self.bra_shade = np.float32(io.imread('./material/bra_shaon_shade.png') / 255)
            self.bra_frill = np.float32(io.imread('./material/bra_shaon_frill.png') / 255)
            self.bra_alpha = self.bra[:, :, 0] > 0
            self.bra_shade_alpha = self.bra_shade[:, :, -1]
            self.bra_frill_mask = self.bra_frill[:, :, -1] > 0

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
        center = pantie[20:170, -200:-15, :3][:, ::-1]
        center = resize(center, [2.3, 2.3])

        # painting colors
        bra_center = np.copy(self.bra_center)
        bra_center[504:504 + center.shape[0], 112:112 + center.shape[1], :3] = center * np.float32(bra_center[504:504 + center.shape[0], 112:112 + center.shape[1], :3] > 0)
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
        patch = np.copy(pantie[-60:-5, 546:, :])
        pantie[-60:, 546:, :] = 0
        [pr, pc, d] = patch.shape
        pantie[120:120 + pr, :pc, :] = patch[::-1, ::-1]
        arrx = np.linspace(0, 1, 100)**2 * 100
        arry = np.sin(np.linspace(0, np.pi, 100) + np.pi / 4) * -100
        pantie = affine_transform_by_arr(pantie, arrx - 110, arry)[30:-60, 95:-30]
        pantie = np.uint8(resize(pantie, [2.5, 2.5]) * 255)
        pantie = np.bitwise_and(pantie, self.mask)
        return Image.fromarray(pantie)

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        if self.with_bra:
            bra = self.gen_bra(image)
            patched = self.paste(patched, bra, self.bra_position)
        patched = self.paste(patched, pantie, self.pantie_position)
        return patched
