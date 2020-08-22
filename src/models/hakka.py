import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_hakka.png', **options):
        super().__init__('薄荷', body=body, pantie_position=[0, 0], **options)
        self.mask_front = io.imread('./mask/mask_hakka_front.png')
        self.mask_back = io.imread('./mask/mask_hakka_back.png')

    def convert_front(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-120:-5, 546:, :])
        [pr, pc, d] = patch.shape
        pantie[125:125 + pr, :pc, :] = patch[::-1, ::-1]
        front = pantie[:, :330]
        arrx = np.zeros(64)
        arrx[20:] += np.sin(np.linspace(0, np.pi / 2, 44)) * 79
        arrx[10:20] += np.sin(np.linspace(0, np.pi, 10)) * 8
        arrx -= 80
        arry = np.zeros(64)
        front = affine_transform_by_arr(front, arrx, arry)[:320]
        front = np.uint8(resize(front, [1.2, 1.12]) * 255)[:, 8:]
        front = np.bitwise_and(front, self.mask_front)
        front = np.concatenate([front[:, ::-1], front], axis=1)
        return Image.fromarray(front)

    def convert_back(self, image):
        pantie = np.array(image)
        pantie[-120:, 546:, :] = 0
        back = np.rot90(pantie[:-15, 330:][:, ::-1])
        arrx = np.zeros(36)
        arry = np.zeros(36)
        arry[5:-5] = np.sin(np.linspace(0, np.pi, 26))**2 * 50
        arry -= 30
        back = affine_transform_by_arr(back, arrx, arry)
        back = np.rot90(back, -1)
        arrx = np.zeros(64)
        arrx[6:] = np.linspace(0, np.pi / 2, 58)**2 * 43
        arrx[45:55] += np.sin(np.linspace(0, np.pi, 10)) * 4
        arrx -= 80
        arry = np.zeros(64)
        back = affine_transform_by_arr(back, arrx, arry)[:320]
        back = np.uint8(resize(back, [1.2, 1.12]) * 255)[:, 18:]
        back = np.bitwise_and(back, self.mask_back)
        back = np.concatenate([back[:, ::-1], back], axis=1)
        return Image.fromarray(back)

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        patched = self.paste(patched, self.convert_front(image), (2180, 1671))
        patched = self.paste(patched, self.convert_back(image), (2907, 1647))
        return patched
