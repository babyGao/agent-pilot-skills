---
name: huopan-listing-search
description: Use when the user is looking for commercial real estate to rent or buy in China — 店铺 / 门面 / 写字楼 / 办公室 / 厂房 / 仓库 / 产业园 / 公寓 / 酒店 — for shop-site selection, office relocation, or property investment, and needs real listings with area, price, location and detail links rendered as cards.
---

# 火盘商业地产房源检索

火盘房源库的对外检索入口，已上线的 MCP 服务，只有一个工具 `search_listings`。
把用户的原话整句传进去，服务端自行拆成检索条件，返回结构化房源。

---

# 一、输出格式

**回复由三部分按序组成：**

1. **一行汇总** —— 命中总数、展示条数、实际生效的条件（取自 `applied_conditions`）
2. **每套房源一张卡片** —— 结构照下面这份原样套用，只替换数据
3. **一句收尾** —— 只说返回值支持的事实：结果跨了哪些维度（`unspecified`）、
   库里覆盖情况、条件可以怎么调

卡片结构：

```markdown
> #### 01　[机场城市航站楼](详情页地址)　★最推荐
>
> 📍 上海 静安区
>
> `写字楼`　`209㎡`　`出租`　`甲级`
>
> ### 5.0 元/㎡/天
>
> > ✨ 这套面积 209 平，正好卡在 200 平左右，日租金 5 块，在静安甲级楼里性价比不错。
```

逐行说明：

| 行 | 内容 |
|---|---|
| 标题 | 两位序号 + 项目名（**项目名本身挂 `detail_url`**，不另起一行放链接）；第一套加 `★最推荐` |
| 位置 | 📍 + `address` |
| 胶囊 | 业态 → 面积 → 租售 → 标签（最多 3 枚）→ `Cap 回报率`（有才加），每枚用反引号 |
| 价格 | `price_text`，用 `###` 放大成卡片主角；**没有价格**时改写成一行 `💰 价格待确认`，不要放大 |
| 自述 | 嵌一层引用 + ✨ + `description`，可裁剪可摘要 |

整卡包在块引用里——渲染器自带的左竖线与浅底就是卡框，**不要用任何 HTML 标记**（`<br>`、`<div>`
在部分平台会被吞掉或原样显示）。多套房源就是多个这样的块引用。

## 数据只用返回里有的

**返回值里没有的字段一律不出现在卡片里。** 距离、车程、地铁几号线、周边配套、竣工年、
房源图片都不在返回值里。可以基于已有事实做**推断**，但要写成推断的语气，不能当事实陈述——
"从行政区看离陆家嘴不远" 可以，"车程 5 分钟" 不行。

面积、价格缺失时写 `面积待确认` / `价格待确认`，不省略、不猜。缺失的字段不会以 null 出现，
而是整个键都不在返回值里。

---

# 二、怎么调

```
POST http://101.42.15.203:8333/api/ai/mcp
Content-Type: application/json
```

Streamable HTTP 传输，**无状态、无鉴权**。不需要 `initialize`，也不需要先 `tools/list`——
第一个请求就可以是 `tools/call`。典型耗时 3~5 秒。

平台只支持旧式 SSE 时改用 `GET /api/ai/mcp/sse`（有状态，须先在同一条流上握手）。
浏览器打开 `/api/ai/mcp/info` 可看服务与工具声明。

```json
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_listings","arguments":{
  "query":"我要在上海陆家嘴附近租一个开火锅店的铺子，400平左右，要有烟道",
  "caller":"doubao","limit":6}}}
```

| 参数 | 说明 |
|---|---|
| `query`（必填） | 用户的找房需求整句。尽量保留原话细节：城市、商圈地标、面积、预算、用途、设施要求 |
| `caller` | 你所在平台名，如 `doubao` / `qwen` / `kimi` / `workbuddy`，仅用于服务端用量统计 |
| `limit` | 返回条数，1~20，默认 5 |

房源在 `result.structuredContent`；`result.content[0].text` 是同一份数据的文本副本。
`result.isError` 为 true 时，`content[0].text` 就是失败原因。

---

# 三、返回字段

顶层：

| 字段 | 含义 |
|---|---|
| `applied_conditions` | 服务端拆出并实际生效的条件（含 `semantic_query`、`soft_tags`） |
| `unspecified` | 用户没说清、因而没作为条件的必填项。非空说明结果跨了这些维度 |
| `total_matched` / `returned` | 命中总数 / 本次返回条数 |
| `recall_channel` | `hybrid` 混合检索；`project_name` 用户指名了某栋楼 |
| `listings` | 房源列表 |
| `relax_options` | 仅 0 命中时出现：各放宽一个条件分别能出多少套 |
| `library_overview` | 仅 0 命中时出现：在库房源的城市、业态、租售分布统计 |

每条房源：

| 字段 | 含义 | 是否总有 |
|---|---|---|
| `title` | 项目名 | 是 |
| `address` / `city` / `district` | 地址、城市、行政区 | 是 |
| `property_type` | 业态中文名 | 是 |
| `transaction_type_label` | 出租 / 出售 | 是 |
| `area_sqm` | 面积数值（㎡），展示时带千分位、单位紧贴 | 常缺 |
| `price_text` | 可读价格，如「5.0 元/㎡/天」「3.2 亿元」 | 常缺 |
| `cap_rate` | 回报率数值，展示成 `Cap 5.2%` | 稀疏 |
| `tags` | 特征标签 | 是 |
| `description` | 房源自述（业主或代理填的原文） | 是 |
| `detail_url` | 官网详情页地址 | 是 |
| `rent_unit_price` / `total_price_wan` 等 | 可参与计算的原始数值 | 看数据 |

---

# 四、一条都没命中

`relax_options` 给出各放宽一个条件分别能出多少套，`library_overview` 给出在库房源真实分布。
据这两组数字说明库里覆盖什么、建议往哪个方向放宽。

# 五、关于这个库

- 只有商业地产，**不含住宅类交易**（住宅租售、二手房、自住公寓查不到）。
- 在库 998 套：出售 748 / 出租 250；上海 776 套，其余为杭州 74、深圳 37、广州 29 等；
  业态以写字楼 576 最多，酒店 135、产业园 112、商铺 103、公寓 53、厂房 19。
  冷门城市或冷门业态本来就少，命中数低不代表调用失败。
- 条件精确到**行政区**；商圈与地标只影响排序，不作硬性筛选（库里没有商圈字段）。
  用户说「陆家嘴」，返回的是浦东新区的房源，未必正好在陆家嘴——把行政区如实写出来。
