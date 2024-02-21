import urllib.request
import html as htmllib
import re
from pathlib import Path


def _replace_charref(s):
    s = s.group(1)
    if s[0:1] == b"#":
        # numeric charref
        if s[1] in b"xX":
            num = int(s[2:].rstrip(b";"), 16)
        else:
            num = int(s[1:].rstrip(b";"))
        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
            return b"\uFFFD"
        return bytes([num])
    else:
        _html5 = {key.encode(): item.encode() for key, item in htmllib._html5.items()}

        if s in _html5:
            return _html5[s]
        # find the longest matching name (as defined by the standard)
        for x in range(len(s) - 1, 1, -1):
            if s[:x] in _html5:
                return _html5[s[:x]] + s[x:]
        else:
            return b"&" + s


_charref = re.compile(
    rb"&(#[0-9]+;?" rb"|#[xX][0-9a-fA-F]+;?" rb"|[^\t\n\f <&#;]{1,32};?)"
)


def unescape(s):
    if b"&" not in s:
        return s
    return _charref.sub(_replace_charref, s)


url = "https://atcoder.jp/contests/abc300/submissions/42095986"

with urllib.request.urlopen(url) as response:
    html = response.read()

# print(b"\x00" in html)

start_s = b'<pre id="submission-code" class="prettyprint linenums">'
end_s = b"</pre>"

start = html.find(start_s) + len(start_s)
end = html.find(end_s, start)

content = html[start:end]

content = unescape(content)

with open(Path(__file__).parent / "get_res.py", "wb") as f:
    f.write(content)

for i, e in enumerate(content, start=-2):
    print(i, e)
