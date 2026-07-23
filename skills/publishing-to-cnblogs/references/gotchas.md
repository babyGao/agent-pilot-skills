# 坑与对策（血泪版）

## 1. 源站图片防盗链 —— 必须重托管

51cto 图床 `s2.51cto.com` 带 `Referer: cnblogs.com` 访问返回 **HTTP 567**（拒绝），
不带 referer 直连返回 **200**。所以：
- 直接把 51cto 图片 URL 放进博客园文章 → **全部裂开，只显示链接文字**。
- 对策：`rehost_images.py` 直连下载（不带 referer 绕过）→ 传博客园图床 → 换 URL。
- 博客园自家图床无防盗链，重托管后永久可显示。

## 2. markdown 多图挤一行不渲染 → 用 HTML 网格

博客园 markdown 解析器对「一行里多张 `![](超长带逗号URL)`」会直接放弃，渲染成纯文本；
且每张原图上千像素宽，就算解析成功也只会各占一行往下堆，排不成网格。
- 对策：`to_html_rows.py` 把连续图片转成 `<div><img width="23%">…</div>`。博客园允许内联 HTML，
  实测保留 `width` 与 `style`，4 张能真正并排。

## 3. 抓取会卡死 → eager 加载 + 0 隐式等待

- `page_load_strategy='normal'` 会一直等 51cto 的广告脚本，永远不结束 → 用 `'eager'`
  + `set_page_load_timeout(40)` + 超时后 `window.stop()`。
- `implicitly_wait(10)` 时，抓取里每个「找不到的选择器」都要空等满 10 秒，十几个选择器叠起来
  就是几分钟卡死 → 抓取阶段设 `implicitly_wait(0)`。
- 源文章页有 JS 反爬，`curl`/`requests` 只能拿到混淆挑战脚本 → 必须用真实浏览器抓。

## 4. 验证时图片“加载失败”多半是假象（懒加载）

博客园文章图片懒加载：`<img>` 初始 `src` 为空，滚动进视口才由 `data-src` 换上。
在**后台自动化标签页**里 IntersectionObserver 常不触发，导致 `naturalWidth=0` 的假象。
- 真正判断图片是否有效：直接 `curl` 图床 URL 看是否 200；或在脚本里强制
  `im.src = im.getAttribute('data-src')` 再测 `naturalWidth`。
- 用户在**可见的真实浏览器**里滚动，图片会正常加载。

## 5. 不要用旧工具的 send_keys 路径

`blog-auto-publishing-tools`（2024）靠 selenium 往编辑器 `#md-editor` 里 `send_keys`，
再点发布按钮。问题：DOM 选择器会随博客园改版失效；大段文本 send_keys 慢且易漏触发框架
onChange。本 skill 改走 REST API（见 cnblogs-api.md），只把浏览器用于登录取 cookie 和抓取。

## 6. 调试 Chrome 用独立 profile，别动用户日常浏览器

用默认 profile 开 `--remote-debugging-port` 需要先完全关掉 Chrome，会打断用户。
改用独立 `--user-data-dir` 的实例，可与日常 Chrome 并存；用户只需在这个新窗口里登录一次博客园。

## 7. 相对链接与内部链接

从 51cto 抓来的正文可能含相对链接（如 `[Claude Code](/ai/tools/288)`），发到博客园会 404。
需要的话在 clean 之后把它们改成绝对地址或去掉。

## 8. Windows 控制台编码

正文含中文/emoji，GBK 控制台 `print` 会崩。脚本已统一把 stdout 切成 utf-8（见 `_common.py`）。
