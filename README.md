# rain

[日本語版の `README.md`](https://github.com/nahco314/rain/blob/master/README.ja.md)

Partially encrypt the code you submit to AtCoder.

Once the code encrypted by rain is submitted to AtCoder, the information about the encrypted part will be lost from the submission results page, and third parties will not be able to view or copy the code. Copy-pasting the encrypted code as is will result in an error.

The encryption algorithm may become unusable due to updates or specification changes on the AtCoder side.

## Install

If you use [rye](https://rye-up.com/guide/installation/):
```commandline
rye install rain-code --git https://github.com/nahco314/rain.git
````

If you use pip:
```commandline
pip install rain-code@git+https://github.com/nahco314/rain.git
```

## Usage

```
rain {cpp} SOURCE OUTPUT
```

The subcommand selects which language code to encrypt (the current version only supports C++), encrypts the SOURCE file, and outputs the result to OUTPUT.

If you submit the output as a copy-paste, the data will not be transmitted properly, so please submit it as [oj](https://github.com/online-judge-tools/oj).

### Usage - C++

```cpp
#define rain_encrypt_u32(x) (x)
#define rain_encrypt_u64(x) (x)
#define rain_encrypt_f32(x) (x)
#define rain_encrypt_f64(x) (x)
````

Enclosing integer/decimal literals with these macros in subsequent code will cause the literals to be encrypted in the post-encryption code.

You can also encrypt not only literals, but also logic in specific sections of code.
To encrypt a section of code, insert the line `// RAIN_START_ENCRYPT` at the beginning of the encryption and `// RAIN_END_ENCRYPT` at the end.

Note that these lines must be filled in exactly one character at a time (no extra spaces, no spaces, or indentation at the beginning of a line will result in no encryption).

## Example

```commandline
$ cat . /main.cpp
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
$ rain cpp . /main.cpp . /c.cpp
Done.
$ oj submit https://atcoder.jp/contests/abc300/tasks/abc300_a . /c.cpp
# Result: https://atcoder.jp/contests/abc300/submissions/50656205
```
