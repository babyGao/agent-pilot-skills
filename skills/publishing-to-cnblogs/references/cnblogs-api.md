# 博客园后台 API 速查

编辑器自己用的接口。鉴权靠登录 cookie（`.CNBlogsCookie` / `.Cnblogs.AspNetCore.Cookies`）
加请求头 `X-XSRF-TOKEN`（取值 = `XSRF-TOKEN` cookie）。cookie 由 `get_cookies.py`
从调试 Chrome 导出。

## 图片上传

```
POST https://upload.cnblogs.com/imageuploader/CorsUpload
Content-Type: multipart/form-data
表单字段名: image            # imgFile 也可
Headers: X-XSRF-TOKEN, Origin: https://i.cnblogs.com
```

返回：

```json
{"success": true, "message": "https://img2024.cnblogs.com/other/<uid>/.../xxx.png"}
```

`message` 就是可直接用的图床 URL。博客园自家图床**无防盗链**，任意 referer 都能显示。

## 读取文章

```
GET https://i.cnblogs.com/api/posts/<postId>
```

返回 `{ "blogPost": {...}, "myConfig": {...} }`。`blogPost` 关键字段：

| 字段 | 说明 |
|---|---|
| `id` | 文章ID，0 表示新建 |
| `title` | 标题 |
| `postBody` | 正文（markdown 源码，**不含 front matter**） |
| `isMarkdown` | 是否按 markdown 渲染，必须 `true` |
| `isPublished` / `isDraft` | 发布 / 草稿 |
| `tags` | 标签数组 |
| `categoryIds` | 个人分类ID数组（可空 `[]`） |
| `postType` | 1 = 随笔 |
| `url` | 发布后的公开地址 |

## 新建 / 更新文章

```
POST https://i.cnblogs.com/api/posts
Content-Type: application/json
Headers: X-XSRF-TOKEN
Body: 整个 blogPost 对象（id != 0 即更新，id = 0 / 缺省即新建）
```

**更新（已验证稳）**：先 `GET` 拿到完整 `blogPost`，只改 `postBody`/`title`/`tags`/`isMarkdown`
再整体 POST 回去——避免漏字段把其它设置清掉。

**新建**：字段较多，`publish.py` 内置了一份最小模板；首次使用发一篇后核对结果是否符合预期。

返回体含 `id` 与公开 `url`。
