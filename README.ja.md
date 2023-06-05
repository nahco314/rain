# rain

AtCoderに提出するコードを暗号化します。

rainによって暗号化されたコードがAtCoderに提出されると、提出結果ページからはコードに関する情報が失われ、第三者がコードを閲覧・コピーすることができなくなります。暗号化されたコードをそのままコピーペーストしても、エラーとなります。

暗号化アルゴリズムは、AtCoder側のアップデートや仕様変更により突然使えなくなる可能性があります。また、AtCoderの仕様を突きコードを公開せずに提出することは、AtCoderからして望ましい行動ではないでしょうから、**利用は慎重にしてください**。

## インストール

まず、 [rye](https://rye-up.com/guide/installation/) をインストールしてください。
```commandline
rye install rain-code --git https://github.com/nahco314/rain.git
```

## 使い方
```
rain {py,cpp} SOURCE OUTPUT [-g, --generator {...}]
```

サブコマンドでどの言語のコードを暗号化するか選択しましす。SOURCEファイルを暗号化し、その結果をOUTPUTに出力します。-gオプションで暗号化アルゴリズムを指定します。

Pythonのジェネレータ:
- aes: 共通鍵を null-bitstring  に埋め込み、AES-256で復号化する。
- embed: ソースコードを直接 null-bitstring で表現する。
- se: aesと同じだが、より短いコードを出力する。
- weak: ソースコードデータをutf-8バイト列として不正なバイト列に埋め込む。コード長は短くなるが、**中身はwgetなどで取得できる**。

C++のジェネレータ:
- tokens: C++コードをトークン単位で分離し、暗号化する。
- tn: tokensと同様のアルゴリズムだが、暗号強度を下げ、より短いコードを出力する。(tokensは極めて長いコードを出力する)

出力結果をコピーペーストで提出すると、データがうまく送信できないので、[oj](https://github.com/online-judge-tools/oj)などで提出してください。

## 例
```commandline
$ cat ./main.py
n, a, b = map(int, input().split())
c = list(map(int, input().split()))

print(c.index(a + b) + 1)
$ rain py ./main.py ./c.py -g se
Done.
$ oj submit https://atcoder.jp/contests/abc300/tasks/abc300_a ./c.py -l 4047
# 結果: https://atcoder.jp/contests/abc300/submissions/41929328
```
