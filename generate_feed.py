import datetime

def generate_feed():
    now = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")

    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>FX Market RSS Feed</title>
    <link>https://reddsloman.github.io/fx-rss-feed/</link>
    <description>Automated FX market updates with macro, sentiment, and technical analysis</description>
    <language>en</language>
    <lastBuildDate>{now}</lastBuildDate>
    <pubDate>{now}</pubDate>
    <atom:link href="https://reddsloman.github.io/fx-rss-feed/feed.xml" rel="self" type="application/rss+xml" />

    <item>
      <title>Sample FX Update</title>
      <link>https://reddsloman.github.io/fx-rss-feed/</link>
      <guid isPermaLink="false">{now}</guid>
      <pubDate>{now}</pubDate>
      <description>EUR/USD, GBP/USD, USD/JPY market update snapshot.</description>
    </item>

  </channel>
</rss>
"""
    return feed

if __name__ == "__main__":
    xml = generate_feed()
    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(xml)
