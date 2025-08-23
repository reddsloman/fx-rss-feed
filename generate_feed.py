#!/usr/bin/env python3
"""
Auto FX Session Updater: generates an RSS feed item each trading session with
- Macro headlines pulled from configurable RSS sources (Reuters et al.)
- Technical snapshot + orderflow bias for EUR/USD, GBP/USD, USD/JPY
- Trade setups (entries, stops, targets) using pivots + ATR + momentum filters

Requirements: see requirements.txt
Env: export ALPHAVANTAGE_API_KEY=your_key
"""

from __future__ import annotations
import os, sys, json, math, time, argparse, html
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

import requests
import pandas as pd
import numpy as np
import feedparser
import yaml

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", "").strip()

PAIRS = [
    ("EUR", "USD"),
    ("GBP", "USD"),
    ("USD", "JPY"),
]

# --- Utility formatting -------------------------------------------------------

def pip_round(value: float, pair: tuple[str,str]) -> float:
    """Round to realistic FX precision: JPY pairs to 2dp, others 4dp."""
    dp = 2 if "JPY" in pair else 4
    return round(float(value), dp)

def fmt_price(value: float, pair: tuple[str,str]) -> str:
    dp = 2 if "JPY" in pair else 4
    return f"{value:.{dp}f}"

def session_label_now() -> str:
    now_utc = datetime.now(timezone.utc)
    ny = now_utc.astimezone(ZoneInfo("America/New_York")).hour
    ln = now_utc.astimezone(ZoneInfo("Europe/London")).hour
    mn = now_utc.astimezone(ZoneInfo("Asia/Manila")).hour

    # Prioritize closest to an "open window"
    if 7 <= mn <= 11:
        return "Asia"
    if 7 <= ln <= 11:
        return "Europe"
    if 8 <= ny <= 12:
        return "US"
    # Fallback by UTC time bands
    h = now_utc.hour
    if 23 <= h or h < 5:
        return "Asia"
    if 5 <= h < 11:
        return "Europe"
    return "US"

# --- Data fetching ------------------------------------------------------------

def fetch_fx_intraday_av(frm: str, to: str, interval: str = "5min") -> pd.DataFrame:
    """Alpha Vantage intraday FX data (OHLC)."""
    if not ALPHAVANTAGE_API_KEY:
        raise RuntimeError("Missing ALPHAVANTAGE_API_KEY environment variable")
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "FX_INTRADAY",
        "from_symbol": frm,
        "to_symbol": to,
        "interval": interval,
        "apikey": ALPHAVANTAGE_API_KEY,
        "outputsize": "compact",
        "datatype": "json",
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    key = f"Time Series FX ({interval})"
    if key not in data:
        raise RuntimeError(f"AlphaVantage intraday response missing key: {data}")
    rows = []
    for ts, ohlc in data[key].items():
        rows.append((pd.to_datetime(ts, utc=True),
                     float(ohlc["1. open"]),
                     float(ohlc["2. high"]),
                     float(ohlc["3. low"]),
                     float(ohlc["4. close"])))
    df = pd.DataFrame(rows, columns=["time","open","high","low","close"]).sort_values("time")
    df.set_index("time", inplace=True)
    return df

def fetch_fx_daily_av(frm: str, to: str) -> pd.DataFrame:
    """Alpha Vantage daily FX data (OHLC)."""
    if not ALPHAVANTAGE_API_KEY:
        raise RuntimeError("Missing ALPHAVANTAGE_API_KEY environment variable")
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "FX_DAILY",
        "from_symbol": frm,
        "to_symbol": to,
        "apikey": ALPHAVANTAGE_API_KEY,
        "outputsize": "compact",
        "datatype": "json",
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    key = "Time Series FX (Daily)"
    if key not in data:
        raise RuntimeError(f"AlphaVantage daily response missing key: {data}")
    rows = []
    for ts, ohlc in data[key].items():
        rows.append((pd.to_datetime(ts, utc=True),
                     float(ohlc["1. open"]),
                     float(ohlc["2. high"]),
                     float(ohlc["3. low"]),
                     float(ohlc["4. close"])))
    df = pd.DataFrame(rows, columns=["date","open","high","low","close"]).sort_values("date")
    df.set_index("date", inplace=True)
    return df

# --- Indicators ---------------------------------------------------------------

def ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()

def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / (loss.replace(0, np.nan))
    rs = rs.replace([np.inf, -np.inf], np.nan).fillna(0)
    return 100 - (100 / (1 + rs))

def macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    macd_line = ema(series, fast) - ema(series, slow)
    signal_line = ema(macd_line, signal)
    hist = macd_line - signal_line
    return macd_line, signal_line, hist

def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high = df["high"]; low = df["low"]; close = df["close"]
    prev_close = close.shift(1)
    tr = pd.concat([high - low, (high - prev_close).abs(), (low - prev_close).abs()], axis=1).max(axis=1)
    return tr.rolling(period).mean()

