# Start command
# uvicorn restapi:app
# gunicorn restapi:app -k uvicorn.workers.UvicornWorker

from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, RedirectResponse
from starlette.requests import Request
from PIL import Image
import os
import sys
import json
import importlib
import numpy as np
from datetime import datetime
import skimage.io as io
from skimage.metrics import *
from src.image_loader import image_loader
sys.path.append('./src/')
import models
import secrets

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
    log.update({str(len(log)): {'model': model, 'image': image, 'flag': flags}})
    try:
        with open(log_dir + logfile, 'w') as f:
            json.dump(log, f, indent=2, separators=(',', ':'))
    except:
        pass


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return f'Here is Quiche Pantie Patch Server! You can access the panties: https://pantie-patch.herokuapp.com/api/dream/****.png. When you convert the panties: https://pantie-patch.herokuapp.com/api/convert/specify_avatar_name/****.png'


os.makedirs(converted_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)
panties = sorted(os.listdir('./dream'))
database = {"models": models.models_namelist, "images": panties}
display_names = make_display_names()
logfile = datetime.today().strftime('%Y_%m_%d_%H_%M') + '.json'
log = {}
try:
    with open(log_dir + logfile, 'w') as f:
        json.dump(log, f)
except:
    pass


class score_processor:
    def __init__(self, workers=2):
        self.panties = sorted(os.listdir(pantie_dir))
        self.done = False
        self.startpoint = 0
        try:
            self.score_matrix = np.load(converted_dir + 'score_matrix.npy')
            if self.score_matrix.shape[0] == len(panties):
                self.done = True
            else:
                pad = len(panties) - self.score_matrix.shape[0]
                self.startpoint = self.score_matrix.shape[0]
                self.score_matrix = np.pad(self.score_matrix, [(0, pad), (0, pad)], mode='constant')
        except:
            self.score_matrix = np.zeros((len(self.panties), len(self.panties)))
        self.workers = workers

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
        ref = io.imread(pantie_dir + panties[num])[50:-edge * 2, edge:-edge, :3]
        for check_pantie in remains:
            tmp = np.array(template_loader.read())[50:-edge * 2, edge:-edge, :3]
            scores.append(mean_squared_error(ref, tmp))
        if full:
            scores = np.insert(scores, num, 0)
        else:
            scores = np.pad(scores, (num + 1, 0), mode='constant')
        return np.array(scores)

    def argument_generator(self, num_pantie, flag=True):
        for i in range(self.startpoint, num_pantie):
            yield (i, flag)

    def start(self):
        t = Thread(target=self.process, args=())
        t.daemon = True
        if self.done is not True:
            t.start()
        return t

    def process(self):
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            nums = len(panties)
            if self.startpoint != 0:
                scores = executor.map(self.score_row, self.argument_generator(nums, True))
            else:
                scores = executor.map(self.score_row, self.argument_generator(nums, False))

            for row, score in enumerate(scores):
                if self.startpoint != 0:
                    self.score_matrix[:, row + self.startpoint] = score
                else:
                    self.score_matrix[row + self.startpoint, :] = score
            self.score_matrix = np.triu(self.score_matrix)
            self.score_matrix += self.score_matrix.T
        np.save(converted_dir + 'score_matrix.npy', self.score_matrix)
        self.done = True


sp = score_processor()
sp_thred = sp.start()


@app.get("/api/")
async def request_apps():
    if os.path.exists('./zips/sharelinks.json'):
        return {"apps": ["dream", "convert", "suggest", "gacha", "zip"]}
    else:
        return {"apps": ["dream", "convert", "suggest", "gacha"]}


@app.get("/api/dream/")
async def request_pantie_list():
    return {"images": panties}


@app.get("/api/dream/{image}")
async def send_pantie(image: str):
    if image not in database['images']:
        raise HTTPException(status_code=404, detail=f"{image} doesn't exist")
    return FileResponse(pantie_dir + image, media_type="image/png")


@app.get("/api/convert/")
async def request_model_list():
    return {"display_names": display_names, "models": models.models_namelist}


@app.get("/api/convert/{model}/")
async def request_model_option_list(model: str):
    with open('./webapp.json', mode='r') as f:
        options = json.load(f)
    if model not in database['models']:
        raise HTTPException(status_code=404, detail=f"{model} doesn't exist")
    display_name = display_names[database['models'].index(model)]
    try:
        options = options[model]
    except:
        options = []
    return {"display_name": display_name, "images": panties, "options": options}


@app.get("/api/convert/{model}/{image}")
async def send_converted(model: str, image: str, request: Request):
    if image not in database['images']:
        raise HTTPException(status_code=404, detail=f"{image} doesn't exist")
    if model not in database['models']:
        raise HTTPException(status_code=404, detail=f"{model} doesn't exist")

    with open('./webapp.json', mode='r') as f:
        options = json.load(f)['all']

    def option_parser(options):
        flags = []
        for key in options.keys():
            if request.query_params.get(key) is not None:
                print(key + ':' + request.query_params.get(key))
                tmp = options[key]
                if request.query_params.get(key) in ['true', 'True', 'yes', 'Yes']:
                    options[key] = True
                else:
                    options[key] = False
                if tmp != options[key]:
                    flags.append(key)
        return options, flags

    options, flags = option_parser(options)
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
    return FileResponse(fdir + image, media_type="image/png")


@app.get("/api/suggest/")
async def request_pantie_list():
    return {"images": panties}


@app.get("/api/suggest/{image}")
async def request_suggest_list(image: str):
    if image not in database['images']:
        raise HTTPException(status_code=404, detail=f"{image} doesn't exist")
    pantie = int(image[:-4]) - 1
    if sp.done:
        scores = sp.score_matrix[pantie, :]
    else:
        scores = sp.score_row((pantie, True))
    rank = np.argsort(scores)
    suggests = [database['images'][index] for index in rank[1:]]
    scores = [scores[index] for index in rank[1:]]
    return {"suggests": suggests, "scores": scores}


@app.get("/api/gacha/")
async def request_gacha_list():
    return {"1ren", "10ren"}


@app.get("/api/gacha/1ren")
async def send_1ren_result():
    return {panties[secrets.randbelow(len(panties))]}


@app.get("/api/gacha/10ren")
async def send_10ren_result():
    return [panties[secrets.randbelow(len(panties))] for i in range(10)]


@app.get("/api/zip/")
async def request_zip_list():
    try:
        with open('./zips/sharelinks.json', mode='r') as f:
            zips = json.load(f)
    except:
        raise HTTPException(status_code=404, detail=f"Zip doesn't exist")
    return {"display_names": display_names, "zips": [k for k in sorted(zips.keys())]}


@app.get("/api/zip/{zipname}")
async def send_zip(zipname: str):
    try:
        with open('./zips/sharelinks.json', mode='r') as f:
            zips = json.load(f)
    except:
        raise HTTPException(status_code=404, detail=f"Zip doesn't exist")
    if zipname not in zips.keys():
        raise HTTPException(status_code=404, detail=f"{zipname} doesn't exist")
    update_log(zipname.split('.')[0], zipname, ['zip'])
    return RedirectResponse(url=zips[zipname])
