from datetime import datetime, timezone

def generate_feed():
    # always use current UTC time (timezone-aware)
    now = datetime.now(timezone.utc)
    now_rfc2822 = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    now_id = now.strftime("%Y%m%d-%H%M%S")

    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>FX Macro + Technical RSS Feed</title>
  <link>https://reddsloman.github.io/fx-rss-feed/</link>
  <atom:link href="https://reddsloman.github.io/fx-rss-feed/index.xml" rel="self" type="application/rss+xml"/>
  <description>Live updates with FX macro fundamentals, sentiment, technicals, and trade setups.</description>
  <lastBuildDate>{now_rfc2822}</lastBuildDate>
  <language>en-us</language>

  <item>
    <title>FX Market Update – {now.strftime("%Y-%m-%d %H:%M:%S")} UTC</title>
    <link>https://www.reuters.com/markets/currencies/</link>
    <description><![CDATA[
      Macro fundamentals, sentiment, and technical trade setups updated.
    ]]></description>
    <pubDate>{now_rfc2822}</pubDate>
    <guid isPermaLink="false">fx-{now_id}</guid>
  </item>
</channel>
</rss>'''
    with open("index.xml", "w", encoding="utf-8") as f:
        f.write(xml)

    print(f"✅ Wrote index.xml successfully at {now_rfc2822}")

if __name__ == "__main__":
    generate_feed()
