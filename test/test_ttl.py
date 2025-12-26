#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import re
import pathlib
try:
    from ttlbackground import TTLLoaderSingle
    from ttlbackground import TTLLoaderBase
except ModuleNotFoundError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
    from ttlbackground import TTLLoaderSingle
    from ttlbackground import TTLLoaderBase
try:
    from nextnextping.pyttl import pyttl
except ModuleNotFoundError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from nextnextping.pyttl import pyttl


def test_paramater():
    """ パラメータ関係のテスト """
    # pyttl
    # 何もないときにメッセージが出る
    ok_flag = True
    dummy_argv = ["pyttl"]
    my_pyttl(ok_flag, dummy_argv, False, False)
    #
    # pyttl ファイル名なし
    ok_flag = True
    dummy_argv = ["pyttl", "-c"]
    my_pyttl(ok_flag, dummy_argv, False, False)
    #
    # pyttl ファイル名なし
    ok_flag = True
    dummy_argv = ["pyttl", "-r"]
    my_pyttl(ok_flag, dummy_argv, False, False)
    #
    # pyttl ヘルプメッセージ
    ok_flag = True
    dummy_argv = ["pyttl", "-h"]
    my_pyttl(ok_flag, dummy_argv, False, False)
    #
    # pyttl ファイル名エラー
    ok_flag = False
    dummy_argv = ["pyttl", "aaa"]
    my_pyttl(ok_flag, dummy_argv, False, False)
    #
    # pyttl result==0のときはエラー
    ok_flag = False
    dummy_argv = ["pyttl", "-r", "test/0001_ng_test.ttl"]
    my_pyttl(ok_flag, dummy_argv, False, False)
    #
    # pyttl チェックモードのときはエラーがでない
    ok_flag = True
    dummy_argv = ["pyttl", "-r", "-c", "test/0001_ng_test.ttl"]
    my_pyttl(ok_flag, dummy_argv, False, False)
    #
    # pyttl チェックモードのときはエラーがでない
    ok_flag = True
    dummy_argv = ["pyttl", "-c", "test/0001_ng_test.ttl"]
    my_pyttl(ok_flag, dummy_argv, False, False)
    #
    # pyttl result==0のときでも resultチェックしなければエラーはでない
    ok_flag = True
    dummy_argv = ["pyttl", "test/0001_ng_test.ttl"]
    my_pyttl(ok_flag, dummy_argv, False, False)


class TTLLoader(TTLLoaderBase):
    def __init__(self):
        super().__init__()

    def start_main(self, files=None):
        # カレントフォルダを保持する
        current_folder = os.getcwd()
        target_result = re.search("test$", current_folder)
        if not target_result:
            # もしテストフォルダでなかったらテストフォルダに移動
            test_folder = os.path.join(current_folder, 'test')
            os.chdir(test_folder)
        #
        # テストデータ保存用のフォルダを作る
        os.makedirs("build", exist_ok=True)
        #
        if files is None:
            # ファイルがいなかったらリストを取ってくる
            files_old = os.listdir('.')
            files = []
            for file in files_old:
                if '.ttl' not in file:
                    continue
                if 'base.ttl' in file:
                    continue
                files.append(file)
        #
        for file in files:
            #
            if self.closeFlag:
                assert 1, "test NG get close event!"
            #
            #
            print()
            message = ""
            ok_flag = False
            if '_ok_' in file:
                message = 'OK'
                ok_flag = True
            else:
                message = 'NG'
                ok_flag = False
            #
            print(f"test {message} file={file}")
            dummy_argv = ["pyttl", "-r", file, 'param1', 'param2', 'param3']
            my_pyttl(ok_flag, dummy_argv, False, False)
            #
            print(f"test file={file} --check")
            dummy_argv = ["pyttl", "-r", "--check", file, 'param1', 'param2', 'param3']
            my_pyttl(ok_flag, dummy_argv, True, False)
            #
            print(f"test file={file} not -r")
            dummy_argv = ["pyttl", file, 'param1', 'param2', 'param3']
            my_pyttl(ok_flag, dummy_argv, False, True)
            #


def my_pyttl(ok_flag, dummy_argv, check_mode, ignore_result):
    if check_mode and ignore_result:
        assert False, f"Exception (check_mode,ignore_result is True) {ok_flag},{check_mode},{ignore_result}"
    try:
        pyttl(dummy_argv)
    except Exception as e:
        if not ok_flag:
            return  # OKフラグがFalseなら正常
        else:
            assert False, str(e)  # OKフラグでないなら異常
    #
    # 成功パターンの場合、
    if not ok_flag:
        # OKフラグが落ちていて、かつ、
        #    checkmode が Ture または
        #    ignorresulte_result が True なら問題ない
        assert check_mode or ignore_result, f"A Exception ok_flagg is {check_mode}, but not success {ok_flag},{check_mode},{ignore_result}"


def test_load_ttl():
    """ ttlファイルが動作するか確認する """
    tTLLoader = TTLLoader()
    tTLLoader.start()
    #


def main():
    if len(sys.argv) <= 1:
        # 何も指定しなかった場合
        tTLLoaderSingle = TTLLoaderSingle()
        tTLLoaderSingle.start()
        #
        sys.exit(-1)
        #
    else:
        # ファイル名を指定してテストを実施する
        file_name = sys.argv[1]
        file_name = pathlib.Path(file_name)
        if not file_name.is_absolute():
            # 相対パスなら絶対パスに書き換える
            file_name = pathlib.Path.cwd() / file_name
        file_name = str(file_name)
        tTLLoader = TTLLoader()
        tTLLoader.start(files=[file_name])
        #


if __name__ == "__main__":
    main()
#
