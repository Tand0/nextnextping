# Ansible TTL macro-like module

## module

ttl
## short_description

TTL macro-like module
## description

- This implementation imitates the TTL used in teraterm.
- Ansible allows you to control the macro language "TTL"
- realize functions such as auto-dial and auto-login.
## author

Ando (@tando)
## attributes

- **check_mode**:
    - **support**: full
    - **description**:
        - Can run in check_mode and return changed status prediction without modifying target.
## options

- **filename**:
    - **description**:
        - TTL macro file name
    - **required**: False
    - **type**: path
- **cmd**:
    - **description**:
        - TTL macro text
    - **required**: False
    - **type**: str
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
    - **default**: []
- **chdir**:
    - **description**:
        - Change into this directory before running the command.
    - **required**: False
    - **type**: path
## seealso

- **name**: nextnextping
- **description**: nextnextping
- **link**: <https://github.com/Tand0/nextnextping>

## Examples

``` yaml
# call ttl from file
---
- name: ../test/0000_ok_test.ttl
  tand0.ttl.ttl:
    filename: 0000_ok_test.ttl
    chdir: ../test
    ignore_result: false
  register: ttl_output
- debug:
    var: ttl_output.stdout_lines


# call ttl from command
- name: "test: connect /cmd"
  tand0.ttl.ttl:
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

## Result

- **changed**:
    - **description**: If TTL is enforced, it will be true.
    - **type**: bool
    - **returned**: always
    - **sample**: True
- **cmd**:
    - **description**:
        - TTL macro text
    - **type**: str
    - **returned**: always
    - **sample**: return = 1
- **ignore_result**:
    - **description**:
        - If result is 0, it fails.
    - **type**: bool
    - **returned**: always
    - **sample**: True
- **filename**:
    - **description**:
        - TTL macro file name
    - **type**: str
    - **returned**: always
    - **sample**: sample.ttl
- **stdout**:
    - **description**: stdout
    - **type**: str
    - **returned**: always
    - **sample**: ""
- **stdout_lines**:
    - **description**: stdout lines
    - **type**: list
    - **returned**: always
    - **sample**: []
- **values**:
    - **description**: This is a parameter for the TTL macro.
    - **type**: dict
    - **returned**: always
    - **sample**:
        - **result**: 1
- **start**:
    - **description**: The command execution start time.
    - **returned**: always
    - **type**: str
    - **sample**: 2016-02-25 09:18:26.429568
- **end**:
    - **description**: The command execution end time.
    - **returned**: always
    - **type**: str
    - **sample**: 2016-02-25 09:18:26.755339
- **delta**:
    - **description**: The command execution delta time.
    - **returned**: always
    - **type**: str
    - **sample**: 0:00:00.325771
- **version**:
    - **description**: This version
    - **returned**: always
    - **type**: str
    - **sample**: 1.29.1
