import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image

from src.models.class_patcher import patcher
from src.utils.imgproc import affine_transform_by_arr, resize


class patcher(patcher):
    def __init__(self, body='./body/body_sirius.png', **options):
        super().__init__('シリウス', body=body, pantie_position=[414, 2000], 
            **options)
        self.mask = io.imread('./mask/mask_sirius.png')

    def convert(self, image):
        pantie = np.array(image)

        # 前面下部を下に伸ばす
        patch = np.copy(pantie[-180:-5, 546:, :])
        patch = skt.resize(patch[::-1, ::-1, :], (80, 65), anti_aliasing=True, 
            mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[127 - 5:127 - 5 + pr, :pc, :] = np.uint8(patch * 255)

        # 前面
        front = pantie[:-150, 8:295]

        # 後面のアフィン変換
        back = pantie[:, 300:]
        back = skt.rotate(back, 20, resize=True)
        arrx = np.zeros(100)
        arry = np.zeros(100)
        # 前面とうまく結合するための調整
        arrx[:10] += (np.linspace(0, 1, 10)**2) * 40
        arrx[:10] -= (np.linspace(1, 0, 10)**2) * 17
        arrx[:40] += (np.linspace(1, 0, 40)**2) * 48
        arrx[50:] += (np.linspace(0, 1, 50)**2) * 200
        arrx -= 20
        back = affine_transform_by_arr(back, arrx, arry)
        back = np.uint8(back[10:-250, 28:-60] * 255)

        # 前面と後面を結合して調整
        [fr, fc, d] = front.shape
        [br, bc, d] = back.shape
        shift_x = 0
        shift_y = 85
        pantie = np.zeros((np.max([fr + shift_y, br]), fc + bc - shift_x, d), 
            dtype=np.uint8)
        pantie[shift_y:shift_y + fr, :fc] = front
        pantie[:br, fc - shift_x:] = back
        pantie = np.uint8(resize(pantie, [2.3, 2.53]) * 255)
        pantie = np.bitwise_and(pantie, self.mask)

        # mirroring
        pantie = np.concatenate((pantie[:, ::-1], pantie), axis=1)
        return Image.fromarray(pantie)
