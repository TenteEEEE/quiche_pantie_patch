from PIL import Image
import os
import sys
import random
import convert_lua_quest as cvt

print("Lua quest pantie patcher. Options: [-r] Random pantie")
args = sys.argv
panties = os.listdir('./dream/')
if len(args)>1:
    if '-r' in args[1:]:
        num = random.randint(0,len(panties))
        fname = panties[num]
    else:
        fname =  input("Type pantie name: ./dream/")
else:
    fname =  input("Type pantie name: ./dream/")

if fname in panties:
    cvt.convert2luaquest(fname)
    pantie = Image.open('./lua_quest_pantie.png')
    origin = Image.open('body_lua_quest.png')
    origin.paste(pantie,(28,3529),pantie)
    origin.save('patched_lua_quest.png')
    print("Done. Please check patched.png.")
else:
    print("Cannot find it")
