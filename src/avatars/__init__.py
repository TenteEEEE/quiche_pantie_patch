import os
# import skimage.io as io
# import skimage.transform as skt
# import skimage.morphology as skm
# from PIL import Image
# import sys
# sys.path.append('./src/avatars')

avatars = os.listdir('./src/avatars/')
try:
    avatars.remove('class_patcher.py')
    avatars.remove('__init__.py')
    avatars.remove('__pycache__')
except:
    pass
avatars = [avatar[:-3] for avatar in avatars]

__all__ = avatars
