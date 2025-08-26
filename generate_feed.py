import datetime
import pytz
from pathlib import Path

# Output file
output_file = Path("feed.xml")

def generate_feed():
    # Current UTC time
    now = datetime.datetime.now(pytz.UTC)
    timestamp = now.strftime("%Y%m%d-%H%M%S")
    pub_date = now.strftime("%a, %d %b %Y %H:%M:%S +0000")

    # Sample FX content (this should later pull live data)
    eurusd = "EUR/USD — ECB tone steady, Bund yields capped. Key levels: 1.1400 support, 1.1480 resistance."
    gbpusd = "GBP/USD — BoE cautious, UK gilt yields weighed. Levels: 1.3520 pivot, 1.3600 resistance."
    usdjpy = "USD/JPY — BoJ stance unchanged, JGB yields steady. Range: 143.50–144.80."
    usd = "USD — Fed outlook remains restrictive; US Treasury yields stable. Dollar index capped under 102.50."

    # RSS XML
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>FX Macro + Technical RSS Feed</title>
  <link>https://reddsloman.github.io/fx-rss-feed/feed.xml</link>
  <description>
    Hourly FX macro + technical updates covering USD, EUR, GBP, JPY with bond market flows, 
    central bank outlooks, and intraday trade setups.
  </description>
  <lastBuildDate>{pub_date}</lastBuildDate>

  <item>
    <title>FX Market Snapshot — {now.strftime("%b %d, %Y %H:%M UTC")}</title>
    <link>https://www.reuters.com/markets/currencies/</link>
    <guid isPermaLink="false">fx-{timestamp}</guid>
    <description><![CDATA[
      <b>{eurusd}</b><br/>
      <b>{gbpusd}</b><br/>
      <b>{usdjpy}</b><br/>
      <b>{usd}</b><br/>
    ]]></description>
    <pubDate>{pub_date}</pubDate>
  </item>

</channel>
</rss>
"""

    # Write file
    output_file.write_text(rss, encoding="utf-8")
    print(f"✅ Feed updated at {pub_date} with GUID fx-{timestamp}")

if __name__ == "__main__":
    generate_feed()
