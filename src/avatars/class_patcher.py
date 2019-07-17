from PIL import Image

class patcher():
    def __init__(self, name, body="./body/body.png", pantie_position=[0,0], options=[]):
        self.name = name
        self.body = Image.open(body)
        self.body_size = self.body.size
        self.pantie_position = pantie_position
        self.options = options
    
    def convert(self, pantie):
        return pantie
    
    def patch(self, pantie):
        pantie = self.convert(pantie)
        patched = self.body.copy()
        patched.paste(pantie,self.pantie_position,pantie)
        return patched
    
    def save(self, image, fname):
        image.save(fname)
