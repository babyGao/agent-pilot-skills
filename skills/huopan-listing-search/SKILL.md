---
name: huopan-listing-search
description: Use when the user is looking for commercial real estate to rent or buy in China — 店铺 / 门面 / 写字楼 / 办公室 / 厂房 / 仓库 / 产业园 / 公寓 / 酒店 — for shop-site selection, office relocation, or property investment, and needs real listings with area, price, location and detail links rendered as cards.
---

# 火盘商业地产房源检索

火盘房源库的对外检索入口，已上线的 MCP 服务，只有一个工具 `search_listings`。
底层是「稠密向量 + BM25 关键词」混合召回，一句自然语言就能查，不必先把需求拆成字段。

## 端点：直接调，不用探测

```
POST http://101.42.15.203:8333/api/ai/mcp
Content-Type: application/json
```

Streamable HTTP 传输，**无状态、无鉴权**。不需要 `initialize`，也不需要先 `tools/list`——
第一个请求就可以是 `tools/call`，同一次调用即返回房源。

平台只支持旧式 SSE 时改用 `GET http://101.42.15.203:8333/api/ai/mcp/sse`（这条是有状态的，
须先在同一条流上握手）。浏览器打开 `/api/ai/mcp/info` 可看服务与工具声明。

请求体：

```json
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_listings","arguments":{
  "query":"陆家嘴附近适合开火锅店的临街商铺，300平上下，有排烟条件，人流量大",
  "transaction_type":"lease","city":"上海","property_type":"retail","limit":6}}}
```

房源在 `result.structuredContent`；`result.content[0].text` 是同一份数据的文本副本。
`result.isError` 为 true 时，`content[0].text` 就是失败原因。

## 参数：1 个必填 + 3 个可选

| 参数 | 取值 | 说明 |
|---|---|---|
| `query` | 自然语言，必填 | 检索词本身 |
| `transaction_type` | `lease` 出租 / `sale` 出售 | 可选 |
| `city` | 城市名，如 `上海` | 可选 |
| `property_type` | `office` 写字楼 / `retail` 商铺门面 / `industrial` 厂房仓库产业园 / `apartment` 公寓 / `hotel` 酒店 | 可选 |
| `limit` | 1~20，默认 5 | 超过 20 会报错 |

填参数时用得上的事实：

- `query` 会整句参与向量与关键词打分。把用户原话里的地段、商圈、面积、预算、用途、装修状况、
  周边配套一并写进去，命中越准；只写「店铺」这类两字词，结果会很泛。
- 三个可选条件是**硬过滤**：填了就绝不返回别的取值，填错方向直接 0 命中。用户明确表达了才填，
  没提就留空，交给 `query` 去软匹配。中文写法（「出租」「上海市」「写字楼」）也认。
- 库里只有商业地产，**不含住宅类交易**（住宅租售、二手房、自住公寓查不到）。
- 在库 998 套：出售 748 / 出租 250；上海 776 套，其余为杭州 74、深圳 37、广州 29 等；
  业态以写字楼 576 最多，酒店 135、产业园 112、商铺 103、公寓 53、厂房 19。
  冷门城市或冷门业态本来就少，命中数低不代表调用失败。

## 返回字段

顶层：`query`、`applied_filters`（实际生效的硬条件）、`total_matched`（命中总数）、
`returned`（本次返回条数）、`listings`。

| 字段 | 含义 | 是否总有 |
|---|---|---|
| `rank` | 排序序号 | 是 |
| `title` | 项目/楼盘名 | 是 |
| `address` / `city` / `district` / `business_zone` | 地址与行政区、商圈 | 地址与城市总有，区与商圈看数据 |
| `transaction_type` / `transaction_type_label` | `lease`/`sale` 与「出租」/「出售」 | 是 |
| `property_type` | 业态，**输出是中文**（写字楼/商铺/酒店…） | 是 |
| `area_sqm` | 面积（㎡） | 常缺 |
| `price_text` | 给人看的价格，如「6.0 元/㎡/天」「3.2 亿元」 | 常缺，出售商铺尤其缺 |
| `rent_unit_price` / `rent_monthly_total` / `total_price_wan` / `unit_price` | 可参与计算的原始数值 | 看数据 |
| `cap_rate` | 回报率 | 看数据 |
| `tags` | 胶囊标签，如「甲级」「5A 级写字楼」 | 是 |
| `description` | 房源自述（业主/代理填的原文） | 是 |
| `detail_url` | 官网详情页地址 | 是 |
| `listing_id` / `market_id` | 内部标识 | 是 |

