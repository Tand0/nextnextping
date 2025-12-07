# -*- coding: utf-8 -*-

# Copyright (c) 2025, Toshikazu Ando
# GNU General Public License v3.0+
# This file is part of Ansible
# See LICENSE to see the full text of the license

DOCUMENTATION = r'''
---
module: ttl
short_description: TTL macro-like module
description:
  - This implementation imitates the TTL used in teraterm.
  - Ansible allows you to control the macro language "TTL"
     - realize functions such as auto-dial and auto-login.
author: Ando (@ando)

attributes:
  check_mode:
    support: full
    description:
      - Can run in check_mode and return changed status
        prediction without modifying target.
      - If not supported, the action will be skipped.

options:
  filename:
    description:
      - TTL macro file name
    required: false
    default:
    type: str
  cmd:
    description:
      - TTL macro text
    required: false
    type: str
    default:
  ignore_result:
    description:
      - If result is 0, it fails.
    required: false
    type: bool
    default: true
  param:
    description:
      - Specify the parameters
    required: false
    type: list
    elements: str
  chdir:
    description:
      - Specify the folder in which the TTL macro will be executed..
    required: false
    type: str

seealso:
  - name: nextnextping
    description: nextnextping
    link: https://github.com/Tand0/nextnextping

'''

EXAMPLES = r'''
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
'''

RETURN = r'''
---
changed:
  description: If TTL is enforced, it will be true.
  type: bool
  returned: always
  sample: true

stdout:
  description: stdout
  type: str
  returned: always
  sample: ""

stdout_lines:
  description: stdout lines
  type: list
  returned: always
  sample: []

values:
  description: This is a parameter for the TTL macro.
  type: dict
  returned: always
  sample: {"result": 1}
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.tand0.ttl.plugins.module_utils.TtlParserWorker import TtlPaserWolker
from ansible_collections.tand0.ttl.plugins.module_utils.TtlParserWorker import Label
import os


def main():
    """ main """
    module = AnsibleModule(
        argument_spec=dict(
            filename=dict(type=str, required=False, default=None),
            cmd=dict(type='str', required=False, default=None),
            ignore_result=dict(type='bool', required=False, default=True),
            param=dict(type=list, required=False, default=[], elements="str"),
            chdir=dict(type='str', required=False, default=None)
        ),
        supports_check_mode=True
    )
    #
    current_directory = os.getcwd()
    chdir = module.params['chdir']
    checkmode = module.check_mode
    changed = not checkmode
    ignore_result = module.params['ignore_result']
    result = {'stdout': '', 'stdout_lines': [], 'value': {}}
    filename = module.params['filename']
    #
    #
    if filename is None and module.params['cmd'] is None:
        module.fail_json(msg='Either the cmd or filename parameter must be given.', **result)
    #
    param_list = []
    if filename is None:
        param_list.append('none.ttl')
    else:
        param_list.append(filename)
    for param_list_list in module.params['param']:
        param_list.append(param_list_list.strip())
    try:
        if chdir is not None:
            os.chdir(chdir)
        myTtlPaserWolker = MyTtlPaserWolker(module)
        if module.params['cmd'] is not None:
            data = module.params['cmd'] + "\n"
            if not checkmode:
                # this is not check mode
                myTtlPaserWolker.execute('cmd', param_list, data=data)
            else:
                # this is check mode
                myTtlPaserWolker.include_only('cmd', data=data)
        if module.params['filename'] is not None:
            if not checkmode:
                # this is not check mode
                myTtlPaserWolker.execute(module.params['filename'], param_list)
            else:
                # this is check mode
                myTtlPaserWolker.include_only(module.params['filename'])
        if not ignore_result and not checkmode:
            ignore_result_value = myTtlPaserWolker.getValue('result', error_stop=False)
            if result is None:
                ignore_result_value = 0
            if ignore_result_value == 0:
                module.fail_json(msg=f"result_check failer v={str(ignore_result_value)}", **result)
    except Exception as e:
        module.fail_json(msg=f"Exception execute {str(e)}", **result)
    finally:
        os.chdir(current_directory)
        if myTtlPaserWolker is not None:
            result['stdout'] = myTtlPaserWolker.my_stdout
            result['stdout_lines'] = result['stdout'].splitlines()
            result['value'] = replace_param(myTtlPaserWolker.value_list)
            myTtlPaserWolker.stop()
    #
    module.exit_json(changed=changed, **result)


def replace_param(data):
    result = None
    if isinstance(data, dict):
        result = {}
        for k, v in data.items():
            result[k] = replace_param(v)
    elif isinstance(data, list) or isinstance(data, tuple):
        result = []
        for v in data:
            result.append(replace_param(v))
    elif isinstance(data, Label):
        result = str(data)
    else:
        result = data
    return result


class MyTtlPaserWolker(TtlPaserWolker):
    """ my TtlPaserWolker  """
    def __init__(self, my_module: AnsibleModule):
        self.my_stdout = ""
        self.my_changed = False
        self.my_module = my_module
        super().__init__()

    def setLog(self, strvar):
        """ log setting """
        self.my_stdout = self.my_stdout + strvar
        self.my_module.log(str(strvar))


if __name__ == '__main__':
    main()
