import datetime
import feedgenerator


def generate_post():
    now = datetime.datetime.utcnow()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S UTC")

    # --- Each currency section grouped here ---
    eurusd = f"""
EUR/USD — Macro & Technical — {timestamp}

Macro snapshot
- Macro watch: central bank guidance, front-end rates, and incoming tier-1 data.
- Sentiment: track risk proxies (equities, credit, volatility) for USD impulses.
- Calendar: next 24–48h data and public remarks relevant to the pair.

Technical snapshot
- Reference rails: n/a (no spot)
"""

    gbpusd = f"""
GBP/USD — Macro & Technical — {timestamp}

Macro snapshot
- Macro watch: BoE forward guidance, UK fiscal stance, and global risk appetite.
- Sentiment: GBP reacts to both UK-specific and broader USD/risk drivers.
- Calendar: monitor data and speeches that impact UK and US rates.

Technical snapshot
- Reference rails: n/a (no spot)
"""

    usdjpy = f"""
USD/JPY — Macro & Technical — {timestamp}

Macro snapshot
- Macro watch: BoJ policy stance, yield spread drivers, and US Treasury direction.
- Sentiment: track equity vol and US-Japan rate differentials.
- Calendar: upcoming Japanese and US events relevant to the pair.

Technical snapshot
- Reference rails: n/a (no spot)
"""

    # Combine into single grouped post
    body = f"""
Generated: {timestamp}

---
{eurusd}
---
{gbpusd}
---
{usdjpy}
"""

    return {
        "title": f"FX Macro + Technical (Auto) — {timestamp}",
        "link": "https://github.com/reddsloman/fx-rss-feed",
        "description": body,
        "pubdate": now,
    }


def generate_feed():
    feed = feedgenerator.Rss201rev2Feed(
        title="FX Macro + Technical (Auto)",
        link="https://github.com/reddsloman/fx-rss-feed",
        description="Automated FX macro + technical snapshots for EUR/USD, GBP/USD, USD/JPY",
        language="en",
    )

    post = generate_post()
    feed.add_item(
        title=post["title"],
        link=post["link"],
        description=post["description"],
        pubdate=post["pubdate"],
    )

    with open("feed.xml", "w", encoding="utf-8") as f:
        feed.write(f, "utf-8")


if __name__ == "__main__":
    generate_feed()
