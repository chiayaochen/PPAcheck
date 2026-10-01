"""Build the reviewed snapshot. No live client API, secrets, or invented fallback data."""
from pathlib import Path
from datetime import datetime, timezone
import json, csv, html
from urllib.parse import urlparse
ROOT = Path(__file__).resolve().parents[1]
def read(name): return json.loads((ROOT/name).read_text())
latest = read('research/holdings.json')
prior = read('research/holdings-2026-09-29.json')
prices = read('research/prices.json')
news = read('research/news-selected.json')
prior_weights = {h['ticker']:h['weight'] for h in prior['holdings'] if h['type']=='COM'}
editorial = {}
for row in csv.reader((ROOT/'research/editorial-news.tsv').open(), delimiter='\t'):
    assert len(row)==3, row
    editorial.setdefault(row[0], []).append(row[1:])
assessments = {}
for row in csv.reader((ROOT/'research/editorial-assessments.tsv').open(), delimiter='\t'):
    assert len(row)==8, row
    t, sector, direction, confidence, thesis, upside, downside, watch = row
    assessments[t] = dict(sector=sector, assessment=dict(direction=direction, confidence=confidence, thesis=thesis, upside=upside, downside=downside, watch=watch))
holdings=[]
for item in latest['holdings']:
    if item['type']!='COM': continue
    t=item['ticker']; p=prices[t]
    assert len(news[t])==len(editorial[t]), (t,len(news[t]),len(editorial[t]))
    translated=[]
    for source,(title,summary) in zip(news[t],editorial[t]):
        host=urlparse(source['url']).hostname
        # Overview aggregators sometimes mislabel the preceding publisher; derive wire labels from the actual URL.
        publisher={'www.prnewswire.com':'公司新聞稿／PR Newswire','www.businesswire.com':'公司新聞稿／Business Wire','www.globenewswire.com':'公司新聞稿／GlobeNewswire','www.reuters.com':'Reuters','www.accessnewswire.com':'公司新聞稿／ACCESS Newswire','investor.avinc.com':'AeroVironment','investor.keysight.com':'Keysight','investors.planet.com':'Planet Labs'}.get(host,source['source'])
        translated.append(dict(date=source['date'],title=title,summary=summary,url=source['url'],source=publisher))
    translated.sort(key=lambda x:x['date'],reverse=True)
    h=dict(ticker=t,name=html.unescape(item['name']),weight=item['weight'],returnWeight=prior_weights.get(t,0),newSincePrior=t not in prior_weights,
           **{k:p[k] for k in ['price','currency','priceDate','change1d','change1m','change3m','priceSource','sparkline']},news=translated,**assessments[t])
    h['priceNote']='8 月上市，缺少 6 月 30 日價格，無法計算完整第三季報酬。' if t=='LYNX' else ''
    h['assessment']['thesis'] += f" 依目前 {h['weight']:.4f}% 比重，若其股價單獨變動 10%，PPA 的機械式敏感度約為 {h['weight']*.1:.4f} 個百分點；這不是報酬預測。"
    holdings.append(h)
q=prices['PPA'];top=sum(h['weight'] for h in holdings[:10]);equity=sum(h['weight'] for h in holdings)
weighted=sum(h['returnWeight']*h['change1d']/100 for h in holdings)
fund=dict(ticker='PPA',name='Invesco Aerospace & Defense ETF',quote={**{k:q[k] for k in ['price','currency','priceDate','change1d','change1m','change3m']},'source':q['priceSource']},
 summary=[dict(title='大型持股決定主要方向',text=f'9 月 30 日前十大占 {top:.2f}%，GE、RTX、BA、LMT 是主要曝險。正向訂單消息仍須轉成利潤，不能直接預測 ETF 上漲。'),
 dict(title='飛彈與商用航空的雙重驅動',text='RTX、LMT、LHX 的增產安排支撐長期需求；BA 認證、GE 引擎及供應鏈成本則構成執行風險。同一採購鏈的合約不可重複加總。'),
 dict(title='最新持股結構已變動',text='相較 9 月 29 日，新增 SPCX、MDA、AADX、LYNX、AVEX，股票增至 66 檔；沒有移除原 61 檔。個股單日貢獻採前日比重估計，情境試算採最新比重。'),
 dict(title='基本面與股價可能不同步',text=f'PPA 9 月價格變化 {q["change1m"]:+.2f}%、第三季 {q["change3m"]:+.2f}%。即使訂單增長，估值與市場預期也會影響報酬；本頁不把新聞當作單日漲跌的已證實原因。')],
 scenarios=[dict(title='需求落實的情境',text='若多年採購變成確定訂單，且產能、交付、利潤率同步改善，核心國防持股可能支持 PPA；尚無足夠資料指定機率或目標價。'),dict(title='執行受阻的情境',text='若航空認證延後、工程超支或政府付款推遲，多檔供應鏈持股可能同跌。集中度會使共同衝擊放大。'),dict(title='成長估值修正的情境',text='即使營運成長，AI、衛星及無人系統的高預期也可能回落。RKLB／IRDM 收購與新上市股票還帶有交易、融資及短歷史風險。')],
 cashHoldings=[h for h in latest['holdings'] if h['type']!='COM'])
