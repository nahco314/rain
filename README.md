# rain

[日本語版の `README.md`](https://github.com/nahco314/rain/blob/master/README.ja.md)

Encrypt the code you submit to AtCoder.

When code encrypted by rain is submitted to AtCoder, information about the code is lost from the submission results page, making it impossible for third parties to view or copy the code. Copy-pasting the encrypted code as is will result in an error.

The encryption algorithm may suddenly become unusable due to updates or specification changes on the AtCoder side. Also, submitting code that penetrates AtCoder's specifications without disclosing it to the public would not be desirable behavior from AtCoder's perspective, so **Please use with caution**.

## Install

first, install [rye](https://rye-up.com/guide/installation/).
```commandline
rye install rain-code --git https://github.com/nahco314/rain.git
```

## Usage
```
rain {py,cpp} SOURCE OUTPUT [-g, --generator {...}]
```

The subcommand selects which language code to encrypt.　Encrypt the SOURCE file and output the result to OUTPUT. The -g option specifies the encryption algorithm.

Generators for Python
- aes: Embed the common key in a null-bitstring and decrypt it with AES-256.
- embed: Represent the source code directly with a null-bitstring.
- se: Same as aes, but outputs shorter code.
- weak: Embeds source code data as a utf-8 byte sequence into an illegal byte sequence. The code length will be shortened, but **the contents will be retrieved by  wget, etc**.

If you submit the output results by copy-pasting, the data cannot be transmitted, so please submit the data using [oj](https://github.com/online-judge-tools/oj) or other means.

## Example
```commandline
$ cat ./main.py
n, a, b = map(int, input().split())
c = list(map(int, input().split()))

print(c.index(a + b) + 1)
$ rain py ./main.py ./c.py -g se
Done.
$ oj submit https://atcoder.jp/contests/abc300/tasks/abc300_a ./c.py -l 4047
# https://atcoder.jp/contests/abc300/submissions/41929328
```
