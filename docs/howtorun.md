# How to run a macro

- マクロファイルを実行するには、2通りの方法があります。

1) pythonから直接起動するには以下のようにします。

```shell
> python nextnextping\ttlmacro.py .\test\028_ok_logetc.ttl
```

2) pythonのソースコードから呼ぶには以下のようにします。

```python
            try:
                ttlPaserWolker = ttlmacro(dummy_argv)
            except Exception as e:
                pass  # ここでエラー処理
            result = ttlPaserWolker.getValue('result')  # valueを取るにはこれを使う
```

3) GUIに組み込んで使うには以下のようにします。ここで `MyTtlPaserWolker`は `TtlPaserWolker` をオーバーライドしたクラスです。

```python
        self.myTtlPaserWolker = None
        try:
            self.myTtlPaserWolker = MyTtlPaserWolker()
            self.myTtlPaserWolker.execute(filename, param_list)
        except Exception:
            return 0  # this is NG!
        finally:
            # なにがあろうとworkerは絶対に殺す
            if self.myTtlPaserWolker is not None:
                self.myTtlPaserWolker.stop()
```

