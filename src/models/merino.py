from PIL import Image, ImageOps
import numpy as np
import skimage.io as io
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body='./body/body_merino.png', **options):
        super().__init__('メリノ', body=body, pantie_position=[19, 1576], **options)
        self.mask = io.imread('./mask/mask_merino.png')
        self.frills = io.imread('./material/merino_frill.png') / 255
        self.shades = io.imread('./material/merino_frill_shade.png') / 255
        self.frill_alpha = self.frills[:, :, -1]
        self.shade_alpha = self.shades[:, :, -1]
        self.edge = io.imread('./material/merino_edge.png') / 255
        self.edge_alpha = self.edge[:, :, -1]

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-140:-5, 546:, :])
        [pr, pc, d] = patch.shape
        pantie[125:125 + pr, :pc, :] = patch[::-1, ::-1]
        front = pantie[:270, 7:100]
        front = np.uint8(resize(front, [1.6, 1.6]) * 255)
        back = pantie[:415, 90:-10]
        back = np.uint8(resize(back, [1.05, 1.35]) * 255)

        [fr, fc, d] = front.shape
        [br, bc, d] = back.shape
        dy = 23
        pantie = np.pad(back, [(0, fr + dy), (0, 0), (0, 0)], mode='constant')
        pantie[br + dy:, -fc:] = front[:, ::-1]
        pantie = np.bitwise_and(pantie, self.mask)
        pantie = np.concatenate((pantie, pantie[:, ::-1]), axis=1)
        return Image.fromarray(pantie)

    def pick_color(self, arr):
        return np.mean(np.mean(arr, axis=0), axis=0)

    def gen_frills(self, image):
        pantie = np.array(image)
        ribbon = pantie[24:32, 15:27, :3] / 255.0
        ribbon_color = self.pick_color(ribbon)
        ribbon_shade = pantie[26:30, 12:15, :3] / 255.0
        ribbon_shade_color = self.pick_color(ribbon_shade)
        ribbon_shade_color = rgb2hsv(ribbon_shade_color[None, None])
        ribbon_shade_color[0, 0, 1] *= ribbon_shade_color[0, 0, 2] / 0.3
        if ribbon_shade_color[0, 0, 1] > 0.7:
            ribbon_shade_color[0, 0, 1] *= 0.7
        ribbon_shade_color[0, 0, 2] *= ribbon_shade_color[0, 0, 2] / 0.4
        ribbon_shade_color = np.clip(hsv2rgb(ribbon_shade_color)[0, 0], 0, 1)

        frills = self.frills[:, :, :3] * ribbon_color
        shades = self.shades[:, :, -1][:, :, None] * ribbon_shade_color
        frills = alpha_brend(shades, frills, self.shade_alpha)
        frills = np.dstack((frills, self.frill_alpha > 0.5))
        return Image.fromarray(np.uint8(frills * 255))

    def gen_edge(self, image):
        pantie = np.array(image)
        ribbon = pantie[24:32, 15:27, :3] / 255.0
        ribbon_color = self.pick_color(ribbon)
        edge = self.edge[:, :, :3] * ribbon_color
        edge = np.dstack((edge, self.edge_alpha))
        return Image.fromarray(np.uint8(edge * 255))

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", (4096, 4096))
        else:
            patched = self.body.copy()
        patched = self.paste(patched, pantie, self.pantie_position)
        frills = self.gen_frills(image)
        front = frills.crop((0, 0, 110, 170))
        back = frills.crop((110, 0, 170, 90))
        patched = self.paste(patched, front, [781, 2022])
        patched = self.paste(patched, ImageOps.mirror(front), [572, 2022])
        patched = self.paste(patched, back, [1388, 1570])
        patched = self.paste(patched, ImageOps.mirror(back), [14, 1570])
        patched = self.paste(patched, self.gen_edge(image), [37, 1474])
        return patched
