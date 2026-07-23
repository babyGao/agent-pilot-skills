# -*- coding: utf-8 -*-
"""清洗抓取来的markdown里的页面噪音。尽力而为，务必人工复查结果。

默认去掉: "登录后复制"、代码块行号(* 1. * 2. ...)、独立版权行、多余空行。
可选按正则裁掉正文前后的页面框架(导航/页脚/相关文章)。

用法:
    python clean.py --md article.md \
        [--cut-before '!\\['] [--cut-after '\\*\\*赞\\*\\*']
  --cut-before: 删除「首个匹配行」之前的所有内容(front matter保留)
  --cut-after : 删除「首个匹配行」及其之后的所有内容
"""
import argparse
import re

from _common import split_front_matter

GUTTER = re.compile(r"^\*\s+\d+\.\s*$")            # 51cto代码查看器的行号
DROP_EXACT = {"登录后复制", "©著作权"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", required=True)
    ap.add_argument("--cut-before", default=None, help="删除此正则首次匹配行之前的内容")
    ap.add_argument("--cut-after", default=None, help="删除此正则首次匹配行及之后的内容")
    args = ap.parse_args()

    text = open(args.md, encoding="utf-8").read()
    fm_dict, body = split_front_matter(text)
    # 重新取原始front matter文本块(保持原样)
    m = re.match(r"^(---\n.*?\n---\n)", text, re.S)
    fm_block = m.group(1) if m else ""

    lines = body.split("\n")

    if args.cut_before:
        pat = re.compile(args.cut_before)
        for i, ln in enumerate(lines):
            if pat.search(ln):
                lines = lines[i:]
                break
    if args.cut_after:
        pat = re.compile(args.cut_after)
        for i, ln in enumerate(lines):
            if pat.search(ln):
                lines = lines[:i]
                break

    kept = []
    for ln in lines:
        s = ln.strip()
        if s in DROP_EXACT or s.startswith("©著作权归作者所有"):
            continue
        if GUTTER.match(s):
            continue
        kept.append(ln)

    out = re.sub(r"\n{3,}", "\n\n", "\n".join(kept)).strip()
    open(args.md, "w", encoding="utf-8").write(fm_block + "\n" + out + "\n")
    print("清洗完成, 正文行数:", len(kept), "-> 覆盖写回", args.md)
    print("请人工检查 %s 是否还有残留噪音" % args.md)


if __name__ == "__main__":
    main()
