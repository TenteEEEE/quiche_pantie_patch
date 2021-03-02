from PIL import Image, ImageOps
import numpy as np
import skimage.io as io
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body='./body/body_kyoko.png', **options):
        super().__init__('京子', body=body, pantie_position=[718, 1464], **options)
        self.mask = io.imread('./mask/mask_kyoko.png')
        try:
            self.with_garter = self.options['with_garter']
        except:
            self.with_garter = self.ask(question='With garter belt?', default=True)
        if self.with_garter:
            self.garter_position = [701, 1272]
            self.garter = np.float32(io.imread('./material/garter_kyoko.png') / 255)
            self.garter_shade = np.float32(io.imread('./material/garter_kyoko_shade.png') / 255)
            self.garter_shade_alpha = self.garter_shade[:, :, -1]

        self.bra_position = [700, 1008]
        self.bra = np.float32(io.imread('./mask/bra_kyoko.png') / 255)
        self.bra_center = np.float32(io.imread('./mask/bra_kyoko_center.png') / 255)
        self.bra_shade = np.float32(io.imread('./material/bra_kyoko_shade.png') / 255)
        self.bra_lace = np.float32(io.imread('./material/bra_kyoko_lace.png') / 255)
        self.bra_shade_alpha = self.bra_shade[:, :, -1]
        self.bra_lace_mask = self.bra_lace[:, :, -1] > 0.3

        self.pantie_ribbon_position = [745, 1528]
        self.bra_ribbon_position = [800, 1173]
        self.ribbon = np.float32(io.imread('./material/ribbon_kyoko.png') / 255)
        self.ribbon_shade = np.float32(io.imread('./material/ribbon_kyoko_shade.png') / 255)
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
        if front_shade_color[0, 0, 1] > 0.7:
            front_shade_color[0, 0, 1] *= 0.7
        front_shade_color[0, 0, 2] *= front_shade_color[0, 0, 2] / 0.4
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

    def gen_garter(self, image):
        pantie = np.array(image)
        front_color, front_shade_color = self.extract_base_color(pantie)
        garter = self.garter[:, :, :3] * front_color
        garter_shade = (self.garter_shade[:, :, -1])[:, :, None] * front_shade_color
        garter = alpha_brend(garter_shade, garter, self.garter_shade_alpha)
        garter = np.dstack((garter, self.garter[:, :, -1] > 0.5))
        return Image.fromarray(np.uint8(np.clip(garter, 0, 1) * 255))

    def gen_bra(self, image):
        pantie = np.array(image)
        front_color, front_shade_color = self.extract_base_color(pantie)
        ribbon = pantie[24:32, 15:27, :3] / 255.0
        ribbon_color = self.pick_color(ribbon)
        center = np.float32(pantie[20:170, -200:-15, :3][:, ::-1]) / 255
        bra_center = np.copy(self.bra_center)
        bra_center[80:80 + center.shape[0], 30:30 + center.shape[1], :3] = center * np.float32(bra_center[80:80 + center.shape[0], 30:30 + center.shape[1], :3] > 0)
        bra = self.bra[:, :, :3] * front_color
        bra_shade = (self.bra_shade[:, :, -1])[:, :, None] * front_shade_color
        bra_lace = self.bra_lace[:, :, :3] * ribbon_color
        bra = alpha_brend(bra_center[:, :, :3], bra[:, :, :3], bra_center[:, :, 0] > 0.1)
        bra = alpha_brend(bra_lace, bra, self.bra_lace_mask)
        bra = alpha_brend(bra_shade, bra, self.bra_shade_alpha)
        bra = np.dstack((bra, self.bra[:, :, 0] > 0.8))
        return Image.fromarray(np.uint8(np.clip(bra, 0, 1) * 255))

    def convert(self, image):
        pantie = np.array(image)
        pantie = ribbon_inpaint(pantie)
        patch = np.copy(pantie[-140:-5, 546:, :])
        [pr, pc, d] = patch.shape
        pantie[125:125 + pr, :pc, :] = patch
        pantie[-140:, 546:, :] = 0
        pantie = np.uint8(resize(pantie, [0.7, 0.7]) * 255)[:170]
        pantie = np.bitwise_and(pantie, self.mask)
        return Image.fromarray(pantie)

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", (4096, 4096))
        else:
            patched = self.body.copy()
        patched = self.paste(patched, pantie, self.pantie_position)
        patched = self.paste(patched, self.gen_bra(image), self.bra_position)
        ribbon = self.gen_ribbon(image)
        patched = self.paste(patched, ribbon, self.pantie_ribbon_position)
        patched = self.paste(patched, ribbon.resize((int(ribbon.width * 0.62), int(ribbon.height * 0.62))), self.bra_ribbon_position)
        if self.with_garter:
            patched = self.paste(patched, self.gen_garter(image), self.garter_position)
        return patched
