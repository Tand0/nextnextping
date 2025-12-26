#!/usr/bin/python
# -*- coding: utf-8 -*-
import typing
import sys
import os
try:
    from nextnextping.grammer.ttl_parser_worker import MyTelnetT1
    from .ttlbackground import MyTelnetT1Server
except ModuleNotFoundError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from nextnextping.grammer.ttl_parser_worker import MyTelnetT1
    from .ttlbackground import MyTelnetT1Server


class MyTelnetT1Mock(MyTelnetT1):
    def __init__(self, client):
        self.binary_message = b''
        super().__init__(client)

    @typing.override
    def send_binary(self, message):
        print(f"send_binary() client /{message}/")
        self.binary_message = message

    def check_binary(self):
        """ 読み込んだらクリアする """
        result = self.binary_message
        self.binary_message = b''
        return result


class MyTelnetT1ServerMock(MyTelnetT1Server):
    def __init__(self, client):
        self.binary_message = b''
        super().__init__(client)

    @typing.override
    def send_binary(self, message):
        print(f"send_binary serer() /{message}/")
        self.binary_message = message

    def check_binary(self):
        """ 読み込んだらクリアする """
        result = self.binary_message
        self.binary_message = b''
        return result


def test_telnet_nego_server():
    """ telnetのネゴシエーションのテスト """
    myTelnet = MyTelnetT1ServerMock(None)
    #
    # 初期メッセージの確認
    assert myTelnet.check_binary() == MyTelnetT1._IAC + MyTelnetT1._WILL + MyTelnetT1._ECHO
    #
    result = myTelnet.change_stream(b'bbb')
    assert result == b'bbb'
    result = myTelnet.change_stream(b'ccc')
    assert result == b'ccc'
    #
    # クライアント側から ECHO にしたいがきたので DONTを返す
    myTelnet = MyTelnetT1ServerMock(None)  # クリアする
    result = myTelnet.change_stream(b'aaa')
    result = result + myTelnet.change_stream(MyTelnetT1._IAC)
    result = result + myTelnet.change_stream(MyTelnetT1._WILL)
    result = result + myTelnet.change_stream(MyTelnetT1._ECHO)
    result = result + myTelnet.change_stream(b'bbb')
    assert myTelnet.check_binary() == MyTelnetT1._IAC + MyTelnetT1._DONT + MyTelnetT1._ECHO
    assert result == b'aaabbb'
    #
    # 2回同じメッセージを送っても応答返らない
    result = myTelnet.change_stream(MyTelnetT1._IAC + MyTelnetT1._WILL + MyTelnetT1._ECHO)
    assert myTelnet.check_binary() == b''
    #
    # クライアント側から サーバを ECHO にしたいがきたので WONTを返す
    result = myTelnet.change_stream(MyTelnetT1._IAC)
    result = result + myTelnet.change_stream(MyTelnetT1._DO)
    result = result + myTelnet.change_stream(MyTelnetT1._ECHO)
    result = result + myTelnet.change_stream(b'xxx')
    assert myTelnet.check_binary() == MyTelnetT1._IAC + MyTelnetT1._WILL + MyTelnetT1._ECHO
    assert result == b'xxx'
    #
    # 2回同じメッセージを送っても応答返らない
    myTelnet.change_stream(MyTelnetT1._IAC + MyTelnetT1._DO + MyTelnetT1._ECHO)
    assert myTelnet.check_binary() == b''
    #
    # binaryは拒否
    myTelnet.change_stream(MyTelnetT1._IAC + MyTelnetT1._DO + MyTelnetT1._NULL)
    assert myTelnet.check_binary() == MyTelnetT1._IAC + MyTelnetT1._WONT + MyTelnetT1._NULL
    myTelnet.change_stream(MyTelnetT1._IAC + MyTelnetT1._DO + MyTelnetT1._NULL)
    assert myTelnet.check_binary() == b''
    #
    # binaryは拒否
    myTelnet.change_stream(MyTelnetT1._IAC + MyTelnetT1._WILL + MyTelnetT1._NULL)
    assert myTelnet.check_binary() == MyTelnetT1._IAC + MyTelnetT1._DONT + MyTelnetT1._NULL
    myTelnet.change_stream(MyTelnetT1._IAC + MyTelnetT1._WILL + MyTelnetT1._NULL)
    assert myTelnet.check_binary() == b''
    #
    # binaryは拒否
    myTelnet = MyTelnetT1ServerMock(None)  # クリアする
    assert myTelnet.check_binary() == MyTelnetT1._IAC + MyTelnetT1._WILL + MyTelnetT1._ECHO
    for i in range(2, 255):  # echo IACは除く
        binary_char = i.to_bytes()
        myTelnet.change_stream(MyTelnetT1._IAC + MyTelnetT1._WILL + binary_char)
        assert myTelnet.check_binary() == MyTelnetT1._IAC + MyTelnetT1._DONT + binary_char
        myTelnet.change_stream(MyTelnetT1._IAC + MyTelnetT1._WILL + binary_char)
        assert myTelnet.check_binary() == b''
        #
        binary_char = i.to_bytes()
        myTelnet.change_stream(MyTelnetT1._IAC + MyTelnetT1._DO + binary_char)
        assert myTelnet.check_binary() == MyTelnetT1._IAC + MyTelnetT1._WONT + binary_char
        myTelnet.change_stream(MyTelnetT1._IAC + MyTelnetT1._DO + binary_char)
        assert myTelnet.check_binary() == b''
    #
    # binaryは拒否
    myTelnet = MyTelnetT1ServerMock(None)  # クリアする
    assert myTelnet.check_binary() == MyTelnetT1._IAC + MyTelnetT1._WILL + MyTelnetT1._ECHO
    for i in range(2, 255):  # echo IACは除く
        print(f"i={i}")
        binary_char = i.to_bytes()
        myTelnet.change_stream(MyTelnetT1._IAC + MyTelnetT1._WONT + binary_char)
        assert myTelnet.check_binary() == MyTelnetT1._IAC + MyTelnetT1._WONT + binary_char
        myTelnet.change_stream(MyTelnetT1._IAC + MyTelnetT1._WONT + binary_char)
        assert myTelnet.check_binary() == b''
        #
        binary_char = i.to_bytes()
        myTelnet.change_stream(MyTelnetT1._IAC + MyTelnetT1._DONT + binary_char)
        assert myTelnet.check_binary() == MyTelnetT1._IAC + MyTelnetT1._DONT + binary_char
        myTelnet.change_stream(MyTelnetT1._IAC + MyTelnetT1._DONT + binary_char)
        assert myTelnet.check_binary() == b''
    #
    # IAC_IAC
    myTelnet = MyTelnetT1ServerMock(None)  # クリアする
    assert myTelnet.check_binary() == MyTelnetT1._IAC + MyTelnetT1._WILL + MyTelnetT1._ECHO
    result = myTelnet.change_stream(b'x' + MyTelnetT1._IAC + MyTelnetT1._IAC + b'z')
    assert b'xz' == result
    #
    # IAC_other
    result = myTelnet.change_stream(b'x' + MyTelnetT1._IAC + b'\x03' + b'z')
    assert b'xIAC_Unkownz' == result
    #
    # EOF
    result = myTelnet.change_stream(b'1' + MyTelnetT1._EOF + b'2')
    assert b'12' == result
    #
    # IAC SB x yyyy IAC SE
    result = myTelnet.change_stream(
        b"a"
        + MyTelnetT1._IAC + MyTelnetT1._SB + b'\x05'
        + b'XX'
        + MyTelnetT1._IAC + MyTelnetT1._SE
        + b'b')
    assert b'ab' == result
    assert myTelnet.sb_se_op == b'\x05'
    assert myTelnet.sb_se == b'XX'
    #
    # IAC SB x yy IAC notSE IAC SE
    result = myTelnet.change_stream(
        b"a"
        + MyTelnetT1._IAC + MyTelnetT1._SB + b'\x03'
        + b'yy'
        + MyTelnetT1._IAC + b'notSE'
        + MyTelnetT1._IAC + MyTelnetT1._SE
        + b'b')
    assert b'ab' == result
    assert myTelnet.sb_se_op == b'\x03'
    assert myTelnet.sb_se == b'yy' + MyTelnetT1._IAC + b'notSE'
    #
    #
    #
    # CR
    result = myTelnet.change_stream(b'2\r\r3')
    assert b'2\r3' == result
    #
    result = myTelnet.change_stream(b'2\r' + b'\00' + b'3')
    assert b'2\r3' == result
    #
    result = myTelnet.change_stream(b'2\r' + b'\00' + b'3')
    assert b'2\r3' == result
    #
    result = myTelnet.change_stream(b'2\r\n3')
    assert b'2\r3' == result
    #
    result = myTelnet.change_stream(b'2\rx3')
    assert b'2x3' == result


