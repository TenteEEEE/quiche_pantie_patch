from flask import Flask, send_from_directory
from flask_restful import Resource, Api, abort
from PIL import Image
import os
import sys
import json
import random
import importlib
import numpy as np
import skimage.io as io
from skimage.measure import *
from src.image_loader import image_loader
sys.path.append('./src/')
import models

app = Flask(__name__)
api = Api(app)
os.makedirs('./converted/', exist_ok=True)
panties = sorted(os.listdir('./dream'))
database = {"models": models.models_namelist, "images": panties}


class request_apps(Resource):
    def get(self):
        return json.dumps({"apps": ["dream", "convert", "suggest"]})


class request_pantie_list(Resource):
    def get(self):
        return json.dumps({"images": panties})


class request_model_option_list(Resource):
    def get(self, model):
        if model not in database['models']:
            return abort(404, message=" {} doesn't exist".format(model))
        return json.dumps({"images": panties})


class request_model_list(Resource):
    def get(self):
        return json.dumps({"models": models.models_namelist})


class request_suggest_list(Resource):
    def get(self, image):
        pantie = int(image[:-4]) - 1
        edge = 100
        panties = sorted(os.listdir('./dream/'))
        ref = io.imread('./dream/' + image)[edge:-edge, edge:-edge, :]
        panties.pop(pantie)
        scores = []
        for i, pantie in enumerate(panties):
            tmp = io.imread('./dream/' + pantie)[edge:-edge, edge:-edge, :]
            score = compare_mse(ref, tmp)
            scores.append(score)
        scores = np.array(scores)
        rank = np.argsort(scores)
        suggests = [panties[index] for index in rank]
        scores = [scores[index] for index in rank]
        return json.dumps({"suggests": suggests, "scores": scores})


class send_pantie(Resource):
    def get(self, image):
        if image not in database['images']:
            return abort(404, message=" {} doesn't exist".format('./dream/' + image))
        return send_from_directory('./dream/', image)


class send_converted(Resource):
    def get(self, model, image):
        # if os.path.isfile('./dream/' + path) is False:
        if image not in database['images']:
            return abort(404, message=" {} doesn't exist".format('./dream/' + image))
        if model not in database['models']:
            return abort(404, message=" {} doesn't exist".format(model))
        if os.path.isfile('./converted/' + model + '/' + image) is False:
            module = importlib.import_module('models.' + model)
            f = open('./webapp.json', mode='r')
            options = json.load(f)
            options['model'] = model
            options['input'] = './body/body_' + model + '.png'
            options['output'] = './converted/' + model + '/' + image
            options['pantie'] = int(image.split('.')[0]) - 1
            patcher = module.patcher(options=options)
            patched = patcher.patch(Image.open('./dream/' + panties[options['pantie']]), transparent=True)
            os.makedirs('./converted/' + model, exist_ok=True)
            patcher.save(patched, options['output'])
        return send_from_directory('./converted/' + model, image)


@app.route('/')
def hello():
    return f'Here is Quiche Pantie Patch Server! You can access the panties: https://pantie-patch.herokuapp.com/dream/****.png. When you convert the panties: https://pantie-patch.herokuapp.com/converted/specify_avatar_name/****.png'


api.add_resource(request_apps, '/api/')
api.add_resource(request_pantie_list, '/dream/', '/api/dream/', '/api/suggest/')
api.add_resource(send_pantie, '/dream/<image>', '/api/dream/<image>')
api.add_resource(request_model_list, '/converted/', '/api/convert/')
api.add_resource(request_model_option_list, '/converted/<model>/', '/api/convert/<model>/')
api.add_resource(send_converted, '/converted/<model>/<image>', '/api/convert/<model>/<image>')
api.add_resource(request_suggest_list, '/suggest/<image>', '/api/suggest/<image>')

if __name__ == '__main__':
    app.run(debug=False)
