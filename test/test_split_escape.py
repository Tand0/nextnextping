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

    x = s.split_escape('\x1bxyz')
    assert x == '\x1bxyz'

    assert s.split_escape_buffer == ''
    assert s.split_escape_state == 0
    x = s.split_escape('--\x1b[2m--')
    assert s.split_escape_buffer == ''
    assert s.split_escape_state == 0
    assert x == '----'

    x = s.split_escape('\x1b[0x')
    assert s.split_escape_buffer == ''
    assert x == ''

    x = s.split_escape('\x1b[0m')
    assert x == ''

    x = s.split_escape('\x1b[0;0m')
    assert x == ''

    x = s.split_escape('\x1b[1;2;3m')
    assert x == ''

    x = s.split_escape('\x1b[1;2;3x')
    assert x == ''

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

    x = s.split_escape('a\033[0mb')
    assert x == 'ab'

    x = s.split_escape('a\033[1mb')
    assert x == 'ab'

    x = s.split_escape('a\033[4mb')
    assert x == 'ab'

    x = s.split_escape('a\033[7mb')
    assert x == 'ab'

    x = s.split_escape('a\033[97mb')
    assert x == 'ab'

    x = s.split_escape('a\033[97Hb')
    assert x == 'ab'

    x = s.split_escape('a\033[2Hb')
    assert x == 'ab'

    x = s.split_escape('a\033[H\033[Jb')
    assert x == 'ab'

    x = s.split_escape('a\033[3;4Hb')
    assert x == 'ab'

    x = s.split_escape('a\033[2Ab')
    assert x == 'ab'

    x = s.split_escape('a\033[2Bb')
    assert x == 'ab'

    x = s.split_escape('a\033[2Cb')
    assert x == 'ab'

    x = s.split_escape('a\033[2Db')
    assert x == 'ab'

    x = s.split_escape('a\033[2Jb')
    assert x == 'ab'

    x = s.split_escape('a\033[2Kb')
    assert x == 'ab'

    x = s.split_escape('a\033[2Kb')
    assert x == 'ab'

    x = s.split_escape('a\033[?1hb')
    assert x == 'ab'

    x = s.split_escape('a\033[?1lb')
    assert x == 'ab'

    x = s.split_escape('\033[?6c')
    assert x == ''

    x = s.split_escape('\033[?1J')
    assert x == ''

    x = s.split_escape('\033[?2J')
    assert x == ''

    x = s.split_escape('\033[?1K')
    assert x == ''

    x = s.split_escape('\033c')
    assert x == ''

    x = s.split_escape('\0337')
    assert x == ''

    x = s.split_escape('\0338')
    assert x == ''

    x = s.split_escape('\033M')
    assert x == ''
#
