# Satoshi Scale

*Price vs intrinsic value · Harga vs nilai intrinsik*

A dashboard that tracks **Bitcoin's spot price** against two proxies for fundamental value, from 2018 to today:

- **Realized Price** — the network-wide average cost basis of every BTC (a psychological floor)
- **Production Floor** — the estimated electricity cost of mining 1 BTC (the miner-capitulation floor)
- An **MVRV** panel with five valuation zones (deep value → euphoria)

Zoomable ranges (3M / 1Y / 2Y / all), a TradingView-style crosshair readout, dark/light theme and English/Bahasa Indonesia (defaults: dark + English, choices remembered per browser).

**[🔗 Open the dashboard](https://juliusgunawan0707.github.io/btc-intrinsic-value/)**

> The repository is still named `btc-intrinsic-value` so existing links keep working; only the title changed.

## Data — free and deterministic

Every figure comes from the **Coin Metrics community API v4** (no API key) and is computed deterministically:

| Metric | Source |
|---|---|
| Spot price, MVRV, active addresses, hashrate | Coin Metrics community (free) |
| Realized Price | derived from MVRV (`spot / MVRV`) |
| Production Floor | electricity-cost model from hashrate |

> Realized Price is derived from MVRV because `CapRealUSD` is now a paid metric — the result still matches public references (LookIntoBitcoin).

A GitHub Action refreshes `data.js` every day at 08:15 WITA. Manual refresh:

```bash
python fetch_data.py    # latest data -> data.js
```

Mining-cost parameters (ASIC efficiency, electricity price) live at the top of `fetch_data.py`.

## Front end

- `index.html` — the whole page; no build step.
- `assets/lightweight-charts-4.1.3.js` — TradingView Lightweight Charts (Apache-2.0), vendored so the page does not fetch a script from a CDN at runtime.
- `favicon.svg` and the header mark — an original engraved-coin design for Satoshi Scale.
- Fonts: Poppins for text; **JetBrains Mono for every number**, because Poppins has no tabular figures (its "1" is 58% the width of its "0", so columns would jitter).
- Loader: the Bitcoin logo draws itself, then fades into the page. The logo is the **public-domain** Bitcoin symbol (Wikimedia Commons, [`Bitcoin.svg`](https://commons.wikimedia.org/wiki/File:Bitcoin.svg), license: Public domain). Skipped under `prefers-reduced-motion`.

## Disclaimer

This is a **dashboard / alert, not investment advice or an automatic buy signal**. It holds no personal portfolio data. Stock-to-Flow and the Rainbow Chart are deliberately left out: they have no fundamental basis.
