
# Tera Tkekitou Language コマンドリファレンス

## break/ continue

- for, while文で戻るのに使います。

## call/retun

- サブルーチンをコールするのに使います。

## end/exit

- 終了するのに使います。

## import
- ttl ファイルを読み込むのみ使います。

## dummy
- こんなコマンドは本来(?)のttlにはありませんが、評価用に作成しました。
- 引数に何を入れてもなにもしません。

## str2int

文字列を整数値に変換する。
```
str2int <intvar> <string>
```

## strcompare

文字列を比較する。比較は pythonの文字列として行う。
```
strcompare <string1> <string2>
```

2つの文字列 string1, string2 を比較し、結果をシステム変数 result に代入する。
文字列の文字コード表現を符号なし整数(最初の文字が最上位バイト)とみなし、2つの文字列に対応する整数値の大小関係を求め、それに応じて以下のようにresult の値が決定される。

```
大小関係	resultの値
<string1> < <string2>	-1
<string1> = <string2>	0
<string1> > <string2>	1
```


## strconcat

文字列を継ぎ足す。
```
strconcat <strvar> <string>
```

## strlen

文字列の長さを返す。
```
strlen <string>
```

## strscan
部分文字列の位置を返す。
```
strscan <string> <substring>
```
  Python側では以下の式でresultを決定している。
```python
                    result = left.find(right)
                    if left < 0:
                        result = 0
                    else:
                        result = result + 1
```

## mpause
休止する。単位はミリ秒
```
mpause <time>
```


## pause
休止する。単位は秒
```
mpause <time>
```


## connect

- SSH接続する。telnet接続やSSH1接続はできません。
- pythonのparamikoを使って接続します。
- 注意！：ssh接続をするには接続先のサーバが必要です。

```
connect 'myserver /ssh    /user=username /passwd=password'
connect 'myserver /ssh /2 /user=username /passwd=password'
connect 'myserver /ssh    /user=username /passwd=password /keyfile=private-key-file'
connect 'myserver /ssh /2 /user=username /passwd=password /keyfile=private-key-file'
```

## closett/disconnect
クローズします。

## testlink

現在のリンクおよび接続の状態を報告する。

```
値	状態
0	ホストへの接続はされていない。
2	ホストへの接続はされている。
```

## send
データを送信する。
```
send <data1> <data2>....
```

## sendln
データを送信する。
```
sendln <data1> <data2>....
```

## wait

文字列を待つ。
```
wait <string1> [<string2> ...]
```

文字列 <string1> [<string2> ...] のうち一つがホストから送られてくるか、タイムアウトが発生するまで MACRO を停止させる。

空文字列が指定された場合、任意の一文字を受信するのを待つ。

システム変数 timeout か mtimeout が 0 より大きい場合、<timeout>.<mtimeout> 秒の時間がすぎるとタイムアウトが発生する。タイムアウトの値が 0 以下の場合は、タイムアウトは発生しない。

これらのコマンドの実行結果はシステム変数 result に格納される。変数 result の値の意味は以下のとおり。
```
値	意味
0	タイムアウト。どの文字列も来なかった。
1	<string1> を受信した。
2	<string2> を受信した。
n	<stringn> を受信した。n=1..n
```

## waitln

文字列を待つ。
```
wait <string1> [<string2> ...]
```

文字列 <string1> [<string2> ...] のうち一つがホストから送られてくるか、タイムアウトが発生するまで MACRO を停止させる。

空文字列が指定された場合、任意の一文字を受信するのを待つ。

システム変数 timeout か mtimeout が 0 より大きい場合、<timeout>.<mtimeout> 秒の時間がすぎるとタイムアウトが発生する。タイムアウトの値が 0 以下の場合は、タイムアウトは発生しない。

これらのコマンドの実行結果はシステム変数 result に格納される。変数 result の値の意味は以下のとおり。
```
値	意味
0	タイムアウト。どの文字列も来なかった。
1	<string1> を受信した。
2	<string2> を受信した。
n	<stringn> を受信した。n=1..n
```



