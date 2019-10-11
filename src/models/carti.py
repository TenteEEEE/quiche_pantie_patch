import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body='./body/body_carti.png', **options):
        super().__init__('カルティ', body=body, pantie_position=[802, 2574], **options)
        self.mask = io.imread('./mask/mask_carti.png')
        try:
            self.with_bra = self.options['with_bra']
        except:
            self.with_bra = self.ask(question='With bra?', default=True)
        if self.with_bra:
            self.bra_position = [892, 2700]
            self.bra = np.float32(io.imread('./mask/bra_carti.png') / 255)
            self.bra_center = np.float32(io.imread('./mask/bra_carti_center.png') / 255)
            self.bra_shade = np.float32(io.imread('./material/bra_carti_shade.png') / 255)
            self.bra_frill = np.float32(io.imread('./material/bra_carti_frill.png') / 255)
            self.bra_lace = np.float32(io.imread('./material/bra_carti_lace.png') / 255)
            self.bra_shade_alpha = self.bra_shade[:, :, -1]
            self.bra_lace_mask = self.bra_lace[:, :, -1] > 0
            self.bra_frill_mask = self.bra_frill[:, :, -1] > 0

    def pick_color(self, arr):
        return np.mean(np.mean(arr, axis=0), axis=0)

    def gen_texture(self, image, size):
        pantie = np.array(image)
        front = pantie[20:100, 30:80, :3]
        front_color = self.pick_color(front)
        front_color = np.append(front_color, 255).astype(np.uint8)
        texture = np.ones((size[0], size[1], 4),  dtype=np.uint8) * front_color
        return Image.fromarray(texture)

    def gen_bra(self, image):
        def alpha_brend(img1, img2, mask):
            return img1 * mask[:, :, None] + img2 * (1 - mask)[:, :, None]
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
        ribbon_shade = pantie[26:30, 12:15, :3] / 255.0
        ribbon_shade_color = self.pick_color(ribbon_shade)

        # making a center texture
        center = pantie[20:170, -200:-15, :3][::-1]
        center = resize(center, [2, 2.5])

        # painting colors
        center_mask = np.uint8(self.bra_center[:center.shape[0], :center.shape[1], 0] > 0)
        bra_frill = self.bra_frill[:, :, :3] * ribbon_shade_color
        bra_center = np.copy(self.bra_center)
        bra_center[:center.shape[0], :center.shape[1], :3] = center * center_mask[:, :, None]
        bra = self.bra[:, :, :3] * front_color
        bra_lace = self.bra_lace[:, :, :3] * front_color
        bra_shade = (self.bra_shade[:, :, -1])[:, :, None] * front_shade_color

        # overlaying layers
        bra = alpha_brend(bra_center[:, :, :3], bra[:, :, :3], bra_center[:, :, 0] > 0)
        bra = alpha_brend(bra_lace, bra, self.bra_lace_mask)
        bra = alpha_brend(bra_frill, bra, self.bra_frill_mask)
        bra = alpha_brend(bra_shade, bra, self.bra_shade_alpha)
        bra = np.dstack((bra, bra[:, :, 0] > 0))
        return Image.fromarray(np.uint8(np.clip(bra, 0, 1) * 255))

    def convert(self, image):
        pantie = np.array(image)

        # prepare for moving from hip to front
        patch = np.copy(pantie[-140:-5, 546:, :])
        patch = skt.resize(patch[::-1, ::-1, :], (patch.shape[0], 50), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[137:137 + pr, :pc, :] = np.uint8(patch * 255)
        pantie = pantie[:-100]

        # Affine transform matrix
        pantie = np.pad(pantie, [(0, 0), (0, 165), (0, 0)], mode='constant')
        io.imshow(pantie)
        arrx = np.zeros(100)
        arry = np.zeros(100)
        arry[10:] += np.linspace(0, -170, 90)
        arry[10:20] -= np.sin(np.linspace(0, np.pi, 10)) * 20
        pantie = affine_transform_by_arr(pantie, arrx, arry)
        pantie = resize(pantie, [1.6, 1.62])
        pantie = np.bitwise_and(np.uint8(pantie * 255), self.mask)
        return Image.fromarray(pantie)

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        patched = self.paste(patched, pantie, self.pantie_position)
        patched = self.paste(patched, self.gen_texture(image, (26, 215)), [1022, 2469])  # ribbon tail
        patched = self.paste(patched, self.gen_texture(image, (107, 76)), [1304, 2337])  # ribbon ring
        patched = self.paste(patched, self.gen_texture(image, (19, 59)),  [1308, 1719])  # ribbon center
        if self.with_bra:
            bra = self.gen_bra(image)
            patched = self.paste(patched, bra, self.bra_position)
        return patched
