import os
from PIL import Image
from queue import Queue
from threading import Thread


class image_loader:
    def __init__(self, fdir, queuesize=10):
        self.fdir = fdir
        self.flist = os.listdir(self.fdir)
        self.Q = Queue(maxsize=queuesize)

    def len(self):
        return self.Q.qsize()

    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        
    def update(self):
        for fname in self.flist:
            image = Image.open(self.fdir + fname)
            self.Q.put(image)

    def read(self, fname=None):
        if fname is None:
            return self.Q.get()
        else:
            return Image.open(self.fdir + fname)
            
