#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from grammer.TtlParserWorker import TtlPaserWolker


class MyTtlPaserWolker(TtlPaserWolker):
    """ my TtlPaserWolker  """
    def __init__(self):
        super().__init__()

    def setLog(self, strvar):
        """ log setting """
        print(strvar, end="")


def ttlmacro(argv):
    if len(argv) <= 1:
        print("Usage: python ttlmacro.py FILE [OPTION]...")
    else:
        ttlPaserWolker = None
        try:
            ttlPaserWolker = MyTtlPaserWolker()
            ttlPaserWolker.execute(argv[1], argv[1:])
        finally:
            # なにがあろうとworkerは絶対に殺す
            if ttlPaserWolker is not None:
                ttlPaserWolker.stop()
        return ttlPaserWolker


if __name__ == "__main__":
    ttlmacro(sys.argv)
    #
