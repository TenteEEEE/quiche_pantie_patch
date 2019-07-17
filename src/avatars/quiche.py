import sys
sys.path.append('./src/avatars')
from class_patcher import patcher

class patcher(patcher):
    def __init__(self):
        super().__init__('Quiche',pantie_position=[1018,828])
