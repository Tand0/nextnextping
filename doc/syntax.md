
# マクロ言語 "Tera Tkekitou Language (TTL)"

- [Antlr 文法で頑張って書きました](./src/grammer/TtlParser.g4) 
- 間違っていたら指摘ください。


## Tera Tkekitou Language ファイル

- UTF-8しか保証しません。

## データ型

- str型: 仕様はPythonに基づきます。
- int型: 仕様はPythonに基づきます。

## 定数の形式

1. 整数型定数

10進数または "$" で始まる16進数で表現する。 浮動小数点は未サポート。

```
例:
    123
    -11
    $3a
    $10F
```

2. 文字列型定数

   文字列型定数を表現する方法は2つ。

  - a) 値となる文字列の両端を ' か " で囲む(両端とも同じ文字で)。文字列値を構成する文字は表示可能で囲み文字と異なる文字ならば何でもよい。

```
例:
    'Hello, world'
    "I can't do that"
    "漢字も可能"
```

  - b) 1文字を ASCII (または JIS ローマ字、Shift-JIS) コード(10進数または$で始まる16進数)で表現し、先頭に "#" をつける。 ASCII コード 0 の文字 (NUL) は文字列定数に含めることができない。

```
例:
    #65     文字 "A"
    #$41    文字 "A"
    #13     CR 文字
```

  - a) と b) は組み合わせることが可能。

```
例:
    'cat readme.txt'#13#10
    'abc'#$0d#$0a'def'#$0d#$0a'ghi'
```

## 変数

- param0, param2 ... param9 は予約語です。
- resultは予約語です。
  - 実施後にresultが0でないとき、実施は成功したとみなされ OK 表示がされます。

## 名前の形式

1) 変数の名前

  Antlr 文法での通り。
```
KEYWORD: [_a-zA-Z][_a-zA-Z0-9]*;
```

2) ラベルの名前

  Antlr 文法での通り。
```
label: ':' KEYWORD ;
```
3) 式と演算子

- たいていの四則演算は使えます。
- たいていの四則演算はint型で計算されます。加算も文字加算はできません。

```
例:
    1 + 1
    4 - 2 * 3      この式の値は-2
    15 % 10        この式の値は5
    3 * (A + 2)    A は整数型の変数
    A and not B
    A <= B         A, B は整数型の変数。
                   結果の値は真のとき1、偽のとき0
```

## 行の形式

- 行の形式は以下に分類できる。どの行も ";" 文字で始まるコメントを含むことができる。また、C言語風コメント（/* 〜 */）も使用可能。
- コメントは MACRO の実行に影響を与えない。

1) 改行

  Antlr 文法での通り。改行と見なされる。
```
RN: '\r'? '\n'
    | ';' ~[\n]* '\n'
    ;
```
1) ホワイトスペース

  Antlr 文法での通り。ホワイトスペースとして文字区切りに使われる。
```
WS1 : [ \t]+ -> skip ;
WS2 : '/*' ~[/]* '*/' -> skip ;
```

2) コマンド行

  1つのコマンド名と0個以上のパラメータ。
```
書式:
    <コマンド> <パラメータ> ...

例:
    connect 'myhost'
    wait 'OK' 'ERROR'
    if result=2 goto error
    sendln 'cat'
    pause A*10
    end
```

3) 代入行

  変数に値を代入する。
```
例:
    A = 33               数値の代入
    B = C                C はすでに値が代入されてなければならない。
    VAL = I*(I+1)	
    A=B=C                B=C の結果 (真:1、偽:0) が A に代入される。
    Error=0<J	
    Username='MYNAME'    文字列の代入
```

  Antlr 文法での通り。
```
input: KEYWORD '=' p11Expression ;
```


3) ラベル行

":" とその直後に続くラベル名からなる。

```
書式:
    :<Label>

例:
    :dial
```

  Antlr 文法での通り。
```
label: ':' KEYWORD ;
```

4) if文その1

  1行で定義せれたif文。
```
; もし A>1 ならば、':label' へ飛ぶ。
if A>1 goto label

; もし result<>0 ならば、A に0を代入。
if result A=0
```

  Antlr 文法での通り。
```
if1
    : 'if' p11Expression line;
```

4) if文その2

  複数行で定義されたif文。

```
if <expression 1> then
  ...
  (<expression 1> が真(0以外)の場合に実行されるコマンド)
  ...
[elseif <expression 2> then]
  ...
  (<expression 1> が偽(0)で、<expression 2>が真の場合に実行されるコマンド)
  ...
[elseif <expression N> then]
  ...
  (<expression 1>, <expression 2>,.., <expression N-1> がすべて偽で、<expression N> が真の場合に実行されるコマンド)
  ...
[else]
  ...
  (上の条件すべてが偽の場合に実行されるコマンド)
  ...
endif
```

  Antlr 文法での通り。
```
if2
    : 'if' p11Expression 'then' RN line+ (elseif)* (else)? 'endif';

elseif:'elseif' p11Expression 'then' RN line+;

else: 'else' RN line+;
```


5) while文

繰り返す。

```
; 10回繰り返す。
i = 10
while i>0
  i = i - 1
endwhile
```

  Antlr 文法での通り。
```
whileEndwhile
    : 'while' p11Expression RN line+ 'endwhile';
```


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

- SSH接続する。
- pythonのparamikoを使って接続します。
- 注意！：ssh接続をするには接続先のサーバが必要です。

```
connect 'myserver /ssh'
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









