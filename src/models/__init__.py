import os
# import skimage.io as io
# import skimage.transform as skt
# import skimage.morphology as skm
# from PIL import Image
# import sys
# sys.path.append('./src/namelist')

namelist = os.listdir('./src/models/')
try:
    namelist.remove('class_patcher.py')
    namelist.remove('__init__.py')
    namelist.remove('__pycache__')
except:
    pass
namelist = [model[:-3] for model in namelist]

__all__ = namelist
