# -*- coding: utf-8 -*-
import subprocess
import os
import time
import sys
import threading

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../test")))
from ttlbackground import TtlLoaderBase


def main():
    current = os.getcwd()
    print(f'current folder={current}')
    #
    os.chdir('..')
    main_run('cmd.exe /C python mybuild.py')
    main_run('cmd.exe /C pytest -s')
    #
    main_sub()
    #
    check_mode = False
    changed = site_import('test/', 'forwsl2/site_import.yml', check_mode)
    print(f'changed={changed}')
    #
    #
    os.chdir(current)
    print(f'current folder={current}')
    #
    main_run('ansible-playbook site.yml')


def main_run(command: str):
    command = command.split()
    subprocess.run(command, check=True)


def main_sub():
    loader = MyLoaderSingle()
    th = threading.Thread(target=loader.start, daemon=True)
    th.start()


class MyLoaderSingle(TtlLoaderBase):
    def __init__(self):
        super().__init__()

    def start_main(self, files=None):
        while True:
            time.sleep(1000)


def site_import(src: str, site_import: str, check_mode: bool) -> bool:
    files = []
    for file in os.listdir(src):
        if '.ttl' not in file:
            continue
        if 'base.ttl' in file:
            continue
        files.append(file)
    text = ''
    j = 0
    for file in files:
        for i in [0, 1, 2, 3]:
            j = j + 1
            ok_flag = True
            if '_ok_' in file:
                ok_flag = True
            else:
                ok_flag = False
            text = text + f'- name: test-{j} {file}\n'
            text = text + '  tand0.ttl.ttl:\n'
            if i == 0 or i == 2:
                text = text + '    filename: ' + file + '\n'
            else:
                text = text + '    cmd: |\n'
                text = text + print_cmd(src, '      ', file)
            text = text + '    chdir: ../test\n'
            text = text + '    ignore_result: False\n'
            text = text + f'  check_mode: {2 <= i}\n'
            text = text + '  register: ttl_output\n'
            text = text + '  ignore_errors: ' + str(not ok_flag) + '\n'
            if i < 2:
                text = text + f'- name: assert-failed-{j} {str(ok_flag)} {file}\n'
                text = text + '  fail:\n'
                text = text + '  when: (not ansible_check_mode) and (ttl_output.failed == ' + str(ok_flag) + ')\n'
            else:
                if ok_flag:
                    text = text + f'- name: assert-changed-{j} {str(ok_flag)} {file}\n'
                    text = text + '  fail:\n'
                    text = text + '  when: ttl_output.changed == True\n'
            if ok_flag:
                text = text + f'- name: debug-stdout {file}\n'
                text = text + '  debug:\n'
                text = text + '     var: ttl_output.stdout_lines\n\n'
    # print(f'{text}', end='')
    return file_save(site_import, text, check_mode)


def print_cmd(src: str, base: str, file: str) -> str:
    src = os.path.join(src, file)
    with open(src, 'r', encoding='utf-8') as f:
        md_text = f.read()
    buffer = ''
    for text in md_text.splitlines():
        if text.strip() == '':
            continue
        buffer = buffer + base + text.strip() + '\n'
    return buffer


def file_save(filename: str, text: str, check_mode: bool):
    # print(f'target={filename}')
    dest_text = ''
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            dest_text = f.read()
    except IOError:
        dest_text = ''
    #
    changed = dest_text != text
    if check_mode:
        # チェックモードなら書き込みを行わない
        return changed
    #
    if changed:
        with open(filename, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
    return changed


if __name__ == "__main__":
    #
    main()
#
