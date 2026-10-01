# PPAcheck 工作狀態

需求與授權：在公開的 chiayaochen/PPAcheck 儲存庫 gh-pages 建立、提交、推送 PPAcheck.html，啟用並驗證 GitHub Pages。已獲使用者明確授權。

已完成內容：官方最新持股於本次重新查核後更新至 2026-09-30，共 69 筆、66 檔普通股。新增 SPCX、MDA、AADX、LYNX、AVEX；原 61 檔皆保留。66 檔及 PPA 皆有 9/30 美股美元收盤資料、單日及 9 月價格變化；65 檔有第三季完整期間資料，LYNX 因尚未上市無 6/30 基準，明確留空。

資料已整合至 data/ppa-data.json，含 96 則具日期與來源的中文新聞、66 檔逐股方向／信心／上行／下行／觀察分析、持股敏感度、完整資料與方法。官方 raw、持股 CSV、前日持股、價格歷史、人工編輯 TSV 與建置腳本皆已保存。前日權重估計與最新權重敏感度分開計算。

已核對：HEI 為 HEICO，HONA 為分拆後 Honeywell Aerospace；MDA/ESLT/CAE 報價為美元；Leidos 合約採更正版 9.26 億美元；LASR 初始 4,400 萬美元與上限 6.27 億分開；RKLB/IRDM 收購未完成，對價有條件。負現金及待收股息依官方資料呈現。

測試：桌面 1440×1000、手機 390×844；搜尋、清除、無結果、排序、詳情、±30% 情境計算、缺值及主控台。手機溢出已修正。GitHub Pages 曾直接查到設定為 gh-pages 根目錄且 HTTPS 強制啟用。

完成狀態：網頁內容已提交 a00fea1 並推送 gh-pages。公開 HTML 與 JSON 皆 HTTP 200，JSON 與本機位元組一致，公開瀏覽器可載入全部 66 檔並操作搜尋／個股詳情。驗證證據及資料限制詳見 research/QA.md。沒有尚未完成的必要工作。

公開網址：https://chiayaochen.github.io/PPAcheck/PPAcheck.html

之後如要更新：先讀本檔與 README.md，保留現有網頁及研究；重新抓取官方最新持股與報價、查核新聞，修改日期和基準，再建置、測試及發布。這是新一輪更新，不要把本次快照誤當作尚未完成。

2026-10-01 重新命名：GitHub 儲存庫與專案名稱改為 PPAcheck；origin 為 git@github.com:chiayaochen/PPAcheck.git。網站與建置腳本中的封存來源網址皆已同步改為 /PPAcheck/。本機資料夾使用 /Users/chiayaombp2023/Documents/ChatGPT/PPAcheck，舊路徑保留相容符號連結供目前 Codex 聊天使用。Codex 側欄名稱尚須使用者手動修改，因電腦操作工具禁止操作 Codex 介面。
