# -*- coding: utf-8 -*-
"""把连续的多张markdown图片排成并排的HTML网格行。

为什么需要: 每张原图往往上千像素宽，纯markdown的 ![](a) ![](b) 只会各占一行往下堆，
排不成一行。博客园允许文章里内联HTML，用 <img width="N%"> 才能真正并排。

规则(与实测一致): 连续图片run >=3张 -> 每行4张(width 23%); 恰好2张 -> 每行2张(48%);
其余保持markdown。可用 --per-row 覆盖大run的每行张数。

用法:
    python to_html_rows.py --md article.md [--per-row 4]
"""
import argparse
import re

from _common import split_front_matter

IMG_LINE = re.compile(r"^!\[[^\]]*\]\([^)]*\)$")
IMG_PAT = re.compile(r"!\[([^\]]*)\]\(([^)]*)\)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", required=True)
    ap.add_argument("--per-row", type=int, default=4, help="大图组每行张数")
    args = ap.parse_args()

    text = open(args.md, encoding="utf-8").read()
    m = re.match(r"^(---\n.*?\n---\n)", text, re.S)
    fm_block = m.group(1) if m else ""
    _, body = split_front_matter(text)
    lines = body.split("\n")

    out, i, n = [], 0, len(lines)
    while i < n:
        if IMG_LINE.match(lines[i].strip()):
            run, j = [], i
            while j < n:
                s = lines[j].strip()
                if IMG_LINE.match(s):
                    run.append(s)
                    j += 1
                elif s == "":
                    k = j
                    while k < n and lines[k].strip() == "":
                        k += 1
                    if k < n and IMG_LINE.match(lines[k].strip()):
                        j = k
                    else:
                        break
                else:
                    break
            per = args.per_row if len(run) >= 3 else (2 if len(run) == 2 else 1)
            if per == 1:
                out.extend(["", run[0], ""])
            else:
                w = max(1, (96 // per))
                out.append("")
                for x in range(0, len(run), per):
                    tags = ""
                    for cell in run[x:x + per]:
                        alt, url = IMG_PAT.findall(cell)[0]
                        tags += ('<img src="%s" alt="%s" width="%d%%" '
                                 'style="display:inline-block;margin:2px;" />' % (url, alt, w))
                    out.append("<div>%s</div>" % tags)
                out.append("")
            i = j
        else:
            out.append(lines[i])
            i += 1

    new_body = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()
    open(args.md, "w", encoding="utf-8").write(fm_block + "\n" + new_body + "\n")
    rows = [l for l in new_body.split("\n") if "<img" in l]
    print("生成 %d 个HTML图片行 -> 覆盖写回 %s" % (len(rows), args.md))


if __name__ == "__main__":
    main()
