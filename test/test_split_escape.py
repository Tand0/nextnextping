#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

try:
    from nextnextping.grammer.ttl_parser_worker import SplitEscape
except ModuleNotFoundError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from nextnextping.grammer.ttl_parser_worker import SplitEscape


def test_split_escape():
    s = SplitEscape()

    x = s.split_escape("\033[33mLondon Bridge is falling down\033[0m")
    assert x == 'London Bridge is falling down'

    x = s.split_escape("London Bridge\x1b[38;25m is \x1b[0mfalling\\ down")
    assert x == 'London Bridge is falling\\ down'

    x = s.split_escape("")
    assert x == ''

    x = s.split_escape("\x1b[0m")
    assert x == ''

    x = s.split_escape("Lorem")
    'London Bridge is falling down'

    x = s.split_escape('\x1b[38;5;32mLondon Bridge is falling down\x1b[0m')
    assert x == 'London Bridge is falling down'

    x = s.split_escape('\x1b[1m\x1b[46m\x1b[31mLondon Bridge is falling down\x1b[0m')
    assert x == 'London Bridge is falling down'

    x = s.split_escape('\x1bx')
    assert x == '\x1bx'

    x = s.split_escape('\x1b[x')
    assert x == '\x1b[x'

    x = s.split_escape('\x1b[0x')
    assert x == '\x1b[0x'

    x = s.split_escape('\x1b[0m')
    assert x == ''

    x = s.split_escape('\x1b[0;0m')
    assert x == ''

    x = s.split_escape('\x1b[1;2;3m')
    assert x == ''

    x = s.split_escape('\x1b[1;2;3x')
    assert x == '\x1b[1;2;3x'

    x = s.split_escape('\x1b[1;2;3;4m')
    assert x == '\x1b[1;2;3;4m'

    x = s.split_escape('London Bridge is falling\x1b')
    x = x + s.split_escape('[0;0m down')
    assert x == 'London Bridge is falling down'


def test_split_escape_dowble():
    """ クラスのフィールドは共有しない """

    s = SplitEscape()
    x = s.split_escape('\x1b[')
    assert x == ''

    s = SplitEscape()
    x = s.split_escape('4m')
    assert x == '4m'

#
