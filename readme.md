# キッシュパンツパッチ
パンツは一期一会  

現在対応アバターはパンツ変換を含め、[キッシュ](https://mutachannel.booth.pm/items/954376)ちゃん、[シャーロ](https://tomori-hikage.booth.pm/items/987296)ちゃん、[吸血鬼アンナ](https://wakonoatorie.booth.pm/items/1067958)ちゃん、[ミルク](https://komado.booth.pm/items/1209496)ちゃん、[リンツ](https://mutachannel.booth.pm/items/1255264)ちゃん、[ルア](https://ficsnade.booth.pm/items/1255054)ちゃん、[右近](http://seiga.nicovideo.jp/seiga/im8378009)ちゃん、[ミーシェ](https://booth.pm/ja/items/1256087)ちゃんです。

## 更新履歴
2019/04/13: [ミーシェ](https://booth.pm/ja/items/1256087)ちゃんの変換に対応しました。  
2019/04/12: [キッシュちゃん素体](https://mutachannel.booth.pm/items/1026956)用のオプションを追加。patch.pyで-nをオプションを指定してください。  
2019/04/10: [右近](http://seiga.nicovideo.jp/seiga/im8378009)ちゃんへの変換スクリプトを[thakyuu](https://github.com/thakyuu)さんが開発、本リポジトリにマージしました。  
2019/04/06: [ルア](https://ficsnade.booth.pm/items/1255054)ちゃんの変換に対応しました。  
2019/03/08: [リンツ](https://mutachannel.booth.pm/items/1255264)ちゃんの変換に対応しました。patch.pyで-lオプションを指定してください。  
2019/02/09: [ミルク](https://komado.booth.pm/items/1209496)ちゃんの変換に対応しました。また、dreamフォルダにあるパンツをすべて変換するスクリプトを追加しました。  
2019/01/30: [キッシュ](https://mutachannel.booth.pm/items/954376)ちゃんの他に、[シャーロ](https://tomori-hikage.booth.pm/items/987296)ちゃんと[吸血鬼アンナ](https://wakonoatorie.booth.pm/items/1067958)ちゃんは変換スクリプトで対応しています。  
ちなみに吸血鬼アンナちゃん、ミルクちゃん、ミーシェちゃんは淫紋も刻めます。詳細はパンツコンバートにて。

## 必要なもの
ペイントもしくはレタッチソフトがある方はbody.pngの上に画像を重ねるだけでOKです。  
それすらも面倒だという人の為に、Pythonスクリプトもあります。  
他アバターへのパンツ変換をしたい方は変換スクリプトを動かすためにPythonが必須です。  
[Python(3系を推奨)](https://www.python.org/downloads/)

必要な外部パッケージはコンソールからワン・コマンドでインストールできます。  
`pip install -r requirements.txt`  

このリポジトリは基本的に毎日更新されるので、最新のパンツを追いたい方はGitのインストール推奨です。  
[Git for windows](https://git-scm.com/)  
インストール後はコンソール(cmdもしくはpowershell)を開いて `git clone https://github.com/TenteEEEE/quiche_pantie_patch.git` でダウンロードできます。  
とりあえず最新版にしたければクローンしたディレクトリで`git pull`でいい感じに更新してくれます。

## パンツパッチ(キッシュ、リンツちゃん)
0. このリポジトリを[ダウンロード](https://github.com/TenteEEEE/quiche_pantie_patch/archive/master.zip)します (gitが分かる人はcloneを推奨)
1. body.pngをあなたのbodyテクスチャで置き換えてください
2. コンソールからpatch.pyを実行します `python patch.py`
3. パンツ番号を聞かれるので好きな番号を入力します 例:0001.png
4. patched.pngが上書き済みテクスチャです Enjoy!

パッチを実行するときに `python patch.py -r` とすると、ランダムでパンツが選ばれます。  
また、`-l`を追加するとリンツちゃん向けの微補正を加えます。`-n`はキッシュちゃん素体用のオプションです。

## パンツコンバート
すべてきれいに変換できるわけではありませんが、[シャーロ](https://tomori-hikage.booth.pm/items/987296)ちゃん、[吸血鬼アンナ](https://wakonoatorie.booth.pm/items/1067958)ちゃん、[ミルク](https://komado.booth.pm/items/1209496)ちゃん、[ルア](https://ficsnade.booth.pm/items/1255054)ちゃん、[右近](http://seiga.nicovideo.jp/seiga/im8378009)ちゃん、[ミーシェ](https://booth.pm/ja/items/1256087)ちゃんのパンツに変換できます。  
基本的にパンツパッチに使うコマンドを `python patch_[character].py` に変えるだけです。  
変換画像だけ欲しいときは `python convert_[character].py`で作れます。  
他にも使用者が多いアバターはできるだけ対応したいので、対応して欲しい人はテストユーザになる覚悟とともにテクスチャ画像を[@tenteeeee_vrc](https://twitter.com/tenteeeee_vrc)に送ってください。

### 特殊オプション
#### シャーロちゃん
* -c: 縫い目の補正方法を変更できます。なんか変になったというときに書いてみてください。

#### アンナちゃん
* -s: 淫紋をお腹に刻みます。

#### ミルクちゃん
* -s: 淫紋をお腹に刻みます。

#### ミーシェちゃん
* -s: 淫紋をお腹に刻みます。

## 変換サンプル
|||
|:-:|:-:|
|[シャーロ](https://tomori-hikage.booth.pm/items/987296)ちゃん|[吸血鬼アンナ](https://wakonoatorie.booth.pm/items/1067958)ちゃん|
|![test](./sample/shaclo_pantie.png)|![test](./sample/anna_pantie.png)|
|[ミルク](https://komado.booth.pm/items/1209496)ちゃん|[ルア](https://ficsnade.booth.pm/items/1255054)ちゃん|
|![test](./sample/milk_pantie.png)|![test](./sample/lua_pantie.png)|
|[右近](http://seiga.nicovideo.jp/seiga/im8378009)ちゃん|[ミーシェ](https://booth.pm/ja/items/1256087)ちゃん|
|![test](./sample/ukon_pantie.png)|![test](./sample/mishe_pantie.png)|


## スペシャルサンクス
[Booth:キッシュちゃん](https://mutachannel.booth.pm/items/954376)  
右近ちゃんパンツコンバータの作者:[thakyuuさん](https://github.com/thakyuu)

## 画像のライセンス
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="クリエイティブ・コモンズ・ライセンス" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br /><a xmlns:cc="http://creativecommons.org/ns#" href="https://twitter.com/tenteeeee_vrc" property="cc:attributionName" rel="cc:attributionURL">TenteEEEE</a> を著作者とするこの <span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/StillImage" rel="dct:type">作品</span> は <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">クリエイティブ・コモンズの 表示 - 非営利 - 継承 4.0 国際 ライセンス</a>で提供されています。  
作品のクレジットの表示が必要なライセンスではありますが、アバターのテクスチャにクレジット表記という無粋なものは不要です！  
どこかで再配布する場合などに別のテキストファイルなどで記載してください。  
また、商用利用したい場合は[@tenteeeee_vrc](https://twitter.com/tenteeeee_vrc)までご相談ください。  

## ソフトウェアのライセンス
MITライセンス(一行で:無料で自由に使える/変更できるが、なにか問題があっても作者は責任を負わない)に従います。  
https://opensource.org/licenses/mit-license.php  
Copyright (c) 2019 TenteEEEE  


---
**English**
# Quiche Pantie Patch
Treasure every pantie encounter as it may not come again.

## Update log
2018/12/05 crop.py crops the pantie texture for pantie designer.  
2018/12/06 patch.py supports random pantie option '-r'. (`python patch.py -r`)  
2018/12/18 convert_shaclo.py converts Quiche pantie to [Shaclo](https://tomori-hikage.booth.pm/items/987296) pantie.  
2018/12/25 convert_shaclo.py supports stitch correction switch.  
2018/12/25 convert_anna.py converts Quiche pantie to [Anna](https://wakonoatorie.booth.pm/items/1067958) pantie.  
2019/02/09 convert_milk.py converts Quiche pantie to [Milk](https://komado.booth.pm/items/1209496) pantie.  
2019/03/08 patch.py supports [Linz](https://mutachannel.booth.pm/items/1255264). Please set -l option when you run the patch.py  
2019/04/06 convert_lua.py converts Quiche pantie to [Lua](https://ficsnade.booth.pm/items/1255054) pantie.  
2019/04/10 [thakyuu](https://github.com/thakyuu) developed [Ukon](http://seiga.nicovideo.jp/seiga/im8378009) converter, and it was merged.  
2019/04/12 patch.py supports [Quiche body](https://mutachannel.booth.pm/items/1026956). Please set -n option when you run the patch.py  
2019/04/13 covert_mishe.py converts Quiche pantie to [Mishe](https://booth.pm/ja/items/1256087) pantie.

# Pre-requirements
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

## Converted examples
|||
|:-:|:-:|
|[Shaclo](https://tomori-hikage.booth.pm/items/987296)|[Anna](https://wakonoatorie.booth.pm/items/1067958)|
|![test](./sample/shaclo_pantie.png)|![test](./sample/anna_pantie.png)|
|[Milk](https://komado.booth.pm/items/1209496)|[Lua](https://ficsnade.booth.pm/items/1255054)|
|![test](./sample/milk_pantie.png)|![test](./sample/lua_pantie.png)|
|[Ukon](http://seiga.nicovideo.jp/seiga/im8378009)|[Mishe](https://booth.pm/ja/items/1256087)|
|![test](./sample/ukon_pantie.png)|![test](./sample/mishe_pantie.png)|

# Any error?
## Windows
Open your favorite terminal and then `pip install -r requirements.txt`.
## Linux/OSX
`pip install -r requirements.txt` or `sudo pip install -r requirements.txt`

# Special thanks
[Quiche model](https://mutachannel.booth.pm/items/954376)  
Developer of the Ukon pantie converter: [thakyuu](https://github.com/thakyuu)

# License for my images
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work by <a xmlns:cc="http://creativecommons.org/ns#" href="https://twitter.com/tenteeeee_vrc" property="cc:attributionName" rel="cc:attributionURL">TenteEEEE</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.  
When you want to use it on your business, please ask [@tenteeeee_vrc](https://twitter.com/tenteeeee_vrc).

# License for my scripts
Released under the MIT license  
https://opensource.org/licenses/mit-license.php  
Copyright (c) 2019 TenteEEEE  
