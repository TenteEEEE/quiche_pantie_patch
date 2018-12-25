# Quiche Pantie Patch
Treasure every pantie encounter as it may not come again.

## Update log
2018/12/05 crop.py crops the pantie texture for pantie designer.  
2018/12/06 patch.py support random pantie option '-r'. (`python patch.py -r`)  
2018/12/18 convert_shaclo.py convert Quiche pantie to [Shaclo](https://tomori-hikage.booth.pm/items/987296) pantie.  
2018/12/25 convert_shaclo.py support stitch correction switch.  
2018/12/25 convert_anna.py convert Quiche pantie to [Anna](https://wakonoatorie.booth.pm/items/1067958) pantie.  

# Pre-required
If you have any paint or retouch software, you can override easily.  
However, I understand that you guys are lazy.   
Don't worry, I prepared a python script to override the body.png.  
[Python(3 is recommended)](https://www.python.org/downloads/)

The patch require external packages.  
I summarized them in the requirements.txt and you can install it easily.  
`pip install -r requirements.txt`

# Texture overriding
1. Overwrite body.png
2. Run patch.py `python patch.py`
3. Put your favorite number (example: 0001.png)
4. Enjoy

The instructions can also be used for Shaclo and Anna patch.  

# Your own dream panties overriding
1. Overwrite body.png
1. Place your panties in the dream folder
2. Run patch.py `python patch.py`
3. Put your pantie name
4. Enjoy

# Any error?
## Windows
Open your favorite terminal and then `pip install -r requirements.txt`.
## Linux/OSX
`pip install -r requirements.txt` or `sudo pip install -r requirements.txt`

# Special thanks
[Quiche model](https://mutachannel.booth.pm/items/954376)
