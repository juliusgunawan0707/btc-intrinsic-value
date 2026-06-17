# ₿ Bitcoin — Harga vs Nilai Intrinsik

Dashboard yang melacak **harga spot BTC** terhadap dua proxy nilai fundamental dari 2018 hingga sekarang:

- **Realized Price** — rata-rata cost basis seluruh BTC di jaringan (lantai psikologis)
- **Mining Floor** — perkiraan biaya listrik produksi 1 BTC (lantai kapitulasi penambang)
- Panel **MVRV** dengan zona valuasi (wajar / premium / euforia)

Rentang waktu bisa di-zoom (3 bulan / 1 tahun / 2 tahun / semua), gaya TradingView.

**[🔗 Buka dashboard](https://juliusgunawan0707.github.io/REPO-NAME/)**

## Data — 100% gratis, deterministik

Semua angka ditarik dari **Coin Metrics community API v4** (tanpa API key) dan dihitung deterministik:

| Metrik | Sumber |
|---|---|
| Harga spot, MVRV, alamat aktif, hashrate | Coin Metrics community (gratis) |
| Realized Price | diturunkan dari MVRV (`spot / MVRV`) |
| Mining Floor | model biaya listrik dari hashrate |

> Realized Price diturunkan dari MVRV karena metrik `CapRealUSD` kini berbayar — hasilnya tetap cocok dengan referensi publik (LookIntoBitcoin).

## Cara pakai

```bash
python fetch_data.py    # refresh data terbaru -> data.js
# lalu buka index.html (atau via GitHub Pages)
```

Parameter mining cost (efisiensi ASIC, tarif listrik) dapat diubah di bagian atas `fetch_data.py`.

## Disclaimer

Alat ini **dashboard/alert, bukan nasihat investasi atau sinyal beli otomatis**. Tidak memuat data portofolio pribadi mana pun. Stock-to-Flow & Rainbow Chart sengaja tidak dipakai karena tidak punya dasar fundamental.
