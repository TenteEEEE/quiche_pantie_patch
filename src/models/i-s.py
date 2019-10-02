import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_i-s.png', **options):
        super().__init__('I-s', body=body, pantie_position=[56, 2458], **options)
        self.mask = io.imread('./mask/mask_i-s.png')
        try:
            self.is_4k = self.options['is_4k']
        except:
            self.is_4k = self.ask(question='4K(4096x4096) resolution texture?', default=False)

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-180:-5, 546:, :])
        patch = skt.resize(patch[::-1, ::-1, :], (200, 65), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[127 - 5:127 - 5 + pr, :pc, :] = np.uint8(patch * 255)

        # # Front affine transform
        front = pantie[:, :300]
        front = skt.rotate(front, -3.0, resize=True)
        arrx = (np.linspace(0, 1, 100)**2) * 15 - 10
        arry = np.zeros(100)
        arry[:50] -= (np.sin(np.linspace(0, 2 * np.pi, 100) - np.pi / 4) * 20)[:50]
        front = affine_transform_by_arr(front, arrx, arry)
        front = np.uint8(front[:-150, :-5] * 255)

        # First back affine transform
        back = pantie[:, 300:]
        back = skt.rotate(back, 27.3, resize=True)
        arrx = np.zeros(100)
        arry = np.zeros(100)
        arrx[:40] += (np.linspace(1, 0, 40)**2) * 70
        arrx[50:] += (np.linspace(0, 1, 50)**2) * 220
        arrx -= 20
        back = affine_transform_by_arr(back, arrx, arry)
        back = np.uint8(back[10:-200, 28:] * 255)

        [fr, fc, d] = front.shape
        [br, bc, d] = back.shape
        shift_x = 0
        shift_y = 85
        pantie = np.zeros((np.max([fr + shift_y, br]), fc + bc - shift_x, d), dtype=np.uint8)
        pantie[shift_y:shift_y + fr, :fc] = front
        pantie[:br, fc - shift_x:] = back
        pantie = np.bitwise_and(pantie, self.mask)

        pantie = np.uint8(resize(pantie, [1.63, 1.83]) * 255)
        return Image.fromarray(pantie)

    def patch(self, image, transparent=False):
        image = self.convert(image)
        if transparent:
            if self.is_4k:
                patched = Image.new("RGBA", (4096, 4096))
            else:
                patched = Image.new("RGBA", (2048, 2048))
        else:
            patched = self.body.copy()
        if self.is_4k or patched.size[0] > 2048:
            pantie_position = self.pantie_position
        else:
            pantie_position = (int(self.pantie_position[0] / 2), int(self.pantie_position[1] / 2))
            image = image.resize((int(image.width / 2), int(image.height / 2)), resample=Image.BICUBIC)
        patched = self.paste(patched, image, pantie_position)
        return patched
