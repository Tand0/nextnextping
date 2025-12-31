# -*- coding: utf-8 -*-

# Copyright (c) 2025, Toshikazu Ando
# GNU General Public License v3.0+
# This file is part of Ansible
# See LICENSE to see the full text of the license

DOCUMENTATION = r'''
---
module: makedoc
short_description: TTL macro-like module
description:
  - This implementation imitates the TTL used in teraterm.
  - Ansible allows you to control the macro language "TTL"
  - realize functions such as auto-dial and auto-login.
author: Ando (@tando)

attributes:
  check_mode:
    support: full
    description:
      - Can run in check_mode and return changed status
        prediction without modifying target.

options:
  src:
    description:
      - sorce file
    required: true
    type: path
  dest:
    description:
      - sorce file
    required: false
    type: path
  css_file_list:
    description:
      - If dest is html, add to css file name
    required: false
    type: list
    elements: str
  extensions:
    description:
      - If dest is html, add to python makedown package
    required: false
    type: list
    elements: str
  replace_list:
    description:
      - If dest is html, replace html
    required: false
    type: list
    elements: dict
    suboptions:
      before:
        description:
          - replace before text
        type: str
      after:
        description:
          - replace after text
        type: str
  overview:
    description:
      - If .py or galaxy.yml, add overview
    required: false
    type: str
    default: ''

seealso:
  - name: nextnextping
    description: nextnextping
    link: https://github.com/Tand0/nextnextping

'''

EXAMPLES = r'''
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
'''

RETURN = r'''
---
changed:
  description: If file is changed, it will be true.
  type: bool
  returned: always
  sample: true

src:
  description:
    - Source file
  type: str
  returned: always
  sample: makedoc.py

dest:
  description:
    - Dest file
  type: bool
  returned: always
  sample: makedoc.md
'''


from ansible.module_utils.basic import AnsibleModule
try:
    from ansible_collections.tand0.makedoc.plugins.module_utils.site_build import makedoc_filename
except (ImportError, ModuleNotFoundError, NameError):
    # def makedoc_filename():
    pass


def main():
    """ main """
    module = AnsibleModule(
        argument_spec=dict(
            src=dict(type='path', required=True),
            dest=dict(type='path', required=False),
            css_file_list=dict(type='list', required=False, default=None, elements='str'),
            extensions=dict(type='list', required=False, default=None, elements='str'),
            replace_list=dict(
                type='list',
                required=False,
                default=None,
                elements='dict',
                options=dict(
                    before=dict(type='str', required=False),
                    after=dict(type='str', required=False))
            ),
            overview=dict(type='str', required=False, default="")
        ),
        supports_check_mode=True
    )
    #
    check_mode = module.check_mode
    src = module.params['src']
    dest = module.params['dest']
    css_file_list = module.params['css_file_list']
    extensions = module.params['extensions']
    replace_list = module.params['replace_list']
    overview = module.params['overview']

    result = {'src': src, 'dest': dest}
    #
    #
    changed = True
    try:
        #
        changed = makedoc_filename(
            src,
            dest,
            check_mode,
            css_file_list,
            extensions,
            replace_list,
            overview
        )
        #
    except Exception as e:
        module.fail_json(msg=f"Exception execute {str(e)}", **result)
    #
    module.exit_json(changed=changed, skipped=False, **result)


if __name__ == '__main__':
    main()
