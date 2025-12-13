# -*- coding: utf-8 -*-
import os
import subprocess
import shutil
import re
import yaml


VERSION = 1.21

INTERNAL = "nextnextping/dist/nextnextping/_internal/"
ANSIBLE_README = "forwsl2/collections/ansible_collections/tand0/ttl/README.md"
ANSIBLE_TARGET = "forwsl2/collections/ansible_collections/tand0/ttl/plugins/modules/ttl.py"
SITE_IMPORT = "forwsl2/site_import.yml"

RESULT_MD_TEXT = """
<html>
<head>
  <meta charset="UTF-8">
  <style type="text/css">
code{
  color: #000;
  background-color:#F6F6CB;
  font-family: Courier, monosce;
  font-size: 13px;
}
pre{
  border-top:#FFCC66 1px solid;
  border-bottom:#888899 1px solid;
  border-left:#FFCC66 1px solid;
  border-right:#888899 1px solid;
  background-color:#F6F6CB;
  padding: 0.5em 0.8em;
  color: #000;
 *width: 100%;
 _width: 100%;
  overflow: auto;
}
h1 {
  padding: 4px 4px 4px 6px;
  border: 1px solid #999;
  color: #000;
  background-color: #ddd;
  font-weight:900;
  font-size: xx-large;
}
h2 {
  padding: 4px 4px 4px 6px;
  border: 1px solid #999;
  color: #900;
  background-color: #eee;
  font-weight:800;
  font-size: x-large;
}
h3 {
  padding: 4px 4px 4px 6px;
  border: 1px solid #aaa;
  color: #900;
  background-color: #eee;
  font-weight: normal;
  font-size: large;
}
h4 {
  padding: 4px 4px 4px 6px;
  border: 1px solid #bbb;
  color: #900;
  background-color: #fff;
  font-weight: normal;
  font-size: large;
}
h5 {
  padding: 4px 4px 4px 6px;
  color: #900;
  font-size: normal;
}
#navcolumn h5 {
  font-size: smaller;
  border-bottom: 1px solid #aaaaaa;
  padding-top: 2px;
  color: #000;
}
  </style>
</head>
<body>
"""

RESULT_MD_TEXT_END = """
</body>
</html>
"""


def main():
    """ main """
    print("hello build version {str(VERSION)}")
    installer()
    sample_dir_copy("bin/", 'nextnextping/dist/nextnextping/')
    file_copy("docs/syntax.md", 'forwsl2/collections/ansible_collections/tand0/ttl/docs/syntax.md')
    file_copy("docs/command.md", 'forwsl2/collections/ansible_collections/tand0/ttl/docs/command.md')
    my_markdown()
    make_version()
    ansible_doc_to_html()
    site_import()
    shutil.make_archive(f'nextnextping/dist/nextnextping-{VERSION}.1', 'zip', 'nextnextping/dist/nextnextping')


def make_version():
    print(f"make version v={str(VERSION)}")
    text = "# -*- coding: utf-8 -*-\n"
    text = f"\nVERSION = {str(VERSION)}\n"
    file_save("nextnextping/grammer/version.py", text)


def installer():
    """ invoke pyinstaller """
    os.chdir("nextnextping")
    #
    command = "pyinstaller --noconsole --noconfirm nextnextping.py --hidden-import=."
    command = command.split()
    print(f"{command}")
    result = subprocess.run(command, capture_output=True, text=True)
    #
    print("stdout:")
    print(result.stdout)
    print("stderr:")
    print(result.stderr)
    #
    os.chdir("..")


def file_copy(src: str, dest: str):
    print("cp ", src, dest)
    result = file_load(src)
    file_save(dest, result)


def sample_dir_copy(base: str, dest: str):
    """ copy to file """
    for foldername in os.listdir(base):
        if not os.path.isdir(base + foldername):
            continue  # 移動元がフォルダでなかった無視
        if 'sample' not in foldername:
            continue  # サンプルでないなら無視
        #
        print("cp -r ", base + foldername, dest + foldername)
        shutil.copytree(base + foldername, dest + foldername, dirs_exist_ok=True)


