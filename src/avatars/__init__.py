import os
# import skimage.io as io
# import skimage.transform as skt
# import skimage.morphology as skm
# from PIL import Image
# import sys
# sys.path.append('./src/namelist')

namelist = os.listdir('./src/avatars/')
try:
    namelist.remove('class_patcher.py')
    namelist.remove('__init__.py')
    namelist.remove('__pycache__')
except:
    pass
namelist = [avatar[:-3] for avatar in namelist]

__all__ = namelist
