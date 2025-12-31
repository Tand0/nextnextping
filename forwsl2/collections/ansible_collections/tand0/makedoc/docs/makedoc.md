# Ansible TTL macro-like module

## module

makedoc
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

- **src**:
    - **description**:
        - sorce file
    - **required**: True
    - **type**: path
- **dest**:
    - **description**:
        - sorce file
    - **required**: False
    - **type**: path
- **css_file_list**:
    - **description**:
        - If dest is html, add to css file name
    - **required**: False
    - **type**: list
    - **elements**: str
- **extensions**:
    - **description**:
        - If dest is html, add to python makedown package
    - **required**: False
    - **type**: list
    - **elements**: str
- **replace_list**:
    - **description**:
        - If dest is html, replace html
    - **required**: False
    - **type**: list
    - **elements**: dict
    - **suboptions**:
        - **before**:
            - **description**:
                - replace before text
            - **type**: str
        - **after**:
            - **description**:
                - replace after text
            - **type**: str
- **overview**:
    - **description**:
        - If .py or galaxy.yml, add overview
    - **required**: False
    - **type**: str
    - **default**: ""
## seealso

- **name**: nextnextping
- **description**: nextnextping
- **link**: <https://github.com/Tand0/nextnextping>

## Examples

``` yaml
- hosts: localhost
  become: False
  vars:
  tasks:
    - name: "create from md file to html folder"
      tand0.makedoc.makedoc:
        src: "{{ item.src }}"
        dest: "{{ item.dest }}"
        css_file_list: ["codehilite.css", "language_html.css"]
        extensions: ["tables", "fenced_code", "attr_list", "codehilite"]
        replace_list:
          - before: 'src="./docs/([^"]+)'
            after: 'src="\1'
          - before: 'href="./docs/([^"]+)'
            after: 'href="\1"'
          - before: 'href="([^"]+)\.md'
            after: 'href="\1.html'
      loop:
        - src: ../README.md
          dest: ../nextnextping/dist/nextnextping/_internal/

    - name: "create from md file to md file"
      tand0.makedoc.makedoc:
        src: "{{ item.src }}"
        dest: "{{ item.dest }}"
      loop:
        - src: ../docs/syntax.md
          dest: collections/ansible_collections/tand0/ttl/docs/syntax.md
        - src: ../docs/command.md
          dest: collections/ansible_collections/tand0/ttl/docs/command.md

    - name: "create from folder to html folder"
      tand0.makedoc.makedoc:
        src: "{{ item.src }}"
        dest: "{{ item.dest }}"
        css_file_list: ["codehilite.css", "language_html.css"]
        extensions: ["tables", "fenced_code", "attr_list", "codehilite"]
        replace_list:
          - before: 'href="([^"]+)\.md'
            after: 'href="\1.html'
      loop:
        - src: ../docs/
          dest: ../nextnextping/dist/nextnextping/_internal/

    - name: "create from galaxy.yml to README.md"
      tand0.makedoc.makedoc:
        src: "{{ item.src }}"
        overview: |
          ## Overview

          - You can connect via SSH using a language called TTL(Terawaros Tekitou Language),]
            which is similar to teraterm macro, and ping other servers as stepping stones.

          ### MACRO for Terawaros Tekitou Lanugage

          - Usage
              - [The macro language Terawaros Tekitou Language (TTL)](./docs/syntax.md)
              - [TTL command reference](./docs/command.md)
      loop:
        - src: collections/ansible_collections/tand0/ttl/galaxy.yml

    - name: "create from galaxy.yml to README.md"
      tand0.makedoc.makedoc:
        src: "{{ item.src }}"
      loop:
        - src: collections/ansible_collections/tand0/makedoc/galaxy.yml
```

## Result

- **changed**:
    - **description**: If file is changed, it will be true.
    - **type**: bool
    - **returned**: always
    - **sample**: True
- **src**:
    - **description**:
        - Source file
    - **type**: str
    - **returned**: always
    - **sample**: makedoc.py
- **dest**:
    - **description**:
        - Dest file
    - **type**: bool
    - **returned**: always
    - **sample**: makedoc.md
