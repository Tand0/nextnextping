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
    type: path
  cmd:
    description:
      - TTL macro text
    required: false
    type: str
    default:
  creates:
    type: path
    description:
      - A filename, when it already exists, this step will B(not) be run.
  removes:
    type: path
    description:
      - A filename, when it does not exist, this step will B(not) be run.
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
    default: []
  chdir:
    description:
      - Change into this directory before running the command.
    required: false
    type: path

seealso:
  - name: nextnextping
    description: nextnextping
    link: https://github.com/Tand0/nextnextping

'''

EXAMPLES = r'''
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

'''

RETURN = r'''
---
changed:
  description: If TTL is enforced, it will be true.
  type: bool
  returned: always
  sample: true

cmd:
  description:
    -  TTL macro text
  type: str
  returned: always
  sample: return = 1

filename:
  description:
    - TTL macro file name
  type: str
  returned: always
  sample: sample.ttl

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

import datetime
from ansible.module_utils.basic import AnsibleModule
IMP_ERR = None
try:
    from ansible_collections.tand0.ttl.plugins.module_utils.ttl_parser_worker import TtlPaserWolker
    from ansible_collections.tand0.ttl.plugins.module_utils.ttl_parser_worker import Label
except (ImportError, ModuleNotFoundError, NameError) as ex:
    class TtlPaserWolker():
        pass
    IMP_ERR = ex
import os


def main():
    """ main """
    module = AnsibleModule(
        argument_spec=dict(
            filename=dict(type='path', required=False, default=None),
            cmd=dict(type='str', required=False, default=None),
            creates=dict(type='path', required=False, default=None),
            removes=dict(type='path', required=False, default=None),
            ignore_result=dict(type='bool', required=False, default=True),
            param=dict(type='list', required=False, default=[], elements='str'),
            chdir=dict(type='path', required=False, default=None)
        ),
        supports_check_mode=True
    )
    #
    if IMP_ERR is not None:
        module.fail_json(msg="missing_required_lib", exception=IMP_ERR)
    #
    current_directory = os.getcwd()
    chdir = module.params['chdir']
    checkmode = module.check_mode
    changed = not checkmode
    ignore_result = module.params['ignore_result']
    filename = module.params['filename']
    cmd = module.params['cmd']
    result = {
        'stdout': '',
        'filename': filename,
        'cmd': cmd,
        'stdout_lines': [],
        'value': {}}
    creates = module.params['creates']
    removes = module.params['removes']
    #
    #
    if filename is None and cmd is None:
        module.fail_json(msg='Either the cmd or filename parameter must be given.', **result)
    #
    if creates:
        if os.path.exists(creates):
            module.exit_json(
                cmd=cmd,
                stdout="skipped, since %s exists" % creates,
                changed=False,
                rc=0
            )

    if removes:
        if not os.path.exists(removes):
            module.exit_json(
                cmd=cmd,
                stdout="skipped, since %s does not exist" % removes,
                changed=False,
                rc=0
            )
    #
    result['start'] = datetime.datetime.now()
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
        if cmd is not None:
            data = cmd + "\n"
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
                module.fail_json(msg=f"ignore_result failer v={str(ignore_result_value)}", **result)
    except Exception as e:
        module.fail_json(msg=f"Exception execute {str(e)}", **result)
    finally:
        os.chdir(current_directory)
        if myTtlPaserWolker is not None:
            result['end'] = datetime.datetime.now()
            result['delta'] = str(result['end'] - result['start'])
            result['start'] = str(result['start'])
            result['end'] = str(result['end'])
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
