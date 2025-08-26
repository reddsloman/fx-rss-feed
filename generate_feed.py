import datetime
import os

FEED_PATH = "feed.xml"

def generate_feed():
    now = datetime.datetime.utcnow()
    pub_date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    guid = now.strftime("%Y%m%d-%H%M%S")

    # Example market summary (you can replace this with live fetch later)
    market_summary = """USD: DXY consolidates near 104.80 as markets await Powell at Jackson Hole.<br>
    EUR/USD: Holding 1.1420 support, resistance 1.1500.<br>
    GBP/USD: Supported near 1.3550, capped at 1.3625.<br>
    USD/JPY: Rangebound 144.20–145.00.<br>"""

    rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>FX RSS Feed</title>
<link>https://reddsloman.github.io/fx-rss-feed/feed.xml</link>
<description>Automated FX Market Summaries and Technical Analysis</description>
<lastBuildDate>{pub_date}</lastBuildDate>

<item>
  <title>FX Market Update – {pub_date}</title>
  <link>https://reddsloman.github.io/fx-rss-feed/feed.xml</link>
  <guid isPermaLink="false">{guid}</guid>
  <pubDate>{pub_date}</pubDate>
  <description><![CDATA[{market_summary}]]></description>
</item>

</channel>
</rss>
"""

    with open(FEED_PATH, "w", encoding="utf-8") as f:
        f.write(rss_content)

if __name__ == "__main__":
    generate_feed()
