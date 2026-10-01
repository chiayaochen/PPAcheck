from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
index=json.loads((ROOT/'research/news-index.json').read_text())
selection={
 'RTX':[5,1,6], 'GE':[13,3], 'BA':[13,21,1], 'LMT':[8,17], 'NOC':[1,8],
 'GD':[5,2], 'PH':[4,7], 'HWM':[7,1], 'LHX':[1,6], 'TDG':[2], 'AXON':[2,6],
 'ETN':[1], 'RKLB':[1], 'ATI':[2], 'CW':[8,2], 'CRS':[3], 'WWD':[1],
 'LDOS':[2,4], 'CACI':[2], 'TXT':[4,16], 'KEYS':[10], 'HII':[1,2], 'DRS':[2],
 'MOG/A':[3], 'TDY':[3], 'VSAT':[1], 'BWXT':[13], 'AVAV':[11], 'KTOS':[3],
 'SARO':[1], 'BAH':[2], 'HXL':[7], 'TTMI':[0,2], 'PL':[7,0], 'MRCY':[1],
 'AIR':[2,3], 'SAIC':[0,1], 'LOAR':[2], 'KBR':[0], 'KRMN':[3], 'OSK':[3,8],
 'RDW':[2], 'AMTM':[1], 'DCO':[1], 'OSIS':[1], 'VVX':[1], 'FLY':[1,2],
 'IRDM':[0], 'ONDS':[1], 'PSN':[1], 'HAWK':[1], 'LASR':[3,6], 'VOYG':[1,2],
 'CDRE':[3], 'BKSY':[0,2]
}
out={t:[index[t][i] for i in ids] for t,ids in selection.items()}
extra=[
 ('HONA','2026-08-05','Honeywell Aerospace reports second quarter results; updates 2026 outlook','https://investor.honeywellaerospace.com/news-releases/news-release-details/honeywell-aerospace-reports-second-quarter-results-updates-2026','Honeywell Aerospace'),
 ('ESLT','2026-08-11','Elbit Systems Reports Second Quarter 2026 Results','https://www.elbitsystems.com/news/elbit-systems-reports-second-quarter-2026-results','Elbit Systems'),
 ('APH','2026-07-29','Amphenol Reports Record Second Quarter 2026 Results','https://investors.amphenol.com/news-and-events/news-details/2026/Amphenol-Reports-Record-Second-Quarter-2026-Results/default.aspx','Amphenol'),
 ('APH','2026-08-06','Amphenol Announces Two-for-One Stock Split','https://investors.amphenol.com/news-and-events/news-details/2026/Amphenol-Announces-Two-for-One-Stock-Split-and-Third-Quarter-2026-Dividend/default.aspx','Amphenol'),
 ('PLTR','2026-08-03','Palantir Reports Q2 2026 Results','https://www.sec.gov/Archives/edgar/data/1321655/000132165526000039/a2026q2ex991pressrelease.htm','Palantir／SEC'),
 ('HEI','2026-08-25','HEICO Reports Third Quarter 2026 Results','https://heico.com/2026/08/25/heico-corporation-reports-record-net-income-up-33-on-record-operating-income-up-34-and-record-net-sales-up-23-for-the-third-quarter-of-fiscal-2026/','HEICO'),
 ('CAE','2026-08-12','CAE reports first quarter fiscal 2027 results','https://www.sec.gov/Archives/edgar/data/1173382/000117338226000040/cae_q1fy27xex1xpressrelease.htm','CAE／SEC'),
 ('IRDM','2026-06-29','Rocket Lab to Acquire Iridium','https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-lab-acquire-iridium-historic-deal-creating-fully','Rocket Lab／Iridium'),
 ('RKLB','2026-06-29','Rocket Lab to Acquire Iridium','https://investors.rocketlabcorp.com/news-releases/news-release-details/rocket-lab-acquire-iridium-historic-deal-creating-fully','Rocket Lab／Iridium')
]
for t,date,title,url,source in extra:
 out.setdefault(t,[]).append(dict(date=date,title=title,url=url,source=source,summary=''))
(ROOT/'research/news-selected.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Companies:',len(out),'News:',sum(map(len,out.values())))
