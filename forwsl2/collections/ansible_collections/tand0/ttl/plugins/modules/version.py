# -*- coding: utf-8 -*-

# Copyright (c) 2025, Toshikazu Ando
# GNU General Public License v3.0+
# This file is part of Ansible
# See LICENSE to see the full text of the license

DOCUMENTATION = r'''
---
module: version
short_description: get this version
description:
  - get this version
author: Ando (@ando)

attributes:
  check_mode:
    support: full
    description: this is ignore

options:
  dummy:
    description:
      - dummy
    required: false
    default: ""
    type: str

seealso:
  - name: nextnextping
    description: nextnextping
    link: https://github.com/Tand0/nextnextping

'''

EXAMPLES = r'''
---
- version:
'''

RETURN = r'''
---
version:
  description: get the version
  type: float
  returned: always
  sample: 1.15
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.tand0.ttl.plugins.module_utils.version import VERSION


def main():
    """ main """
    module = AnsibleModule(
        argument_spec={
            'dummy': {'type': 'str', 'required': False, 'default': ""}
        },
        supports_check_mode=True
    )
    #
    result = {'version': str(VERSION)}
    #
    module.exit_json(**result)


if __name__ == '__main__':
    main()
