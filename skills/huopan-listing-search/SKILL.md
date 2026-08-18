---
name: huopan-listing-search
description: Use when the user is looking for commercial real estate to rent or buy in China — 店铺 / 门面 / 写字楼 / 办公室 / 厂房 / 仓库 / 产业园 / 公寓 / 酒店 — for shop-site selection, office relocation, or property investment, and needs real listings with area, price, location and detail links rendered as cards.
---

# 火盘商业地产房源检索

火盘房源库的对外检索入口，已上线的 MCP 服务，只有一个工具 `search_listings`。

**把用户的原话整句传进去就行。** 服务端会用自己的模型把它拆成交易类型、业态、城市、
地标、面积、预算等条件，再做向量与关键词混合检索。不需要你预先拆字段。

## 端点：直接调，不用探测

```
POST http://101.42.15.203:8333/api/ai/mcp
Content-Type: application/json
```

Streamable HTTP 传输，**无状态、无鉴权**。不需要 `initialize`，也不需要先 `tools/list`——
第一个请求就可以是 `tools/call`，同一次调用即返回房源。典型耗时 3~5 秒。

平台只支持旧式 SSE 时改用 `GET http://101.42.15.203:8333/api/ai/mcp/sse`（这条是有状态的，
须先在同一条流上握手）。浏览器打开 `/api/ai/mcp/info` 可看服务与工具声明。

请求体：

```json
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_listings","arguments":{
  "query":"我要在上海陆家嘴附近租一个开火锅店的铺子，400平左右，要有烟道",
  "caller":"doubao","limit":6}}}
```

| 参数 | 说明 |
|---|---|
| `query`（必填） | 用户的找房需求整句。尽量保留原话细节：城市、商圈地标、面积、预算、用途、设施要求。细节越全，条件拆得越准 |
| `caller` | 你所在平台名，如 `doubao` / `qwen` / `kimi` / `workbuddy`，用于服务端用量统计，不影响结果 |
| `limit` | 返回条数，1~20，默认 5 |

房源在 `result.structuredContent`；`result.content[0].text` 是同一份数据的文本副本。
`result.isError` 为 true 时，`content[0].text` 就是失败原因。

## 返回内容

顶层字段：

| 字段 | 含义 |
|---|---|
| `applied_conditions` | 服务端从这句话里拆出、并实际生效的条件（含 `semantic_query` 语义检索词、`soft_tags` 只影响排序的软条件） |
| `unspecified` | 用户没说清、因而没作为条件的必填项。非空表示结果跨了这些维度，值得回头问用户一句 |
| `total_matched` / `returned` | 命中总数 / 本次返回条数 |
| `recall_channel` | `hybrid` 混合检索；`project_name` 用户指名了某栋楼，直接返回那栋 |
| `listings` | 房源列表 |
| `relax_options` | 仅 0 命中时出现：各放宽一个条件分别能出多少套 |
| `library_overview` | 仅 0 命中时出现：在库房源的城市、业态、租售分布统计 |

每条房源：

| 字段 | 含义 | 是否总有 |
|---|---|---|
| `title` | 项目/楼盘名 | 是 |
| `city` / `district` / `address` | 城市、行政区、地址 | 是 |
| `transaction_type_label` | 出租 / 出售 | 是 |
| `property_type` | 业态中文名 | 是 |
| `area_sqm` | 面积（㎡） | 常缺 |
| `price_text` | 可读价格，如「6.0 元/㎡/天」「3.2 亿元」 | 常缺 |
| `tags` | 特征标签 | 是 |
| `description` | 房源自述（业主或代理填的原文） | 是 |
| `detail_url` | 官网详情页地址 | 是 |
| `rent_unit_price` / `total_price_wan` 等 | 可参与计算的原始数值 | 看数据 |

**缺失的字段不会以 null 出现，而是整个键都不在里面。** 面积和价格缺失属常态，源数据就没有，
不要编造，也不要因此丢弃这条房源。

## 渲染：Markdown 表格

一行一套房，左列项目名、右列详情，读起来是卡片列表。

```markdown
共命中 4 套，展示 2 套 · 条件：上海 静安区 · 出租 · 写字楼 · 180~220㎡

| 房源 | 详细信息 |
|:--|:--|
| **1. 机场城市航站楼**<br>`写字楼` `出租` | **上海 · 静安区**<br>面积 209㎡ ｜ 租金 5.0 元/㎡/天<br>标签：甲级<br>2002 年竣工<br>[查看详情 →](https://www.hpan.com.cn/rent/97fd5637ada20d0e4c50d834e30b7c87) |
| **2. 闸北广场**<br>`写字楼` `出租` | **上海 · 静安区**<br>租金 2.0 元/㎡/天<br>标签：甲级<br>主力租户飞利浦<br>[查看详情 →](https://www.hpan.com.cn/rent/0ed0e942fb6fbd410382a9127c29106c) |
```

渲染时用得上的几条：

- 缺失字段整项不写，别留占位符，也别写「暂无」以外的猜测值。
- `detail_url` 是唯一真实可点的地址；目前**没有房源图片**，别放假图。
- `description` 是甲方填的原文，可能有重复字样或英文残留，可裁剪、可摘要。
- 表头那行如实写 `applied_conditions` 里的条件——用户才知道是按什么找的。
- 平台若不渲染 `<br>`，把第二列改成一行、用 ` · ` 连接。

## 一条都没命中

`relax_options` 会给出各放宽一个条件分别能出多少套，`library_overview` 给出在库房源的真实分布。
据这两组数字向用户说明库里覆盖什么、建议往哪个方向放宽，别只回一句查不到。

## 关于这个库

- 只有商业地产，**不含住宅类交易**（住宅租售、二手房、自住公寓查不到）。
- 在库 998 套：出售 748 / 出租 250；上海 776 套，其余为杭州 74、深圳 37、广州 29 等；
  业态以写字楼 576 最多，酒店 135、产业园 112、商铺 103、公寓 53、厂房 19。
  冷门城市或冷门业态本来就少，命中数低不代表调用失败。
- 条件精确到**行政区**；商圈和地标只影响排序，不作硬性筛选（库里没有商圈字段）。
  所以用户说「陆家嘴」，返回的是浦东新区的房源，未必正好在陆家嘴——展示时把行政区如实写出来。
