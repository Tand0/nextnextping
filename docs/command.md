
# TTL command reference

Command index

- Communication commands
  <!-- - [bplusrecv](https://teratermproject.github.io/manual/5/en/macro/command/bplusrecv.html) -->
  <!-- - [bplussend](https://teratermproject.github.io/manual/5/en/macro/command/bplussend.html) -->
  <!-- - [callmenu](https://teratermproject.github.io/manual/5/en/macro/command/callmenu.html) -->
  - [changedir](https://teratermproject.github.io/manual/5/en/macro/command/changedir.html)
  <!-- -  [clearscreen](https://teratermproject.github.io/manual/5/en/macro/command/clearscreen.html) -->
  - [closett](https://teratermproject.github.io/manual/5/en/macro/command/closett.html)
  - [connect](https://teratermproject.github.io/manual/5/en/macro/command/connect.html) // Supplementary information  [connect](#connect)
  <!-- -  [cygconnect](https://teratermproject.github.io/manual/5/en/macro/command/cygconnect.html) -->
  - [disconnect](https://teratermproject.github.io/manual/5/en/macro/command/disconnect.html)
  - [dispstr](https://teratermproject.github.io/manual/5/en/macro/command/dispstr.html)
  <!-- - [enablekeyb](https://teratermproject.github.io/manual/5/en/macro/command/enablekeyb.html) -->
  - [flushrecv](https://teratermproject.github.io/manual/5/en/macro/command/flushrecv.html)
  - [gethostname](https://teratermproject.github.io/manual/5/en/macro/command/gethostname.html)
  <!-- - [getmodemstatus](https://teratermproject.github.io/manual/5/en/macro/command/getmodemstatus.html) -->
  - [gettitle](https://teratermproject.github.io/manual/5/en/macro/command/gettitle.html)
  <!-- - [getttpos](https://teratermproject.github.io/manual/5/en/macro/command/getttpos.html) -->
  <!-- - [kmtfinish](https://teratermproject.github.io/manual/5/en/macro/command/kmtfinish.html) -->
  <!-- - [kmtget](https://teratermproject.github.io/manual/5/en/macro/command/kmtget.html) -->
  <!-- - [kmtrecv](https://teratermproject.github.io/manual/5/en/macro/command/kmtrecv.html) -->
  <!-- - [kmtsend](https://teratermproject.github.io/manual/5/en/macro/command/kmtsend.html) -->
  <!-- - [loadkeymap](https://teratermproject.github.io/manual/5/en/macro/command/loadkeymap.html) -->
  <!-- - [logautoclosemode](https://teratermproject.github.io/manual/5/en/macro/command/logautoclosemode.html) -->
  - [logclose](https://teratermproject.github.io/manual/5/en/macro/command/logclose.html)
  - [loginfo](https://teratermproject.github.io/manual/5/en/macro/command/loginfo.html)
  - [logopen](https://teratermproject.github.io/manual/5/en/macro/command/logopen.html) // Supplementary information  [logopen](#logopen)
  - [logpause](https://teratermproject.github.io/manual/5/en/macro/command/logpause.html)
  <!-- - [logrotate](https://teratermproject.github.io/manual/5/en/macro/command/logrotate.html) -->
  - [logstart](https://teratermproject.github.io/manual/5/en/macro/command/logstart.html)
  - [logwrite](https://teratermproject.github.io/manual/5/en/macro/command/logwrite.html)
  <!-- - [quickvanrecv](https://teratermproject.github.io/manual/5/en/macro/command/quickvanrecv.html) -->
  <!-- - [quickvansend](https://teratermproject.github.io/manual/5/en/macro/command/quickvansend.html) -->
  - [recvln](https://teratermproject.github.io/manual/5/en/macro/command/recvln.html)
  <!-- - [restoresetup](https://teratermproject.github.io/manual/5/en/macro/command/restoresetup.html) -->
   - [scprecv](https://teratermproject.github.io/manual/5/en/macro/command/scprecv.html) // The contents are sftp
   - [scpsend](https://teratermproject.github.io/manual/5/en/macro/command/scpsend.html) // The contents are sftp
  - [send](https://teratermproject.github.io/manual/5/en/macro/command/send.html)
  <!-- - [sendbinary](https://teratermproject.github.io/manual/5/en/macro/command/sendbinary.html) -->
  - [sendbreak](https://teratermproject.github.io/manual/5/en/macro/command/sendbreak.html) // Send to `Ctrl-C`
  <!-- - [sendbroadcast](https://teratermproject.github.io/manual/5/en/macro/command/sendbroadcast.html) -->
  - [sendfile](https://teratermproject.github.io/manual/5/en/macro/command/sendfile.html) // Not implemented
  <!-- - [sendkcode](https://teratermproject.github.io/manual/5/en/macro/command/sendkcode.html) -->
  - [sendln](https://teratermproject.github.io/manual/5/en/macro/command/sendln.html)
  <!-- - [sendlnbroadcast](https://teratermproject.github.io/manual/5/en/macro/command/sendlnbroadcast.html) -->
  <!-- - [sendlnmulticast](https://teratermproject.github.io/manual/5/en/macro/command/sendlnmulticast.html) -->
  - [sendtext](https://teratermproject.github.io/manual/5/en/macro/command/sendtext.html)
  <!-- - [sendmulticast](https://teratermproject.github.io/manual/5/en/macro/command/sendmulticast.html) -->
  - [setbaud](https://teratermproject.github.io/manual/5/en/macro/command/setbaud.html)
  <!-- - [setdebug](https://teratermproject.github.io/manual/5/en/macro/command/setdebug.html) -->
  - [setdtr](https://teratermproject.github.io/manual/5/en/macro/command/setdtr.html)
  <!-- - [setecho](https://teratermproject.github.io/manual/5/en/macro/command/setecho.html) -->
  - [setflowctrl](https://teratermproject.github.io/manual/5/en/macro/command/setflowctrl.html)
  <!-- - [setmulticastname](https://teratermproject.github.io/manual/5/en/macro/command/setmulticastname.html) -->
  - [setrts](https://teratermproject.github.io/manual/5/en/macro/command/setrts.html)
  <!-- - [setserialdelaychar](https://teratermproject.github.io/manual/5/en/macro/command/setserialdelaychar.html) -->
  <!-- - [setserialdelayline](https://teratermproject.github.io/manual/5/en/macro/command/setserialdelayline.html) -->
  - [setspeed](https://teratermproject.github.io/manual/5/en/macro/command/setspeed.html)
  <!-- - [setsync](https://teratermproject.github.io/manual/5/en/macro/command/setsync.html) -->
  - [settitle](https://teratermproject.github.io/manual/5/en/macro/command/settitle.html)
  <!-- - [showtt](https://teratermproject.github.io/manual/5/en/macro/command/showtt.html) -->
  - [testlink](https://teratermproject.github.io/manual/5/en/macro/command/testlink.html)
  - [unlink](https://teratermproject.github.io/manual/5/en/macro/command/unlink.html)
  - [wait](https://teratermproject.github.io/manual/5/en/macro/command/wait.html)
  - [wait4all](https://teratermproject.github.io/manual/5/en/macro/command/wait4all.html) // Same as wait
  <!-- - [waitevent](https://teratermproject.github.io/manual/5/en/macro/command/waitevent.html) -->
  - [waitln](https://teratermproject.github.io/manual/5/en/macro/command/waitln.html)
  - [waitn](https://teratermproject.github.io/manual/5/en/macro/command/waitn.html)
  <!-- - [waitrecv](https://teratermproject.github.io/manual/5/en/macro/command/waitrecv.html) -->
  <!-- - [waitregex](https://teratermproject.github.io/manual/5/en/macro/command/waitregex.html) -->
  <!-- - [xmodemrecv](https://teratermproject.github.io/manual/5/en/macro/command/xmodemrecv.html) -->
  <!-- - [xmodemsend](https://teratermproject.github.io/manual/5/en/macro/command/xmodemsend.html) -->
  <!-- - [ymodemrecv](https://teratermproject.github.io/manual/5/en/macro/command/ymodemrecv.html) -->
  <!-- - [ymodemsend](https://teratermproject.github.io/manual/5/en/macro/command/ymodemsend.html) -->
  <!-- - [zmodemrecv](https://teratermproject.github.io/manual/5/en/macro/command/zmodemrecv.html) -->
  <!-- - [zmodemsend](https://teratermproject.github.io/manual/5/en/macro/command/zmodemsend.html) -->

- Control commands
  - [break](./syntax.md#break)
  - [call](./syntax.md#call)
  - [continue](./syntax.md#continue)
  - [do, loop](./syntax.md#do)
  - [end](./syntax.md#endexit)
  - [execcmnd](https://teratermproject.github.io/manual/5/en/macro/command/execcmnd.html)
  - [exit](./syntax.md#endexit)
  - [for, next](./syntax.md#for)
  - goto // It's not implemented.  I hate GOTO statements. When I was little, my mother forced me to use GOTO in Error Handling in VBA, but now I'm have the right not to use GOTO statements.
  - [if, then, elseif, else, endif](./syntax.md#if)
  - [include](./syntax.md#include)
  - [mpause](https://teratermproject.github.io/manual/5/en/macro/command/mpause.html)
  - [pause](https://teratermproject.github.io/manual/5/en/macro/command/pause.html)
  - [return](./syntax.md#call)
  - [until, enduntil](./syntax.md#until)
  - [while, endwhile](./syntax.md#while)

- String operation commands
  - [code2str](https://teratermproject.github.io/manual/5/en/macro/command/code2str.html)
  - [expandenv](https://teratermproject.github.io/manual/5/en/macro/command/expandenv.html)
  - [int2str](https://teratermproject.github.io/manual/5/en/macro/command/int2str.html)
  - [regexoption](https://teratermproject.github.io/manual/5/en/macro/command/regexoption.html)
  - [sprintf](https://teratermproject.github.io/manual/5/en/macro/command/sprintf.html)
  - [sprintf2](https://teratermproject.github.io/manual/5/en/macro/command/sprintf2.html)
  - [str2code](https://teratermproject.github.io/manual/5/en/macro/command/str2code.html)
  - [str2int](https://teratermproject.github.io/manual/5/en/macro/command/str2int.html)
  - [strcompare](https://teratermproject.github.io/manual/5/en/macro/command/strcompare.html)
  - [strconcat](https://teratermproject.github.io/manual/5/en/macro/command/strconcat.html)
  - [strcopy](https://teratermproject.github.io/manual/5/en/macro/command/strcopy.html)
  - [strinsert](https://teratermproject.github.io/manual/5/en/macro/command/strinsert.html)
  - [strjoin](https://teratermproject.github.io/manual/5/en/macro/command/strjoin.html)
  - [strlen](https://teratermproject.github.io/manual/5/en/macro/command/strlen.html)
  - [strmatch](https://teratermproject.github.io/manual/5/en/macro/command/strmatch.html)
  - [strremove](https://teratermproject.github.io/manual/5/en/macro/command/strremove.html)
  - [strreplace](https://teratermproject.github.io/manual/5/en/macro/command/strreplace.html)
  - [strscan](https://teratermproject.github.io/manual/5/en/macro/command/strscan.html)
  - [strspecial](https://teratermproject.github.io/manual/5/en/macro/command/strspecial.html)
  - [strsplit](https://teratermproject.github.io/manual/5/en/macro/command/strsplit.html)
  - [strtrim](https://teratermproject.github.io/manual/5/en/macro/command/strtrim.html)
  - [tolower](https://teratermproject.github.io/manual/5/en/macro/command/tolower.html)
  - [toupper](https://teratermproject.github.io/manual/5/en/macro/command/toupper.html)

- File operation commands
  - [basename](https://teratermproject.github.io/manual/5/en/macro/command/basename.html)
  - [dirname](https://teratermproject.github.io/manual/5/en/macro/command/dirname.html)
  - [fileclose](https://teratermproject.github.io/manual/5/en/macro/command/fileclose.html)
  - [fileconcat](https://teratermproject.github.io/manual/5/en/macro/command/fileconcat.html)
  - [filecopy](https://teratermproject.github.io/manual/5/en/macro/command/filecopy.html)
  - [filecreate](https://teratermproject.github.io/manual/5/en/macro/command/filecreate.html)
  - [filedelete](https://teratermproject.github.io/manual/5/en/macro/command/filedelete.html)
  <!-- - [filelock](https://teratermproject.github.io/manual/5/en/macro/command/filelock.html) -->
  <!-- - [filemarkptr](https://teratermproject.github.io/manual/5/en/macro/command/filemarkptr.html) -->
  - [fileopen](https://teratermproject.github.io/manual/5/en/macro/command/fileopen.html)
  - [filereadln](https://teratermproject.github.io/manual/5/en/macro/command/filereadln.html)
  - [fileread](https://teratermproject.github.io/manual/5/en/macro/command/fileread.html)
  - [filerename](https://teratermproject.github.io/manual/5/en/macro/command/filerename.html)
  - [filesearch](https://teratermproject.github.io/manual/5/en/macro/command/filesearch.html)
  <!-- - [fileseek](https://teratermproject.github.io/manual/5/en/macro/command/fileseek.html) -->
  <!-- - [fileseekback](https://teratermproject.github.io/manual/5/en/macro/command/fileseekback.html) -->
  - [filestat](https://teratermproject.github.io/manual/5/en/macro/command/filestat.html)
  <!-- - [filestrseek](https://teratermproject.github.io/manual/5/en/macro/command/filestrseek.html) -->
  <!-- - [filestrseek2](https://teratermproject.github.io/manual/5/en/macro/command/filestrseek2.html) -->
  - [filetruncate](https://teratermproject.github.io/manual/5/en/macro/command/filetruncate.html)
  <!-- - [fileunlock](https://teratermproject.github.io/manual/5/en/macro/command/fileunlock.html) -->
  - [filewrite](https://teratermproject.github.io/manual/5/en/macro/command/filewrite.html)
  - [filewriteln](https://teratermproject.github.io/manual/5/en/macro/command/filewriteln.html)
  - [findfirst, findnext, findclose](https://teratermproject.github.io/manual/5/en/macro/command/findoperations.html)
  - [foldercreate](https://teratermproject.github.io/manual/5/en/macro/command/foldercreate.html)
  - [folderdelete](https://teratermproject.github.io/manual/5/en/macro/command/folderdelete.html)
  - [foldersearch](https://teratermproject.github.io/manual/5/en/macro/command/foldersearch.html)
  - [getdir](https://teratermproject.github.io/manual/5/en/macro/command/getdir.html)
  <!-- - [getfileattr](https://teratermproject.github.io/manual/5/en/macro/command/getfileattr.html) -->
  - [makepath](https://teratermproject.github.io/manual/5/en/macro/command/makepath.html)
  - [setdir](https://teratermproject.github.io/manual/5/en/macro/command/setdir.html)
  <!-- - [setfileattr](https://teratermproject.github.io/manual/5/en/macro/command/setfileattr.html) -->

- Password commands
  - [delpassword](https://teratermproject.github.io/manual/5/en/macro/command/delpassword.html)
  - [delpassword2](https://teratermproject.github.io/manual/5/en/macro/command/delpassword2.html) // Supplementary information [password](#password)
  - [getpassword](https://teratermproject.github.io/manual/5/en/macro/command/getpassword.html)
  - [getpassword2](https://teratermproject.github.io/manual/5/en/macro/command/getpassword2.html) // Supplementary information [password](#password)
  - [ispassword](https://teratermproject.github.io/manual/5/en/macro/command/ispassword.html)
  - [ispassword2](https://teratermproject.github.io/manual/5/en/macro/command/ispassword2.html)
  - [passwordbox](https://teratermproject.github.io/manual/5/en/macro/command/passwordbox.html) // Limited
  - [setpassword](https://teratermproject.github.io/manual/5/en/macro/command/setpassword.html)
  - [setpassword2](https://teratermproject.github.io/manual/5/en/macro/command/setpassword2.html) // Supplementary information [password](#password)

- Miscellaneous commands
  - [assert](#assert) // Original commands
  <!-- - [beep](https://teratermproject.github.io/manual/5/en/macro/command/beep.html) -->
  - [bringupbox](https://teratermproject.github.io/manual/5/en/macro/command/bringupbox.html)  // Limited
  - [checksum8](https://teratermproject.github.io/manual/5/en/macro/command/checksum8.html) -->
  - [checksum8file](https://teratermproject.github.io/manual/5/en/macro/command/checksum8.html)
  - [checksum16](https://teratermproject.github.io/manual/5/en/macro/command/checksum16.html)
  - [checksum16file](https://teratermproject.github.io/manual/5/en/macro/command/checksum16.html)
  - [checksum32](https://teratermproject.github.io/manual/5/en/macro/command/checksum32.html)
  - [checksum32file](https://teratermproject.github.io/manual/5/en/macro/command/checksum32.html)
  - [closesbox](https://teratermproject.github.io/manual/5/en/macro/command/closesbox.html)  // Limited
  <!-- - [clipb2var](https://teratermproject.github.io/manual/5/en/macro/command/clipb2var.html) -->
  - [crc16](https://teratermproject.github.io/manual/5/en/macro/command/crc16.html)  // CRC-16/IBM-SDLC
  - [crc16file](https://teratermproject.github.io/manual/5/en/macro/command/crc16.html) // CRC-16/IBM-SDLC
  - [crc32](https://teratermproject.github.io/manual/5/en/macro/command/crc32.html)  // CRC-32/ISO-HDLC
  - [crc32file](https://teratermproject.github.io/manual/5/en/macro/command/crc32.html)  // CRC-32/ISO-HDLC
  - [exec](https://teratermproject.github.io/manual/5/en/macro/command/exec.html)
  - [dirnamebox](https://teratermproject.github.io/manual/5/en/macro/command/dirnamebox.html)  // Limited
  - [filenamebox](https://teratermproject.github.io/manual/5/en/macro/command/filenamebox.html)  // Limited
  - [getdate](https://teratermproject.github.io/manual/5/en/macro/command/getdate.html)
  - [getenv](https://teratermproject.github.io/manual/5/en/macro/command/getenv.html)
  - [getipv4addr](https://teratermproject.github.io/manual/5/en/macro/command/getipv4addr.html)
  - [getipv6addr](https://teratermproject.github.io/manual/5/en/macro/command/getipv6addr.html)
  <!-- - [getspecialfolder](https://teratermproject.github.io/manual/5/en/macro/command/getspecialfolder.html) -->
  - [gettime](https://teratermproject.github.io/manual/5/en/macro/command/gettime.html)
  - [getttdir](https://teratermproject.github.io/manual/5/en/macro/command/getttdir.html)
  - [getver](https://teratermproject.github.io/manual/5/en/macro/command/getver.html)
  - [ifdefined](https://teratermproject.github.io/manual/5/en/macro/command/ifdefined.html)
  - [inputbox](https://teratermproject.github.io/manual/5/en/macro/command/inputbox.html)  // Limited
  - [intdim](https://teratermproject.github.io/manual/5/en/macro/command/intdim.html)
  - [listbox](https://teratermproject.github.io/manual/5/en/macro/command/listbox.html)  // Limited
  - [messagebox](https://teratermproject.github.io/manual/5/en/macro/command/messagebox.html)  // Limited
  - [random](https://teratermproject.github.io/manual/5/en/macro/command/random.html)
  <!-- - [rotateleft](https://teratermproject.github.io/manual/5/en/macro/command/rotateleft.html) -->
  <!-- - [rotateright](https://teratermproject.github.io/manual/5/en/macro/command/rotateright.html) -->
  <!-- - [setdate](https://teratermproject.github.io/manual/5/en/macro/command/setdate.html) -->
  <!-- - [setdlgpos](https://teratermproject.github.io/manual/5/en/macro/command/setdlgpos.html) -->
  - [setenv](https://teratermproject.github.io/manual/5/en/macro/command/setenv.html)
  <!-- - [setexitcode](https://teratermproject.github.io/manual/5/en/macro/command/setexitcode.html) -->
  <!-- - [settime](https://teratermproject.github.io/manual/5/en/macro/command/settime.html) -->
  <!-- - [show](https://teratermproject.github.io/manual/5/en/macro/command/show.html) -->
  - [statusbox](https://teratermproject.github.io/manual/5/en/macro/command/statusbox.html)  // Limited
  - [strdim](https://teratermproject.github.io/manual/5/en/macro/command/strdim.html)
  - [uptime](https://teratermproject.github.io/manual/5/en/macro/command/uptime.html)
  <!-- - [var2clipb](https://teratermproject.github.io/manual/5/en/macro/command/var2clipb.html) -->
  - [yesnobox](https://teratermproject.github.io/manual/5/en/macro/command/yesnobox.html)  // Limited


## assert
- This command does not exist in the original ttl, but I created it for evaluation purposes.
    - こんなコマンドは本来(?)のttlにはありませんが、評価用に作成しました。
- If the first argument is 0, the function will terminate abnormally. The same applies if the first argument is false (i.e., zero).
    - 第一引数が0の場合は異常終了します。第一引数が偽(つまりゼロ)の場合も同様です。

```
assert "intvar"  "strval"+
```

```
assert  0 = 0  "strval" ; Completes normally
assert  1 = 0  "strval" ; Completes NOT normally
```

## connect
```
connect <command line parameters>
```
- SSH connection. Telnet connection, SSH1 connection, and COM port connection are not possible.
  - SSH接続します。telnet接続やSSH1接続、COMポート接続はできません。


### telnet connection

- The following example shows a telnet connection.
- If the `nossh` option is not specified, an SSH2 connection will be used.

```
connect 'myserver:22 /noss /T=1'  ; telnet and telnet negotiation
connect 'myserver:22 /noss /T=0'  ; telnet and telnet NOT negotiation
connect 'myserver:22 /noss'  ; telnet and telnet NOT negotiation
```

### SSH1 connection

### SSH2 connection

- SSH2 connect using python paramiko.
- `/ask4passwd` cannot be used.
    - `/ask4passwd` は使えません。
- SSH1 cannot be used due to security issues.
- telnet cannot be used due to security issues.
- If you specify `/1`, it is not supported due to Paramiko security reasons.
- If you omit `/2`, you will connect using SSH2.
- To make an ssh connection, you need a server to connect to.
  - ssh接続をするには接続先のサーバが必要です。

```
connect 'myserver /ssh    /user=username /passwd=password'
connect 'myserver /ssh /2 /user=username /passwd=password'
connect 'myserver /ssh    /user=username /passwd=password /keyfile=private-key-file'
connect 'myserver /ssh /2 /user=username /passwd=password /keyfile=private-key-file'
```

### Serial connection

- Serial connect using python paramiko.
    - pythonの pyserial を使って接続します。
- Because of the pyserial specification, the parameters passed are different from those of teraterm macros.
    - pyserial の仕様により、渡されるパラメータは teraterm マクロとは異なります。
    - Linuxの場合は `/dev/pts/*` や `/dev/ttyS*` のように指定します。
    - Windowsの場合は `COM0` または `0` のように指定します。
    - Windowsの場合で先頭文字が数字の場合 `COM0` のように内部で `COM` を付与します。

```
For Linux:
connect '/C=/dev/pts/8'

For Windows:
connect '/C=COM4'
or
connect '/C=4'
```

### command line connection
- '/cmd' goes into the command line.
    - '/cmd'はcommand lineに入ります。
- When starting python, `cmd` is launched on Windows, and `/bin/sh` on other systems.
    - python起動の場合、windowsでは `cmd` 、それ以外では `/bin/sh` が起動します。

```
connect '/cmd'
```

## logopen

```
logopen <filename> <binary flag> <append flag> [<plain text flag> [<timestamp flag> [<hide dialog flag> [<include screen buffer flag> [<timestamp type>]]]]]
```

- Causes to start logging.
- Received characters are written to the file `filename`. The file name CANNOT use the format specified in the log settings.
    - ファイル `filename` に受信した文字が書き込まれる。ファイル名はログの設定の書式が利用でき`ない`。
- To change the current directory, use the `changedir` macro.
    - カレントディレクトリを変更するには `changedir` マクロを使用する。
- The `binary flag` is ignored.
- If `append flag` != 0 then append to the file.
- `plain text flag` is ignored.
- If `timestamp flag` != 0 then add the time to the beginning of the log line.
- If `binary flag` == 0 then `plain text flag`, `timestamp flag` is ignored.
- `hide dialog flag` is ignored.
- `include screen buffer flag>` is ignored.
- `timestamp type` specifies the format following. The default is `0`.
    - `timestamp type` は 以下の形式を指定する。デフォルトは `0`である。

```
value	Meaning
0	Local Time
1	UTC
2	Elapsed Time (Logging)
3	Elapsed Time (Connection)
```

## About the restrictions of xxxxbox

- Commands in xxxxbox are ignored
    - `ttlmacoro.py` から直接ttlを呼ぶと、xxxbox系は無視されます。
    - nextnextpingをGUIで起動すると、画面はでますがかなりいい加減に作っています。
        - そもそも論として pingがしたいだけなのになぜTTLを実装した……

## About executing exec

- バッチファイルを実行したとき、コマンドプロンプトが `CP932` を期待しているので、ファイルが `utf-8` ですとフォルダ名が文字化けます。
    - 何が言いたいかというと `filewrite` で書き込んだデータは  `utf-8` です。
      　- これでバッチファイルを作って、かつフォルダだったりした場合文字化けます。
  　    - なので、 `filewrite` は一律  `CP932` で書き込もうかと思ったのですが、通常テキストなどで `utf-8` を期待している場合もありそうなので対処保留としました。
        - 対処方法は検討中。＞ 本家もそうなら放置かな……
- あと、もはやttlとはまったく関係ないですが、
    - Windows で `*.bast` を `\\192.168.1.1\aaa` のようなUNCパス形式で実行するとすべからく変な動きをします。
    - そういうときは `pushd` と `popd` を使いましょう。。。


## password
- It is not compatible with TeraTerm.
    - `setpassword2`, `getpassword` は本家では aes-256-ctrで暗号化されていますが、こちらでは Python の `cryptography.fernet.Fernet` を使っています。
    - 何が言いたいのかというと、互換性はありません。

