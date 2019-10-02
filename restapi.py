from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, send_from_directory, request, jsonify
from flask_restful import Resource, Api, abort
from flask_cors import CORS
from PIL import Image
import os
import sys
import json
import random
import importlib
import numpy as np
from datetime import datetime
import skimage.io as io
from skimage.measure import *
from src.image_loader import image_loader
sys.path.append('./src/')
import models

### Parameters #################################################
pantie_dir = './dream/'
converted_dir = './converted/'
log_dir = './logs/'
################################################################


def make_display_names():
    with open('./webapp.json', mode='r') as f:
        options = json.load(f)['all']
    display_names = [importlib.import_module('models.' + model).patcher(options=options).name for model in models.models_namelist]
    return display_names

def update_log(model, image, flags):
    log.update({str(len(log)):{'model':model, 'image':image,'flag':flags}})
    try:
        with open(log_dir+logfile, 'r+') as f:
            json.dump(log,f,indent=2,separators=(',', ':'))
    except:
        pass

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

os.makedirs(converted_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)
panties = sorted(os.listdir('./dream'))
database = {"models": models.models_namelist, "images": panties}
display_names = make_display_names()
logfile = datetime.today().strftime('%Y_%m_%d_%H_%M') + '.json'
log = {}
try:
    with open(log_dir+logfile, 'w') as f:
        json.dump(log,f)
except:
    pass


class score_processor:
    def __init__(self, workers=2):
        self.panties = sorted(os.listdir(pantie_dir))
        self.score_matrix = np.zeros((len(self.panties), len(self.panties)))
        self.workers = workers
        self.done = False

    # it is for triangular score matrix. when you set full, it calculate a line of the full matrix
    def score_row(self, args):
        num = args[0]
        full = args[1]
        edge = 100
        remains = self.panties.copy()
        if full:
            remains.pop(num)
        else:
            [remains.pop(0) for i in range(num + 1)]
        template_loader = image_loader(fdir=pantie_dir, queuesize=32)
        template_loader.flist = remains
        template_loader.start()
        scores = []
        ref = io.imread('./dream/%04d.png' % (num + 1))[50:-edge * 2, edge:-edge, :3]
        for check_pantie in remains:
            tmp = np.array(template_loader.read())[50:-edge * 2, edge:-edge, :3]
            scores.append(compare_mse(ref, tmp))
        return np.array(scores)

    def argument_generator(self, num_pantie, flag=True):
        for i in range(num_pantie):
            yield (i, flag)

    def start(self):
        t = Thread(target=self.process, args=())
        t.daemon = True
        t.start()
        return t

    def process(self):
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            nums = len(os.listdir(pantie_dir))
            # score_matrix = np.zeros((nums, nums))
            scores = executor.map(self.score_row, self.argument_generator(nums, False))
            for row, score in enumerate(scores):
                self.score_matrix[row, row + 1:] = score
            self.score_matrix += self.score_matrix.T
        self.done = True


sp = score_processor()
sp_thred = sp.start()


class request_apps(Resource):
    def get(self):
        return {"apps": ["dream", "convert", "suggest"]}


class request_pantie_list(Resource):
    def get(self):
        return {"images": panties}


class request_model_option_list(Resource):
    def __init__(self):
        with open('./webapp.json', mode='r') as f:
            self.options = json.load(f)

    def get(self, model):
        if model not in database['models']:
            return abort(404, message=" {} doesn't exist".format(model))
        display_name = display_names[database['models'].index(model)]
        try:
            options = self.options[model]
        except:
            options = []
        return jsonify({"display_name": display_name, "images": panties, "options": options})


class request_model_list(Resource):
    def get(self):
        return jsonify({"models": models.models_namelist, "display_names": display_names})


class request_suggest_list(Resource):
    def get(self, image):
        panties = sorted(os.listdir(pantie_dir))
        pantie = int(image[:-4]) - 1
        if sp.done:
            scores = sp.score_matrix[pantie, :]
        else:
            scores = sp.score_row((pantie, True))
        rank = np.argsort(scores)
        suggests = [panties[index] for index in rank[1:]]
        scores = [scores[index] for index in rank[1:]]
        return {"suggests": suggests, "scores": scores}


class send_pantie(Resource):
    def get(self, image):
        if image not in database['images']:
            return abort(404, message=" {} doesn't exist".format(pantie_dir + image))
        return send_from_directory(pantie_dir, image)


class send_converted(Resource):
    def __init__(self):
        with open('./webapp.json', mode='r') as f:
            self.options = json.load(f)['all']

    def option_parser(self):
        options = self.options.copy()
        flags = []
        for key in options.keys():
            if request.args.get(key) is not None:
                print(key + ':' + request.args.get(key))
                tmp = options[key]
                if request.args.get(key) == 'true':
                    options[key] = True
                else:
                    options[key] = False
                if tmp != options[key]:
                    flags.append(key)
        return options, flags

    def get(self, model, image):
        if image not in database['images']:
            return abort(404, message=" {} doesn't exist".format(pantie_dir + image))
        if model not in database['models']:
            return abort(404, message=" {} doesn't exist".format(model))
        options, flags = self.option_parser()
        fdir = f'{converted_dir}{model}/'
        if len(flags) == 0:
            fdir += 'default/'
        elif len(flags) == 1:
            fdir += f'{flags[0]}/'
        else:
            fdir += 'others/'
        if not os.path.exists(fdir + image) or 'others' in fdir:
            os.makedirs(fdir, exist_ok=True)
            module = importlib.import_module('models.' + model)
            options['model'] = model
            options['input'] = './body/body_' + model + '.png'
            options['output'] = fdir + image
            options['pantie'] = int(image.split('.')[0]) - 1
            patcher = module.patcher(options=options)
            patched = patcher.patch(Image.open(pantie_dir + panties[options['pantie']]), transparent=True)
            patcher.save(patched, options['output'])
        update_log(model, image, flags)
        return send_from_directory(fdir, image)


@app.route('/')
def hello():
    return f'Here is Quiche Pantie Patch Server! You can access the panties: https://pantie-patch.herokuapp.com/api/dream/****.png. When you convert the panties: https://pantie-patch.herokuapp.com/api/convert/specify_avatar_name/****.png'


api.add_resource(request_apps, '/api/')
api.add_resource(request_pantie_list, '/api/dream/', '/api/suggest/')
api.add_resource(send_pantie, '/api/dream/<image>')
api.add_resource(request_model_list, '/api/convert/')
api.add_resource(request_model_option_list, '/api/convert/<model>/')
api.add_resource(send_converted, '/api/convert/<model>/<image>')
api.add_resource(request_suggest_list, '/api/suggest/<image>')

if __name__ == '__main__':
    app.run(debug=False)
