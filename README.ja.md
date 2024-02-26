# rain

AtCoderに提出するコードを部分的に暗号化します。

rainによって暗号化されたコードがAtCoderに提出されると、提出結果ページからは暗号箇所に関する情報が失われ、第三者がコードを閲覧・コピーすることができなくなります。暗号化されたコードをそのままコピーペーストしても、エラーとなります。

暗号化アルゴリズムは、AtCoder側のアップデートや仕様変更により使えなくなる可能性があります。

## インストール

[rye](https://rye-up.com/guide/installation/) を使う場合:
```commandline
rye install rain-code --git https://github.com/nahco314/rain.git
```

pip を使う場合:
```commandline
pip install rain-code@git+https://github.com/nahco314/rain.git
```

## 使い方
```
rain {cpp} SOURCE OUTPUT
```

サブコマンドでどの言語のコードを暗号化するか選択しましす(現バージョンは C++ にのみ対応しています)。SOURCEファイルを暗号化し、その結果をOUTPUTに出力します。

出力結果をコピーペーストで提出すると、データがうまく送信できないので、[oj](https://github.com/online-judge-tools/oj)などで提出してください。

### 使い方 - C++

まず、これらのマクロを定義してください:
```cpp
#define rain_encrypt_u32(x) (x)
#define rain_encrypt_u64(x) (x)
#define rain_encrypt_f32(x) (x)
#define rain_encrypt_f64(x) (x)
```

以降のコード内でこれらのマクロで整数/小数リテラルを囲むことで、暗号化後のコードでそのリテラルが暗号化されます。

また、リテラルだけでなく、特定箇所のロジックを暗号化することもできます。
コードのある区間を暗号化するには、暗号化を開始する箇所に `// RAIN_START_ENCRYPT` という行を挿入し、終了する箇所に `// RAIN_END_ENCRYPT` という行を挿入します。

なお、これらの行は1文字単位で正確に記入してください(空白が余分に入ってたり、逆になかったり、行の頭にインデントがあったりすると暗号化されません)。

## 例
```commandline
$ cat ./main.cpp
#include <bits/stdc++.h>
using namespace std;

#define rain_encrypt_u32(x) (x)
#define rain_encrypt_u64(x) (x)
#define rain_encrypt_f32(x) (x)
#define rain_encrypt_f64(x) (x)

int main() {
// RAIN_START_ENCRYPT
    int n, a, b;
    cin >> n >> a >> b;
// RAIN_END_ENCRYPT

    vector<int> c(rain_encrypt_u32(301));
    for (int i = 0; i < n; i++) {
        cin >> c[i];
    }

    for (int i = 0; i < n; i++) {
// RAIN_START_ENCRYPT
        if (c[i] == a + b) {
            cout << i + 1 << endl;
            return 0;
        }
// RAIN_END_ENCRYPT
    }
}
$ rain cpp ./main.cpp ./c.cpp
Done.
$ oj submit https://atcoder.jp/contests/abc300/tasks/abc300_a ./c.cpp
# 結果: https://atcoder.jp/contests/abc300/submissions/50656205
```
