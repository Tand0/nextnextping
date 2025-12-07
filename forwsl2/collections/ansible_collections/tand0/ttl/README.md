

# Ansible TTL macro like collection
## Overview
- You can ping and see if the result is OK or not.
- You can connect via SSH using a language called Terawaros Tekitou Language, which is similar to teraterm macro, and ping other servers as stepping stones.

## MACRO for Terawaros Tekitou Lanugage

- Usage
    - [the macro language Terawaros Tekitou Language (TTL)](./docs/syntax.md)　
    - [TTL command reference](./docs/command.md)

## module

ttl
## short_description

TTL macro-like module
## description


 - : This implementation imitates the TTL used in teraterm.
 - : Ansible allows you to control the macro language "TTL" - realize functions such as auto-dial and auto-login.
## author

Ando (@ando)
## attributes


- check_mode: 

    - support: full
    - description: 

         - : Can run in check_mode and return changed status prediction without modifying target.
         - : If not supported, the action will be skipped.
## options


- filename: 

    - description: 

         - : TTL macro file name
    - required: False
    - default: None
    - type: str
- cmd: 

    - description: 

         - : TTL macro text
    - required: False
    - type: str
    - default: None
- ignore_result: 

    - description: 

         - : If result is 0, it fails.
    - required: False
    - type: bool
    - default: True
- param: 

    - description: 

         - : Specify the parameters
    - required: False
    - type: list
    - elements: str
- chdir: 

    - description: 

         - : Specify the folder in which the TTL macro will be executed..
    - required: False
    - type: str
## seealso


 - :

    - name: nextnextping
    - description: nextnextping
    - link: https://github.com/Tand0/nextnextping

# Examples
``` yaml

---
- name: ../test/0000_ok_test.ttl
  ttl:
    filename: 0000_ok_test.ttl
    chdir: ../test
    result_check: true
  register: ttl_output
- debug:
    msg: "{{ ttl_output.stdout_lines }}"

- name: assert OK
  ttl:
    cmd: |
      result = 1
  register: ttl_output
- debug:
  msg: "{{ ttl_output }}"

```


# Result

## changed


- description: If TTL is enforced, it will be true.
- type: bool
- returned: always
- sample: True
## stdout


- description: stdout
- type: str
- returned: always
- sample: 
## stdout_lines


- description: stdout lines
- type: list
- returned: always
- sample: 

## values


- description: This is a parameter for the TTL macro.
- type: dict
- returned: always
- sample: 

    - result: 1
</body>
</html>
