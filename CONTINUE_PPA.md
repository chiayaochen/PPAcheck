# PPAcheck 工作狀態

需求與授權：在公開的 chiayaochen/ChatGPTwork 儲存庫 gh-pages 建立、提交、推送 PPAcheck.html，啟用並驗證 GitHub Pages。已獲使用者明確授權。

已完成內容：官方最新持股於本次重新查核後更新至 2026-09-30，共 69 筆、66 檔普通股。新增 SPCX、MDA、AADX、LYNX、AVEX；原 61 檔皆保留。66 檔及 PPA 皆有 9/30 美股美元收盤資料、單日及 9 月價格變化；65 檔有第三季完整期間資料，LYNX 因尚未上市無 6/30 基準，明確留空。

資料已整合至 data/ppa-data.json，含 96 則具日期與來源的中文新聞、66 檔逐股方向／信心／上行／下行／觀察分析、持股敏感度、完整資料與方法。官方 raw、持股 CSV、前日持股、價格歷史、人工編輯 TSV 與建置腳本皆已保存。前日權重估計與最新權重敏感度分開計算。

已核對：HEI 為 HEICO，HONA 為分拆後 Honeywell Aerospace；MDA/ESLT/CAE 報價為美元；Leidos 合約採更正版 9.26 億美元；LASR 初始 4,400 萬美元與上限 6.27 億分開；RKLB/IRDM 收購未完成，對價有條件。負現金及待收股息依官方資料呈現。

測試：桌面 1440×1000、手機 390×844；搜尋、清除、無結果、排序、詳情、±30% 情境計算、缺值及主控台。手機溢出已修正。GitHub Pages 曾直接查到設定為 gh-pages 根目錄且 HTTPS 強制啟用。

接續重點：如果工作中斷，先檢查 git status、遠端 gh-pages 與 research/QA.md 的發布紀錄；內容已完成，避免重做。尚需提交與推送、等待 Pages 部署，核對公開網址及 JSON 與本機一致，然後在本檔和 QA.md 寫入完成證據。

公開網址：https://chiayaochen.github.io/ChatGPTwork/PPAcheck.html

若需接續可貼：請讀取 CONTINUE_PPA.md 與 research/QA.md，從尚未完成的發布／驗證步驟繼續完成 PPAcheck.html。我已授權提交、推送 gh-pages 與驗證 GitHub Pages；保留已完成的 66 檔持股及 96 則研究，勿重做或填造資料。
