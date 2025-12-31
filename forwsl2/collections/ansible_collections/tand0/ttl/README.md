# Ansible Collection - tand0.ttl

## Overview

- You can connect via SSH using a language called TTL(Terawaros Tekitou Language), which is similar to teraterm macro, and ping other servers as stepping stones.

### MACRO for Terawaros Tekitou Lanugage

- Usage
    - [The macro language Terawaros Tekitou Language (TTL)](./docs/syntax.md)
    - [TTL command reference](./docs/command.md)

## Modules

- **module**: [tand0.ttl.ttl](docs/ttl.md)

## Basic Data

### galaxy.yml

- **namespace**: tand0
- **name**: ttl
- **version**: 1.29.1
- **readme**: README.md
- **authors**:
    - Toshikazu Ando
- **description**: TTL macro-like collection
- **license**:
    - MIT
    - GPL-3.0-or-later
- **license_file**: ""
- **tags**: []
- **dependencies**:
- **repository**: <https://github.com/Tand0/nextnextping.git>
- **documentation**: <https://github.com/Tand0/nextnextping/README.md>
- **homepage**: <https://github.com/Tand0/nextnextping>
- **issues**: <https://github.com/Tand0/nextnextping/issues>
- **build_ignore**: []

### requirements.txt

- paramiko
- antlr4-python3-runtime
- uptime
- pexpect
- cryptography
- pyserial

### runtime.yml

- **requires_ansible**: >=2.9.10
