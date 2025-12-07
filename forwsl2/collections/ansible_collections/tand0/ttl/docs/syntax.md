
# マクロ言語 "Terawaros Tkekitou Language (TTL)"

- [Antlr 文法で頑張って書きました](../src/grammer/TtlParser.g4) 
- 間違っていたら指摘ください。

- [マクロ言語 "Terawaros Tkekitou Language (TTL)"](#マクロ言語-terawaros-tkekitou-language-ttl)
  - [Terawaros Tkekitou Language ファイル](#terawaros-tkekitou-language-ファイル)
  - [データ型](#データ型)
  - [定数の形式](#定数の形式)
    - [int型](#int型)
    - [str型](#str型)
    - [int配列型](#int配列型)
    - [str配列型](#str配列型)
  - [変数](#変数)
  - [名前の形式](#名前の形式)
    - [変数の名前](#変数の名前)
    - [ラベルの名前](#ラベルの名前)
    - [式と演算子](#式と演算子)
  - [行の形式](#行の形式)
    - [改行](#改行)
    - [ホワイトスペース](#ホワイトスペース)
    - [コマンド行](#コマンド行)
    - [代入行](#代入行)
    - [ラベル行](#ラベル行)
    - [if](#if)
      - [if文その2](#if文その2)
      - [if文その2](#if文その2-1)
    - [while](#while)
    - [until](#until)
    - [do](#do)
    - [break](#break)
    - [continue](#continue)
    - [call](#call)
    - [end/exit](#endexit)


## Terawaros Tkekitou Language ファイル

- UTF-8しか保証しません。

## データ型

- int型: 仕様はPythonのintに基づきます。
- str型: 仕様はPythonのstrに基づきます。
- int配列型: 内部的には `a[0]` といった`[` や `]`まで含んだ文字の変数として１つのデータ型になっています。
- str配列型: 内部的には `a[0]` といった`[` や `]`まで含んだ文字の変数として１つのデータ型になっています。

## 定数の形式

### int型

10進数または "$" で始まる16進数で表現する。 浮動小数点は未サポート。

```
例:
    123
    -11
    $3a
    $10F
```

### str型

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

  - Antlr 文法では以下の通り。
```
STRING1: ('\'' ~[']* '\'' | '"' ~["]* '"' | '#' '$'? [a-fA-F0-9]+)+;
strContext: STRING1;
```

### int配列型

- `a[0]` までを文字列化して、変数型として扱われます

```
a[0] = 1
a[1] = 2
```

- `a[b]` を `a[0]` に変換して文字列化して、変数型として扱われます

```
b = 0
a[b] = 1
```

### str配列型

```
b = 0
a[b] = "aaa"
```



## 変数

- param0, param2 ... param9 は予約語です。
- resultは予約語です。
  - 実施後にresultが0でないとき、実施は成功したとみなされ OK 表示がされます。

## 名前の形式

### 変数の名前

  Antlr 文法では以下の通り。
```
KEYWORD: [_a-zA-Z][_a-zA-Z0-9]*;
keyword: KEYWORD (LEFT_KAKKO (intExpression| strExpression) RIGHT_KAKKO)?;
LEFT_KAKKO: '[';
RIGHT_KAKKO: ']';
```

### ラベルの名前

  Antlr 文法では以下の通り。
```
label: ':' KEYWORD ;
```
### 式と演算子

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

- 行の形式は以下に分類できる。どの行も ";" 文字で始まるコメントを含むことができる。
  また、C言語風コメント（/* 〜 */）も使用可能。
- コメントは MACRO の実行に影響を与えない。

### 改行

  Antlr 文法では以下の通り。改行と見なされる。
```
RN: '\r'? '\n'
    | ';' ~[\n]* '\n'
    ;
```
### ホワイトスペース

  Antlr 文法では以下の通り。ホワイトスペースとして文字区切りに使われる。

```
WS1 : [ \t]+ -> skip ;
WS2 : '/*' ~[/]* '*/' -> skip ;
```

### コマンド行

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

### 代入行

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

  Antlr 文法では以下の通り。
```
input: KEYWORD '=' p11Expression ;
```


### ラベル行

":" とその直後に続くラベル名からなる。

```
書式:
    :<Label>

例:
    :dial
```

  Antlr 文法では以下の通り。
```
label: ':' KEYWORD ;
```

### if

#### if文その2
- 1行で定義せれたif文。
```
; もし A>1 ならば、':label' へ飛ぶ。
if A>1 goto label

; もし result<>0 ならば、A に0を代入。
if result A=0
```

- Antlr 文法では以下の通り。
```
if1
    : 'if' p11Expression line;
```

#### if文その2

- 複数行で定義されたif文。

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

- Antlr 文法では以下の通り。
```
if2
    : 'if' p11Expression 'then' RN line+ (elseif)* (else)? 'endif';

elseif:'elseif' p11Expression 'then' RN line+;

else: 'else' RN line+;
```

### for
- 繰り返す。
```
for <intvar> <first> <last>

  ...

  ...

next
```

`for` と `next` の間のコマンドを、整数変数 `intvar` の値が `last` と等しくなるまで、繰りかえす。
`intvar` の初期値は `first` 。もし `last` が `first` より大きい場合、`intvar` は `next` 行に来るたびに 1 足される。もし `last` が `fast` より小さい場合、`intvar` は "next" 行に来るたびに 1 引かれる。


```
; 10回繰り返す。
for i 1 10
  sendln 'abc'
next

; 5回繰り返す。
for i 5 1
  sendln 'abc'
next
```

- Antlr 文法では以下の通り。
```
forNext
    : 'for' keyword p11Expression p11Expression RN commandline+ 'next';
```

### while

- 繰り返す。

```
; 10回繰り返す。
i = 10
while i>0
  i = i - 1
endwhile
```

- Antlr 文法では以下の通り。
```
whileEndwhile
    : 'while' p11Expression RN line+ 'endwhile';
```

### until
- 繰り返す。
- Antlr 文法では以下の通り。
```
untilEnduntil
    : 'until' p11Expression RN commandline+ 'enduntil';
```


### do
- 繰り返す。
- Antlr 文法では以下の通り。
```
doLoop
    : 'do' p11Expression? RN commandline+ 'loop' p11Expression?;
```

### break
- 繰り返しを中断する。

### continue
- 繰り返しを途中で止め、次の繰り返しに進む。

### call

- サブルーチンをコールする。`return` で戻る。
```
messagebox "I'm in main." "test"
; ":sub" へ飛ぶ。
call sub
messagebox "Now I'm in main" "test"
end

; サブルーチンの始まり。
:sub
messagebox "Now I'm in sub" "test"
; メインルーチンへもどる。
return
```

### end/exit

- 終了するのに使います。


### include

- インクルードファイルに移る。
- `exit` でメインファイルに戻ります。



