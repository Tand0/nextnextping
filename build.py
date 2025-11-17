import os
import subprocess
import shutil
import re

INTERNAL = "nextnextping/dist/nextnextping/_internal/"


def main():
    """ メイン処理 """
    installer()
    file_copy("bin/", "nextnextping/dist/nextnextping/")
    file_copy("doc/", INTERNAL)
    my_markdown()


def installer():
    """ pyinstaller を実行する """
    print("hello build")
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


def file_copy(base: str, dest: str):
    """ ファイルをコピーする """
    for filename in os.listdir(base):
        if not ('init.json' in filename or '.csv' in filename or '.png' in filename):
            continue
        #
        print("copy", base + filename, dest + filename)
        shutil.copy(base + filename, dest + filename)


def my_markdown():
    """ markdownをhtmlに変換する """
    filename = "README.md"
    filename_html = filename.replace(".md", ".html")
    md_text = file_load(filename)
    md_text = md_text.replace("\"./doc/", "\"")
    md_text = md_text.replace("(./doc/", "(")
    md_text = md_text.replace(".md", ".html")
    html = markdown_to_html(md_text)
    file_save(INTERNAL + filename_html, html)
    #
    base = "./doc/"
    for filename in os.listdir(base):
        if not ('.md' in filename):
            continue
        filename_html = filename.replace(".md", ".html")
        md_text = file_load(base + filename)
        html = markdown_to_html(md_text)
        file_save(INTERNAL + filename_html, html)


def file_load(filename: str) -> str:
    md_text = ''
    with open(filename, "r", encoding="utf-8") as f:
        md_text = f.read()
    return md_text


def file_save(filename: str, text: str) -> str:
    print("save", filename)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)


def markdown_to_html(md_text: str) -> str:
    tree_state = True
    result_md_text = """
<html>
<head>
  <meta charset="UTF-8">
  <style type="text/css">
code{
  color: #000;
  background-color:#F6F6CB;
  font-family: Courier, monospace;
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
    result_md_text = result_md_text + """
</body>
</html>
"""
    return result_md_text


if __name__ == "__main__":
    #
    main()
    #
#
