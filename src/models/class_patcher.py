from PIL import Image


class patcher():
    def __init__(self, name, body="./body/body.png", pantie_position=[0, 0], options=None):
        self.name = name
        self.body = Image.open(body)
        self.body_size = self.body.size
        self.pantie_position = pantie_position
        try:
            self.options = options['options']
        except:
            self.options = options

    def convert(self, image):
        return image

    def paste(self, ref, image, position):
        ref.paste(image, position, image)
        return ref

    def patch(self, image, transparent=False):
        image = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()

        patched = self.paste(patched, image, self.pantie_position)
        return patched

    def save(self, image, fname):
        image.save(fname)

    def ask(self, question, default=False, default_msg=None):
        if default_msg is None:
            default_msg = 'y' if default else 'n'
        message = question + ' [default:' + default_msg + '] (y/n):'
        while True:
            ans = input(message)
            if ans in ['', 'y', 'n']:
                break
        matching_char = ['', 'y'] if default else ['', 'n']

        if ans in matching_char:
            return True if default else False
        else:
            return False if default else True
