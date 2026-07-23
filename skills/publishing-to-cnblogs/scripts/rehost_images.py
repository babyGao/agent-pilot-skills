# -*- coding: utf-8 -*-
"""把markdown里的外链图片重托管到博客园图床，并改写URL。

为什么必须做: 源站(如51cto s2.51cto.com)有防盗链——图片带cnblogs referer访问
会被拒(HTTP 5xx)，所以直接引用会全部裂开。本脚本: 直连下载(不带referer可绕过)
-> 上传到博客园图床(CorsUpload) -> 把md里的URL换成 img*.cnblogs.com 。

用法:
    python rehost_images.py --md article.md --cookies cookies.json
"""
import argparse
import json
import re

import requests

from _common import session_from_cookies

UPLOAD = "https://upload.cnblogs.com/imageuploader/CorsUpload"
IMG_RE = re.compile(r"!\[([^\]]*)\]\((https?://[^)\s]+)\)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", required=True)
    ap.add_argument("--cookies", default="cookies.json")
    ap.add_argument("--skip-host", default="cnblogs.com",
                    help="URL已包含此串则跳过(默认不重传已在博客园的图)")
    args = ap.parse_args()

    s = session_from_cookies(args.cookies)
    md = open(args.md, encoding="utf-8").read()

    urls = []
    for _, u in IMG_RE.findall(md):
        if args.skip_host in u:
            continue
        if u not in urls:
            urls.append(u)

    url_map = {}
    for u in urls:
        # 直连下载：不带referer，绕过源站防盗链
        r = requests.get(u, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200 or len(r.content) < 500:
            print("下载失败 HTTP %s: %s" % (r.status_code, u[:70]))
            continue
        up = s.post(UPLOAD, files={"image": ("img.png", r.content, "image/png")}, timeout=60)
        j = up.json()
        if j.get("success"):
            url_map[u] = j["message"]
            print("重托管 OK -> %s" % j["message"])
        else:
            print("上传失败:", up.text[:150])

    def repl(m):
        alt, u = m.group(1), m.group(2)
        return "![%s](%s)" % (alt, url_map.get(u, u))

    md2 = IMG_RE.sub(repl, md)
    open(args.md, "w", encoding="utf-8").write(md2)
    json.dump(url_map, open("url_map.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    remaining = len([u for _, u in IMG_RE.findall(md2) if args.skip_host not in u])
    print("=" * 40)
    print("重托管 %d 张; 仍是外链的图片数:" % len(url_map), remaining)
    if remaining:
        print("!! 仍有外链图片未处理，检查上面的失败项")


if __name__ == "__main__":
    main()
