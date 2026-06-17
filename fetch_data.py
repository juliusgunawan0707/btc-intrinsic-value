#!/usr/bin/env python3
"""
BTC Intrinsic Value — penarik data deterministik (semua sumber GRATIS).

Output: data.js  ->  window.BTC_DATA = {...}  (dibaca langsung oleh index.html via file://)

Sumber gratis:
  - Coin Metrics community API v4 (tanpa API key):
      PriceUSD     = harga spot harian
      CapMVRVCur   = rasio MVRV  -> Realized Price = PriceUSD / MVRV
      AdrActCnt    = alamat aktif (info tambahan)
      HashRate     = hashrate jaringan [TH/s] -> dasar mining cost floor

Realized Price diturunkan dari MVRV karena CapRealUSD kini berbayar.
Mining cost floor = perkiraan biaya listrik produksi 1 BTC (lihat parameter di bawah).
Angka 100% deterministik; tidak ada LLM yang mengarang nilai.
"""
import urllib.request, json, sys, datetime

# ---------- Parameter mining cost (bisa diubah) ----------
EFFICIENCY_J_PER_TH = 20.0   # efisiensi rata-rata fleet ASIC (J/TH). Modern ~18-25
PRICE_PER_KWH       = 0.05   # tarif listrik penambang ($/kWh), asumsi murah
ELEC_SHARE          = 1.0    # 1.0 = floor LISTRIK murni (titik kapitulasi penambang)
# ---------------------------------------------------------

CM = ("https://community-api.coinmetrics.io/v4/timeseries/asset-metrics"
      "?assets=btc&metrics=PriceUSD,CapMVRVCur,AdrActCnt,HashRate"
      "&frequency=1d&start_time=2018-01-01&page_size=10000")

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def block_subsidy(date_str):
    """Subsidy BTC per blok berdasarkan halving."""
    d = date_str[:10]
    if d < "2020-05-11": return 12.5
    if d < "2024-04-20": return 6.25
    return 3.125

def fetch():
    print("Menarik data Coin Metrics community ...", file=sys.stderr)
    rows, data = [], get(CM)
    rows.extend(data['data'])
    while data.get('next_page_url'):
        data = get(data['next_page_url'])
        rows.extend(data['data'])
    print(f"  {len(rows)} baris.", file=sys.stderr)
    return rows

def num(r, k):
    v = r.get(k)
    try: return float(v)
    except (TypeError, ValueError): return None

def build(rows):
    out = []
    for r in rows:
        price = num(r, 'PriceUSD')
        mvrv  = num(r, 'CapMVRVCur')
        if price is None or mvrv is None or mvrv == 0:
            continue
        t = r['time'][:10]
        realized = price / mvrv

        # mining cost floor (proxy listrik all-in)
        hr = num(r, 'HashRate')  # TH/s
        floor = None
        if hr and hr > 0:
            power_w   = hr * EFFICIENCY_J_PER_TH                 # TH/s * J/TH = W
            kwh_day   = power_w * 24 / 1000.0
            elec_cost = kwh_day * PRICE_PER_KWH                  # $/hari listrik jaringan
            btc_day   = 144 * block_subsidy(t)                  # BTC ditambang/hari
            if btc_day > 0:
                floor = (elec_cost / btc_day) / ELEC_SHARE      # all-in $/BTC

        out.append({
            "t": t,
            "price": round(price, 2),
            "realized": round(realized, 2),
            "floor": round(floor, 2) if floor else None,
            "mvrv": round(mvrv, 4),
            "addr": num(r, 'AdrActCnt'),
        })
    return out

def main():
    rows = fetch()
    series = build(rows)
    last = series[-1]
    meta = {
        "generated": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "params": {"eff_j_per_th": EFFICIENCY_J_PER_TH,
                   "price_per_kwh": PRICE_PER_KWH,
                   "elec_share": ELEC_SHARE},
        "source": "Coin Metrics community API v4 (gratis)",
        "n": len(series),
        "range": [series[0]["t"], series[-1]["t"]],
        "latest": last,
    }
    payload = {"meta": meta, "series": series}
    with open("data.js", "w", encoding="utf-8") as f:
        f.write("window.BTC_DATA = ")
        json.dump(payload, f, separators=(",", ":"))
        f.write(";")
    print(f"OK -> data.js  ({len(series)} hari, {meta['range'][0]}..{meta['range'][1]})", file=sys.stderr)
    print(f"Terkini {last['t']}: spot ${last['price']:,.0f}  realized ${last['realized']:,.0f}  "
          f"floor ${last['floor']:,.0f}  MVRV {last['mvrv']:.2f}", file=sys.stderr)

if __name__ == "__main__":
    main()