data=dict(meta=dict(generatedAt=datetime.now(timezone.utc).isoformat(timespec='seconds'),holdingsDate=latest['asOf'],pricesDate='2026-09-30',newsThrough='2026-09-30',checkedAt='2026-10-01',returnWeightsDate='2026-09-29',
 freshnessNote='資料快照：官方持股與股價截至 2026-09-30；新聞精選截止同日、2026-10-01 查核。頁面不會自動更新，並非即時報價。',
 limitations=['分析方向針對未來 6–12 個月的營運條件，不是買賣評級、目標價或個人化建議；信心程度是資料與事件成熟度的質性判斷。','新聞為逐股精選，並非完整事件清單；多數為公司新聞稿，可能偏向有利敘述。未取得可核對的數據不予填造。','報價為美元美股收盤，不含盤前盤後、股息再投資、費用及台幣匯率；各公司財年可能與曆年不同。','LYNX 缺少 2026-06-30 上市價格，第三季欄位顯示「未取得」，不以 IPO 價或零填補。','9 月 30 日持股與前日有顯著變動；沒有日內交易時間與成交成本，單日貢獻只能是前日持股的近似估計，不能當作正式績效歸因。']),
 fund=fund,holdings=holdings,
 sources=[dict(id='invesco',title='Invesco 官方完整持股 API（可變動）',url=latest['source'],date=latest['asOf'],type='基金發行人'),dict(id='fund-prices',title='PPA 歷史每日收盤價格',url=q['priceSource']['url'],date=q['priceDate'],type='Stock Analysis'),dict(id='holdings-snapshot',title='本次官方持股原始 JSON 快照',url='https://chiayaochen.github.io/PPAcheck/research/ppa-invesco-raw.json',date=latest['asOf'],type='封存資料'),dict(id='prices-snapshot',title='本次全部價格、基準日與歷史序列',url='https://chiayaochen.github.io/PPAcheck/research/prices.json',date=q['priceDate'],type='可重算資料')],
 methodology=[
 f'完整範圍：Invesco 9 月 30 日列出 69 筆項目，其中 66 檔普通股，股票比重合計 {equity:.6f}%。最新查核時官方 API 的有效日期為 9 月 30 日。',
 '另 3 筆為證券借貸會計項目（比重 0%、市值 0.01 美元）、USD 現金及等價物（比重 -0.109813%）、待收股息（507,180.08 美元、官方未列比重）。保留官方分類與空值；不把待收股息再加入股票權重，不把負現金改成零。',
 '股票報價以公開歷史表為準，66 檔當日收盤均與官方持股市值÷股數核對至 0.03 美元以內；MDA、ESLT、CAE 採美國掛牌美元報價，不混入本國市場幣別。',
 '單日＝9 月 30 日收盤÷9 月 29 日收盤−1；9 月＝9 月 30 日÷8 月 31 日−1；第三季＝9 月 30 日÷6 月 30 日−1。乘以 100 顯示百分比。採來源分割調整後的收盤價，並非含配息調整的總報酬。',
 '单日估計貢獻（百分點）＝9 月 29 日股票比重（%）×9 月 30 日價格變化（%）÷100。新增 5 檔前日快照不存在，因此此估計的前日比重為 0；並非宣稱調整當日完全沒有損益。',
 f'前日 61 檔合计估計貢獻 {weighted:+.4f} 個百分點；PPA 實際市場價格變化 {q["change1d"]:+.4f}%。差異可能包括換股、交易時點、現金、費用及折溢價，無足夠資料拆解各原因。',
 '敏感度試算＝最新持股比重（%）×假設個股漲跌（%）÷100，假設其他價格、權重不變；不包含相關性、再平衡或複利，不是情境機率模型。',
 '每檔研究列出公告日期、中文摘要及原始來源。事實摘要與分析推論分欄；合約上限、選擇權、框架、MOU、未完成收購與已實現收入分開處理。',
 '方向以事件如何影響需求、利潤與現金流判讀；中等信心代表有可查證財務／合約但仍有執行條件，低信心用於早期技術、未量化合作及較高事件不確定性。沒有以利多篇數產生分數。',
 '個別新聞與價格來源在點選股票後列出；完整中文研究和數據可下載 JSON。下次更新需重新核對持股、價格與新聞；這份資料不會自動刷新。'] )
data['methodology']=[s.replace('单日','單日').replace('合计','合計') for s in data['methodology']]
assert len(holdings)==66
assert len(set(h['ticker'] for h in holdings))==66
assert all(h['priceDate']=='2026-09-30' and h['news'] for h in holdings)
assert all(abs(h['price']-next(i['holdingImpliedPrice'] for i in latest['holdings'] if i['ticker']==h['ticker'])) < .03 for h in holdings)
(ROOT/'data').mkdir(exist_ok=True)
(ROOT/'data/ppa-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(f'{len(holdings)} equities; {sum(len(h["news"]) for h in holdings)} dated news entries; weights {equity:.6f}%; top10 {top:.6f}%; prior contribution {weighted:.6f}pp')
