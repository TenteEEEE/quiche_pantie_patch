from PIL import Image, ImageOps
import numpy as np
import skimage.io as io
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body='./body/body_kyoko_alpha.png', **options):
        super().__init__('京子(Alpha)', body=body, pantie_position=[718, 1464], **options)
        try:
            self.with_garter = self.options['with_garter']
        except:
            self.with_garter = self.ask(question='With garter belt?', default=True)
        self.garter_position = [0, 3491]
        self.pantie_position = [0, 3714]
        self.lace = np.float32(io.imread('./material/kyoko_alpha_lace.png') / 255)
        self.lace_alpha = self.lace[:, :, -1]

    def pick_color(self, arr):
        return np.mean(np.mean(arr, axis=0), axis=0)

    def convert(self, image):
        pantie = np.array(image)
        ribbon = pantie[24:32, 15:27, :3] / 255.0
        ribbon_color = self.pick_color(ribbon)
        lace = self.lace[:, :, :3] * ribbon_color
        lace = np.dstack((lace, self.lace_alpha))
        return Image.fromarray(np.uint8(lace * 255))

    def patch(self, image, transparent=False):
        lace = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", (4096, 4096))
        else:
            patched = self.body.copy()
        patched = self.paste(patched, lace, self.pantie_position)
        if self.with_garter:
            patched = self.paste(patched, lace, self.garter_position)
        return patched
