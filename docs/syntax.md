
# The MACRO Language Terawaros Tekitou Language (TTL)

- [The MACRO Language Terawaros Tekitou Language (TTL)](#the-macro-language-terawaros-tekitou-language-ttl)
    - [Encoding](#encoding)
    - [Data Types](#data-types)
    - [Formats of constants](#formats-of-constants)
        - [Integer-type constants](#integer-type-constants)
        - [String-type constants](#string-type-constants)
        - [Integer Array](#integer-array)
        - [String Array](#string-array)
    - [Variables](#variables)
    - [System variables](#system-variables)
        - [User variables](#user-variables)
        - [Label](#label)
        - [Expressions and operators](#expressions-and-operators)
    - [Line formats](#line-formats)
        - [Line breaks](#line-breaks)
        - [White space](#white-space)
        - [Command line](#command-line)
        - [Assignment line](#assignment-line)
        - [Label line](#label-line)
        - [if, then, elseif, else, endif](#if-then-elseif-else-endif)
            - [if: Format 1](#if-format-1)
            - [if: Format 2](#if-format-2)
        - [for, next](#for-next)
        - [while, endwhile](#while-endwhile)
        - [until](#until)
        - [do](#do)
        - [break](#break)
        - [continue](#continue)
        - [call](#call)
        - [end, exit](#end-exit)
        - [include](#include)
        - [exit](#exit)

## Encoding

- Only UTF-8 is supported.

## Data Types

- Integer: The specification is based on Python `int`.
- Integer: The specification is based on Python `str`.
- Integer Array: Internally, it is treated as a `int` like `a[XXX]`, where `XXX` is a number in the range `[0-9]+`.
- String Array: Internally, it is treated as a `string` like `a[XXX]`, where `XXX` is a number in the range `[0-9]+`.

## Formats of constants

### Integer-type constants

A integer-type constant is expressed as a decimal number or a hexadecimal number which begins with a "$" character. Floating point operation is not supported.

```text
Example:
    123
    -11
    $3a
    $10F
```

### String-type constants

   There are two ways of expressing a string-type constant.

- a) A character string quoted by ' or " (both sides must be same).

```text
Example:
    'Hello, world'
    "I can't do that"
    "漢字も可能"
```

- b) A single character expressed as a "#" followed by an ASCII code (decimal or hexadecimal number). Note: Strings can not contain NUL (ASCII code 0) characters.

```text
Example:
    #65     The character "A".
    #$41    The character "A".
    #13     The CR character.
```

- Format a) and b) can be combined in one expression.

```text
Example:
    'cat readme.txt'#13#10
    'abc'#$0d#$0a'def'#$0d#$0a'ghi'
```

- In Antlr it would look like following:

```text
STRING1: ('\'' ~[']* '\'' | '"' ~["]* '"' | '#' '$'? [a-fA-F0-9]+)+;
strContext: STRING1;
```

### Integer Array

- The string up to `a[0]` is converted and treated as a variable type.

```text
a[0] = 1
a[1] = 2
```

- `a[b]` is converted to `a[0]`, stringified, and treated as a variable type

```text
b = 0
a[b] = 1
```

### String Array

```text
b = 0
a[b] = "aaa"
```

## Variables

## System variables

- result
    - If the result is not 0 after execution, the execution is considered successful.
- param0, param1 ... param9
- param[0], param[1] ... param9
- inputstr, matchstr, groupmatchstr1 ... groupmatchstr9, paramcnt, timeout, mtimeout
- error

### User variables

- In Antlr it would look like following:

```text
KEYWORD: [_a-zA-Z][_a-zA-Z0-9]*;
keyword: KEYWORD (LEFT_KAKKO (intExpression| strExpression) RIGHT_KAKKO)?;
LEFT_KAKKO: '[';
RIGHT_KAKKO: ']';
```

### Label

- In Antlr it would look like following:

```text
label: ':' KEYWORD ;
```

### Expressions and operators

- Most of the four arithmetic operations can be used.
- Arithmetic operations are performed using the int type. Arithmetic operations cannot be performed using the str type.

```text
Example:
    1 + 1
    4 - 2 * 3      ; resut = -2
    15 % 10        ; result = 5
    3 * (A + 2)    ; A is user variable
    A and not B
    A <= B         ; if true = 1, false = 0
```

## Line formats

- There are four kinds of line formats for macro files. Any line can contain a comment which begins with a ";" character
- Comments give no effect on the execution of MACRO.

### Line breaks

- In Antlr it would look like following:

```text
RN: '\r'? '\n'
    | ';' ~[\n]* '\n'
    ;
```

### White space

- In Antlr it would look like following:

```text
WS1 : [ \t]+ -> skip ;
WS2 : '/*' ~[/]* '*/' -> skip ;
```

### Command line

- Lines containing a single command with parameters.

```text
Format:
    <command> <parameter> ...

Example:
    connect 'myhost'
    wait 'OK' 'ERROR'
    if result=2 goto error
    sendln 'cat'
    pause A*10
    end
```

### Assignment line

Lines which contain an assignment statement.

```text
Format:
    <Variable> = <Value (constant, variable, expression)>

Example:
    A = 33
    B = C            C must already have a value.
    VAL = I*(I+1)
    A=B=C            The value of B=C (0 for false, 1 for true) is assigned to A.
    Error=0<J
    Username='MYNAME'
```

- In Antlr it would look like following:

```text
input: KEYWORD '=' p11Expression ;
```

### Label line

Lines which begin with a ':' character followed by a label identifier.

```text
Format:
    :<Label>

Example:
    :dial
```

- In Antlr it would look like following:

```text
label: ':' KEYWORD ;
```

### if, then, elseif, else, endif

Conditional branching

#### if: Format 1

```text
if result A=0
```

- In Antlr it would look like following:

```text
if1
    : 'if' p11Expression line;
```

#### if: Format 2

```text
if <expression 1> then
  ...
  (Statements for the case:  <expression 1> is true (non-zero).)
  ...
[elseif <expression 2> then]
  ...
  (Statements for the case:  <expression 1> is false (zero) and <expression 2> is true.)
  ...
[elseif <expression N> then]
  ...
  (Statements for the case:  <expression 1>, <expression 2>,... and <expression N-1> are all false, and <expression N> is true.)
  ...
[else]
  ...
  (Statements for the case:  all the conditions above are false (zero).)
  ...
endif
```

- In Antlr it would look like following:

```text
if2
    : 'if' p11Expression 'then' RN line+ (elseif)* (else)? 'endif';

elseif:'elseif' p11Expression 'then' RN line+;

else: 'else' RN line+;
```

### for, next

- Repeats

```text
for <intvar> <first> <last>

  ...

  ...

next
```

- The commands between `for` and `next` are repeated until the value of the integer variable `intvar` is equal to `last`.
- The initial value of `intvar` is `first`.
- If `last` is greater than `first`, `intvar` is incremented by 1 each time the `next` line is reached.
- If `last` is less than `fast`, `intvar` is decremented by 1 each time the "next" line is reached.

```text
for i 1 10
  sendln 'abc'
next

for i 5 1
  sendln 'abc'
next
```

- In Antlr it would look like following:

```text
forNext
    : 'for' keyword p11Expression p11Expression RN commandline+ 'next';
```

### while, endwhile

- Repeats

```text
i = 10
while i>0
  i = i - 1
endwhile
```

- In Antlr it would look like following:

```text
whileEndwhile
    : 'while' p11Expression RN line+ 'endwhile';
```

### until

- Repeats.
- In Antlr it would look like following:

```text
untilEnduntil
    : 'until' p11Expression RN commandline+ 'enduntil';
```

### do

- Repeats.
- In Antlr it would look like following:

```text
doLoop
    : 'do' p11Expression? RN commandline+ 'loop' p11Expression?;
```

### break

- Quit from "for" and "while" loop.

### continue

- Continue from "for" and "while" loop.

### call

- Calls a subroutine.
- Use `return` to return.

```text
messagebox "I'm in main." "test"
;
call sub
messagebox "Now I'm in main" "test"
end

;
:sub
messagebox "Now I'm in sub" "test"
; Back to the mail
return
```

### end, exit

- Quit from ttl.

### include

- Include a file.

### exit

- Quit from "include".
