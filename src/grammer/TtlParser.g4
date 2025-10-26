/**
 * export CLASSPATH=".:/usr/local/lib/antlr-4.13.2-complete.jar:$CLASSPATH"
 * alias antlr4='java -jar /usr/local/lib/antlr-4.13.2-complete.jar'
 * alias grun='java org.antlr.v4.runtime.misc.TestRig'
 * cd /mnt/d/gitwork/NextNextPing/src/grammer/
 * antlr4 -visitor -Dlanguage=Python3 TtlParser.g4
 */
grammar TtlParser;


NUMBER: [-+]? [0-9]+;
NUMBER_16: '$' [-+]? [a-fA-F0-9]+;

//NUMBER_ASCII: '#' '$'? [a-fA-F0-9]+;
//STRING1: '\'' ~[']* '\'';
//STRING2: '"' ~["]* '"';
//strContext: (STRING1 | STRING2 | NUMBER_ASCII)+;
STRING1: ('\'' ~[']* '\'' | '"' ~["]* '"' | '#' '$'? [a-fA-F0-9]+)+;
strContext: STRING1;


KEYWORD: [_a-zA-Z][_a-zA-Z0-9]*;
keyword: KEYWORD;

strExpression: strContext| keyword;

intContext
    : NUMBER
    | NUMBER_16
    ;
intExpression: intContext | keyword | '(' p11Expression ')';

p1Expression
    : intExpression
    | 'not' intExpression
    | '~' intExpression
    | '!' intExpression
    ;

p2Expression
    : p1Expression
    | p2Expression '*' p1Expression
    | p2Expression '/' p1Expression
    | p2Expression '%' p1Expression
    ;

p3Expression
    : p2Expression
    | p3Expression '+' p2Expression
    | p3Expression '-' p2Expression
    ;

p4Expression
    : p3Expression
    | p4Expression '>>>' p3Expression
    | p4Expression '>>' p3Expression
    | p4Expression '<<' p3Expression
    ;

p5Expression
    : p4Expression
    | p5Expression 'and' p4Expression
    | p5Expression '&' p4Expression
    ;

p6Expression
    : p5Expression
    | p6Expression 'xor' p5Expression
    | p6Expression '^' p5Expression
    ;

p7Expression
    : p6Expression
    | p7Expression 'or' p6Expression
    | p7Expression '|' p6Expression
    ;

p8Expression
    : p7Expression
    | p8Expression '<' p7Expression
    | p8Expression '>' p7Expression
    | p8Expression '<=' p7Expression
    | p8Expression '>=' p7Expression
    ;

p9Expression
    : p8Expression
    | p9Expression '=' p8Expression
    | p9Expression '==' p8Expression
    | p9Expression '<>' p8Expression
    | p9Expression '!=' p8Expression
    ;

p10Expression
    : p9Expression
    | p10Expression '&&' p9Expression
    ;

p11Expression
    : p10Expression
    | p11Expression '||' p10Expression
    ;

RN: '\r'? '\n'
    | ';' ~[\n]* '\n'
    ;

WS1 : [ \t]+ -> skip;
WS2 : '/*' ~[/]* '*/'-> skip;

command
    : 'bplusrecv'
    | 'bplussend' strExpression
    | 'callmenu' p11Expression
    | 'changedir' strExpression
    | 'clearscreen' strExpression
    | 'closett' 
    | 'connect' strExpression
    | 'cygconnect' strExpression?
    | 'disconnect'
    | 'dispstr' strExpression+
    | 'enablekeyb' p11Expression
    | 'flushrecv' 
    | 'gethostname' KEYWORD
    | 'getmodemstatus' KEYWORD
    | 'gettitle' KEYWORD
    | 'getttpos' p11Expression p11Expression p11Expression p11Expression p11Expression p11Expression p11Expression p11Expression p11Expression
    | 'kmtfinish'
    | 'kmtget' strExpression
    | 'kmtrecv'
    | 'kmtsend' strExpression
    | 'loadkeymap' strExpression
    | 'logautoclosemode' p11Expression
    | 'logclose'
    | 'loginfo' strExpression
    | 'logopen' strExpression p11Expression+
    | 'logpause'
    | 'logrotate' strExpression p11Expression?
    | 'logstart' 
    | 'logwrite' strExpression
    | 'quickvanrecv'
    | 'quickvansend' strExpression
    | 'recvln'
    | 'restoresetup' strExpression
    | 'scprecv' strExpression strExpression?
    | 'scpsend' strExpression strExpression?
    | 'send' strExpression+
    | 'sendbinary' (strExpression|p11Expression)+
    | 'sendbreak'
    | 'sendbroadcast' (strExpression|p11Expression)+
    | 'sendfile' strExpression p11Expression
    | 'sendkcode' p11Expression p11Expression
    | 'sendln' strExpression*
    | 'sendlnbroadcast' strExpression*
    | 'sendlnmulticast' strExpression (strExpression|p11Expression)+
    | 'sendtext' (strExpression|p11Expression)+
    | 'sendmulticast' strExpression (strExpression|p11Expression)+
    | 'setbaud' p11Expression
    | 'setdebug' p11Expression
    | 'setdtr' p11Expression
    | 'setecho' p11Expression
    | 'setflowctrl' p11Expression
    | 'setmulticastname' strExpression
    | 'setrts' p11Expression
    | 'setserialdelaychar' p11Expression
    | 'setserialdelayline' p11Expression
    | 'setspeed' p11Expression
    | 'setsync' p11Expression
    | 'settitle' strExpression
    | 'showtt' p11Expression
    | 'testlink'
    | 'unlink'
    | 'wait' strExpression+
    | 'wait4all' strExpression+
    | 'waitevent' p11Expression
    | 'waitln' strExpression+
    | 'waitn' p11Expression
    | 'waitrecv' strExpression p11Expression p11Expression
    | 'waitregex' strExpression+
    | 'xmodemrecv' strExpression p11Expression p11Expression
    | 'xmodemsend' strExpression p11Expression
    | 'ymodemrecv'
    | 'ymodemsend' strExpression
    | 'zmodemrecv' 
    | 'zmodemsend' strExpression p11Expression

    | 'break'
    | 'call' KEYWORD
    | 'continue'
    | 'end'
    | 'execcmnd' strExpression
    | 'exit'
    | 'goto' strExpression
    | 'include' strExpression
    | 'mpause' p11Expression
    | 'pause' p11Expression
    | 'return'

    | 'code2str' KEYWORD p11Expression
    | 'expandenv' KEYWORD strExpression?
    | 'int2str' KEYWORD p11Expression
    | 'regexoption' strExpression+
    | 'sprintf' strExpression (strExpression|p11Expression)*
    | 'sprintf2' KEYWORD strExpression (strExpression|p11Expression)*
    | 'str2code' KEYWORD strExpression
    | 'str2int' KEYWORD strExpression
    | 'strcompare' strExpression strExpression
    | 'strconcat' KEYWORD strExpression
    | 'strcopy' strExpression p11Expression p11Expression strExpression
    | 'strinsert' KEYWORD p11Expression strExpression
    | 'strjoin ' KEYWORD strExpression p11Expression?
    | 'strlen' strExpression
    | 'strmatch' strExpression strExpression
    | 'strremove' KEYWORD p11Expression p11Expression
    | 'strreplace' KEYWORD p11Expression strExpression strExpression
    | 'strscan' strExpression strExpression
    | 'strspecial' KEYWORD strExpression
    | 'strsplit' KEYWORD strExpression p11Expression?
    | 'strtrim' KEYWORD strExpression
    | 'tolower' KEYWORD strExpression
    | 'toupper' KEYWORD strExpression
    | 'basename' KEYWORD strExpression
    | 'dirname' KEYWORD strExpression
    | 'fileclose' KEYWORD
    | 'fileconcat' strExpression strExpression
    | 'filecopy' strExpression strExpression
    | 'filecreate' strExpression strExpression
    | 'filedelete' strExpression
    | 'filelock' KEYWORD p11Expression?
    | 'filemarkptr' KEYWORD
    | 'fileopen' KEYWORD strExpression p11Expression p11Expression?
    | 'filereadln' KEYWORD KEYWORD
    | 'fileread' KEYWORD p11Expression KEYWORD
    | 'filerename' strExpression strExpression
    | 'filesearch' strExpression
    | 'fileseek' KEYWORD strExpression
    | 'fileseekback' KEYWORD
    | 'filestat' strExpression p11Expression p11Expression? p11Expression?
    | 'filestrseek' KEYWORD strExpression
    | 'filestrseek2' KEYWORD strExpression
    | 'filetruncate' strExpression p11Expression
    | 'fileunlock' KEYWORD
    | 'filewrite' KEYWORD (strExpression|p11Expression)*
    | 'filewriteln' KEYWORD (strExpression|p11Expression)*
    | 'findfirst' KEYWORD strExpression KEYWORD
    | 'findnext' KEYWORD KEYWORD
    | 'findclose' KEYWORD
    | 'foldercreate' strExpression
    | 'folderdelete' strExpression
    | 'foldersearch' strExpression
    | 'getdir' KEYWORD
    | 'getfileattr' strExpression
    | 'makepath' KEYWORD strExpression p11Expression
    | 'setdir' strExpression
    | 'setfileattr' strExpression p11Expression
    | 'delpassword' strExpression strExpression
    | 'delpassword2' strExpression strExpression
    | 'getpassword' strExpression strExpression KEYWORD
    | 'getpassword2' strExpression strExpression KEYWORD p11Expression
    | 'ispassword' strExpression strExpression
    | 'ispassword2' strExpression strExpression
    | 'passwordbox' strExpression strExpression p11Expression?
    | 'setpassword' strExpression strExpression KEYWORD
    | 'setpassword2' strExpression strExpression KEYWORD strExpression

    | 'beep' p11Expression?
    | 'bringupbox'
    | 'checksum8' KEYWORD strExpression
    | 'checksum8file' KEYWORD strExpression
    | 'checksum16' KEYWORD strExpression
    | 'checksum16file' KEYWORD strExpression
    | 'checksum32' KEYWORD strExpression
    | 'checksum32file' KEYWORD strExpression
    | 'closesbox'
    | 'clipb2var' KEYWORD p11Expression
    | 'crc16' KEYWORD strExpression
    | 'crc16file' KEYWORD strExpression
    | 'crc32' KEYWORD strExpression
    | 'crc32file' KEYWORD strExpression
    | 'exec' strExpression strExpression? p11Expression? strExpression?
    | 'dirnamebox' strExpression p11Expression?
    | 'filenamebox' strExpression p11Expression? strExpression?
    | 'getdate' KEYWORD strExpression? strExpression?
    | 'getenv' strExpression KEYWORD
    | 'getipv4addr' strExpression p11Expression
    | 'getipv6addr' strExpression p11Expression
    | 'getspecialfolder' p11Expression strExpression
    | 'gettime' KEYWORD strExpression? strExpression?
    | 'getttdir' KEYWORD
    | 'getver' KEYWORD p11Expression
    | 'ifdefined' KEYWORD
    | 'inputbox' strExpression strExpression strExpression? p11Expression?
    | 'intdim' strExpression p11Expression
    | 'listbox' strExpression strExpression KEYWORD p11Expression? strExpression*
    | 'messagebox' strExpression strExpression p11Expression?
    | 'random' KEYWORD p11Expression
    | 'rotateleft' KEYWORD p11Expression p11Expression
    | 'rotateright' KEYWORD p11Expression p11Expression
    | 'setdate' strExpression
    | 'setdlgpos' p11Expression*
    | 'setenv' strExpression strExpression
    | 'setexitcode' p11Expression
    | 'settime' strExpression
    | 'show' p11Expression
    | 'statusbox' strExpression strExpression p11Expression?
    | 'strdim' KEYWORD p11Expression
    | 'uptime' KEYWORD
    | 'var2clipb' strExpression
    | 'yesnobox' strExpression strExpression p11Expression?
    | 'dummy' (strExpression|p11Expression)*
    ;

forNext
    : 'for' KEYWORD p11Expression p11Expression RN commandline+ 'next';

whileEndwhile
    : 'while' p11Expression RN commandline+ 'endwhile';

untilEnduntil
    : 'until' p11Expression RN commandline+ 'enduntil';

doLoop
    : 'do' p11Expression? RN commandline+ 'loop' p11Expression?;

if1
    : 'if' p11Expression commandline;

if2
    : 'if' p11Expression 'then' RN commandline+ (elseif)* (else)? 'endif';

elseif:'elseif' p11Expression 'then' RN commandline+;

else: 'else' RN commandline+;

input: KEYWORD '=' (strExpression | p11Expression);

label: ':' KEYWORD ;

commandline
    : input RN
    | if2
    | if1
    | forNext RN
    | whileEndwhile RN
    | label RN
    | command RN
    | untilEnduntil RN
    | doLoop RN
    | RN
    ;

statement: commandline+ EOF;


/*  */
