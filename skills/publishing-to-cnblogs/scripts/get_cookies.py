# -*- coding: utf-8 -*-
"""从已登录的调试Chrome导出博客园cookies，供后续API脚本使用。

用法:
    python get_cookies.py --out cookies.json [--port 9222]

前提: 调试Chrome里已登录 https://i.cnblogs.com 。
"""
import argparse
import json
import time

from selenium.webdriver.common.by import By

from _common import connect_chrome


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="cookies.json")
    ap.add_argument("--port", type=int, default=9222)
    args = ap.parse_args()

    driver = connect_chrome(args.port)
    driver.switch_to.new_window("tab")
    try:
        driver.get("https://i.cnblogs.com/posts")
    except Exception as e:
        print("load warn:", e)
    time.sleep(3)

    cookies = driver.get_cookies()
    json.dump(cookies, open(args.out, "w", encoding="utf-8"), ensure_ascii=False)
    names = [c["name"] for c in cookies]
    logged_in = any(n in names for n in (".CNBlogsCookie", ".Cnblogs.AspNetCore.Cookies"))
    has_xsrf = "XSRF-TOKEN" in names
    print("导出 %d 个cookie -> %s" % (len(cookies), args.out))
    print("已登录:", logged_in, "| 含XSRF-TOKEN:", has_xsrf)
    if not (logged_in and has_xsrf):
        print("!! 未检测到登录态或XSRF。请先在调试Chrome里登录博客园后台再重试。")
    driver.close()


if __name__ == "__main__":
    main()