**缺失的字段不会以 null 出现，而是整个键都不在 JSON 里。** 面积和价格缺失属常态，
源数据本来就没有，不要编造，也不要因此丢弃这条房源。

## 渲染成 HTML 卡片

拿到结果后输出一份自包含、可直接预览的 HTML（内联样式，不引外部资源）。

- 缺失字段就不显示那一行，别留占位符或写「暂无」以外的猜测值。
- `detail_url` 是唯一真实可点的地址，放在卡片上。
- 目前**没有房源图片**，别放假图或占位图，用文字与标签把版面撑起来。
- `description` 是甲方填的原文，可能含重复字样或英文残留，可以裁剪、摘要，不必原样照抄。
- 卡片之外值得带一句总览：命中总数、生效条件、本次展示几条。

一个够用的骨架：

```html
<!doctype html><meta charset="utf-8">
<style>
 body{margin:0;padding:24px;background:#f6f7f9;font:15px/1.6 system-ui,"Microsoft YaHei",sans-serif;color:#1f2328}
 .sum{margin-bottom:16px;color:#57606a}
 .grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}
 .card{background:#fff;border:1px solid #e4e7ec;border-radius:12px;padding:16px;display:flex;flex-direction:column;gap:8px}
 .name{font-size:17px;font-weight:600}
 .price{color:#d9480f;font-weight:600}
 .meta{color:#57606a;font-size:13px}
 .tags{display:flex;flex-wrap:wrap;gap:6px}
 .tag{background:#f0f4ff;color:#3451b2;border-radius:999px;padding:2px 10px;font-size:12px}
 .desc{color:#57606a;font-size:13px;max-height:4.8em;overflow:hidden}
 a{margin-top:auto;color:#1f6feb;text-decoration:none;font-size:13px}
</style>
<div class="sum">共命中 11 套，展示 2 套 · 条件：上海 / 出租 / 商铺</div>
<div class="grid">
  <div class="card">
    <div class="name">商业中心广场</div>
    <div class="price">6.0 元/㎡/天</div>
    <div class="meta">上海 黄浦区 · 商铺 · 出租 · 30000㎡</div>
    <div class="tags"><span class="tag">5A 级写字楼</span></div>
    <div class="desc">2016-10 竣工，现有租户 Starbucks、Nike Running、The north face 等。</div>
    <a href="https://www.hpan.com.cn/rent/a0f63d26257a6678eba61c48659d0b23" target="_blank">查看详情 →</a>
  </div>
  <!-- 同一批里没有价格的那条：整行不出现，其余照常 -->
  <div class="card">
    <div class="name">外滩 22 号</div>
    <div class="meta">上海 黄浦区 · 商铺 · 出租 · 100㎡</div>
    <div class="tags"><span class="tag">历史保护建筑/甲级物业</span></div>
    <div class="desc">1910 年竣工，现有租户 Mr &amp; Mrs Bund，独立门面约 100㎡，可做餐饮。</div>
    <a href="https://www.hpan.com.cn/rent/e480dd78a85791811191f2e1b100d6d6" target="_blank">查看详情 →</a>
  </div>
</div>
```

## 一条都没命中

`total_matched` 为 0 时，返回里会多一个 `library_overview`——一段现成的中文在库统计
（租售、业态、城市分布、面积与总价分位数）。据它向用户交代库里实际覆盖什么、
建议往哪个方向放宽（换城市、换业态、去掉硬条件、放宽面积或预算），别只回一句查不到。
