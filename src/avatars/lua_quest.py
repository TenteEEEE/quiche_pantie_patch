import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.avatars.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_lua_quest.png'):
        super().__init__('Lua-Quest', body=body, pantie_position=[28, 3529])
        self.mask = io.imread('./mask/mask_lua_quest.png')

    def convert(self, image):
        pantie = np.array(image)

        patch = np.copy(pantie[-140:-5, 546:, :])
        patch = skt.resize(patch[::-1, ::-1, :], (230, 65), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[127 - 5:127 - 5 + pr, :pc, :] = np.uint8(patch * 255)

        front = pantie[:350, :300, :]
        front = np.pad(front, [(0, 0), (100, 130), (0, 0)], mode='constant')
        front = perspective_transform(front, np.matrix('1, 0.05, 0; 0, 1, 0; 0.0005,0,1'))
        front = perspective_transform(front, np.matrix('1, 0.0, 0; 0, 1, 0; -0.0009,0,1'))
        front = front[:-45, 70:335]
        front = resize(front, [1.7, 1.7])

        back = pantie[:380, 300:, :]
        back = np.pad(back, [(15, 0), (0, 200), (0, 0)], mode='constant')
        back = perspective_transform(back, np.matrix('1, -0.1, 0; 0.01, 1, 0; -0.0006,0,1'))
        back = back[:-70, 10:290, :]
        back = resize(back, [1.36, 1.36])

        [fr, fc, _] = front.shape
        [br, bc, _] = back.shape
        shift_y = 20
        pantie = np.zeros((np.max([fr, br]) + shift_y, fc + bc, d))
        pantie[shift_y:shift_y + fr, :fc, :] = front
        pantie[:br, fc:, :] = back
        pantie = pantie[12:, 16:, :]
        pantie = np.bitwise_and(np.uint8(pantie * 255), self.mask)
        return Image.fromarray(pantie)