def my_markdown():
    """ Change markdown to html """
    filename = "README.md"
    filename_html = filename.replace(".md", ".html")
    md_text = file_load(filename)
    md_text = md_text.replace("\"./docs/", "\"")
    md_text = md_text.replace("(./docs/", "(")
    md_text = md_text.replace(".md", ".html")
    html = markdown_to_html(md_text)
    file_save(INTERNAL + filename_html, html)
    #
    base = "./docs/"
    for filename in os.listdir(base):
        if '.md' in filename:
            filename_html = filename.replace(".md", ".html")
            md_text = file_load(base + filename)
            html = markdown_to_html(md_text)
            file_save(INTERNAL + filename_html, html)
        elif ".png" in filename:
            print("cp -r ", base + filename, INTERNAL + filename)
            shutil.copy2(base + filename, INTERNAL + filename)


def file_load(filename: str) -> str:
    md_text = ''
    with open(filename, "r", encoding="utf-8") as f:
        md_text = f.read()
    return md_text


def file_save(filename: str, text: str):
    print("save", filename)
    with open(filename, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def markdown_to_html(md_text: str) -> str:
    tree_state = True
    result_md_text = RESULT_MD_TEXT
    index_level = []
    for line in md_text.splitlines():
        line = line.rstrip("\n")
        line = line.rstrip("\r")
        line = re.sub(r'<!--.*-->', '', line)
        result = re.search(r"^\s*```", line)
        index_level_now = -1
        if result:
            if tree_state:
                line = "<code><pre>"
            else:
                line = "</pre></code>"
            # 反転
            tree_state = not tree_state
        elif not tree_state:
            line = line.replace('&', "&amp;")
            line = line.replace('<', "&lt;")
            line = line.replace('>', "&gt;")
        elif not re.search(r"\S", line):
            continue  # 空文なのでスキップ
        else:
            result = re.search(r"^\s*(\#+)\s*(.*)", line)
            if result:
                header_len = len(result.group(1))
                line = result.group(2)
                line = f"<h{str(header_len)} id=\"{line}\">{line}</h{str(header_len)}>"
            else:
                result = re.search(r"^(\s*-)\s*(.+)", line)
                if result:
                    index_level_now = len(result.group(1))
                    line = result.group(2)
                    line = (" " * index_level_now) + "<li>" + line
        # 戻し処理
        if len(index_level) == 0 and 0 <= index_level_now:
            # 最初は詰む
            index_level.append(index_level_now)
            line = "<ul>\n" + line
        elif 0 < len(index_level) and index_level[-1] < index_level_now:
            # もしも現状より現在スペースが大きいなら、レベルを１つ上げる
            index_level.append(index_level_now)
            line = (" " * index_level_now) + "<ul>\n" + line
        # もし現状より現在スペースが小さいなら、同じインデントになるまで下げ続ける
        while 0 < len(index_level):
            if index_level_now < index_level[-1]:
                pre_post_text = "</ul>"
                line = pre_post_text + "\n" + line
                index_level = index_level[:-1]
                continue
            break
        line = re.sub(r'`([^`]+)`', r"<code>\1</code>", line)
        line = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', "<a href=\"\\2\">\\1</a>", line)
        result_md_text = result_md_text + "\n" + line
    while 0 < len(index_level):
        if -1 < index_level[-1]:
            line = line + "\n" + (" " * index_level[-1]) + "</ul>"
            index_level = index_level[1:]
            continue
        break
    result_md_text = result_md_text + RESULT_MD_TEXT_END
    return result_md_text


def ansible_doc_to_html() -> str:
    md_text = ''
    with open(ANSIBLE_TARGET, "r", encoding="utf-8") as f:
        md_text = f.read()
    state = 0
    for text in md_text.splitlines():
        if state == 0:
            if "DOCUMENTATION" in text:
                md_text = text
                state = 1
        elif state == 1:
            if "import AnsibleModule" in text:
                break
            md_text = md_text + "\n" + text
    local_scope = {}
    exec(md_text, {}, local_scope)
    # print(f"{json.dumps(local_scope, indent=4)}")
    doc = local_scope['DOCUMENTATION']
    example = local_scope['EXAMPLES']
    ret = local_scope['RETURN']
    html = "\n\n# Ansible TTL macro like collection\n"
    html = html + '''## Overview
- You can connect via SSH using a language called Terawaros Tekitou Language, which is similar to teraterm macro, and ping other servers as stepping stones.

## MACRO for Terawaros Tekitou Lanugage

- Usage
    - [The macro language Terawaros Tekitou Language (TTL)](./docs/syntax.md)　
    - [TTL command reference](./docs/command.md)
'''

    data_dict = yaml.safe_load(doc)
    for k, v in data_dict.items():
        html = html + f"\n## {k}\n"
        html = html + dict_to_md(0, v)
    #
    html = html + "\n\n# Examples\n"
    html = html + "``` yaml\n" + example.strip() + "\n```\n"
    #
    html = html + "\n\n# Result\n"
    data_dict = yaml.safe_load(ret)
    for k, v in data_dict.items():
        html = html + f"\n## {k}\n"
        html = html + dict_to_md(0, v)
    #
    file_save(ANSIBLE_README, html)


def dict_to_md(level, v) -> str:
    html = ''
    # print(f"{v}")
    if isinstance(v, dict):
        for kk, vv in v.items():
            if isinstance(vv, dict) or isinstance(vv, list):
                html = html + (" " * (level))
                html = html + f"- **{kk}**: \n"
                html = html + dict_to_md(level + 4, vv)
            else:
                html = html + (" " * (level))
                html = html + f"- **{kk}**: {str(vv)}\n"
    elif isinstance(v, list):
        for vv in v:
            if isinstance(vv, dict) or isinstance(vv, list):
                html = html + dict_to_md(level, vv)
            else:
                html = html + (" " * (level))
                html = html + f"- {str(vv)}\n"
    else:
        html = str(v)
    return html


def site_import():
    files = []
    for file in os.listdir('test'):
        if '.ttl' not in file:
            continue
        if 'base.ttl' in file:
            continue
        files.append(file)
    text = ""
    text = text + "- hosts: localhost\n"
    text = text + "  become: False\n"
    text = text + "  collections:\n"
    text = text + "    - tand0.ttl\n"
    text = text + "  tasks:\n"
    j = 0
    for file in files:
        for i in [0, 1, 2, 3]:
            j = j + 1
            ok_flag = True
            if '_ok_' in file:
                ok_flag = True
            else:
                ok_flag = False
            text = text + f"    - name: test-{j} {file}\n"
            text = text + "      ttl:\n"
            if i == 0 or i == 2:
                text = text + "        filename: " + file + "\n"
            else:
                text = text + "        cmd: |\n"
                text = text + print_cmd("          ", file)
            text = text + "        chdir: ../test\n"
            text = text + "        ignore_result: False\n"
            text = text + f"      check_mode: {2 <= i}\n"
            text = text + "      register: ttl_output\n"
            text = text + "      ignore_errors: " + str(not ok_flag) + "\n"
            if i < 2:
                text = text + f"    - name: assert-failed-{j} {str(ok_flag)} {file}\n"
                text = text + "      fail:\n"
                text = text + "      when: (not ansible_check_mode) and (ttl_output.failed == " + str(ok_flag) + ")\n"
            else:
                if ok_flag:
                    text = text + f"    - name: assert-changed-{j} {str(ok_flag)} {file}\n"
                    text = text + "      fail:\n"
                    text = text + "      when: ttl_output.changed == True\n"
            if ok_flag:
                text = text + f"    - name: debug-stdout {file}\n"
                text = text + "      debug:\n"
                text = text + "         var: ttl_output.stdout_lines\n\n"
    # print(f"{text}", end="")
    file_save(SITE_IMPORT, text)


def print_cmd(base: str, file: str) -> str:
    with open("test/" + file, "r", encoding="utf-8") as f:
        md_text = f.read()
    buffer = ''
    for text in md_text.splitlines():
        if text.strip() == '':
            continue
        buffer = buffer + base + text.strip() + "\n"
    return buffer


if __name__ == "__main__":
    #
    main()
#
