# -*- coding: utf-8 -*-
"""通过博客园后台API发布/更新文章(markdown模式)。

比selenium往编辑器里send_keys可靠得多: 直接调编辑器自己用的REST接口。
- 更新已发布文章(已验证稳): 传 --post-id，先GET原对象、改postBody/title/tags再POST。
- 新建文章: 不传 --post-id。新建负载字段较多，首次使用请发一篇确认字段无缺。

用法:
    python publish.py --md article.md --cookies cookies.json           # 新建
    python publish.py --md article.md --cookies cookies.json --post-id 21841129   # 更新
"""
import argparse
import json

from _common import session_from_cookies, split_front_matter

API = "https://i.cnblogs.com/api/posts"


def build_body(md_path):
    fm, body = split_front_matter(open(md_path, encoding="utf-8").read())
    return fm, body.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", required=True)
    ap.add_argument("--cookies", default="cookies.json")
    ap.add_argument("--post-id", type=int, default=None)
    ap.add_argument("--title", default=None, help="覆盖front matter里的title")
    ap.add_argument("--draft", action="store_true", help="存草稿而非发布")
    args = ap.parse_args()

    s = session_from_cookies(args.cookies)
    fm, body = build_body(args.md)
    title = args.title or fm.get("title") or "无标题"
    tags = fm.get("tags") or []

    if args.post_id:
        # 更新: 拉原对象 -> 改字段 -> POST(id!=0即更新)
        r = s.get("%s/%d" % (API, args.post_id), timeout=30)
        r.raise_for_status()
        blog = r.json()["blogPost"]
        blog["postBody"] = body
        blog["title"] = title
        blog["tags"] = tags
        blog["isMarkdown"] = True
        blog["isDraft"] = args.draft
        payload = blog
    else:
        # 新建: 最小负载模板(首次使用请核对结果)
        payload = {
            "id": 0,
            "postType": 1,
            "title": title,
            "postBody": body,
            "isMarkdown": True,
            "isDraft": args.draft,
            "isPublished": not args.draft,
            "displayOnHomePage": True,
            "isAllowComments": True,
            "includeInMainSyndication": True,
            "tags": tags,
            "categoryIds": [],
            "inSiteCandidate": False,
            "inSiteHome": False,
            "autoDesc": "",
            "entryName": None,
        }

    resp = s.post(API, data=json.dumps(payload),
                  headers={"Content-Type": "application/json"}, timeout=60)
    print("POST /api/posts -> HTTP", resp.status_code)
    print(resp.text[:400])
    resp.raise_for_status()
    out = resp.json()
    print("=" * 40)
    print("成功 | id=%s" % out.get("id"))
    print("URL :", out.get("url"))
    print("验证: 在浏览器打开该URL，滚动确认图片逐张加载(博客园图片懒加载)")


if __name__ == "__main__":
    main()
