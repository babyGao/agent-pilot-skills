# -*- coding: utf-8 -*-
"""用调试Chrome抓取源文章(如51cto)正文，转成markdown。

为什么要用浏览器: 51cto等页面有JS反爬，curl/requests只拿到混淆的挑战脚本，
真实浏览器能正常渲染。抓完务必人工过一遍，再跑 clean.py。

用法:
    python scrape.py --url <文章URL> --out article.md [--port 9222]
"""
import argparse
import re
import time

from markdownify import markdownify as md
from selenium.webdriver.common.by import By

from _common import connect_chrome

# 默认选择器按优先级尝试；不同站点可按需增改
TITLE_SEL = ["h1.artical-title", "h1.article-title", ".artical-title", "h1"]
BODY_SEL = [".article-detail", ".article-content", ".artical-content",
            ".content", "article", "#result", ".editor-preview", ".post"]
TAG_SEL = [".tags a", ".label a", ".article-tags a", "a.tag"]


def pick_text(driver, selectors):
    for sel in selectors:
        try:
            el = driver.find_element(By.CSS_SELECTOR, sel)
            if el.text.strip():
                return el.text.strip()
        except Exception:
            pass
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out", default="article.md")
    ap.add_argument("--port", type=int, default=9222)
    args = ap.parse_args()

    driver = connect_chrome(args.port)
    driver.switch_to.new_window("tab")
    try:
        driver.get(args.url)
    except Exception as e:
        print("加载超时(继续解析已加载部分):", e)
        try:
            driver.execute_script("window.stop();")
        except Exception:
            pass
    time.sleep(3)

    title = pick_text(driver, TITLE_SEL) or driver.title.split("_")[0].strip()

    # 正文: 选文本量最大的候选容器
    body_html, best = "", 0
    for sel in BODY_SEL:
        try:
            for el in driver.find_elements(By.CSS_SELECTOR, sel):
                if len(el.text) > best:
                    best, body_html = len(el.text), (el.get_attribute("innerHTML") or "")
        except Exception:
            pass

    tags = []
    for sel in TAG_SEL:
        try:
            for el in driver.find_elements(By.CSS_SELECTOR, sel):
                t = el.text.strip().lstrip("#").strip()
                if t and t not in tags:
                    tags.append(t)
        except Exception:
            pass
    tags = tags[:6]

    body_md = md(body_html, heading_style="ATX", strip=["script", "style"]).strip()
    fm_tags = "\n".join("  - %s" % t for t in tags) if tags else "  - 博客园"
    front = '---\ntitle: "%s"\ntags:\n%s\n---\n\n' % (title, fm_tags)
    open(args.out, "w", encoding="utf-8").write(front + body_md + "\n")
    driver.close()

    print("标题:", title)
    print("标签:", tags)
    print("正文字符数:", len(body_md), "-> 已写入", args.out)
    print("下一步: 人工检查 + 跑 clean.py 去噪")


if __name__ == "__main__":
    main()
