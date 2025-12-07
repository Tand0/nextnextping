# -*- coding: utf-8 -*-
import os
import re


VERSION = 1.17
GRAMMER = "nextnextping/grammer"


def main():
    """ メイン処理 """
    snake_cake()


def camel_to_snake(name: str) -> str:
    # 大文字の前にアンダースコアを入れて小文字化
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_cake():
    for file in os.listdir(GRAMMER):
        new_filename = camel_to_snake(file)
        if file == new_filename:
            continue
        file = os.path.join(GRAMMER, file)
        new_filename = os.path.join(GRAMMER, new_filename)
        print(f"hit! {file} -> {new_filename}")
        os.rename(file, new_filename)


def file_load(filename: str) -> str:
    md_text = ''
    with open(filename, "r", encoding="utf-8") as f:
        md_text = f.read()
    return md_text


def file_save(filename: str, text: str):
    print("save", filename)
    with open(filename, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


if __name__ == "__main__":
    #
    main()
#
