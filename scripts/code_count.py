#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统计 ../src 下的 Python 代码量，按文件列出明细"""

import io
import tokenize
from pathlib import Path


def analyze(path: Path):
    try:
        src = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None

    lines = src.splitlines()
    total = len(lines)
    blank = sum(1 for l in lines if not l.strip())

    comment_lines = set()
    docstring_lines = set()

    try:
        tokens = tokenize.generate_tokens(io.StringIO(src).readline)
        for tok in tokens:
            if tok.type == tokenize.COMMENT:
                comment_lines.add(tok.start[0])
            elif tok.type == tokenize.STRING:
                s = tok.string.lstrip("rRbBuUfF")
                if s.startswith(('"""', "'''")):
                    start_line = tok.start[0]
                    line_text = lines[start_line - 1] if start_line <= total else ""
                    before = line_text[: tok.start[1]].strip()
                    if not before:
                        for ln in range(tok.start[0], tok.end[0] + 1):
                            docstring_lines.add(ln)
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return None

    special = comment_lines | docstring_lines
    code = total - blank - len(special)
    return code, len(comment_lines), blank, len(docstring_lines)


SRC = Path("..") / "src"

rows = []
total = {"code": 0, "comment": 0, "blank": 0, "doc": 0}
failed = []

for f in sorted(SRC.rglob("*.py")):
    r = analyze(f)
    if r is None:
        failed.append(f)
        continue
    code, comment, blank, doc = r
    rows.append((str(f.relative_to(SRC)), code, comment, blank, doc))
    total["code"] += code
    total["comment"] += comment
    total["blank"] += blank
    total["doc"] += doc

rows.sort(key=lambda x: x[1], reverse=True)

w = max(len(r[0]) for r in rows) if rows else 10
w = max(w, 4)

print(f"{'文件':<{w}} {'代码':>6} {'注释':>6} {'空行':>6} {'doc':>5}")
print("-" * (w + 28))
for name, code, comment, blank, doc in rows:
    print(f"{name:<{w}} {code:>6} {comment:>6} {blank:>6} {doc:>5}")
print("-" * (w + 28))
print(f"{'总计':<{w}} {total['code']:>6} {total['comment']:>6} "
      f"{total['blank']:>6} {total['doc']:>5}")

if failed:
    print("\n读取/解析失败:")
    for f in failed:
        print(f"  {f}")