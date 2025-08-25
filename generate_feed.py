import json
import os
from datetime import datetime, timezone
from typing import Dict, Optional

import requests
from feedgenerator import Rss201rev2Feed

# ------------------------------------------------------------
# Config
# ------------------------------------------------------------
FEED_TITLE = "FX Macro + Technical (Auto)"
FEED_LINK = "https://github.com/reddsloman/fx-rss-feed"
FEED_DESC = "Automated, per-currency snapshots (macro + technical), regenerated hourly."

PAIRS = [
    ("EUR", "USD"),
    ("GBP", "USD"),
    ("USD", "JPY"),
]

AV_FUNCTION = "CURRENCY_EXCHANGE_RATE"  # Alpha Vantage function for spot FX
AV_ENDPOINT = "https://www.alphavantage.co/query"

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def fmt_ts(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")

def fetch_av_rate(frm: str, to: str, apikey: Optional[str]) -> Optional[Dict[str, str]]:
    """
    Fetch a live exchange rate from Alpha Vantage if API key is present.
    Returns dict with 'rate', 'bid', 'ask', 'refreshed' or None on error.
    """
    if not apikey:
        return None
    try:
        params = {
            "function": AV_FUNCTION,
            "from_currency": frm,
            "to_currency": to,
            "apikey": apikey,
        }
        r = requests.get(AV_ENDPOINT, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        blob = data.get("Realtime Currency Exchange Rate", {})
        rate = blob.get("5. Exchange Rate")
        bid = blob.get("8. Bid Price")
        ask = blob.get("9. Ask Price")
        refreshed = blob.get("6. Last Refreshed")
        if rate:
            return {
                "rate": rate,
                "bid": bid or "",
                "ask": ask or "",
                "refreshed": refreshed or "",
            }
    except Exception:
        pass
    return None

def round_levels(spot: float, step: float):
    """
    Create simple round-number levels around spot (purely mechanical,
    avoids external libs — serves as lightweight reference rails).
    """
    base = round(spot / step) * step
    levels = [base - 2*step, base - step, base, base + step, base + 2*step]
    return [round(x, 4) for x in levels]

def build_item_content(symbol: str,
                       spot_info: Optional[Dict[str, str]],
                       generated_at: datetime) -> Dict[str, str]:
    """
    Build HTML description for each pair, combining macro/tech placeholders with
    optional live spot and mechanically derived levels.
    """
    pair_title = symbol
    ts = fmt_ts(generated_at)

    # Spot block
    if spot_info and spot_info.get("rate"):
        rate = spot_info["rate"]
        bid = spot_info.get("bid") or "—"
        ask = spot_info.get("ask") or "—"
        refreshed = spot_info.get("refreshed") or "—"
        spot_html = (
            f"<p><b>Spot</b>: {rate} &nbsp; "
            f"<b>Bid</b>: {bid} &nbsp; <b>Ask</b>: {ask} "
            f"&nbsp; <i>(Last Refreshed: {refreshed} UTC)</i></p>"
        )
        try:
            spot_float = float(rate)
        except Exception:
            spot_float = None
    else:
        spot_html = "<p><b>Spot</b>: n/a (AV key not set or fetch skipped)</p>"
        spot_float = None

    # Technical rails: simple round-number references (no external TA libs)
    levels_html = ""
    if spot_float is not None:
        # pick a step roughly suited per pair
        step = 0.0010
        if symbol == "USD/JPY":
            step = 0.10
        lvls = round_levels(spot_float, step)
        # S2, S1, Pivot, R1, R2 analog (mechanical)
        if len(lvls) == 5:
            s2, s1, pivot, r1, r2 = lvls
        else:
            s2 = s1 = pivot = r1 = r2 = "—"
        levels_html = (
            "<ul>"
            f"<li><b>Reference rails</b> (mechanical): "
            f"S2 {s2} · S1 {s1} · Pivot {pivot} · R1 {r1} · R2 {r2}</li>"
            "</ul>"
        )
    else:
        levels_html = "<ul><li><b>Reference rails</b>: n/a (no spot)</li></ul>"

    # Macro placeholders — kept generic, safe, non-speculative
    macro_html = (
        "<ul>"
        "<li>Macro watch: central bank guidance, front-end rates, and incoming tier-1 data.</li>"
        "<li>Sentiment: track risk proxies (equities, credit, volatility) for USD impulses.</li>"
        "<li>Calendar: next 24–48h data and public remarks relevant to the pair.</li>"
        "</ul>"
    )

    description = (
        f"<p><i>Generated: {ts}</i></p>"
        f"{spot_html}"
        "<h4>Macro snapshot</h4>"
        f"{macro_html}"
        "<h4>Technical snapshot</h4>"
        f"{levels_html}"
        "<p><i>Note: Levels are mechanical reference rails around spot; "
        "no forward-looking statements included.</i></p>"
    )

    # Minimal link target (kept stable); you can change to a pair-specific URL if desired.
    link = "https://reddsloman.github.io/fx-rss-feed/rss.xml"

    return {
        "title": f"{pair_title} — Macro & Technical — {ts}",
        "link": link,
        "description": description,
    }

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    generated_at = now_utc()

    # Prepare feed
    feed = Rss201rev2Feed(
        title=FEED_TITLE,
        link=FEED_LINK,
        description=FEED_DESC,
        language="en",
    )

    av_key = os.environ.get("ALPHAVANTAGE_API_KEY")

    items_out = []

    for frm, to in PAIRS:
        symbol = f"{frm}/{to}"
        spot_info = fetch_av_rate(frm, to, av_key)
        content = build_item_content(symbol, spot_info, generated_at)

        # Add to RSS
        feed.add_item(
            title=content["title"],
            link=content["link"],
            description=content["description"],
            pubdate=generated_at,
        )

        # Mirror to JSON
        items_out.append({
            "symbol": symbol,
            "title": content["title"],
            "link": content["link"],
            "generated": fmt_ts(generated_at),
            "spot": spot_info or {},
            "description_html": content["description"],
        })

    # Write RSS
    with open("rss.xml", "w", encoding="utf-8") as f:
        feed.write(f, "utf-8")

    # Write JSON mirror
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump({"generated": fmt_ts(generated_at), "items": items_out}, f, indent=2)

    print("✅ Feed generated successfully: output.json + rss.xml")


if __name__ == "__main__":
    main()