def test_telnet_nego_client():
    """ telnetのネゴシエーションのテスト """
    myTelnet = MyTelnetT1Mock(None)
    #
    # 初期メッセージの確認
    assert myTelnet.check_binary() == MyTelnetT1._IAC + MyTelnetT1._DO + MyTelnetT1._ECHO
    #
    result = myTelnet.change_stream(b'aaa')
    assert result == b'aaa'
    #
    #
    # サーバ側から ECHO にしたいがきた
    myTelnet = MyTelnetT1Mock(None)  # クリアする
    result = myTelnet.change_stream(b'aaa')
    result = result + myTelnet.change_stream(MyTelnetT1._IAC)
    result = result + myTelnet.change_stream(MyTelnetT1._WILL)
    result = result + myTelnet.change_stream(MyTelnetT1._ECHO)
    result = result + myTelnet.change_stream(b'bbb')
    assert myTelnet.check_binary() == MyTelnetT1._IAC + MyTelnetT1._DO + MyTelnetT1._ECHO
    assert result == b'aaabbb'
    #
    # サーバ側から クライアントを ECHO にしたいがきた
    myTelnet = MyTelnetT1Mock(None)  # クリアする
    result = myTelnet.change_stream(MyTelnetT1._IAC)
    result = result + myTelnet.change_stream(MyTelnetT1._DO)
    result = result + myTelnet.change_stream(MyTelnetT1._ECHO)
    result = result + myTelnet.change_stream(b'xxx')
    assert myTelnet.check_binary() == MyTelnetT1._IAC + MyTelnetT1._WONT + MyTelnetT1._ECHO
    assert result == b'xxx'
    #
    # IAC_NAWS
    myTelnet.change_stream(MyTelnetT1._IAC + MyTelnetT1._DO + MyTelnetT1._NAWS)
    target = (MyTelnetT1._IAC + MyTelnetT1._WILL + MyTelnetT1._NAWS
              + MyTelnetT1._IAC + MyTelnetT1._SB + MyTelnetT1._NAWS
              + b'\0' + b'\x50' + b'\0' + b'\x18'
              + MyTelnetT1._IAC + MyTelnetT1._SE)
    assert myTelnet.check_binary() == target
    #
    # IAC_Terminal_Type
    myTelnet.change_stream(MyTelnetT1._IAC + MyTelnetT1._DO + MyTelnetT1._Terminal_Type)
    target = (MyTelnetT1._IAC + MyTelnetT1._WILL + MyTelnetT1._Terminal_Type
              + MyTelnetT1._IAC + MyTelnetT1._SB + MyTelnetT1._Terminal_Type
              + MyTelnetT1._IS + b'VT100'
              + MyTelnetT1._IAC + MyTelnetT1._SE)
    assert myTelnet.check_binary() == target

#
