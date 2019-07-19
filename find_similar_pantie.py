import numpy as np
import skimage.io as io
from skimage.measure import *
import os
import argparse

parser = argparse.ArgumentParser(description='似ているパンツを検索します. This script finds similar panties')
parser.add_argument('pantie', help='パンツの番号を数値で指定してください. Please input pantie number', type=int)
parser.add_argument('-l', '--list', help='リストアップする数. Number of displayed similar pantie', type=int, default=5)
parser.add_argument('-e', '--edge', help='周辺エッジのトリミング数. Number of triming edge around the corner', type=int, default=50)
parser.add_argument('-s', '--ssim', help='SSIMで視覚的に近いもの探す. Calculate the cost by SSIM',action="store_true")
args = parser.parse_args()

panties = os.listdir('./dream/')
fname = panties[args.pantie-1]
ref = io.imread('./dream/'+fname)[args.edge:-args.edge,args.edge:-args.edge,:]
panties.pop(args.pantie-1)

print('Start searching similar panties as: ' + fname)
scores = []
for i,pantie in enumerate(panties):
    print('\rProcess: ' + pantie + ' [' + str(np.around((i+1)/len(panties)*100,2)) + '%]', end="")
    tmp = io.imread('./dream/'+pantie)[args.edge:-args.edge,args.edge:-args.edge,:]
    if args.ssim:
        score = (1-compare_ssim(ref,tmp,multichannel=True))*100
    else:
        score = compare_mse(ref,tmp)
    scores.append(score)
print("\nDone! Close the image window to show the next suggestion. (Lower score is better)")

scores = np.array(scores)
rank = np.argsort(scores)
for i, index in enumerate(rank[:args.list]):
    print('Rank ' + str(i+1) + ': ' + panties[index] + ', Score: ' + str(np.around(scores[index],2)))
    io.imshow(io.imread('./dream/'+panties[index]))
    io.show()
