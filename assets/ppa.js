(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const state = { data: null, holdings: [], selected: null, filter: '', sort: 'weight' };
  const number = value => typeof value === 'number' && Number.isFinite(value);
  const escape = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const fmt = (value, digits = 2) => number(value) ? value.toLocaleString('zh-TW', { minimumFractionDigits: digits, maximumFractionDigits: digits }) : '未取得';
  const pct = (value, signed = true, digits = 2) => number(value) ? `${signed && value > 0 ? '+' : ''}${fmt(value, digits)}%` : '未取得';
  const pp = (value, digits = 3) => number(value) ? `${value > 0 ? '+' : ''}${fmt(value === 0 ? 0 : value, digits)}` : '未取得';
  const tone = value => !number(value) || value === 0 ? '' : value > 0 ? 'positive' : 'negative';
  const text = (id, value) => { $(id).textContent = value; };
  const date = value => value ? String(value).replace('T', ' ').replace(/\.\d+Z$/, ' UTC').replace(/Z$/, ' UTC') : '未取得';
  const url = value => { try { const u = new URL(value); return ['https:', 'http:'].includes(u.protocol) ? u.href : ''; } catch { return ''; } };
  const link = (value, label, css = '') => { const safe = url(value); return safe ? `<a class="${css}" href="${escape(safe)}" target="_blank" rel="noopener noreferrer">${escape(label)}</a>` : escape(label); };
  const list = value => Array.isArray(value) ? value : value ? [value] : [];
  const narrative = value => typeof value === 'string' ? value : value && typeof value === 'object' ? value.text || value.summary || value.description || value.body || value.thesis || '' : '';
  const narrativeHtml = value => { const values = list(value).map(narrative).filter(Boolean); return values.length > 1 ? `<ul>${values.map(item => `<li>${escape(item)}</li>`).join('')}</ul>` : `<p>${escape(values[0] || '未取得足夠資料。')}</p>`; };
  const contribution = holding => number(holding.returnWeight) && number(holding.change1d) ? holding.returnWeight * holding.change1d / 100 : null;
  const impactClass = direction => /正向|偏多|上行|利多|positive|bullish/i.test(direction || '') ? 'direction-positive' : /負向|偏空|下行|利空|negative|bearish/i.test(direction || '') ? 'direction-negative' : '';
  const directionText = value => ({positive:'偏正向',negative:'偏負向',neutral:'中性',mixed:'多空並存',bullish:'偏正向',bearish:'偏負向',uncertain:'不確定'})[value] || value || '未取得';
  const confidenceText = value => ({high:'高',medium:'中',low:'低'})[value] || value || '未取得';
  const returnCell = value => `<td class="numeric ${tone(value)} ${number(value) ? '' : 'missing'}">${escape(pct(value))}</td>`;
  const defaults = [
    { title: '持股價格變動', text: '個股新聞透過營收、利潤、現金流與市場預期影響股價，再依持股權重傳導至 PPA。' },
    { title: '持股比重結構', text: '同樣的價格變動，權重越大的持股，對 PPA 的直接影響越大。小型持股仍可能帶來較高波動。' },
    { title: '市場與產業事件', text: '共同產業因素可能同時影響多檔持股。單一股票的敏感度試算不包含這些連動。' }
  ];

  function renderOverview() {
    const { meta = {}, fund = {} } = state.data;
    const quote = fund.quote || {};
    text('as-of', `持股 ${date(meta.holdingsDate)} · 價格 ${date(meta.pricesDate || quote.priceDate)} · 新聞檢索至 ${date(meta.newsThrough)}`);
    text('freshness-note', meta.freshnessNote || '本頁為人工整理的資料快照，不會隨開啟頁面自動更新；價格、持股與新聞可能採用不同日期，詳見各項來源。');
    $('fund-price').innerHTML = number(quote.price) ? `${fmt(quote.price)}<span class="metric-unit">${escape(quote.currency || 'USD')}</span>` : '未取得';
    text('fund-return', `單日 ${pct(quote.change1d)} · ${date(quote.priceDate || meta.pricesDate)}`);
    const weighted = state.holdings.filter(h => number(h.weight));
    const totalWeight = weighted.reduce((sum, h) => sum + h.weight, 0);
    const topTen = [...weighted].sort((a, b) => b.weight - a.weight).slice(0, 10).reduce((sum, h) => sum + h.weight, 0);
    text('top-ten', weighted.length ? pct(topTen, false) : '未取得');
    text('weight-coverage', `${state.holdings.length} 檔股票 · 股票比重 ${pct(totalWeight, false)}`);
    const available = weighted.filter(h => number(h.change1d));
    const coverage = available.reduce((sum, h) => sum + (h.returnWeight || 0), 0);
    const impact = available.reduce((sum, h) => sum + contribution(h), 0);
    $('daily-impact').innerHTML = available.length ? `${pp(impact)}<span class="metric-unit">百分點</span>` : '未取得';
    $('daily-impact').className = available.length ? tone(impact) : '';
    text('impact-coverage', `前日比重 ${pct(coverage, false)} · 非實際報酬`);
    const researched = state.holdings.filter(h => list(h.news).some(n => url(n.url)));
    const researchWeight = researched.reduce((sum, h) => sum + (number(h.weight) ? h.weight : 0), 0);
    $('research-count').innerHTML = `${researched.length}<span class="metric-unit">/ ${state.holdings.length} 檔</span>`;
    text('research-coverage', `附日期、來源及分析 · 股票覆蓋完整`);
    text('holdings-count', `${state.holdings.length} 檔股票`);
    text('top-ten-legend', weighted.length ? pct(topTen, false) : '未取得');
    $('concentration-bar').innerHTML = `<span style="width:${Math.max(0, Math.min(100, topTen))}%"></span>`;
    const summary = list(fund.summary).length ? list(fund.summary).slice(0, 4) : defaults;
    $('fund-summary').innerHTML = summary.map((item, i) => `<div class="driver"><span class="driver-number">${String(i + 1).padStart(2, '0')}</span><div><h3>${escape(typeof item === 'object' ? item.title || `觀察 ${i + 1}` : defaults[i]?.title || `觀察 ${i + 1}`)}</h3><p>${escape(narrative(item))}</p>${item.url ? link(item.url, '研究來源 ↗') : ''}</div></div>`).join('');
    $('fund-scenarios').innerHTML = list(fund.scenarios).map((item, i) => `<article class="fund-scenario"><h3>${escape(typeof item === 'object' ? item.title || item.name || `情境 ${i + 1}` : `情境 ${i + 1}`)}</h3><p>${escape(narrative(item))}</p></article>`).join('');
    text('generated-at', `整理時間：${date(meta.generatedAt)}`);
  }

  function renderTable() {
    const term = state.filter.trim().toLocaleLowerCase();
    const holdings = state.holdings.filter(h => `${h.ticker} ${h.name} ${h.sector || ''}`.toLocaleLowerCase().includes(term));
    holdings.sort((a, b) => {
      if (state.sort === 'ticker') return String(a.ticker).localeCompare(String(b.ticker));
      const first = state.sort === 'impact' ? contribution(a) : a[state.sort];
      const second = state.sort === 'impact' ? contribution(b) : b[state.sort];
      if (!number(first) && !number(second)) return String(a.ticker).localeCompare(String(b.ticker));
      if (!number(first)) return 1;
      if (!number(second)) return -1;
      return state.sort === 'impact' ? Math.abs(second) - Math.abs(first) : second - first;
    });
    $('holdings-body').innerHTML = holdings.length ? holdings.map(h => {
      const impact = contribution(h);
      const direction = directionText(h.assessment?.direction);
      return `<tr${h.ticker === state.selected ? ' class="selected"' : ''}><td><button class="stock-button" type="button" data-ticker="${escape(h.ticker)}" aria-label="查看 ${escape(h.ticker)} ${escape(h.name)} 的研究"><span class="ticker">${escape(h.ticker)}</span><span class="company" title="${escape(h.name)}">${escape(h.name)}</span></button></td><td class="numeric">${escape(pct(h.weight, false))}</td><td class="numeric">${escape(fmt(h.price))}<span class="money-currency">${escape(h.currency || '')}</span></td>${returnCell(h.change1d)}${returnCell(h.change1m)}${returnCell(h.change3m)}<td class="numeric ${tone(impact)}">${escape(pp(impact))}</td><td><span class="direction ${impactClass(h.assessment?.direction)}">${escape(direction)}</span></td></tr>`;
    }).join('') : '<tr><td colspan="8" class="empty-cell">找不到符合條件的持股，請改用股票代號或公司名稱搜尋。</td></tr>';
    text('table-result', `顯示 ${holdings.length} / ${state.holdings.length} 檔 · 比重為 9/30 快照 · 單日貢獻用 9/29 比重估計（百分點）`);
  }

  function priceSource(h) {
    const source = h.priceSource || {};
    return typeof source === 'string' ? link(source, '價格來源 ↗') : link(source.url, source.title || source.name || '價格來源 ↗');
  }

  function showHolding(ticker, shouldScroll = true) {
    const h = state.holdings.find(item => item.ticker === ticker);
    if (!h) return;
    state.selected = ticker;
    const assessment = h.assessment || {};
    text('detail-title', `${h.ticker} · 個股研究`);
    text('detail-sector', h.sector || '產業分類未取得');
    const impact = number(h.weight) ? h.weight * .1 : null;
    $('detail-metrics').innerHTML = `<div class="detail-metric company-metric"><span>${escape(h.ticker)}</span><strong>${escape(h.name)}</strong><small>持股快照 ${escape(date(state.data.meta?.holdingsDate))}</small></div><div class="detail-metric"><span>持股比重</span><strong>${escape(pct(h.weight, false))}</strong><small>在 PPA 中的權重</small></div><div class="detail-metric"><span>參考股價 · ${escape(h.currency || '')}</span><strong>${escape(fmt(h.price))}</strong><small>${escape(date(h.priceDate || state.data.meta?.pricesDate))} · ${priceSource(h)}</small></div><div class="detail-metric"><span>單日變化</span><strong class="${tone(h.change1d)}">${escape(pct(h.change1d))}</strong><small>9 月 ${escape(pct(h.change1m))}<br>第三季 ${escape(pct(h.change3m))}</small></div><div class="detail-metric"><span>個股 +10% 對 PPA 的影響</span><strong class="${tone(impact)}">${escape(pp(impact))}</strong><small>百分點 · 其餘條件不變</small></div>`;
    $('detail-price-note').textContent = [h.priceNote, h.newSincePrior ? '9/30 新增持股；前日快照無此持股，故前日比重貢獻估計為 0，不能據此推定調整當日實際損益。' : `單日貢獻採 9/29 比重 ${fmt(h.returnWeight, 4)}%，情境試算採 9/30 比重。`].filter(Boolean).join(' ');
    const news = list(h.news);
    $('detail-news').innerHTML = news.length ? news.map(n => `<article class="news-article"><div class="news-meta">${escape(date(n.date))} · ${escape(n.source || '原始來源')}</div><h4>${link(n.url, n.title || '新聞原文')}</h4><p>${escape(n.summary || '摘要未取得，請參閱原始來源。')}</p>${link(n.url, '查看原文 ↗', 'news-source-link')}</article>`).join('') : '<p class="empty-news">本次資料快照未取得足夠可查證的近期個股新聞。這不代表該公司沒有新聞或投資風險。</p>';
    $('detail-assessment').innerHTML = `<div class="assessment-meta"><div><span>判讀方向 · 分析推論</span><strong class="${impactClass(assessment.direction)}">${escape(directionText(assessment.direction))}</strong></div><div><span>信心程度</span><strong>${escape(confidenceText(assessment.confidence))}</strong></div></div><div class="assessment-thesis">${narrativeHtml(assessment.thesis)}</div>${[['上行因素',assessment.upside],['下行風險',assessment.downside],['後續觀察',assessment.watch]].map(([heading,content]) => `<section class="assessment-block"><h4>${heading}</h4>${narrativeHtml(content)}</section>`).join('')}`;
    $('holding-detail').hidden = false;
    $('scenario-ticker').value = ticker;
    renderScenario();
    renderTable();
    if (shouldScroll) {
      $('holding-detail').scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
      $('detail-title').focus({ preventScroll: true });
      history.replaceState(null, '', `#stock=${encodeURIComponent(ticker)}`);
    }
  }

  function renderScenario() {
    const h = state.holdings.find(item => item.ticker === $('scenario-ticker').value);
    const shock = Number($('scenario-shock').value);
    text('shock-value', pct(shock, true, 0));
    $('shock-value').className = tone(shock);
    const result = h && number(h.weight) ? h.weight * shock / 100 : null;
    $('scenario-result').innerHTML = number(result) ? `${pp(result)} <span>個百分點</span>` : '未取得';
    $('scenario-result').className = tone(result);
    text('scenario-formula', h ? `${h.ticker} 比重 ${pct(h.weight, false)} × ${pct(shock, true, 0)}` : '請選擇持股');
  }

  function renderSources() {
    $('sources-list').innerHTML = list(state.data.sources).map(s => `<li>${link(s.url, s.title || s.name || '原始資料')}<small>${escape([s.type, s.date ? `資料日期 ${date(s.date)}` : ''].filter(Boolean).join(' · '))}</small></li>`).join('');
    const methods = list(state.data.methodology);
    $('methodology-list').innerHTML = methods.length ? methods.map(item => `<li>${escape(narrative(item))}</li>`).join('') : '<li>各項數據以來源快照日期為準；缺失數值以「未取得」顯示。</li><li>個股單日貢獻（百分點）＝持股比重（%）× 個股單日漲跌（%）÷ 100。</li>';
    const limitations = list(state.data.meta?.limitations);
    $('limitations').innerHTML = limitations.length ? `<h4>閱讀前請留意</h4><ul>${limitations.map(item => `<li>${escape(narrative(item))}</li>`).join('')}</ul>` : '';
  }

  function attachEvents() {
    $('holding-search').addEventListener('input', event => { state.filter = event.target.value; renderTable(); });
    $('holding-sort').addEventListener('change', event => { state.sort = event.target.value; renderTable(); });
    $('holdings-body').addEventListener('click', event => { const button = event.target.closest('[data-ticker]'); if (button) showHolding(button.dataset.ticker); });
    $('close-detail').addEventListener('click', () => {
      const selected = state.selected;
      state.selected = null;
      $('holding-detail').hidden = true;
      renderTable();
      $('holdings').scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
      history.replaceState(null, '', '#holdings');
      const button = [...document.querySelectorAll('[data-ticker]')].find(item => item.dataset.ticker === selected);
      if (button) button.focus({ preventScroll: true });
    });
    $('scenario-ticker').addEventListener('change', renderScenario);
    $('scenario-shock').addEventListener('input', renderScenario);
    document.querySelectorAll('.site-header nav a').forEach(anchor => anchor.addEventListener('click', () => {
      document.querySelectorAll('.site-header nav a').forEach(item => item.classList.toggle('active', item === anchor));
    }));
    window.addEventListener('hashchange', () => { if (location.hash.startsWith('#stock=')) showHolding(decodeURIComponent(location.hash.slice(7))); });
  }

  async function init() {
    try {
      const response = await fetch('data/ppa-data.json', { cache: 'no-cache' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      if (!Array.isArray(data.holdings) || !data.holdings.length) throw new Error('持股資料為空');
      state.data = data;
      state.holdings = data.holdings;
      renderOverview(); renderTable(); renderSources();
      $('scenario-ticker').innerHTML = [...state.holdings].sort((a,b) => (b.weight || 0) - (a.weight || 0)).map(h => `<option value="${escape(h.ticker)}">${escape(h.ticker)} · ${escape(h.name)}</option>`).join('');
      ['holding-search','holding-sort','scenario-ticker','scenario-shock'].forEach(id => { $(id).disabled = false; });
      renderScenario(); attachEvents();
      $('load-status').hidden = true;
      if (location.hash.startsWith('#stock=')) showHolding(decodeURIComponent(location.hash.slice(7)), false);
    } catch (error) {
      $('load-status').classList.add('error');
      $('load-status').textContent = '資料載入失敗。請重新整理頁面，或由「資料與方法」下載 JSON 確認資料檔案。';
      $('holdings-body').innerHTML = '<tr><td colspan="8" class="empty-cell">資料尚未成功載入。</td></tr>';
      text('as-of', '資料日期未取得');
      console.error('PPAcheck data load failed:', error);
    }
  }
  init();
})();
