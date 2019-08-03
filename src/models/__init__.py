import os

models_namelist = sorted(os.listdir('./src/models/'))
try:
    models_namelist.remove('class_patcher.py')
    models_namelist.remove('__init__.py')
    models_namelist.remove('__pycache__')
except:
    pass
models_namelist = [model[:-3] for model in models_namelist]

__all__ = models_namelist
