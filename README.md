# PPAcheck

公開網頁：[PPAcheck.html](https://chiayaochen.github.io/PPAcheck/PPAcheck.html)。GitHub Pages 使用 `gh-pages` 根目錄，網站為無需登入的靜態頁面。

本次資料：Invesco 官方持股與美股收盤截至 **2026-09-30**，於 **2026-10-01** 查核。完整包含 66 檔普通股、3 筆現金／會計項目、96 則精選新聞及每檔條件式影響分析。資料快照不自動更新。

價格欄位為單日、9 月及第三季的收盤價格變化，不含股息再投資。LYNX 8 月才上市，缺少 6 月底基準，第三季留為 null。其他價格與官方市值除以股數交叉核對。單日估計貢獻採 9/29 比重，敏感度試算採 9/30 比重。負現金、待收股息及合約上限均保留原始意義。

## 檔案

- `PPAcheck.html`、`assets/ppa.css`、`assets/ppa.js`：網頁與互動。
- `data/ppa-data.json`：公開中文研究資料。
- `research/ppa-invesco-raw.json`、`research/holdings.json`、`research/holdings.csv`：官方來源快照與整理。
- `research/holdings-2026-09-29.json`：前日持股，供單日貢獻估計。
- `research/prices.json`：價格與基準日的歷史序列。
- `research/news-selected.json`：經人工選取、修正來源與日期的新聞索引。
- `research/editorial-news.tsv`、`research/editorial-assessments.tsv`：人工撰寫的摘要與分析。
- `research/QA.md`：檢查結果。

## 本機預覽與更新

在專案目錄執行 `python3 -m http.server 8765 --bind 127.0.0.1`，開啟 `http://127.0.0.1:8765/PPAcheck.html`。請使用 HTTP 預覽，因網頁會讀取同目錄下的 JSON。

更新時，先下載並封存 Invesco 最新完整持股，再逐股查核公開歷史價格與新聞。`scripts/parse_prices.py` 解析已下載的公開歷史表；`scripts/extract_news.py` 僅收集候選資訊，不能直接視為已查核研究。`scripts/select_news.py` 是首次研究的候選篩選紀錄，不應用來覆寫目前已修正的 `news-selected.json`。

人工核對公司身分、公告日期、訂單上限與實際訂單、財年及幣別，更新 TSV，再執行 `python3 scripts/build_data.py`。建置程式目前明確鎖定本次快照的日期和範圍，下次更新需要一併修改基準與說明，不能只更換資料檔。最後更新資產版本、測試並正常推送 `gh-pages`。

此頁為公開資訊研究；分析方向不是目標價、報酬保證或個人化投資建議。