def pivots_classic(prev_high: float, prev_low: float, prev_close: float) -> dict:
    P = (prev_high + prev_low + prev_close) / 3.0
    R1 = 2 * P - prev_low
    S1 = 2 * P - prev_high
    R2 = P + (prev_high - prev_low)
    S2 = P - (prev_high - prev_low)
    R3 = prev_high + 2 * (P - prev_low)
    S3 = prev_low - 2 * (prev_high - P)
    return {"P": P, "R1": R1, "S1": S1, "R2": R2, "S2": S2, "R3": R3, "S3": S3}

# --- Bias & Setups ------------------------------------------------------------

@dataclass
class TechSnapshot:
    close: float
    ema20: float
    ema50: float
    rsi14: float
    macd_hist: float
    atr14: float
    pivots: dict

def bias_from_snapshot(s: TechSnapshot) -> str:
    votes = 0
    votes += 1 if s.close > s.ema50 else -1
    votes += 1 if s.rsi14 > 50 else -1
    votes += 1 if s.macd_hist > 0 else -1
    if votes >= 2:
        return "bullish"
    if votes <= -2:
        return "bearish"
    return "neutral"

def build_setup(pair: tuple[str,str], snap: TechSnapshot) -> dict:
    b = bias_from_snapshot(snap)
    p = snap.pivots
    a = snap.atr14
    close = snap.close

    def rr_format(x): return fmt_price(x, pair)

    setup = {"bias": b}

    if b == "bullish":
        entry = p["S1"]
        stop = p["S2"] - 0.25 * a
        tp1 = p["R1"]
        tp2 = p["R2"]
    elif b == "bearish":
        entry = p["R1"]
        stop = p["R2"] + 0.25 * a
        tp1 = p["S1"]
        tp2 = p["S2"]
    else:
        # Neutral: breakout pair of ideas
        entry = None
        stop = None
        tp1 = None
        tp2 = None
        setup["alt_buy_breakout"] = {
            "entry_above": rr_format(p["R1"] + 0.25 * a),
            "stop_below": rr_format(p["P"] - 0.25 * a),
            "tp": rr_format(p["R2"])
        }
        setup["alt_sell_breakdown"] = {
            "entry_below": rr_format(p["S1"] - 0.25 * a),
            "stop_above": rr_format(p["P"] + 0.25 * a),
            "tp": rr_format(p["S2"])
        }

    if b in ("bullish","bearish"):
        setup["entry"] = rr_format(entry)
        setup["stop"] = rr_format(stop)
        setup["tp1"] = rr_format(tp1)
        setup["tp2"] = rr_format(tp2)

    setup["spot"] = rr_format(close)
    setup["pivots"] = {k: rr_format(v) for k, v in p.items()}
    setup["rsi14"] = round(float(snap.rsi14), 2)
    setup["ema20"] = rr_format(snap.ema20)
    setup["ema50"] = rr_format(snap.ema50)
    setup["macd_hist"] = round(float(snap.macd_hist), 6)
    setup["atr14"] = rr_format(a)
    return setup

# --- Macro headlines ----------------------------------------------------------

def fetch_headlines(sources_yml_path: str, limit: int = 6) -> list[dict]:
    headlines = []
    try:
        with open(sources_yml_path, "r") as f:
            cfg = yaml.safe_load(f) or {}
    except Exception as e:
        cfg = {}

    feeds = []
    for _, urls in (cfg or {}).items():
        feeds.extend(urls or [])

    for url in feeds:
        try:
            d = feedparser.parse(url)
            for entry in d.entries[:2]:  # take top 2 from each feed
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()
                published = entry.get("published", "") or entry.get("updated", "")
                if title and link:
                    headlines.append({"title": title, "link": link, "published": published})
        except Exception:
            continue

    # dedupe by title
    seen = set()
    deduped = []
    for h in headlines:
        if h["title"] in seen:
            continue
        seen.add(h["title"])
        deduped.append(h)
    return deduped[:limit]

# --- Core generation ----------------------------------------------------------

def tech_snapshot_for_pair(frm: str, to: str) -> TechSnapshot:
    intraday = fetch_fx_intraday_av(frm, to, "5min")
    daily = fetch_fx_daily_av(frm, to)
    last_close = intraday["close"].iloc[-1]
    ema20_val = ema(intraday["close"], 20).iloc[-1]
    ema50_val = ema(intraday["close"], 50).iloc[-1]
    rsi14_val = rsi(intraday["close"], 14).iloc[-1]
    macd_line, signal_line, hist = macd(intraday["close"])
    macd_hist_val = hist.iloc[-1]

    # pivots from previous day's HLC
    prev_day = daily.iloc[:-1].iloc[-1]
    piv = pivots_classic(prev_day["high"], prev_day["low"], prev_day["close"])
    atr14_val = atr(daily, 14).iloc[-1]

    return TechSnapshot(
        close=float(last_close),
        ema20=float(ema20_val),
        ema50=float(ema50_val),
        rsi14=float(rsi14_val),
        macd_hist=float(macd_hist_val),
        atr14=float(atr14_val),
        pivots=piv
    )

