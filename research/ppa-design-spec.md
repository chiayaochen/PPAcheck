# PPAcheck design specification

The frontend-app-builder and imagegen skills were read before design and implementation. The built-in image generator produced and displayed two coordinated concepts before coding. No generated artwork is shipped because this product is a code-native financial research interface.

Primary concept: `/Users/chiayaombp2023/.codex/generated_images/01a0f60b-31c1-7922-b518-b2142457bbe6/exec-24b94758-cad3-438a-886e-bb7b9fd76d15.png`
Detail concept: `/Users/chiayaombp2023/.codex/generated_images/01a0f60b-31c1-7922-b518-b2142457bbe6/exec-71c25bf5-75e9-4146-ba3f-e3db0cd548dd.png`

Both are 1536 × 1024. Both were inspected using view_image before implementation. Prompt design: complete Traditional Chinese finance dashboard; pure white, navy text, teal accents; horizontal navigation, open metrics, searchable holdings table, analytical right rail, sensitivity calculator, detailed holding research and source/methodology continuation. Placeholder em dashes were used in design only, never as actual financial data.

## Locked design system

- Pure white page/surfaces; navy #14283b; muted blue-gray #647487; teal #117d79; borders #dbe3e9; notice surface #f2f6f8; negative muted red #ad4b52.
- Chinese/system sans-serif: -apple-system, BlinkMacSystemFont, Segoe UI, Noto Sans TC, PingFang TC, Microsoft JhengHei, sans-serif. Tabular numerals. 44px desktop headline, 28px section title, 16px body, 13px metadata. Mobile headline 30px.
- Maximum 1392px content, desktop 48px gutters, mobile 20px. Open layouts, thin dividers, 4px control radii. No repeated card grid, illustrations, shadows, hero badges, or gradients.
- Header 72px white with bottom rule, PPAcheck wordmark on left, four nav links on right. The image generated a white header; this is the accepted color lock.
- Metrics use a four-column divider strip. Holdings layout is about 72/28 table/research rail. Table scrolls vertically for the full inventory. Detail panel is in document flow after holdings and appears when a ticker is selected. Calculator is a horizontal open band. Sources/methodology use columns below a rule.
- Icons only use simple text glyphs for search, external links, and return. No production bitmap assets.
- Allowed first-screen copy: PPAcheck, 總覽, 完整持股, 情境試算, 資料與方法; 看懂 PPA，從每一檔持股開始。; 持股新聞、價格變化與影響判讀，集中在一份可追溯的資料快照。; PPA 參考價格; 前十大持股比重; 單日估計貢獻; 持股研究覆蓋; 完整持股; 影響 PPA 的關鍵; 持股集中度. Data dates, verified financial values, coverage annotations, and honest limitations are intentional functional additions required by the user.

## Data contract

`data/ppa-data.json`. Weight and returns use percentage units (8.7 means 8.7%). Numeric null/missing is always 未取得, never zero. Quote object: `{price,currency,priceDate,change1d,change1m,change3m,source}`. `priceSource` can be a URL or `{title,url}`. `sparkline` may be a number array but is optional and not used to invent a chart. `summary` and `methodology` may contain strings or objects. News objects carry source/title/date/url/summary. Assessment carries direction/confidence/thesis/upside/downside/watch, allowing text or arrays for narrative sections.

`change1m` is labeled 9 月漲跌 and `change3m` 第三季漲跌 per verified price baseline instructions from data owner. No YTD column. Single-day estimated contribution = sum(weight × dailyReturn / 100) in percentage points. It is explicitly described as an approximate sensitivity, with coverage and exclusions shown. Scenario = weight × shock / 100 percentage points, all else fixed.

## Intended deviations and QA handoff

- Real verified content replaces concept placeholders, so data-bearing text naturally differs.
- Added third-quarter return and contribution columns because user requires detailed stock price changes and PPA effects.
- Table internally scrolls to accommodate complete holdings while preserving the concept's page rhythm.
- Search label, keyboard focus, return button, load/error state, dates, formula explanations and source link validation are functional requirements.
- Root agent performs desktop/mobile browser checks, action checks, and concept-versus-render view_image review before publication. This file does not assert unperformed browser QA.
