import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body='./body/body_rainy.png', **options):
        super().__init__('レイニィ', body=body, pantie_position=[1806, 702], **options)

        self.bra_position = [53, 468]
        self.bra = np.float32(io.imread('./mask/bra_rainy.png') / 255)
        self.bra_center = np.float32(io.imread('./mask/bra_rainy_center.png') / 255)
        self.bra_shade = np.float32(io.imread('./material/bra_rainy_shade.png') / 255)
        self.bra_component = np.float32(io.imread('./material/bra_rainy_component.png') / 255)
        self.bra_shade_alpha = self.bra_shade[:, :, -1]
        self.bra_component_mask = self.bra_component[:, :, -1] > 0.5

        self.bra_bottom_position = [258, 47]
        self.bra_bottom = np.float32(io.imread('./material/bra_rainy_bottom.png')[:, :, -1] / 255)

    def pick_color(self, arr):
        return np.mean(np.mean(arr, axis=0), axis=0)

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-190:-5, 546:, :])
        pantie[-190:, 546:, :] = 0
        patch = np.uint8(resize(patch, [1, 1.3]) * 255)
        [pr, pc, d] = patch.shape
        pantie[125:125 + pr, :pc, :] = patch[::-1, ::-1]
        pantie = np.uint8(resize(pantie, [3.7, 3.6]) * 255)[85:]
        return Image.fromarray(pantie)

    def gen_upper_panite(self, image):
        pantie = np.array(image)
        edge = resize(pantie[:50], [3.7, 3.3])[:150, 28:]
        arrx = np.zeros(25)
        arry = np.zeros(25)
        arry[2:-2] = np.linspace(0, 1, 21)**3 * -50
        arry[7:-7] += np.sin(np.linspace(0, np.pi, 11)) * -22
        arry[13:] += np.sin(np.linspace(0, np.pi, 12)) * -13
        arry[17:] += np.sin(np.linspace(0, np.pi, 8))**1.5 * 50
        edge = affine_transform_by_arr(edge, arrx, arry)
        edge = np.uint8(edge[:110, 1:] * 255)
        edge = np.concatenate([edge[:, ::-1], edge], axis=1)
        return Image.fromarray(edge)

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
        center = resize(center, [5, 5])

        bra_center = np.copy(self.bra_center)
        bra_center[-center.shape[0]:, :center.shape[1], :3] = center * np.float32(bra_center[-center.shape[0]:, :center.shape[1], :3] > 0)
        bra = self.bra[:, :, :3] * front_color
        bra_shade = (self.bra_shade[:, :, -1])[:, :, None] * front_shade_color
        bra_component = self.bra_component[:, :, :3] * ribbon_color

        # overlaying layers
        bra = alpha_brend(bra_center[:, :, :3], bra[:, :, :3], bra_center[:, :, 0] > 0.1)
        bra = alpha_brend(bra_component, bra, self.bra_component_mask)
        bra = alpha_brend(bra_shade, bra, self.bra_shade_alpha)
        bra = np.dstack((bra, self.bra[:, :, 0] > 0.8))
        return Image.fromarray(np.uint8(np.clip(bra, 0, 1) * 255))

    def gen_bra_bottom(self, image):
        pantie = np.array(image)
        front = pantie[20:100, 30:80, :3] / 255.0
        front_shade = pantie[130:150, 0:40, :3] / 255.0
        front_color = self.pick_color(front)
        front_shade_color = self.pick_color(front_shade)
        r, c = self.bra_bottom.shape
        bottom = np.ones((r, c, 3), dtype=np.float32) * front_color
        bottom_shade = self.bra_bottom[:, :, None] * front_shade_color
        bottom = alpha_brend(bottom_shade, bottom, self.bra_bottom)
        bottom = np.dstack((bottom, bottom[:, :, 0] > 0))
        return Image.fromarray(np.uint8(np.clip(bottom, 0, 1) * 255))

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", (4096, 4096))
        else:
            patched = self.body.copy()
        patched = self.paste(patched, pantie, self.pantie_position)
        patched = self.paste(patched, self.gen_upper_panite(image), (5, 243))
        patched = self.paste(patched, self.gen_bra(image), self.bra_position)
        patched = self.paste(patched, self.gen_bra_bottom(image), self.bra_bottom_position)
        return patched
