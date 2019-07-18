import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_milk.png'):
        super().__init__('Milk', body=body, pantie_position=[741, 224])
        self.mask = io.imread('./mask/mask_milk.png')
        self.sign_position = [754, 113]

    def convert(self, image):
        pantie = np.array(image)
        mask = io.imread('./mask/mask_milk.png')
        pantie = np.bitwise_and(pantie, mask)
        [r, c, d] = pantie.shape
        front = pantie[:160 + 30, :200, :]
        back = pantie[:300, 200:, ]
        patch = pantie[-100:-5, 546:, :][::-1, ::-1, :]

        # Front and front patch pre-processing
        front = resize(front, (2, 2))
        patch = resize(patch, (1.0, 1.15))
        [fr, fc, _] = front.shape
        [pr, pf, _] = patch.shape
        patch_pad = np.zeros((fr, fc, d))
        patch_pad[-pr:, :pf, :] = patch
        patch_pad = perspective_transform(patch_pad, np.matrix('1, 0, 0; 0, 1, 0; -0.002,0,1'))
        patch_pad = patch_pad[-pr - 40:, :pf - 20, :][:, ::-1, :]
        [pr, pf, _] = patch_pad.shape

        # Alpha blending and transform between front and front patch
        remain = front[-pr:, :pf, :] * np.float32(skm.dilation(patch_pad[:, :, -1] == 0))[:, :, np.newaxis]
        nonzeromask = np.logical_or(skm.dilation(patch_pad[:, :, -1] == 1), remain[:, :, -1] == 1)
        patch_pad = remain + patch_pad
        normalizer = patch_pad[:, :, -1][:, :, np.newaxis]
        normalizer[normalizer == 0] = 1
        patch_pad = patch_pad / normalizer
        patch_pad[:, :, -1] = np.float32(nonzeromask)
        front[-pr:, :pf, :] = patch_pad
        front = perspective_transform(front, np.matrix('1, 0, 0; 0, 1, 0; -0.001,0,1'))
        front = front[:, :-120, :]
        front = affine_transform(front, 30, 0, inv=True)

        # Back transform
        back = resize(back, (1.3, 1.3))[:, ::-1, :]
        back = perspective_transform(back, np.matrix('1, 0, 0; 0, 1, 0; 0.0002,0,1'))[:, ::-1, :]
        back = affine_transform(back, 70, 150, inv=False)
        back = back[:, 138:, :]

        [fr, fc, _] = front.shape
        [br, bc, _] = back.shape
        pantie = np.zeros((np.max([fr, br]), fc + bc - 2, d))
        shiftr = 35
        row_point = np.clip(shiftr + fr, 0, np.max([fr, br]))
        pantie[shiftr:row_point, :fc, :] = front[:-(shiftr + fr - row_point), :, :]
        pantie[:bc, fc - 1:, :] = back[:, 1:, :]
        # io.imshow(pantie)

        # Finalize
        pantie = np.uint8(pantie * 255)
        return Image.fromarray(pantie)
