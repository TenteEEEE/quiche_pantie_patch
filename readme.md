
[English](https://github.com/TenteEEEE/quiche_pantie_patch?#quiche-pantie-patch)

# キッシュちゃんパンツパッチ
![logo](./material/logo_256.png)  
パンツは一期一会   

当リポジトリはキッシュちゃんに限らず、**様々な3Dアバターにパンツを着せることだけが目的のプログラムです。**  
キッシュちゃんのUVに合わせてパンツを描けば、他のアバター向けに自動変換後、テクスチャに貼り付けます。  
対応アバターは[**キッシュちゃんパンツパッチ対応表**](https://docs.google.com/spreadsheets/d/1z6Kw_KkmiUfvYbeaBYnFoxirTYy4BvlyBG6XmHB00_E/edit?usp=sharing)をご確認ください。  
対応したいモデラーさんは[**CC0ぱんつ**](https://github.com/TenteEEEE/quiche_pantie_patch/wiki/CC0%E3%81%B1%E3%82%93%E3%81%A4)**の利用を検討してください。**  

## 導入
透過PNGの作成であれば[らぼてんDiscord](https://discord.gg/ad4Qsfa)のてんてーさんBotに話しかける、もしくは[Joniburn](https://github.com/joniburn)さんの[ウェブアプリ](https://joniburn.github.io/quiche-pantie-patch-gui/)を使えばこのツールの導入は不要です。  
ウェブアプリの方は手元のテクスチャへのパッチに対応したようなので、それで十分であれば以下のインストールは不要です。  
[Sansuke](https://github.com/sansuke05)さんが[Unityの拡張エディタ](https://github.com/sansuke05/quiche-pantie-patch-unity-editor)をBoothにて[頒布](https://sansuke05.booth.pm/items/1582611)されています。  
こちらも要チェックです！

パンツパッチ本体の導入メリットは、Unityに反映するまで完全自動化できるという点ですので、それが必要であればWikiの[インストール](https://github.com/TenteEEEE/quiche_pantie_patch/wiki/Installation-%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)を読んで下記の導入してください。

## 使い方
基本的にどのアバターであっても`python patch.py`としてパッチャーを起動するだけですが、主に2つの使い方を想定しています。

1. それぞれのアバターにパンツをパッチする (対話形式でのパッチ)
1. よく使うアバターに同様の設定でパンツをパッチし続ける (jsonセットアップでのパッチ)

詳しくはWikiの[使い方](https://github.com/TenteEEEE/quiche_pantie_patch/wiki/Usage-%E4%BD%BF%E3%81%84%E6%96%B9)をチェックしてください。  

## 対応してほしいアバターがある
* モデラー(著作者)  
ぜひ[CC0ぱんつ](https://github.com/TenteEEEE/quiche_pantie_patch/wiki/CC0%E3%81%B1%E3%82%93%E3%81%A4)のメッシュまたはUVの利用を検討してください。  
こちらはすでに変換プログラムがあり、ぱんつ位置は簡単に変更できます。  
* モデル利用者  
[対応モデルの拡充ガイドライン](https://github.com/TenteEEEE/quiche_pantie_patch/wiki/%E5%AF%BE%E5%BF%9C%E3%83%A2%E3%83%87%E3%83%AB%E6%8B%A1%E5%85%85%E3%81%AE%E3%82%AC%E3%82%A4%E3%83%89%E3%83%A9%E3%82%A4%E3%83%B3)を読んでからお問い合わせください。  

## 開発者の方へ
対応アバターのスクリプトを書いてみたい人はコードや[Wiki](https://github.com/TenteEEEE/quiche_pantie_patch/wiki)のFor Developersを読むと分かりやすいかも。

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
|[VRoid](https://vroid.com)ちゃん|[ノイ](https://ficsnade.booth.pm/items/1572406)ちゃん|
|![test](./sample/vroid_pantie.png)|![test](./sample/noy_pantie.png)|
|[フィリナ](https://nagatorokoyori.booth.pm/items/1577042)ちゃん|[Differe](https://tyubaki.booth.pm/items/1580267)ちゃん|
|![test](./sample/firina_pantie.png)|![test](./sample/differe_pantie.png)|
|[I-s(アイズ)](https://atelier-alca.booth.pm/items/1572567)ちゃん|[ブランカ](https://atelier-krull.booth.pm/items/1563233)ちゃん|
|![test](./sample/i-s_pantie.png)|![test](./sample/blanca_pantie.png)|
|[シャーロ(冬服)](https://atelier-alca.booth.pm/items/1572567)ちゃん|[カルティ](https://takewaka.booth.pm/items/1555399)ちゃん|
|![test](./sample/shaclo_winter_pantie.png)|![test](./sample/carti_pantie.png)|
|[愛奈](https://narazaka.booth.pm/items/1319390)ちゃん|[受付嬢](https://mk22.booth.pm/items/1568317)さん|
|![test](./sample/aina_pantie.png)|![test](./sample/uketsukejo_pantie.png)|
|[クロノス](https://karekitsune.booth.pm/items/1542143)ちゃん|[CC0ぱんつ](https://github.com/TenteEEEE/quiche_pantie_patch/wiki/CC0%E3%81%B1%E3%82%93%E3%81%A4)|
|![test](./sample/chronos_pantie.png)|![test](./sample/cc0_pantie.png)|
|[ハティ](https://kokorobouzu.booth.pm/items/1451160)ちゃん|[カロナーフ](https://bbkktn.booth.pm/items/1651921)ちゃん|
|![test](./sample/hati_pantie.png)|![test](./sample/caronauff_pantie.png)|
|[量産型のらきゃっと](https://noracat.booth.pm/items/1216498)|[フィリ](https://regs.booth.pm/items/1629301)ちゃん|
|![test](./sample/masscat_pantie.png)|![test](./sample/phyri_pantie.png)|
|[いな屋さんのビキニ](https://inani.booth.pm/items/1422414)|[シリウス](https://hyuuganatu.booth.pm/items/1723127)ちゃん|
|![test](./sample/inabikini_pantie.png)|![test](./sample/sirius_pantie.png)|
|[コロナ](https://hirune-vr.booth.pm/items/1700848)ちゃん|[響狐リク](https://kar.booth.pm/items/1148939)ちゃん|
|![test](./sample/corona_pantie.png)|![test](./sample/liqu_pantie.png)|
|[スピカ](https://wakonoatorie.booth.pm/items/1808374)ちゃん|[みみの](https://lsw.booth.pm/items/1336133)ちゃん|
|![test](./sample/supica_pantie.png)|![test](./sample/mimino_pantie.png)|
|[転生ルナーフ](https://bbkktn.booth.pm/items/2006071)ちゃん|[リーメ&リーバ](https://tomori-hikage.booth.pm/items/972559)ちゃん|
|![test](./sample/lunauff_pantie.png)|![test](./sample/leeme_reeva_pantie.png)|
|[ソルティ](https://steller.booth.pm/items/1672165)ちゃん|[シャオン](https://kutsushita03.booth.pm/items/2048231)ちゃん|
|![test](./sample/salty_pantie.png)|![test](./sample/shaon_pantie.png)|
|[NecoMaid](https://sonovr.booth.pm/items/1843586)ちゃん|[リネィ](https://cocca.booth.pm/items/1665790)ちゃん|
|![test](./sample/necomaid_pantie.png)|![test](./sample/reney_pantie.png)|
|[東狐千春](https://yueou.booth.pm/items/1814958)ちゃん|[ロポリこん](https://mido0021.booth.pm/items/1415037)ちゃん|
|![test](./sample/chiharu_pantie.png)|![test](./sample/lopolykon_pantie.png)|
|[マロン](https://booth.pm/ja/items/1105063)ちゃん|[リアアリス](https://booth.pm/ja/items/2146588)ちゃん|
|![test](./sample/marron_pantie.png)|![test](./sample/rearalice_pantie.png)|
|[式神(零)](https://booth.pm/ja/items/2033949)||
|![test](./sample/rei_pantie.png)||

## スペシャルサンクス
[Booth:キッシュちゃん](https://mutachannel.booth.pm/items/954376)  
右近ちゃん、Differeちゃんパンツコンバータの作者:[thakyuu](https://github.com/thakyuu)さん  
patch.pyのargparse対応:[4hiziri](https://github.com/4hiziri)さん  
[ウェブアプリ](https://joniburn.github.io/quiche-pantie-patch-gui/)、シリウスちゃんコンバータの開発者:[Joniburn](https://github.com/joniburn)さん  
[Unityの拡張エディタ](https://github.com/sansuke05/quiche-pantie-patch-unity-editor)の開発者:[Sansuke](https://github.com/sansuke05)さん  
[CC0ぱんつ](https://github.com/TenteEEEE/quiche_pantie_patch/wiki/CC0%E3%81%B1%E3%82%93%E3%81%A4)のモデラー: [socho](https://twitter.com/socho_v)  

## ライセンス
複雑になってきたので、[Wikiのライセンス](https://github.com/TenteEEEE/quiche_pantie_patch/wiki/License-%E3%83%A9%E3%82%A4%E3%82%BB%E3%83%B3%E3%82%B9)をご確認ください。

---
**English**
# Quiche Pantie Patch
You look the pantie only once.

The purpose of the repository is to apply various panties to various 3D models.  

## Installation
If you just make the transparent textures, you don't have to install it.  
You can make it by my DiscordBot in [my server](https://discord.gg/ad4Qsfa), or [web app](https://joniburn.github.io/quiche-pantie-patch-gui/).  
Or you can choose [UnityEditor](https://github.com/sansuke05/quiche-pantie-patch-unity-editor) which is developed by [Sansuke](https://github.com/sansuke05).  
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
|[VRoid](https://vroid.com)|[Noy](https://ficsnade.booth.pm/items/1572406)|
|![test](./sample/vroid_pantie.png)|![test](./sample/noy_pantie.png)|
|[Firina](https://nagatorokoyori.booth.pm/items/1577042)|[Differe](https://tyubaki.booth.pm/items/1580267)|
|![test](./sample/firina_pantie.png)|![test](./sample/differe_pantie.png)|
|[I-s](https://atelier-alca.booth.pm/items/1572567)|[Blanca](https://atelier-krull.booth.pm/items/1563233)|
|![test](./sample/i-s_pantie.png)|![test](./sample/blanca_pantie.png)|
|[Shaclo(winter clothes)](https://atelier-alca.booth.pm/items/1572567)|[Carti](https://takewaka.booth.pm/items/1555399)|
|![test](./sample/shaclo_winter_pantie.png)|![test](./sample/carti_pantie.png)|
|[Aina](https://narazaka.booth.pm/items/1319390)|[Uketsukejo](https://mk22.booth.pm/items/1568317)|
|![test](./sample/aina_pantie.png)|![test](./sample/uketsukejo_pantie.png)|
|[Chronos](https://karekitsune.booth.pm/items/1542143)|[CC0 Pantie](https://github.com/TenteEEEE/quiche_pantie_patch/wiki/CC0%E3%81%B1%E3%82%93%E3%81%A4)|
|![test](./sample/chronos_pantie.png)|![test](./sample/cc0_pantie.png)|
|[Hati](https://kokorobouzu.booth.pm/items/1451160)|[Caronauff](https://bbkktn.booth.pm/items/1651921)|
|![test](./sample/hati_pantie.png)|![test](./sample/caronauff_pantie.png)|
|[Masscat](https://noracat.booth.pm/items/1216498)|[Phyri](https://regs.booth.pm/items/1629301)|
|![test](./sample/masscat_pantie.png)|![test](./sample/phyri_pantie.png)|
|[Inaya's bikini](https://inani.booth.pm/items/1422414)|[Sirius](https://hyuuganatu.booth.pm/items/1723127)|
|![test](./sample/inabikini_pantie.png)|![test](./sample/sirius_pantie.png)||
|[Corona](https://hirune-vr.booth.pm/items/1700848)|[Liqu](https://kar.booth.pm/items/1148939)|
|![test](./sample/corona_pantie.png)|![test](./sample/liqu_pantie.png)|
|[Supica](https://wakonoatorie.booth.pm/items/1808374)|[Mimino](https://lsw.booth.pm/items/1336133)|
|![test](./sample/supica_pantie.png)|![test](./sample/mimino_pantie.png)|
|[Lunauff](https://bbkktn.booth.pm/items/2006071)|[Leeme & Reeva](https://tomori-hikage.booth.pm/items/972559)|
|![test](./sample/lunauff_pantie.png)|![test](./sample/leeme_reeva_pantie.png)|
|[Salty](https://steller.booth.pm/items/1672165)|[Shaon](https://kutsushita03.booth.pm/items/2048231)|
|![test](./sample/salty_pantie.png)|![test](./sample/shaon_pantie.png)|
|[NecoMaid](https://sonovr.booth.pm/items/1843586)|[Reney](https://cocca.booth.pm/items/1665790)|
|![test](./sample/necomaid_pantie.png)|![test](./sample/reney_pantie.png)|
|[Touko Chiharu](https://yueou.booth.pm/items/1814958)|[Lopolykon](https://mido0021.booth.pm/items/1415037)|
|![test](./sample/chiharu_pantie.png)|![test](./sample/lopolykon_pantie.png)|
|[Marron](https://booth.pm/ja/items/1105063)|[RearAlice](https://booth.pm/ja/items/2146588)|
|![test](./sample/marron_pantie.png)|![test](./sample/rearalice_pantie.png)|
|[Rei](https://booth.pm/ja/items/2033949)||
|![test](./sample/rei_pantie.png)||

## Special thanks
[Quiche model](https://mutachannel.booth.pm/items/954376)  
Developer of the Ukon and Differe pantie converter: [thakyuu](https://github.com/thakyuu)  
Improvement of patch.py:[4hiziri](https://github.com/4hiziri)  
Developer of the [web app](https://joniburn.github.io/quiche-pantie-patch-gui/) and Sirius pantie converter: [Joniburn](https://github.com/joniburn)  
Developer of the [UnityEditor](https://github.com/sansuke05/quiche-pantie-patch-unity-editor): [Sansuke](https://github.com/sansuke05)  
Modeler of the [CC0 Pantie](https://github.com/TenteEEEE/quiche_pantie_patch/wiki/CC0%E3%81%B1%E3%82%93%E3%81%A4): [socho](https://twitter.com/socho_v)  

## License
See [Wiki/License](https://github.com/TenteEEEE/quiche_pantie_patch/wiki/License-%E3%83%A9%E3%82%A4%E3%82%BB%E3%83%B3%E3%82%B9)
