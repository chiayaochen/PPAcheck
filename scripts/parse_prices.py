"""Parse downloaded public daily-history tables; no credentials required."""
from datetime import datetime
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]

def plain(text):
    return html.unescape(re.sub(r"<[^>]*>", "", text)).strip()

def parse(path):
    body = path.read_text()
    table = re.search(r"<table[\s>].*?</table>", body, re.S)
    if not table:
        raise ValueError(f"No historical table: {path.name}")
    rows = []
    for row in re.findall(r"<tr[\s>].*?</tr>", table.group(), re.S):
        cells = [plain(x) for x in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]
        if len(cells) < 8:
            continue
        date = datetime.strptime(cells[0], "%b %d, %Y").date().isoformat()
        rows.append({"date": date, "close": float(cells[4].replace(",", "")),
                     "adjustedClose": float(cells[5].replace(",", "")),
                     "dailyChangeReported": float(cells[6].replace("%", "").replace(",", "").replace("−", "-")) if cells[6] not in ('-', '—') else None})
    # The public table's pagination uses these server-rendered daily records.
    # Parse numeric fields only, without evaluating downloaded JavaScript.
    by_date = {row['date']: row for row in rows}
    for match in re.finditer(r'\{[^{}]*\bt:"(\d{4}-\d{2}-\d{2})"[^{}]*\}', body):
        record = match.group()
        def field(key):
            value = re.search(r'(?:\{|,)'+key+r':(-?(?:\d*\.)?\d+)(?=,|\})', record)
            return float(value.group(1)) if value else None
        close = field('c')
        if close is not None:
            by_date.setdefault(match.group(1), {'date': match.group(1), 'close': close,
                                    'adjustedClose': field('a'), 'dailyChangeReported': field('ch')})
    rows = list(by_date.values())
    rows.sort(key=lambda r: r["date"], reverse=True)
    if not rows:
        raise ValueError(f"No price rows: {path.name}")
    latest = rows[0]
    dates = {r["date"]: r for r in rows}
    def change(base):
        value = dates.get(base)
        return round((latest["close"] / value["close"] - 1) * 100, 4) if value else None
    ticker = path.stem.replace("MOG.A", "MOG/A")
    slug = path.stem.lower()
    source = f"https://stockanalysis.com/{'etf' if ticker == 'PPA' else 'stocks'}/{slug}/history/"
    title = re.search(r"<title>(.*?)</title>", body, re.S)
    return {"ticker": ticker, "title": plain(title.group(1)) if title else None,
            "price": latest["close"], "currency": "USD", "priceDate": latest["date"],
            "change1d": round((latest["close"] / rows[1]["close"] - 1) * 100, 4) if len(rows) > 1 else None,
            "change1m": change("2026-08-31"), "change3m": change("2026-06-30"),
            "baseDate1m": "2026-08-31", "baseDate3m": "2026-06-30",
            "priceSource": {"title": "Stock Analysis 每日收盤價", "url": source},
            "sparkline": [r["close"] for r in reversed(rows[:22])],
            "history": rows}

if __name__ == "__main__":
    prices = {}
    for path in sorted((ROOT / "research/quotes").glob("*.html")):
        try:
            row = parse(path)
            prices[row["ticker"]] = row
        except Exception as error:
            print(f"ERROR {path.name}: {error}")
    (ROOT / "research/prices.json").write_text(json.dumps(prices, ensure_ascii=False, indent=2) + "\n")
    print(f"Parsed {len(prices)} securities")
    for ticker, row in prices.items():
        print(ticker, row["priceDate"], row["price"], row["change1d"], row["change1m"], row["change3m"], row["title"])