def build_report(sources_yml_path: str) -> dict:
    ts = datetime.now(timezone.utc)
    session = session_label_now()

    macro = fetch_headlines(sources_yml_path, limit=6)

    setups = {}
    for frm, to in PAIRS:
        snap = tech_snapshot_for_pair(frm, to)
        setups[f"{frm}/{to}"] = build_setup((frm,to), snap)

    return {
        "generated_at_utc": ts.isoformat(),
        "session": session,
        "macro_headlines": macro,
        "setups": setups
    }

# --- RSS feed utilities -------------------------------------------------------

def load_items_db(path: str) -> list[dict]:
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_items_db(path: str, items: list[dict]):
    with open(path, "w") as f:
        json.dump(items, f, indent=2)

def html_report_from_payload(payload: dict) -> str:
    ts = html.escape(payload["generated_at_utc"])
    session = html.escape(payload["session"])
    pieces = [f"<p><strong>Session:</strong> {session} | <strong>Generated (UTC):</strong> {ts}</p>"]

    if payload.get("macro_headlines"):
        pieces.append("<h3>Macro Headlines</h3><ul>")
        for h in payload["macro_headlines"]:
            t = html.escape(h["title"])
            l = html.escape(h["link"])
            pieces.append(f'<li><a href="{l}">{t}</a></li>')
        pieces.append("</ul>")

    pieces.append("<h3>Trade Setups</h3>")
    for pair, data in payload["setups"].items():
        pieces.append(f"<h4>{pair}</h4>")
        pieces.append("<ul>")
        pieces.append(f"<li>Spot: {data['spot']} | Bias: {html.escape(data['bias'])}</li>")
        if "entry" in data:
            pieces.append(f"<li>Entry: {data['entry']} | SL: {data['stop']} | TP1: {data['tp1']} | TP2: {data['tp2']}</li>")
        else:
            altb = data.get("alt_buy_breakout", {})
            alts = data.get("alt_sell_breakdown", {})
            pieces.append("<li>Neutral Play:</li>")
            pieces.append("<li>Buy Breakout: entry &gt; {0}, SL &lt; {1}, TP {2}</li>".format(
                altb.get("entry_above","-"), altb.get("stop_below","-"), altb.get("tp","-")))
            pieces.append("<li>Sell Breakdown: entry &lt; {0}, SL &gt; {1}, TP {2}</li>".format(
                alts.get("entry_below","-"), alts.get("stop_above","-"), alts.get("tp","-")))
        piv = data["pivots"]
        pieces.append(f"<li>Pivots: P {piv['P']} | R1 {piv['R1']} | S1 {piv['S1']} | R2 {piv['R2']} | S2 {piv['S2']}</li>")
        pieces.append(f"<li>RSI14: {data['rsi14']} | EMA20: {data['ema20']} | EMA50: {data['ema50']} | MACD Hist: {data['macd_hist']} | ATR14: {data['atr14']}</li>")
        pieces.append("</ul>")
    return "\n".join(pieces)

def write_rss(feed_path: str, items_db_path: str, payload: dict, max_items: int = 60):
    items = load_items_db(items_db_path)
    now = datetime.now(timezone.utc)
    guid = now.strftime("%Y%m%d%H%M%S")
    title = f"FX Session Plan — {payload['session']} — {now.strftime('%Y-%m-%d %H:%M UTC')}"
    link = "https://example.com/fx-session-feed"  # optional; replace with your repo page
    description = html_report_from_payload(payload)

    items.append({
        "guid": guid,
        "title": title,
        "link": link,
        "pubDate": now.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "description": description
    })
    items = items[-max_items:]
    save_items_db(items_db_path, items)

    # build RSS
    rss_items = []
    for it in reversed(items):  # newest first
        rss_items.append(f"""
  <item>
    <title>{html.escape(it['title'])}</title>
    <link>{html.escape(it['link'])}</link>
    <guid isPermaLink="false">{html.escape(it['guid'])}</guid>
    <pubDate>{html.escape(it['pubDate'])}</pubDate>
    <description><![CDATA[{it['description']}]]></description>
  </item>""")

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>FX Session Feed</title>
  <link>{html.escape(link)}</link>
  <description>Automated EUR/USD, GBP/USD, USD/JPY session plans</description>
  <language>en-us</language>
  <lastBuildDate>{items[-1]['pubDate']}</lastBuildDate>
{''.join(rss_items)}
</channel>
</rss>
"""
    with open(feed_path, "w") as f:
        f.write(rss)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", default="config/sources.yml", help="YAML with RSS URLs")
    ap.add_argument("--out", default="feed.xml", help="RSS output path")
    ap.add_argument("--itemsdb", default="data/items.json", help="Internal item store")
    args = ap.parse_args()

    payload = build_report(args.sources)
    os.makedirs(os.path.dirname(args.itemsdb), exist_ok=True)
    write_rss(args.out, args.itemsdb, payload, max_items=60)
    print(f"Wrote RSS to {args.out} with session {payload['session']}")

if __name__ == "__main__":
    main()
