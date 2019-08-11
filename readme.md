# キッシュちゃんパンツパッチ
パンツは一期一会  

当リポジトリはキッシュちゃんに限らず、**様々な3Dアバターにパンツを着せることだけが目的のプログラムです。**  
キッシュちゃんのUVに合わせてパンツを描けば、他のアバター向けに自動変換後、テクスチャに貼り付けます。  
現在対応アバターは、[キッシュ](https://mutachannel.booth.pm/items/954376)ちゃん(素体はブラジャーも対応)、[キッシュ・ライト](https://mutachannel.booth.pm/items/1379653)ちゃん、[シャーロ](https://tomori-hikage.booth.pm/items/987296)ちゃん、[吸血鬼アンナ](https://wakonoatorie.booth.pm/items/1067958)ちゃん([ライト](https://wakonoatorie.booth.pm/items/1405336))、[ミルク](https://komado.booth.pm/items/1209496)ちゃん、[リンツ](https://mutachannel.booth.pm/items/1255264)ちゃん(素体はブラジャーも対応)、[ルア](https://ficsnade.booth.pm/items/1255054)ちゃん([クエスト](https://ficsnade.booth.pm/items/1414368))、[右近](http://seiga.nicovideo.jp/seiga/im8378009)ちゃん、[ミーシェ](https://ponderogen.booth.pm/items/1256087)ちゃん、[ファジー](https://nagatorokoyori.booth.pm/items/1255283)ちゃん、 [たぬ](https://udonfactory.booth.pm/items/1414433)ちゃん、[ラムネ](https://komado.booth.pm/items/1411609)、[幽狐](https://armadillon.booth.pm/items/1484117)ちゃんです。

## 導入
透過PNGの作成であれば[らぼてんDiscord](https://discord.gg/ad4Qsfa)のてんてーさんBotに話しかける、もしくは[Joniburn](https://github.com/joniburn)さんの[ウェブアプリ](https://joniburn.github.io/quiche-pantie-patch-gui/)を使えば導入は不要です。  
手物のテクスチャに全自動でパッチしたければ下記の導入を進めてください。

2019/06/12以降は[自動インストールバッチファイル](https://gist.github.com/TenteEEEE/1ef33308bd841e3c5f1c8a1a8ab95d67)を実行するのが一番簡単です。  
導入後はパンツパッチのフォルダでコマンドプロンプトを開き、`git pull`でいい感じにしてくれます。  
画像つきの導入手順は[**こちら**](https://github.com/TenteEEEE/quiche_pantie_patch/wiki/Installation-%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)から！

手動で導入する場合は、[siro_choco0621](https://twitter.com/siro_choco0621)さんが導入についての[メモ](https://twitter.com/siro_choco0621/status/1131587508238659585)をまとめてくださいましたので、こちらを参考に！  
URL: https://twitter.com/siro_choco0621/status/1131587508238659585

### プログラム起動の確認
1. **パンツパッチのフォルダ直下(somewhere\quiche_pantie_patch)でコンソールを起動する** [参考URL](https://www.lifehacker.jp/2013/03/130320windows_cmd.html)
1. `python patch.py` でプログラムを起動する
1. なにか動いてアバター一覧が表示されればOKです。

パンツパッチに限らず多くのプログラムはプログラムフォルダ直下で動くようになっています。  
**必ずパンツパッチのフォルダでコンソールを起動してください。**  

## 使い方
基本的にどのアバターであっても`python patch.py`としてパッチャーを起動するだけですが、主に2つの使い方を想定しています。

1. それぞれのアバターにパンツをパッチする (対話形式でのパッチ)
1. よく使うアバターに同様の設定でパンツをパッチし続ける (jsonセットアップでのパッチ)

### 1. 対話形式の使い方
1. bodyフォルダにアバターのテクスチャを置く (できればもともと配置されている名前に合わせたほうが楽)
1. **パンツパッチのフォルダでコンソールを起動する** [参考URL](https://www.lifehacker.jp/2013/03/130320windows_cmd.html)
1. `python patch.py` でプログラムを起動する
1. アバター一覧が表示されるので番号を入力してEnter
1. 適宜オプションについて聞かれるのでy/nで答える(Enterを打てばデフォルトの動作になる)
1. patched.png がパンツパッチされたものです

使い方がわからないときは`python patch.py -h`で説明が出力されます。  

#### オプション
* -m: モデル名を指定する。  
例: `python patch.py -m quiche`
* -a: すべてのパンツをパッチする。 パッチされたものはconvertedフォルダのモデル名のフォルダに作成されます。  
例: `python patch.py -m quiche -a`
* -f: -aは上書きをしません。 上書きするときはこちらも指定してください。  
例: `python patch.py -m quiche -a -f`
* -i: bodyテクスチャのファイル名を指定。  
例: `python patch.py -m quiche -i ./body/body.png`
* -o: 出力されるテクスチャのファイル名を指定。  
例: `python patch.py -m quiche -o patched.png`
* -d: -a時に出力されるディレクトリを指定。  
例: `python patch.py -m quiche -d linz`
* -p: パンツを指定。指定しなければ最新のものが適用される。 -a時は開始番号にもなる。  
例: `python patch.py -m quiche -p 101`
* -r: ランダムにパンツを選ぶ。  
例: `python patch.py -m quiche -r`
* -t: 透過PNGで作成。 配布するときに便利なオプションで、私以外に需要はおそらくない。  
例: `python patch.py -m quiche -t`
* -j: [favorite.json](favorite.json)の設定を読み込んでパッチする。 このとき他の引数は全て無効化されます。  
例: `python patch.py -j`

### 2. jsonによる設定の自動読み込みでの使い方
jsonによる設定読み込みに対応しました。対話形式がだるい/毎日最新のパンツをパッチするつもりの人には便利かも。  
json読み込みによるパッチは `python patch.py -j` です。

jsonは開発者にはよく使われている形式のファイルですが、基本的に以下のようなただのテキストファイルです。  
お気に入りのエディタで開いて設定してください。項目はなんとなく分かると思います。
こちらのサンプルはリンツちゃん素体用の設定例です。  
`git pull`で最新のパンツを取り込んだ後、この設定で`python patch.py -j`すれば、勝手に最新のパンツだけ変換されます。  
``` json
{
  "":"-----Common Setup-----",
  "model":"quiche_nbody",
  "input":"./body/body_linz.png",
  "output":"patched.png",
  
  "":"I guess normally true is comfortable for you. When you set false, it patches a single pantie",
  "all":true,
  
  "":"When you set all, you can define the directory name. default will be a model name",
  "":"It may useful when you make Linz texture using quiche model",
  "directory":"default",

  "":"Pantie number. 0 means the latest one. It may comfort for you.",
  "pantie":0,

  "":"When you want to update all converted textures, set true",
  "force":false,

  "":"When you want to make transparent textures, set true",
  "transparent": false,

  "":"When you want to choose a pantie randomly, set true",
  "random": false,

  "":"-----Setup for Quiche and Linz bra-----",
  "with_bra":true,
  "is_lace":false,
  "dis_ribbon":false,
  "dis_shading":false,
  "dis_decoration":false,
  "dis_texturing":false,

  "":"-----Setup for immoral sign-----",
  "add_sign":false,
  "fsign":"./material/anna_sign.png",

  "":"-----Setup for stitch correction for Shaclo-----",
  "stitch_correction":false,
  
  "":"-----Setup for frill correction for Fuzzy-----",
  "is_frill":false
}
```

## 変換サンプル
|||
|:-:|:-:|
|[シャーロ](https://tomori-hikage.booth.pm/items/987296)ちゃん|[吸血鬼アンナ](https://wakonoatorie.booth.pm/items/1067958)ちゃん|
|![test](./sample/shaclo_pantie.png)|![test](./sample/anna_pantie.png)|
|[ミルク](https://komado.booth.pm/items/1209496)ちゃん|[ルア](https://ficsnade.booth.pm/items/1255054)ちゃん|
|![test](./sample/milk_pantie.png)|![test](./sample/lua_pantie.png)|
|[右近](http://seiga.nicovideo.jp/seiga/im8378009)ちゃん|[ミーシェ](https://ponderogen.booth.pm/items/1256087)ちゃん|
|![test](./sample/ukon_pantie.png)|![test](./sample/mishe_pantie.png)|
|[ファジー](https://nagatorokoyori.booth.pm/items/1255283)ちゃん|[吸血鬼アンナ light](https://wakonoatorie.booth.pm/items/1405336)ちゃん|
|![test](./sample/fuzzy_pantie.png)|![test](./sample/anna_light_pantie.png)|
|キッシュ/リンツ用のブラ(フリル)|キッシュ/リンツ用のブラ(レース)|
|![test](./sample/bra_frill.png)|![test](./sample/bra_lace.png)|
|[ルア・クエスト](https://ficsnade.booth.pm/items/1414368)ちゃん|[たぬ](https://udonfactory.booth.pm/items/1414433)ちゃん|
|![test](./sample/lua_quest_pantie.png)|![test](./sample/tanu_pantie.png)|
|[ラムネ](https://komado.booth.pm/items/1411609)ちゃん|[幽狐](https://armadillon.booth.pm/items/1484117)ちゃん|
|![test](./sample/ramne_pantie.png)|![test](./sample/yuko_pantie.png)|

## 対応してほしいアバターがある/開発者の方へ
未対応のアバターがあれば、テストユーザーになる覚悟とともにボディのテクスチャ(できればUVマップのあるもの)を[@tenteeeee_vrc](https://twitter.com/tenteeeee_vrc)まで送っていただければ何とかなるかも。  
対応アバターのスクリプトを書いてみたい人はコードや[Wiki](https://github.com/TenteEEEE/quiche_pantie_patch/wiki)のFor Developersを読むと分かりやすいかも。

## スペシャルサンクス
[Booth:キッシュちゃん](https://mutachannel.booth.pm/items/954376)  
右近ちゃんパンツコンバータの作者:[thakyuu](https://github.com/thakyuu)さん  
patch.pyのargparse対応:[4hiziri](https://github.com/4hiziri)さん  
[ウェブアプリ](https://joniburn.github.io/quiche-pantie-patch-gui/)の開発者:[Joniburn](https://github.com/joniburn)さん  

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
You look the pantie only once.

The purpose of the repository is to apply various panties to various 3D models.  

## Installation
If you just make the transparent textures, you don't have to install it.  
You can make it by my DiscordBot in [my server](https://discord.gg/ad4Qsfa), or [web app](https://joniburn.github.io/quiche-pantie-patch-gui/).  
When it is not enough, please follow the following instruction.

Please check it out [the automatic install batch](https://gist.github.com/TenteEEEE/1ef33308bd841e3c5f1c8a1a8ab95d67).  
You just run the batch file with administrator permission.

## Usage
1. Put your body texture in the body folder
1. **Start a console in the pantie patch folder**
1. Run the command `python patch.py`
1. It asks about avatars, so type a number
1. Some avatars have a special option. Please answer the question when you see it.
1. patched.png is the patched texture. Enjoy!

When you want to know the help, please run `python patch.py -h`

#### Options
* -m: Name of the model (e.g. `python patch.py -m quiche`)
* -a: Convert all the panties. The patched textures will be exported to converted/modelname folder. (e.g. `python patch.py -m quiche -a`)
* -f: -a doesn't overwrite. When you want to overwrite them, set it. (e.g. `python patch.py -m quiche -a -f`)
* -i: Name of the body texture (e.g. `python patch.py -m quiche -i ./body/body.png`)
* -o: Name of the output texture (e.g. `python patch.py -m quiche -o patched.png`)
* -d: Name of the directory when you set -a (e.g. `python patch.py -m quiche -d linz`)
* -p: Pantie number. The default is the latest pantie. When you set -a, it will be start number (e.g. `python patch.py -m quiche -p 101`)
* -r: It chooses a pantie randomly (e.g. `python patch.py -m quiche -r`)
* -t: Patched to transparent textures.  (e.g. `python patch.py -m quiche -t`)
* -j: Load favorite.json for auto configuration (e.g. `python patch.py -j`)

[favorite.json](favorite.json) is useful to run the program. Please check it out.

## Converted examples
|||
|:-:|:-:|
|[Shaclo](https://tomori-hikage.booth.pm/items/987296)|[Anna](https://wakonoatorie.booth.pm/items/1067958)|
|![test](./sample/shaclo_pantie.png)|![test](./sample/anna_pantie.png)|
|[Milk](https://komado.booth.pm/items/1209496)|[Lua](https://ficsnade.booth.pm/items/1255054)|
|![test](./sample/milk_pantie.png)|![test](./sample/lua_pantie.png)|
|[Ukon](http://seiga.nicovideo.jp/seiga/im8378009)|[Mishe](https://ponderogen.booth.pm/items/1256087)|
|![test](./sample/ukon_pantie.png)|![test](./sample/mishe_pantie.png)|
|[Fuzzy](https://nagatorokoyori.booth.pm/items/1255283)|[Anna light](https://wakonoatorie.booth.pm/items/1405336)|
|![test](./sample/fuzzy_pantie.png)|![test](./sample/anna_light_pantie.png)|
|Bra for Quiche and Linz (Frill)|Bra for Quiche and Linz (Lace)|
|![test](./sample/bra_frill.png)|![test](./sample/bra_lace.png)|
|[Lua for Quest](https://ficsnade.booth.pm/items/1414368)|[Tanu](https://udonfactory.booth.pm/items/1414433)|
|![test](./sample/lua_quest_pantie.png)|![test](./sample/tanu_pantie.png)|
|[Ramne](https://komado.booth.pm/items/1411609)|[Yuko](https://armadillon.booth.pm/items/1484117)|
|![test](./sample/ramne_pantie.png)|![test](./sample/yuko_pantie.png)|

## Special thanks
[Quiche model](https://mutachannel.booth.pm/items/954376)  
Developer of the Ukon pantie converter: [thakyuu](https://github.com/thakyuu)  
Improvement of patch.py:[4hiziri](https://github.com/4hiziri)  
Developer of the [web app](https://joniburn.github.io/quiche-pantie-patch-gui/): [Joniburn](https://github.com/joniburn)  

## License for my images
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work by <a xmlns:cc="http://creativecommons.org/ns#" href="https://twitter.com/tenteeeee_vrc" property="cc:attributionName" rel="cc:attributionURL">TenteEEEE</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.  
When you want to use it on your business, please ask [@tenteeeee_vrc](https://twitter.com/tenteeeee_vrc).

## License for my scripts
Released under the MIT license  
https://opensource.org/licenses/mit-license.php  
Copyright (c) 2019 TenteEEEE  
