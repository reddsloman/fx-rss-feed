# FX Session Auto Updater (RSS)

This kit posts **three times per trading day** (Asia, Europe, US) to an RSS feed with:
- Macro headlines (Reuters + other feeds)
- Technical snapshot (EUR/USD, GBP/USD, USD/JPY)
- Trade setups (entries, stops, targets) generated from pivots/ATR/momentum

## Quick Start (GitHub)

1) **Create / use** a GitHub repo (your existing FX RSS repo works).
2) **Add files** from this kit to the repo root keeping the same structure:
```
requirements.txt
scripts/generate_feed.py
config/sources.yml
.github/workflows/session-feed.yml
data/           # will be created automatically
```
3) **Create secret**: `ALPHAVANTAGE_API_KEY` in the repo (Settings → Secrets and variables → Actions → New repository secret).
   - Get a free key at: https://www.alphavantage.co/support/#api-key
4) **Enable Actions** if disabled.
5) The workflow is scheduled at:
   - `23:30 UTC` (Asia session ~ 07:30 Manila)
   - `06:30 UTC` (Europe session ~ 07:30 London during BST)
   - `12:30 UTC` (US session ~ 08:30 New York during EDT)
6) To run **manually**: Actions → *Session Feed (Auto)* → Run workflow.

## Local Test

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ALPHAVANTAGE_API_KEY=your_key
python scripts/generate_feed.py --sources config/sources.yml --out feed.xml
```

Open `feed.xml` to inspect the generated RSS (each run adds an item).

## Customize

- **Pairs**: edit `PAIRS` inside `scripts/generate_feed.py`.
- **Macro sources**: add/remove URLs in `config/sources.yml` (e.g., Reuters FX / central banks RSS).
- **Session labeling**: tweak `session_label_now()` if you prefer different windows.
- **Trade logic**: adjust `build_setup()` to change entries/stops/targets rules.

## Notes

- Alpha Vantage free tier easily supports 3 runs/day for 3 pairs.
- If you prefer a different data vendor, tell me and I’ll adapt the fetchers.
