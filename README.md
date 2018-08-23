# 藍(Indigo)
人狼知能エージェント by 徳島大学 工学部 知能情報工学科 A6グループ 谷岡研究室

## 概要
[AIWolfPy](https://github.com/k-harada/AIWolfPy)をベースに開発しましたが、通信部分以外はほぼ一から作っています。\
アルゴリズムの解説は[Indigoアルゴリズム解説.pdf](/doc/Indigoアルゴリズム解説.pdf)をご覧ください。

## 必要ライブラリ
+ [SudachiPy](https://github.com/WorksApplications/SudachiPy) (日本語形態素解析器)
+ Pandas

## 実行方法
Python3でのみ動作します（Python 3.6.5で動作確認済み）
### 自然言語エージェント
```
$ python Indigo_nl.py -h [hostname] -p [port_number]
```
[hostname]と[port_number]の箇所は読み替えてください。