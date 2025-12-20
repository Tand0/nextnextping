# -*- coding: utf-8 -*-
import os
import subprocess

VERSION = 1.25


def main():
    """ main """
    print("hello build version {str(VERSION)}")
    make_version()
    installer()


def make_version():
    print(f"make version v={str(VERSION)}")
    text = "# -*- coding: utf-8 -*-\n"
    text = f"\nVERSION = {str(VERSION)}\n"
    file_save("nextnextping/grammer/version.py", text)


def file_save(filename: str, text: str):
    print("save", filename)
    with open(filename, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


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


if __name__ == "__main__":
    #
    main()
#
