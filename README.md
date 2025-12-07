# NextNextPing

このソフトウェアはwindowsで多数の装置にpingを打つためのExPingのようなツールです。

- [For Eingish](./README_en.md)
- [For Ansible](./forwsl2/collections/ansible_collections/tand0/ttl/README.md)

## Introduction

- EXPing は実に素晴らしい。周期的にpingを発行してネットワーク上で止まったところをNG表示してくれるのだ。
- しかしながら問題がある。
- pingしか対応していないのだ。
- ネットワークを確認したいのであれば、ping以外にもtracerouteをしてほしいし、なんならsshで接続してサーバを踏み台としたpingを打ちたいのだ。
- そこで用意したのは新しい GUIの pingを打つツールだ。
- ついでにtracerouteを打てるようにした。
- そして踏み台サーバを用いたpingも用意しようとした。
- しかし、ここでpingをするには中継のコマンドプロンプトが分からないという問題があった。
- そう、teraterm マクロのような機能が簡単に作れないのだ。
- ならば作ればよいのだ。
- そこで、pingを打つために必要な機能だけ teraterm マクロの機能から持ってきたのがこのソフトウェアになります。

## Overview
- pythonで作ったので多分Linuxでも動きます。
- pingを打ってその結果でOKまたはNGが分かります。
- teraterm macro に似せた Terawaros Tekitou Language (テラワロスてきとうランゲージ、通称ttl)と呼ばれる言語で SSH接続し、他のサーバを踏み台としてpingを打てます。

## Screen image

- [Screen image](./docs/screen.md)

# MACRO for Terawaros Tekitou Lanugage


Terawaros Tekitou Lanugage は NextNextPing 用マクロ実行プログラムです。マクロ言語 "Terawaros Tekitou Language (TTL)" によって、NextNextPing を制御し、オートダイアル、オートログインなどの機能を実現することができます。

- 使い方
     - [マクロの実行方法](./docs/howtorun.md)
- [The MACRO Language Terawaros Tekitou Language (TTL)](./docs/syntax.md)　
- [TTL command reference](./docs/command.md)

# Ping TTL macro creation support tool

- ping を打つための TTLマクロを作成するのは面倒なので、指定をするとサンプルが出てきてそのまま使えるようにしました。

- ツールの使い方
    - [Ping TTL macro creation support tool](./docs/tool.md)


# 基本的な使い方

  - Basic -- sample01/setting.txt に例があります。
      - nextnextpingを起動します。
      - [トップ画面](./docs/screen.md#トップ画面)で適当にipを並べます。
      - メニューバーから、File ⇒ Setting で [設定画面](./docs/screen.md#設定画面) を開いて設定を変更します。
      - Updateボタンをクリックします。
      - Pingボタンをクリックします。
      - しばらくするとpingに成功したものがOK、失敗したものがNGで表示されます。
      - メニューバーから、File ⇒ Save setting で設定の保存ができます。
      - メニューバーから、File ⇒ Save log でログの保存ができます。
      - メニューバーから、File ⇒ Exit で終了できます。
  - Advanced -- sample02/setting.txt に例があります。
      - nextnextpingを起動します。
      - メニューバーから、Tool ⇒ Sheet をクリックします。
      - 設定用CSVファイルを作成します。やり方は２種類あります。
          -  メニューバーから、File ⇒ Load csv で保存した csvをロードします。
          -  Createボタンを押して [設定画新規作成または編集画面面](./docs/tool.md#新規作成または編集画面) を開いて編集します。
          - 行をダブルクリックすると編集ができます。
      - 今後のために File ⇒ Save csv で保存した csvをセーブします。
      - メニューバーから、Go ⇒ Create ttl で ttlを自動生成します。
      - メニューバーから、File ⇒ Closeでツールを終了します。
      - [結果表示画面](./docs/screen.md#結果表示画面) からPingボタンをクリックします。
      - しばらくするとpingに成功したものがOK、失敗したものがNGで表示されます。
      - メニューバーから、File ⇒ Save log でログの保存ができます。
      - メニューバーから、File ⇒ Exit で終了できます。
  - Legend -- sample03/setting.txt に例があります。
      - nextnextpingを起動します。
      - メニューバーから、File ⇒ Setting で [設定画面](./docs/screen.md#設定画面) を開いて設定を変更します。
      - ttlを自作します。
      - [トップ画面](./docs/screen.md#トップ画面)で`[`説明文`]` `(`ttl`)`  `ttlマクロのファイル名` と記述します。
      - Updateボタンをクリックします。
      - Pingボタンをクリックします。
      - しばらくするとpingに成功したものがOK、失敗したものがNGで表示されます。
           - 失敗の条件はエラーが発生したか、または、 `result` が 0 である場合のいずれかです。
      - メニューバーから、File ⇒ Save setting で設定の保存ができます。
      - メニューバーから、File ⇒ Save log でログの保存ができます。
      - メニューバーから、File ⇒ Exit で終了できます。


# 開発者に向けた README

- 動作確認方法
  - 以下、カレントフォルダを `.` とする
  - 必要なパッケージが入ってなかったら入れる
  - 別のPCにインストールしたときはフォルダ名等は見直す
  - `python build.py` を実行する
  - `cd .\bin` に移動する
        - `python ..\nextnextping\nextnextping` を実行して動作に問題ないことを確認する
  - `cd .` に戻る
  - `pytest -s` を実行してすべての test にパスする
        - 内部で Mock の ssh や scp サーバを起動します
        - Layer4 port 2200 を占有します。必要あれば適当に変えてください
  - `wsl` を起動する
        - `wsl` の中で `pytest -s` を実行してすべての test にパスする
        - `wsl` の中で `python3 test/test_nextnextping.py` を起動しっぱなにする
        - `wsl` の中で実行しないと後続の `site.yml` が正常動作しません
        - Mock の ssh や scp サーバを起動します
        - Layer4 port 2200 を占有します。必要あれば適当に変えてください
  - もう一枚コマンドプロンプトを起動して `wsl` を起動する
        - `cd .\forwsl2` に移動する
        - `wsl` の中で `ansible-palybook site.yml` を実行してすべての test にパスする
        - `wsl` を `exit` で抜ける
  - `.\nextnextping\dist\` 配下に公開に必要な zip と tar.gz が出来上がる
  - エラーが出た時は、指示に従って見直す
    - pyinstall, tkinter, pytest など必要なパッケージが入ってないとエラーになります
    - フォルダ名は環境に合わせて修正が必要です
