# -*- coding: utf-8 -*-
"""共享工具：连接调试Chrome、用导出的cookies构造带鉴权的requests会话。

所有脚本共用。连接的是一个「调试模式」的Chrome（见 SKILL.md 的一次性准备），
浏览器里必须已登录博客园。
"""
import io
import json
import os
import sys

import selenium
from selenium import webdriver

# Windows 控制台默认GBK，正文含中文/emoji会崩，统一切到utf-8
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def connect_chrome(port=9222, page_load="eager"):
    """附着到 127.0.0.1:<port> 上已在运行的调试Chrome（复用其登录态）。

    默认走 Selenium Manager 自动匹配 chromedriver（selenium>=4.6）。
    若自动下载不可用，设环境变量 CHROMEDRIVER 指向手动下载的驱动。
    """
    opts = webdriver.chrome.options.Options()
    opts.page_load_strategy = page_load
    opts.add_experimental_option("debuggerAddress", "127.0.0.1:%d" % port)
    driver_path = os.environ.get("CHROMEDRIVER")
    if driver_path:
        service = webdriver.chrome.service.Service(driver_path)
        driver = webdriver.Chrome(service=service, options=opts)
    else:
        driver = webdriver.Chrome(options=opts)
    driver.set_page_load_timeout(40)
    driver.implicitly_wait(0)  # 关键：0 隐式等待，避免抓取时每个缺失选择器都卡满
    return driver


def session_from_cookies(cookies_path):
    """用 get_cookies.py 导出的 cookies 构造 requests 会话（含 X-XSRF-TOKEN）。"""
    import requests

    cookies = json.load(open(cookies_path, encoding="utf-8"))
    s = requests.Session()
    for c in cookies:
        s.cookies.set(c["name"], c["value"], domain=c.get("domain"))
    xsrf = next((c["value"] for c in cookies if c["name"] == "XSRF-TOKEN"), "")
    s.headers.update({
        "User-Agent": "Mozilla/5.0",
        "X-XSRF-TOKEN": xsrf,
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://i.cnblogs.com",
        "Referer": "https://i.cnblogs.com/posts/edit",
    })
    return s


def split_front_matter(md_text):
    """返回 (front_matter_dict, body_without_front_matter)。无front matter则({}, 原文)。"""
    import re

    import yaml

    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", md_text, re.S)
    if not m:
        return {}, md_text
    fm = yaml.safe_load(m.group(1)) or {}
    return fm, m.group(2).lstrip("\n")
