import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body="./body/body_fuzzy.png", **options):
        super().__init__("ファジー", body=body, pantie_position=[845, 1593], **options)
        self.mask = io.imread("./mask/mask_fuzzy.png")
        try:
            self.is_frill = self.options["is_frill"]
        except:
            self.is_frill = self.ask(question="Is there a frill on the hip?", default=False)

    def convert(self, image):
        pantie = np.array(image)
        pantie = np.bitwise_and(pantie, self.mask)

        # move from hip to front
        if self.is_frill:
            patch = np.copy(pantie[-230:-5, 485:, :])
            patch = np.pad(patch, [(0, 0), (100, 100), (0, 0)], mode="constant")
            patch = skt.rotate(patch, 90)
        else:
            patch = np.copy(pantie[-212:-5, 485:, :])
            patch = np.pad(patch, [(0, 0), (100, 100), (0, 0)], mode="constant")
            patch = skt.rotate(patch, 90)
        # Affine transform matrix for patch
        [r, c, d] = patch.shape
        src_cols = np.linspace(0, c, 10)
        src_rows = np.linspace(0, r, 10)
        src_rows, src_cols = np.meshgrid(src_rows, src_cols)
        src = np.dstack([src_cols.flat, src_rows.flat])[0]
        shifter_row = np.zeros(src.shape[0])
        shifter_col = np.zeros(src.shape[0])
        shifter_row = +(np.sin(np.linspace(0, 1 * np.pi, src.shape[0]) + np.pi / 8) * 60)
        dst_rows = src[:, 1] + shifter_row + 25
        dst_cols = src[:, 0] + shifter_col
        dst = np.vstack([dst_cols, dst_rows]).T
        affin = skt.PiecewiseAffineTransform()
        affin.estimate(src, dst)
        patch = np.uint8(skt.warp(patch, affin) * 255)
        pantie[-250:, 485:, :] = 0
        if self.is_frill:
            patch = skt.rotate(patch, 90)[:, 59:160]
            patch = skt.resize(patch[:, :, :], (215, 86), anti_aliasing=True, mode="reflect")
            pantie[119 : 119 + 215, :86, :] = np.uint8(patch * 255)
        else:
            patch = skt.rotate(patch, 90)[:, 68:155]
            patch = skt.resize(patch[:, :, :], (210, 90), anti_aliasing=True, mode="reflect")
            pantie[119 : 119 + 210, :90, :] = np.uint8(patch * 255)

        # Affine transform matrix for whole image
        pantie = np.pad(pantie, [(50, 0), (50, 0), (0, 0)], mode="constant")
        [r, c, d] = pantie.shape
        src_cols = np.linspace(0, c, 10)
        src_rows = np.linspace(0, r, 10)
        src_rows, src_cols = np.meshgrid(src_rows, src_cols)
        src = np.dstack([src_cols.flat, src_rows.flat])[0]
        shifter_row = np.zeros(src.shape[0])
        shifter_col = np.zeros(src.shape[0])
        shifter_row = np.sin(np.linspace(0, 1 * np.pi, src.shape[0]) - np.pi / 2) * 80
        shifter_row[30:60] += (np.sin(np.linspace(0, 1 * np.pi, src.shape[0]) - np.pi / 8) * 40)[30:60]
        shifter_row[:30] += (np.sin(np.linspace(0, 1 * np.pi, src.shape[0]) + np.pi / 2) * 60)[:30]

        shifter_col = np.sin(np.linspace(0, 1 * np.pi, src.shape[0]) + np.pi / 2) * 125
        shifter_col[-50:] -= (np.sin(np.linspace(0, 1 * np.pi, src.shape[0]) - np.pi / 3) * 260)[-50:]
        shifter_col = abs(shifter_col)

        shifter_row = np.convolve(shifter_row, np.ones(30) / 30, mode="valid")
        shifter_col = np.convolve(shifter_col, np.ones(10) / 10, mode="valid")
        shifter_row = skt.resize(shifter_row, (100, 1), anti_aliasing=True, mode="reflect")[:, 0]
        shifter_col = skt.resize(shifter_col, (100, 1), anti_aliasing=True, mode="reflect")[:, 0]
        shifter_row[0:20] = -17

        dst_rows = src[:, 1] + shifter_row - 20
        dst_cols = src[:, 0] + shifter_col - 80
        dst = np.vstack([dst_cols, dst_rows]).T
        affin = skt.PiecewiseAffineTransform()
        affin.estimate(src, dst)
        pantie = np.uint8(skt.warp(pantie, affin) * 255)[20:-30, 19:-180, :]
        [r, c, d] = pantie.shape
        npantie = np.zeros((r, c * 2, d), dtype=np.uint8)
        npantie[:, c:, :] = pantie
        npantie[:, :c, :] = pantie[:, ::-1, :]

        # Finalize
        npantie = skt.resize(
            npantie,
            (int(npantie.shape[0] * 2.51 * 1.04), int(npantie.shape[1] * 2.51)),
            anti_aliasing=True,
            mode="reflect",
        )
        npantie = np.uint8(npantie * 255)
        return Image.fromarray(npantie)
