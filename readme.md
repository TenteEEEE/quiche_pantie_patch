# Quiche Pantie Patch
Treasure every pantie encounter as it may not come again.

## Update log
2018/12/05 crop.py crops the pantie texture for pantie designer.  
2018/12/06 patch.py support random pantie option '-r'. (`python patch.py -r`)  
2018/12/18 convert_shaclo.py convert Quiche pantie to [Shaclo](https://booth.pm/ja/items/987296) pantie.  

Currently, Shaclo pantie converter has an issue that it cannot convert a pantie which has a unique hip texture. It is caused by stitch correction of the hip. I will make an option to choose correction algorithm in the future.

# Pre-required
If you have any paint or retouch software, you can override easily.  
However, I understand that you guys are lazy.   
Don't worry, I prepared a python script to override the body.png.  
[Python(3 is recommended)](https://www.python.org/downloads/)

For Shaclo pantie converter, scikit-image is required.  
`pip install scikit-image`

# Texture overriding
1. Overwrite body.png
2. Run patch.py `python patch.py`
3. Put your favorite number (example: 0001.png)
4. Enjoy

# Your own dream panties overriding
1. Overwrite body.png
1. Place your panties in the dream folder
2. Run patch.py `python patch.py`
3. Put your pantie name
4. Enjoy

# Any error?
## Windows
Open your favorite terminal and then `pip install pillow`.
## Linux/OSX
`pip install pillow` or `sudo pip install pillow`

# Special thanks
[Quiche model](https://booth.pm/ja/items/954376)
