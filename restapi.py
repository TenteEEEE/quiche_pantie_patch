from flask import Flask, send_from_directory
from flask_restful import Resource, Api, abort
from PIL import Image
import os
import sys
import json
import random
import importlib
from src.image_loader import image_loader
sys.path.append('./src/')
import models

app = Flask(__name__)
# app.config['production'] = True
api = Api(app)
os.makedirs('./converted/', exist_ok=True)
panties = sorted(os.listdir('./dream'))

class image(Resource):
    def get(self, path):
        return send_from_directory('./dream/', path)
        
class model(Resource):
    def get(self, model, path):
        if os.path.isfile('./dream/'+path) is False:
            return abort(404, message=" {} doesn't exist".format('./dream/'+path))
        if model not in models.models_namelist:
            return abort(404, message=" {} doesn't exist".format(model))
        if os.path.isfile('./converted/'+model+path) is False:
            module = importlib.import_module('models.' + model)
            f = open('./webapp.json',mode='r')
            options = json.load(f)
            options['model'] = model
            options['input'] = './body/body_' + model + '.png'
            options['output'] = './converted/'+model+'/'+path
            options['pantie'] = int(path.split('.')[0])-1
            patcher = module.patcher(options=options)
            patched = patcher.patch(Image.open('./dream/'+panties[options['pantie']]), transparent=True)
            os.makedirs('./converted/'+model, exist_ok=True)
            patcher.save(patched, options['output'])
            # return abort(404, message=" {} doesn't exist".format('./converted/'+model+path))
        return send_from_directory('./converted/'+model, path)

@app.route('/')
def hello():
    return f'Here is Quiche Pantie Patch Server!'

api.add_resource(image, '/dream/<path>')
api.add_resource(model, '/converted/<model>/<path>')

if __name__ == '__main__':
    app.run(debug=False)
