import sys
from grammer.TtlParserWorker import TtlPaserWolker


def ttlmacro(argv):
    if len(argv) <= 1:
        print("Usage: python ttlmacro.py FILE [OPTION]...")
    else:
        ttlPaserWolker = None
        try:
            ttlPaserWolker = TtlPaserWolker()
            ttlPaserWolker.execute(argv[1], argv[1:])
            return ttlPaserWolker
        finally:
            # なにがあろうとworkerは絶対に殺す
            if ttlPaserWolker is not None:
                ttlPaserWolker.stop()


if __name__ == "__main__":
    ttlmacro(sys.argv)
    #
