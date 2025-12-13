

# Ansible TTL macro like collection
## Overview
- You can connect via SSH using a language called TTL(Terawaros Tekitou Language), which is similar to teraterm macro, and ping other servers as stepping stones.

## MACRO for Terawaros Tekitou Lanugage

- Usage
    - [The macro language Terawaros Tekitou Language (TTL)](./docs/syntax.md)　
    - [TTL command reference](./docs/command.md)

## module
ttl
## short_description
TTL macro-like module
## description
- This implementation imitates the TTL used in teraterm.
- Ansible allows you to control the macro language "TTL"
- realize functions such as auto-dial and auto-login.

## author
Ando (@ando)
## attributes
- **check_mode**: 
    - **support**: full
    - **description**: 
        - Can run in check_mode and return changed status prediction without modifying target.
        - If not supported, the action will be skipped.

## options
- **filename**: 
    - **description**: 
        - TTL macro file name
    - **required**: False
    - **default**: None
    - **type**: path
- **cmd**: 
    - **description**: 
        - TTL macro text
    - **required**: False
    - **type**: str
    - **default**: None
- **creates**: 
    - **type**: path
    - **description**: 
        - A filename, when it already exists, this step will B(not) be run.
- **removes**: 
    - **type**: path
    - **description**: 
        - A filename, when it does not exist, this step will B(not) be run.
- **ignore_result**: 
    - **description**: 
        - If result is 0, it fails.
    - **required**: False
    - **type**: bool
    - **default**: True
- **param**: 
    - **description**: 
        - Specify the parameters
    - **required**: False
    - **type**: list
    - **elements**: str
    - **default**: 
- **chdir**: 
    - **description**: 
        - Change into this directory before running the command.
    - **required**: False
    - **type**: path

## seealso
- **name**: nextnextping
- **description**: nextnextping
- **link**: https://github.com/Tand0/nextnextping


# Examples
``` yaml
# call ttl from file
---
- name: ../test/0000_ok_test.ttl
  ttl:
    filename: 0000_ok_test.ttl
    chdir: ../test
    ignore_result: false
  register: ttl_output
- debug:
    var: ttl_output.stdout_lines


# call ttl from command
- name: "test: connect /cmd"
  ttl:
    cmd: |
      connect '/cmd'
      ;
      flushrecv
      sendln 'pwd'
      wait 'pwd'
      wait '$'
      ;
      flushrecv
      sendln 'ls'
      wait 'ls'
      wait '$'
  register: ttl_output
- name: "test: connect /cmd"
  debug:
    var: ttl_output.stdout_lines
```


# Result

## changed
- **description**: If TTL is enforced, it will be true.
- **type**: bool
- **returned**: always
- **sample**: True

## cmd
- **description**: 
    - TTL macro text
- **type**: str
- **returned**: always
- **sample**: return = 1

## filename
- **description**: 
    - TTL macro file name
- **type**: str
- **returned**: always
- **sample**: sample.ttl

## stdout
- **description**: stdout
- **type**: str
- **returned**: always
- **sample**: 

## stdout_lines
- **description**: stdout lines
- **type**: list
- **returned**: always
- **sample**: 

## values
- **description**: This is a parameter for the TTL macro.
- **type**: dict
- **returned**: always
- **sample**: 
    - **result**: 1
