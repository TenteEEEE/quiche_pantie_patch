from PIL import Image, ImageOps
import numpy as np
import skimage.io as io
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body='./body/body_wolferia.png', **options):
        super().__init__('ウルフェリア', body=body, pantie_position=[285, 2301], **options)
        self.mask = io.imread('./mask/mask_wolferia.png')

        self.bra_position = [263, 373]
        self.bra = np.float32(io.imread('./mask/bra_wolferia.png') / 255)
        self.bra_center = np.float32(io.imread('./mask/bra_wolferia_center.png') / 255)
        self.bra_shade = np.float32(io.imread('./material/bra_wolferia_shade.png') / 255)
        self.bra_shade_alpha = self.bra_shade[:, :, -1]

        self.bra_component = np.float32(io.imread('./material/bra_wolferia_component.png') / 255)
        self.bra_component_shade = np.float32(io.imread('./material/bra_wolferia_component_shade.png') / 255)
        self.bra_component_shade_alpha = self.bra_component_shade[:, :, -1]

        self.ribbon_position = [300, 2766]
        self.ribbon = np.float32(io.imread('./material/ribbon_wolferia.png') / 255)
        self.ribbon_shade = np.float32(io.imread('./material/ribbon_wolferia_shade.png') / 255)
        self.ribbon_shade_alpha = self.ribbon_shade[:, :, -1]

    def pick_color(self, arr):
        return np.mean(np.mean(arr, axis=0), axis=0)

    def extract_base_color(self, pantie):
        front = pantie[20:100, 30:80, :3] / 255.0
        front_shade = pantie[130:150, 0:40, :3] / 255.0
        front_color = self.pick_color(front)
        front_shade_color = self.pick_color(front_shade)
        front_shade_color = rgb2hsv(front_shade_color[None, None])
        front_shade_color[0, 0, 1] *= front_shade_color[0, 0, 2] / 0.3
        front_shade_color[0, 0, 1] *= 4
        front_shade_color[0, 0, 2] *= front_shade_color[0, 0, 2] / 0.2
        front_shade_color = np.clip(hsv2rgb(front_shade_color)[0, 0], 0, 1)
        return front_color, front_shade_color

    def gen_ribbon(self, image):
        pantie = np.array(image)
        ribbon = pantie[24:32, 15:27, :3] / 255.0
        ribbon_color = self.pick_color(ribbon)
        ribbon_shade = pantie[26:30, 12:15, :3] / 255.0
        ribbon_shade_color = self.pick_color(ribbon_shade)
        ribbon = self.ribbon[:, :, :3] * ribbon_color
        ribbon_shade = (self.ribbon_shade[:, :, -1])[:, :, None] * ribbon_shade_color
        ribbon = alpha_brend(ribbon_shade, ribbon, self.ribbon_shade_alpha)
        ribbon = np.dstack((ribbon, self.ribbon[:, :, -1] > 0.5))
        return Image.fromarray(np.uint8(np.clip(ribbon, 0, 1) * 255))

    def gen_component(self, image):
        pantie = np.array(image)
        front_color, front_shade_color = self.extract_base_color(pantie)
        ribbon = pantie[24:32, 15:27, :3] / 255.0
        ribbon_color = self.pick_color(ribbon)
        component = self.bra_component[:, :, :3] * front_color
        component_shade = (self.bra_component_shade[:, :, -1])[:, :, None] * front_shade_color
        component = alpha_brend(component_shade, component, self.bra_component_shade_alpha)
        component = np.dstack((component, self.bra_component[:, :, 0]))
        return Image.fromarray(np.uint8(np.clip(component, 0, 1) * 255))

    def gen_bra(self, image):
        pantie = np.array(image)
        front_color, front_shade_color = self.extract_base_color(pantie)
        ribbon = pantie[24:32, 15:27, :3] / 255.0
        ribbon_color = self.pick_color(ribbon)
        center = np.float32(pantie[20:170, -250:-15, :3][:, ::-1]) / 255
        center = resize(center, [7, 7])
        bra_center = np.copy(self.bra_center)
        bra_center[300:300 + center.shape[0], 290:290 + center.shape[1], :3] = center * np.float32(bra_center[300:300 + center.shape[0], 290:290 + center.shape[1], :3] > 0)
        bra = self.bra[:, :, :3] * front_color
        bra_shade = (self.bra_shade[:, :, -1])[:, :, None] * front_shade_color
        bra = alpha_brend(bra_center[:, :, :3], bra[:, :, :3], bra_center[:, :, 0] > 0.1)
        bra = alpha_brend(bra_shade, bra, self.bra_shade_alpha)
        bra = np.dstack((bra, self.bra[:, :, 0]))
        return Image.fromarray(np.uint8(np.clip(bra, 0, 1) * 255))

    def convert(self, image):
        pantie = np.array(image)
        pantie = ribbon_inpaint(pantie)
        patch = np.copy(pantie[-50:-5, 546:, :])
        [pr, pc, d] = patch.shape
        pantie[120:120 + pr, :pc, :] = patch
        pantie = np.uint8(resize(pantie, [3.32, 3.1]) * 255)
        pantie = np.bitwise_and(pantie, self.mask)
        return Image.fromarray(pantie)

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", (4096, 4096))
        else:
            patched = self.body.copy()
        patched = self.paste(patched, self.gen_ribbon(image), self.ribbon_position)
        patched = self.paste(patched, pantie, self.pantie_position)
        patched = self.paste(patched, self.gen_bra(image), self.bra_position)
        patched = self.paste(patched, self.gen_component(image), [0, 0])
        return patched
