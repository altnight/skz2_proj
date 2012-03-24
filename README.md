スカンディナヴィア半島2
===========================

##環境

- Django
- Tweepy
- gunicorn
- nginx
- Debian
- さくらVPS

##機能

- t.co展開
- - できた
- bitlay展開
  - 無理にやらなくていい
  - でもbit.ly短縮はできたい
- キーボードショートカット
  - 左右スクロールくらいはやりたい
- フィルタリング機能
  - レートわけ、レートでリスト作成
  - レートは3段階
  -   undef合わせると4つ
    -   できる気がしない
  - あとはリストのめんばーでフィルタリング
  - リストのメンバーから振り分けを作成
- api limit表示
  - できた
- 発言, reply, fav, RT 非公式RTできる
  - 非公式RTはできなくてもいい
  - ngword指定できる
  - 抽出できたらいいかも
- マルチカラムで表示切り替えをする
  - 結局スカンディナヴィア半島1と同じになるかも……
    - そのかわりGUIは充実させたい

##UI

- jQuery
  - jQueryUI
- CoffeeScript
- Sass
  - Lessにしました
- padding詰める
  - できなければWindowを左右にスクロールする機能(like tweetdeck)
- header
  - twitterのtweetボタンをつける

##実装

- OAuth
  - すべてのstatusobjectをDBにいれておく
- 任意のリストを読み込む
  - reload intervalを設定できる
  - UserStreamは諦めた
- textのパース
  - だいたいおk?
- リストの一覧を取ってくる、リストを読み込む
  - 公式RTのやった人の表示
    - できた
  - 複数アカウントでの動作確認
