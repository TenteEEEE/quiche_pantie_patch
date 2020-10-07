from PIL import Image, ImageOps
import numpy as np
import skimage.io as io
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body='./body/body_glaze.png', **options):
        super().__init__('ぐれーず', body=body, pantie_position=[265, 2019], **options)
        self.mask = io.imread('./mask/mask_glaze.png')
        self.pantie_edge = io.imread('./material/glaze_pantie_edge.png') / 255.

        try:
            self.with_bra = self.options['with_bra']
        except:
            self.with_bra = self.ask(question='With bra?', default=True)
        if self.with_bra:
            self.bra_mask = io.imread('./mask/bra_glaze_center.png')
            self.bra_others = io.imread('./material/glaze_others.png') / 255.

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-140:-5, 546:, :])
        [pr, pc, d] = patch.shape
        arrx = np.zeros(25) - 10
        arry = np.zeros(25) - 5
        arrx[6:-10] += np.sin(np.linspace(0, np.pi, 9)) * 4
        arrx[-15:] -= np.sin(np.linspace(0, np.pi / 2, 15)) * 5
        arry[1:5] -= np.sin(np.linspace(0, np.pi, 4)) * 25
        arry[5:] += np.sin(np.linspace(0, np.pi / 2, 20)) * 40
        pantie = affine_transform_by_arr(pantie, arrx, arry)
        pantie[125:125 + pr, :pc, :] = np.float32(patch[::-1, ::-1] / 255)
        pantie = np.uint8(resize(pantie[:320, :-50], [3.25, 3.15]) * 255)[:, 38:]
        pantie = np.bitwise_and(pantie, self.mask)
        pantie = np.concatenate((pantie[:, ::-1], pantie), axis=1)
        return Image.fromarray(pantie)

    def gen_bra_center(self, image):
        pantie = np.array(image)
        center = np.uint8(resize(pantie[15:150, 450:], [7.85, 7.85]) * 255)
        center = np.bitwise_and(center, self.bra_mask)
        return Image.fromarray(center)

    def gen_colored_tex(self, image, texture):
        pantie = np.array(image)
        tex = np.copy(texture)
        front = pantie[20:100, 30:80, :3] / 255.0
        front_color = np.mean(np.mean(front, axis=0), axis=0)
        front_shade = pantie[130:150, 0:40, :3] / 255.0
        front_shade_color = np.mean(np.mean(front_shade, axis=0), axis=0)
        # tex[:, :, :3] = tex[:, :, :3] * front_shade_color
        tex[:, :, :3] = tex[:, :, :3] * front_color
        return Image.fromarray(np.uint8(tex * 255))

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", (4096, 4096))
        else:
            patched = self.body.copy()
        patched = self.paste(patched, pantie, self.pantie_position)
        patched = self.paste(patched, self.gen_colored_tex(image, self.pantie_edge), [258, 1907])
        if self.with_bra:
            bra_center = self.gen_bra_center(image)
            patched = self.paste(patched, bra_center, [528, 162])
            patched = self.paste(patched, ImageOps.mirror(bra_center), [2173, 162])
            patched = self.paste(patched, self.gen_colored_tex(image, self.bra_others), [251, 921])
        return patched
