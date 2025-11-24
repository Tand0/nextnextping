
# Terawaros Tkekitou Language コマンドリファレンス

コマンドの分類

- 通信コマンド
  <!-- - [bplusrecv](https://teratermproject.github.io/manual/5/ja/macro/command/bplusrecv.html) -->
  <!-- - [bplussend](https://teratermproject.github.io/manual/5/ja/macro/command/bplussend.html) -->
  <!-- - [callmenu](https://teratermproject.github.io/manual/5/ja/macro/command/callmenu.html) -->
  - [changedir](https://teratermproject.github.io/manual/5/ja/macro/command/changedir.html)
  <!-- -  [clearscreen](https://teratermproject.github.io/manual/5/ja/macro/command/clearscreen.html) -->
  - [closett](https://teratermproject.github.io/manual/5/ja/macro/command/closett.html)
  - [connect](https://teratermproject.github.io/manual/5/ja/macro/command/connect.html) // 補足あり  [connect](#connect)
  <!-- -  [cygconnect](https://teratermproject.github.io/manual/5/ja/macro/command/cygconnect.html) -->
  - [disconnect](https://teratermproject.github.io/manual/5/ja/macro/command/disconnect.html)
  - [dispstr](https://teratermproject.github.io/manual/5/ja/macro/command/dispstr.html)
  <!-- - [enablekeyb](https://teratermproject.github.io/manual/5/ja/macro/command/enablekeyb.html) -->
  - [flushrecv](https://teratermproject.github.io/manual/5/ja/macro/command/flushrecv.html)
  - [gethostname](https://teratermproject.github.io/manual/5/ja/macro/command/gethostname.html)
  <!-- - [getmodemstatus](https://teratermproject.github.io/manual/5/ja/macro/command/getmodemstatus.html) -->
  - [gettitle](https://teratermproject.github.io/manual/5/ja/macro/command/gettitle.html)
  <!-- - [getttpos](https://teratermproject.github.io/manual/5/ja/macro/command/getttpos.html) -->
  <!-- - [kmtfinish](https://teratermproject.github.io/manual/5/ja/macro/command/kmtfinish.html) -->
  <!-- - [kmtget](https://teratermproject.github.io/manual/5/ja/macro/command/kmtget.html) -->
  <!-- - [kmtrecv](https://teratermproject.github.io/manual/5/ja/macro/command/kmtrecv.html) -->
  <!-- - [kmtsend](https://teratermproject.github.io/manual/5/ja/macro/command/kmtsend.html) -->
  <!-- - [loadkeymap](https://teratermproject.github.io/manual/5/ja/macro/command/loadkeymap.html) -->
  <!-- - [logautoclosemode](https://teratermproject.github.io/manual/5/ja/macro/command/logautoclosemode.html) -->
  - [logclose](https://teratermproject.github.io/manual/5/ja/macro/command/logclose.html)
  - [loginfo](https://teratermproject.github.io/manual/5/ja/macro/command/loginfo.html)
  - [logopen](https://teratermproject.github.io/manual/5/ja/macro/command/logopen.html) // 補足あり  [logopen](#logopen)
  - [logpause](https://teratermproject.github.io/manual/5/ja/macro/command/logpause.html)
  <!-- - [logrotate](https://teratermproject.github.io/manual/5/ja/macro/command/logrotate.html) -->
  - [logstart](https://teratermproject.github.io/manual/5/ja/macro/command/logstart.html)
  - [logwrite](https://teratermproject.github.io/manual/5/ja/macro/command/logwrite.html)
  <!-- - [quickvanrecv](https://teratermproject.github.io/manual/5/ja/macro/command/quickvanrecv.html) -->
  <!-- - [quickvansend](https://teratermproject.github.io/manual/5/ja/macro/command/quickvansend.html) -->
  - [recvln](https://teratermproject.github.io/manual/5/ja/macro/command/recvln.html)
  <!-- - [restoresetup](https://teratermproject.github.io/manual/5/ja/macro/command/restoresetup.html) -->
   - [scprecv](https://teratermproject.github.io/manual/5/ja/macro/command/scprecv.html) // 諸般の事情で中身はsftpになっています
   - [scpsend](https://teratermproject.github.io/manual/5/ja/macro/command/scpsend.html) // 諸般の事情で中身はsftpになっています
  - [send](https://teratermproject.github.io/manual/5/ja/macro/command/send.html)
  <!-- - [sendbinary](https://teratermproject.github.io/manual/5/ja/macro/command/sendbinary.html) -->
  - [sendbreak](https://teratermproject.github.io/manual/5/ja/macro/command/sendbreak.html) // `Ctrl-C` を投げるだけ
  <!-- - [sendbroadcast](https://teratermproject.github.io/manual/5/ja/macro/command/sendbroadcast.html) -->
  - [sendfile](https://teratermproject.github.io/manual/5/ja/macro/command/sendfile.html) // 未実装
    - [exec](https://teratermproject.github.io/manual/5/ja/macro/command/exec.html)でSCPを呼ぶか [logopen](#logopen) で `/cmd` モードから SFPTを呼んでください
  <!-- - [sendkcode](https://teratermproject.github.io/manual/5/ja/macro/command/sendkcode.html) -->
  - [sendln](https://teratermproject.github.io/manual/5/ja/macro/command/sendln.html)
  <!-- - [sendlnbroadcast](https://teratermproject.github.io/manual/5/ja/macro/command/sendlnbroadcast.html) -->
  <!-- - [sendlnmulticast](https://teratermproject.github.io/manual/5/ja/macro/command/sendlnmulticast.html) -->
  - [sendtext](https://teratermproject.github.io/manual/5/ja/macro/command/sendtext.html)
  <!-- - [sendmulticast](https://teratermproject.github.io/manual/5/ja/macro/command/sendmulticast.html) -->
  <!-- - [setbaud](https://teratermproject.github.io/manual/5/ja/macro/command/setbaud.html) -->
  <!-- - [setdebug](https://teratermproject.github.io/manual/5/ja/macro/command/setdebug.html) -->
  - [setdtr](https://teratermproject.github.io/manual/5/ja/macro/command/setdtr.html)
  <!-- - [setecho](https://teratermproject.github.io/manual/5/ja/macro/command/setecho.html) -->
  <!-- - [setflowctrl](https://teratermproject.github.io/manual/5/ja/macro/command/setflowctrl.html) -->
  <!-- - [setmulticastname](https://teratermproject.github.io/manual/5/ja/macro/command/setmulticastname.html) -->
  <!-- - [setrts](https://teratermproject.github.io/manual/5/ja/macro/command/setrts.html) -->
  <!-- - [setserialdelaychar](https://teratermproject.github.io/manual/5/ja/macro/command/setserialdelaychar.html) -->
  <!-- - [setserialdelayline](https://teratermproject.github.io/manual/5/ja/macro/command/setserialdelayline.html) -->
  <!-- - [setspeed](https://teratermproject.github.io/manual/5/ja/macro/command/setspeed.html) -->
  <!-- - [setsync](https://teratermproject.github.io/manual/5/ja/macro/command/setsync.html) -->
  - [settitle](https://teratermproject.github.io/manual/5/ja/macro/command/settitle.html)
  <!-- - [showtt](https://teratermproject.github.io/manual/5/ja/macro/command/showtt.html) -->
  - [testlink](https://teratermproject.github.io/manual/5/ja/macro/command/testlink.html)
  - [unlink](https://teratermproject.github.io/manual/5/ja/macro/command/unlink.html)
  - [wait](https://teratermproject.github.io/manual/5/ja/macro/command/wait.html)
  - [wait4all](https://teratermproject.github.io/manual/5/ja/macro/command/wait4all.html) // 実質waitと同じ
  <!-- - [waitevent](https://teratermproject.github.io/manual/5/ja/macro/command/waitevent.html) -->
  - [waitln](https://teratermproject.github.io/manual/5/ja/macro/command/waitln.html)
  - [waitn](https://teratermproject.github.io/manual/5/ja/macro/command/waitn.html)
  <!-- - [waitrecv](https://teratermproject.github.io/manual/5/ja/macro/command/waitrecv.html) -->
  <!-- - [waitregex](https://teratermproject.github.io/manual/5/ja/macro/command/waitregex.html) -->
  <!-- - [xmodemrecv](https://teratermproject.github.io/manual/5/ja/macro/command/xmodemrecv.html) -->
  <!-- - [xmodemsend](https://teratermproject.github.io/manual/5/ja/macro/command/xmodemsend.html) -->
  <!-- - [ymodemrecv](https://teratermproject.github.io/manual/5/ja/macro/command/ymodemrecv.html) -->
  <!-- - [ymodemsend](https://teratermproject.github.io/manual/5/ja/macro/command/ymodemsend.html) -->
  <!-- - [zmodemrecv](https://teratermproject.github.io/manual/5/ja/macro/command/zmodemrecv.html) -->
  <!-- - [zmodemsend](https://teratermproject.github.io/manual/5/ja/macro/command/zmodemsend.html) -->

- 制御コマンド
  - [break](./syntax.md#break)
  - [call](./syntax.md#call)
  - [continue](./syntax.md#continue)
  - [do, loop](./syntax.md#do)
  - [end](./syntax.md#endexit)
  - [execcmnd](https://teratermproject.github.io/manual/5/ja/macro/command/execcmnd.html)
  - [exit](./syntax.md#endexit)
  - [for, next](./syntax.md#for)
  - goto // 実装していません。本家はインタプリタですが、こちらはコンパイラなので実装が難しいです。
  - [if, then, elseif, else, endif](./syntax.md#if)
  - [include](./syntax.md#include)
  - [mpause](https://teratermproject.github.io/manual/5/ja/macro/command/mpause.html)
  - [pause](https://teratermproject.github.io/manual/5/ja/macro/command/pause.html)
  - [return](./syntax.md#call)
  - [until, enduntil](./syntax.md#until)
  - [while, endwhile](./syntax.md#while)

- 文字列操作コマンド
  - [code2str](https://teratermproject.github.io/manual/5/ja/macro/command/code2str.html)
  - [expandenv](https://teratermproject.github.io/manual/5/ja/macro/command/expandenv.html)
  - [int2str](https://teratermproject.github.io/manual/5/ja/macro/command/int2str.html)
  - [regexoption](https://teratermproject.github.io/manual/5/ja/macro/command/regexoption.html)
  - [sprintf](https://teratermproject.github.io/manual/5/ja/macro/command/sprintf.html)
  - [sprintf2](https://teratermproject.github.io/manual/5/ja/macro/command/sprintf2.html)
  - [str2code](https://teratermproject.github.io/manual/5/ja/macro/command/str2code.html)
  - [str2int](https://teratermproject.github.io/manual/5/ja/macro/command/str2int.html)
  - [strcompare](https://teratermproject.github.io/manual/5/ja/macro/command/strcompare.html)
  - [strconcat](https://teratermproject.github.io/manual/5/ja/macro/command/strconcat.html)
  - [strcopy](https://teratermproject.github.io/manual/5/ja/macro/command/strcopy.html)
  - [strinsert](https://teratermproject.github.io/manual/5/ja/macro/command/strinsert.html)
  - [strjoin](https://teratermproject.github.io/manual/5/ja/macro/command/strjoin.html)
  - [strlen](https://teratermproject.github.io/manual/5/ja/macro/command/strlen.html)
  - [strmatch](https://teratermproject.github.io/manual/5/ja/macro/command/strmatch.html)
  - [strremove](https://teratermproject.github.io/manual/5/ja/macro/command/strremove.html)
  - [strreplace](https://teratermproject.github.io/manual/5/ja/macro/command/strreplace.html)
  - [strscan](https://teratermproject.github.io/manual/5/ja/macro/command/strscan.html)
  - [strspecial](https://teratermproject.github.io/manual/5/ja/macro/command/strspecial.html)
  - [strsplit](https://teratermproject.github.io/manual/5/ja/macro/command/strsplit.html)
  - [strtrim](https://teratermproject.github.io/manual/5/ja/macro/command/strtrim.html)
  - [tolower](https://teratermproject.github.io/manual/5/ja/macro/command/tolower.html)
  - [toupper](https://teratermproject.github.io/manual/5/ja/macro/command/toupper.html)

- ファイル操作コマンド
  - [basename](https://teratermproject.github.io/manual/5/ja/macro/command/basename.html)
  - [dirname](https://teratermproject.github.io/manual/5/ja/macro/command/dirname.html)
  - [fileclose](https://teratermproject.github.io/manual/5/ja/macro/command/fileclose.html)
  - [fileconcat](https://teratermproject.github.io/manual/5/ja/macro/command/fileconcat.html)
  - [filecopy](https://teratermproject.github.io/manual/5/ja/macro/command/filecopy.html)
  - [filecreate](https://teratermproject.github.io/manual/5/ja/macro/command/filecreate.html)
  - [filedelete](https://teratermproject.github.io/manual/5/ja/macro/command/filedelete.html)
  <!-- - [filelock](https://teratermproject.github.io/manual/5/ja/macro/command/filelock.html) -->
  <!-- - [filemarkptr](https://teratermproject.github.io/manual/5/ja/macro/command/filemarkptr.html) -->
  - [fileopen](https://teratermproject.github.io/manual/5/ja/macro/command/fileopen.html)
  - [filereadln](https://teratermproject.github.io/manual/5/ja/macro/command/filereadln.html)
  - [fileread](https://teratermproject.github.io/manual/5/ja/macro/command/fileread.html)
  - [filerename](https://teratermproject.github.io/manual/5/ja/macro/command/filerename.html)
  - [filesearch](https://teratermproject.github.io/manual/5/ja/macro/command/filesearch.html)
  <!-- - [fileseek](https://teratermproject.github.io/manual/5/ja/macro/command/fileseek.html) -->
  <!-- - [fileseekback](https://teratermproject.github.io/manual/5/ja/macro/command/fileseekback.html) -->
  - [filestat](https://teratermproject.github.io/manual/5/ja/macro/command/filestat.html)
  <!-- - [filestrseek](https://teratermproject.github.io/manual/5/ja/macro/command/filestrseek.html) -->
  <!-- - [filestrseek2](https://teratermproject.github.io/manual/5/ja/macro/command/filestrseek2.html) -->
  - [filetruncate](https://teratermproject.github.io/manual/5/ja/macro/command/filetruncate.html)
  <!-- - [fileunlock](https://teratermproject.github.io/manual/5/ja/macro/command/fileunlock.html) -->
  - [filewrite](https://teratermproject.github.io/manual/5/ja/macro/command/filewrite.html)
  - [filewriteln](https://teratermproject.github.io/manual/5/ja/macro/command/filewriteln.html)
  - [findfirst, findnext, findclose](https://teratermproject.github.io/manual/5/ja/macro/command/findoperations.html)
  - [foldercreate](https://teratermproject.github.io/manual/5/ja/macro/command/foldercreate.html)
  - [folderdelete](https://teratermproject.github.io/manual/5/ja/macro/command/folderdelete.html)
  - [foldersearch](https://teratermproject.github.io/manual/5/ja/macro/command/foldersearch.html)
  - [getdir](https://teratermproject.github.io/manual/5/ja/macro/command/getdir.html)
  <!-- - [getfileattr](https://teratermproject.github.io/manual/5/ja/macro/command/getfileattr.html) -->
  - [makepath](https://teratermproject.github.io/manual/5/ja/macro/command/makepath.html)
  - [setdir](https://teratermproject.github.io/manual/5/ja/macro/command/setdir.html)
  <!-- - [setfileattr](https://teratermproject.github.io/manual/5/ja/macro/command/setfileattr.html) -->

- パスワードコマンド
  - [delpassword](https://teratermproject.github.io/manual/5/ja/macro/command/delpassword.html)
  - [delpassword2](https://teratermproject.github.io/manual/5/ja/macro/command/delpassword2.html) // 補足あり [password](#password)
  - [getpassword](https://teratermproject.github.io/manual/5/ja/macro/command/getpassword.html)
  - [getpassword2](https://teratermproject.github.io/manual/5/ja/macro/command/getpassword2.html) // 補足あり [password](#password)
  - [ispassword](https://teratermproject.github.io/manual/5/ja/macro/command/ispassword.html)
  - [ispassword2](https://teratermproject.github.io/manual/5/ja/macro/command/ispassword2.html)
  - [passwordbox](https://teratermproject.github.io/manual/5/ja/macro/command/passwordbox.html) // 制限あり
  - [setpassword](https://teratermproject.github.io/manual/5/ja/macro/command/setpassword.html)
  - [setpassword2](https://teratermproject.github.io/manual/5/ja/macro/command/setpassword2.html) // 補足あり [password](#password)

- その他のコマンド
  - [assert](#assert) // 独自コマンド
  <!-- - [beep](https://teratermproject.github.io/manual/5/ja/macro/command/beep.html) -->
  - [bringupbox](https://teratermproject.github.io/manual/5/ja/macro/command/bringupbox.html)  // 制限あり
  - [checksum8](https://teratermproject.github.io/manual/5/ja/macro/command/checksum8.html) -->
  - [checksum8file](https://teratermproject.github.io/manual/5/ja/macro/command/checksum8.html)
  - [checksum16](https://teratermproject.github.io/manual/5/ja/macro/command/checksum16.html)
  - [checksum16file](https://teratermproject.github.io/manual/5/ja/macro/command/checksum16.html)
  - [checksum32](https://teratermproject.github.io/manual/5/ja/macro/command/checksum32.html)
  - [checksum32file](https://teratermproject.github.io/manual/5/ja/macro/command/checksum32.html)
  - [closesbox](https://teratermproject.github.io/manual/5/ja/macro/command/closesbox.html)  // 制限あり
  <!-- - [clipb2var](https://teratermproject.github.io/manual/5/ja/macro/command/clipb2var.html) -->
  - [crc16](https://teratermproject.github.io/manual/5/ja/macro/command/crc16.html)  // CRC-16/IBM-SDLC
  - [crc16file](https://teratermproject.github.io/manual/5/ja/macro/command/crc16.html) // CRC-16/IBM-SDLC
  - [crc32](https://teratermproject.github.io/manual/5/ja/macro/command/crc32.html)  // CRC-32/ISO-HDLC
  - [crc32file](https://teratermproject.github.io/manual/5/ja/macro/command/crc32.html)  // CRC-32/ISO-HDLC
  - [exec](https://teratermproject.github.io/manual/5/ja/macro/command/exec.html)
  - [dirnamebox](https://teratermproject.github.io/manual/5/ja/macro/command/dirnamebox.html)  // 制限あり
  - [filenamebox](https://teratermproject.github.io/manual/5/ja/macro/command/filenamebox.html)  // 制限あり
  - [getdate](https://teratermproject.github.io/manual/5/ja/macro/command/getdate.html)
  - [getenv](https://teratermproject.github.io/manual/5/ja/macro/command/getenv.html)
  - [getipv4addr](https://teratermproject.github.io/manual/5/ja/macro/command/getipv4addr.html)
  - [getipv6addr](https://teratermproject.github.io/manual/5/ja/macro/command/getipv6addr.html)
  <!-- - [getspecialfolder](https://teratermproject.github.io/manual/5/ja/macro/command/getspecialfolder.html) -->
  - [gettime](https://teratermproject.github.io/manual/5/ja/macro/command/gettime.html)
  - [getttdir](https://teratermproject.github.io/manual/5/ja/macro/command/getttdir.html)
  - [getver](https://teratermproject.github.io/manual/5/ja/macro/command/getver.html)
  - [ifdefined](https://teratermproject.github.io/manual/5/ja/macro/command/ifdefined.html) // labelは未実装です
  - [inputbox](https://teratermproject.github.io/manual/5/ja/macro/command/inputbox.html)  // 制限あり
  - [intdim](https://teratermproject.github.io/manual/5/ja/macro/command/intdim.html)
  - [listbox](https://teratermproject.github.io/manual/5/ja/macro/command/listbox.html)  // 制限あり
  - [messagebox](https://teratermproject.github.io/manual/5/ja/macro/command/messagebox.html)  // 制限あり
  - [random](https://teratermproject.github.io/manual/5/ja/macro/command/random.html)
  <!-- - [rotateleft](https://teratermproject.github.io/manual/5/ja/macro/command/rotateleft.html) -->
  <!-- - [rotateright](https://teratermproject.github.io/manual/5/ja/macro/command/rotateright.html) -->
  <!-- - [setdate](https://teratermproject.github.io/manual/5/ja/macro/command/setdate.html) -->
  <!-- - [setdlgpos](https://teratermproject.github.io/manual/5/ja/macro/command/setdlgpos.html) -->
  - [setenv](https://teratermproject.github.io/manual/5/ja/macro/command/setenv.html)
  <!-- - [setexitcode](https://teratermproject.github.io/manual/5/ja/macro/command/setexitcode.html) -->
  <!-- - [settime](https://teratermproject.github.io/manual/5/ja/macro/command/settime.html) -->
  <!-- - [show](https://teratermproject.github.io/manual/5/ja/macro/command/show.html) -->
  - [statusbox](https://teratermproject.github.io/manual/5/ja/macro/command/statusbox.html)  // 制限あり
  - [strdim](https://teratermproject.github.io/manual/5/ja/macro/command/strdim.html)
  - [uptime](https://teratermproject.github.io/manual/5/ja/macro/command/uptime.html)
  <!-- - [var2clipb](https://teratermproject.github.io/manual/5/ja/macro/command/var2clipb.html) -->
  - [yesnobox](https://teratermproject.github.io/manual/5/ja/macro/command/yesnobox.html)  // 制限あり


## assert
- こんなコマンドは本来(?)のttlにはありませんが、評価用に作成しました。
- 第一引数が0の場合は異常終了します。第一引数が偽(つまりゼロ)の場合も同様です。

```
assert "intvar"  "strval"+
```

```
assert  0 = 0  "strval" ; 正常終了する
assert  1 = 0  "strval" ; 異常終了する
```

## connect
```
connect <command line parameters>
```
- SSH接続します。telnet接続やSSH1接続、COMポート接続はできません。

### SSH2接続
- pythonのparamikoを使って接続します。
- `/ask4passwd` は使えません。
- `/2` を省略するとSSH2で接続します。
- 注意！：ssh接続をするには接続先のサーバが必要です。

```
connect 'myserver /ssh    /user=username /passwd=password'
connect 'myserver /ssh /2 /user=username /passwd=password'
connect 'myserver /ssh    /user=username /passwd=password /keyfile=private-key-file'
connect 'myserver /ssh /2 /user=username /passwd=password /keyfile=private-key-file'
```

### command line に接続
- command lineに入ります。pingなど好きなコマンドが打てます。

```
connect '/cmd'
```
## logopen

```
logopen <filename> <binary flag> <append flag> [<plain text flag> [<timestamp flag> [<hide dialog flag> [<include screen buffer flag> [<timestamp type>]]]]]
```

- ログを開始する。
- ファイル `filename` に受信した文字が書き込まれる。ファイル名はログの設定の書式が利用でき`ない`。
- ログを開始したあとも次のコマンドは実行される。
- ログの設定のフォルダにログは作成される。
- カレントディレクトリを変更するには `changedir` マクロを使用する。
- `binary flag` は無視される。
- `append flag` の値が0以外の場合、そのファイルに追加して書き込む。
- `plain text flag` は無視される。
- `timestamp flag` が 0 以外の場合、ログの行頭に時刻を追加する。
- ただし、`binary flag` が 0 以外の場合、`plain text flag`, `timestamp flag` は両方とも無視される。
- `hide dialog flag` は無視される。
- `include screen buffer flag>`は無視される。
- `timestamp type` は 以下の形式を指定する。デフォルトは `0`である。
```
値	意味
0	ローカルタイム
1	UTC
2	経過時間 (Logging)
3	経過時間 (Connection)
```

## xxxxbox系の制限について

- `ttlmacoro.py` から直接ttlを呼ぶと、xxxbox系は無視されます。
- nextnextpingをGUIで起動すると、画面はでますがかなりいい加減に作っています。
  - そもそも論として pingがしたいだけなのになぜ実装した……

## execの実行について

- バッチファイルを実行したとき、コマンドプロンプトが `CP932` を期待しているので、ファイルが `utf-8` ですとフォルダ名が文字化けます。
  - 何が言いたいかというと `filewrite` で書き込んだデータは  `utf-8` です。
  　- これでバッチファイルを作って、かつフォルダだったりした場合文字化けます。
  　- なので、 `filewrite` は一律  `CP932` で書き込もうかと思ったのですが、通常テキストなどで `utf-8` を期待している場合もありそうなので対処保留としました。
    - 対処方法は検討中。＞ 本家もそうなら放置かな……
- あと、もはやttlとはまったく関係ないですが、
  - バッチファイルを `\\192.168.1.1\aaa` といった UNCパス形式の上で実行するとすべからく変な動きをします。
  - そういうときは `pushd` と `popd` を使いましょう。。。


## password

- `setpassword2`, `getpassword` は本家では aes-256-ctrで暗号化されていますが、こちらでは Python の `cryptography.fernet.Fernet` を使っています。
- 何が言いたいのかというと、互換性はありません。




