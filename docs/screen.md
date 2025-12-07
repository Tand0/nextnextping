
# Screen image

## トップ画面

<img src="./screen001a.png" width="60%">

  - トップの画面です。
  - pingを打つIPを指定します。
  - `;` でコメントアウトができます。
  - カッコつきの文字で`(traceroute)`と先頭に書くと、tracerouteをしてくれます。
  - カッコつきの文字で`(show)`と先頭に書くと、ipconfig相当を打てます。
  - カッコつきの文字で`(ttl)`と先頭に書くと、terawaros tekitou languageを読み込み、SSH接続できるのでpingを打てます。
  - カギカッコ`[` と `]`つきの文字で説明として使われます。
  - `Update` ボタンを実行すると、トップの画面を解析して行で表現します。[結果表示画面](#結果表示画面) に遷移します。

### メニューバー

<img src="./screen009a.png" width="25%">

  - メニューバー上の File ⇒ Save setting を実行すると、設定をセーブしれます。
  - メニューバー上の File ⇒ Load setting を実行すると、設定をロードします。
  - メニューバー上の File ⇒ Save log を実行すると、実行したときのログをセーブします。
  - メニューバー上の File ⇒ Load log を実行すると、実行したときのログをロードします。
  - メニューバー上の File ⇒ Setting を実行すると、[設定画面](#設定画面) 用ダイアログが開きます。


<img src="./screen004a.png" width="25%">

- メニューバー上の Tool ⇒ Sheet を実行すると、[ping用TTLマクロ作成支援ツール](./tool.md) を起動します。

## 結果表示画面

<img src="./screen002a.png" width="60%">

  - `Ping` ボタンを実行すると、pingを定期的に実行します。
  - `Stop` ボタンを実行すると、pingの実行を停止します。
  - 結果は OK またはNGで表示されます。ttlの場合は、エラーとなるか、最後まで行って`result`が0のときにNGで表示されます。

## ログ画面

<img src="./screen003a.png" width="60%">

  - 結果表示画面の行をクリックすると、その行に対応したログが表示されます。


## 設定画面

<img src="./screen010.png" width="50%">

  - debug: デバッグモードにします。
  - loop: 最後までpingを実行したあと、ループします。
  - wait_time: ping実行後、次のpingを行うまでの時間です。
  - TTL macro
      - messagebox: True のとき、ttl実行時にmessageboxを表示しません。
      - log: True のとき、ttl実行時にlogopen関連を無視します。

