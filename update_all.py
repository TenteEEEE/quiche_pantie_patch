from PIL import Image
from tqdm import tqdm
from copy import copy
import hashlib
import os
import json
import importlib
import sys
sys.path.append('./src/')
import models

### Parameters #########################
algorithm = 'sha256'
hash_dict_name = './converted/hash_dict'
converted_dir = './converted/'
pantie_dir = './dream/'
checkflags = {'default', 'with_bra', 'is_lace', 'add_sign', 'stitch_correction', 'is_frill', 'use_ribbon_mesh', 'is_4k'}
########################################


def read_hash(fname, algorithm='sha256'):
    try:
        with open(fname, 'r', encoding='UTF-8') as f:
            hash = hashlib.new(algorithm)
            tmp = f.read()
            hash.update(tmp.encode('utf-8'))
    except:
        return False
    return hash.hexdigest()


def make_hash_dict(checklist, algorithm='sha256'):
    hash_dict = {'algorithm': algorithm}
    for f in checklist:
        hash_dict[f.split('/')[-1]] = read_hash(f + '.py', algorithm)
    return hash_dict


def write_hash_dict(fname, hash_dict):
    try:
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(hash_dict, f)
    except:
        return False
    return True


def read_hash_dict(fname):
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            hash_dict = json.load(f)
    except:
        return None
    return hash_dict


checklist = models.models_namelist
checklist = ['./src/models/' + f for f in checklist]
checklist.append('./src/utils/imgproc')

# Check hash of the models, then make an updated model list
latest_hash = make_hash_dict(checklist, algorithm)
keys = latest_hash.keys()
updated = []
if os.path.exists(hash_dict_name):
    previous_hash = read_hash_dict(hash_dict_name)
    for key in keys:
        try:
            if previous_hash[key] != latest_hash[key]:
                updated.append(key)
        except:  # new model is available
            updated.append(key)
    if 'imgproc' in updated:
        updated = list(keys)[1:-1]  # remove algorithm and imgproc
else:
    updated = list(keys)[1:-1]

# Update panties
f = open('./webapp.json', mode='r')
options = json.load(f)
panties = set(os.listdir(pantie_dir))
for model in models.models_namelist:
    print(f'{model} is updating...')
    module = importlib.import_module('models.' + model)
    try:
        available_options = checkflags & set(options[model])
    except:
        available_options = set()
    available_options.add('default')
    for option in available_options:
        print(f'Process: {option} of {model}...')
        fdir = f'{converted_dir}{model}/{option}/'
        os.makedirs(fdir, exist_ok=True)
        # os.makedirs(f'{converted_dir}{model}/default/', exist_ok=True)
        if model in updated:
            nonexists = panties
        else:
            # nonexists = sorted(panties - set(os.listdir(f'{converted_dir}{model}/default/')))
            nonexists = sorted(panties - set(os.listdir(fdir)))        
        setup = copy(options['all'])
        if option != 'default':
            setup[option] = not setup[option]
        patcher = module.patcher(options=setup)
        for pantie in tqdm(sorted(nonexists)):
            patched = patcher.patch(Image.open(pantie_dir + pantie), transparent=True)
            patcher.save(patched, f'{fdir}{pantie}')

# Update hash dictionary
write_hash_dict(hash_dict_name, latest_hash)
