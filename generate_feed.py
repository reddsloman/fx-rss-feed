import datetime

def generate_feed(items, output_file="feed.xml"):
    now = datetime.datetime.utcnow()
    build_date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>FX RSS Feed</title>
  <link>https://reddsloman.github.io/fx-rss-feed/feed.xml</link>
  <description>Automated FX Market Summaries and Technical Analysis</description>
  <lastBuildDate>{build_date}</lastBuildDate>
  <atom:link href="https://reddsloman.github.io/fx-rss-feed/feed.xml" 
             rel="self" 
             type="application/rss+xml" />
"""

    # Add items
    for item in items:
        rss += f"""  <item>
    <title>{item['title']}</title>
    <link>{item['link']}</link>
    <guid isPermaLink="false">{item['guid']}</guid>
    <pubDate>{item['pubDate']}</pubDate>
    <description><![CDATA[{item['description']}]]></description>
  </item>
"""

    rss += """</channel>
</rss>
"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rss)

    print(f"✅ RSS feed generated: {output_file}")


if __name__ == "__main__":
    # Example usage
    items = [
        {
            "title": "FX Market Update – Sample",
            "link": "https://reddsloman.github.io/fx-rss-feed/feed.xml",
            "guid": "20250826-022252",
            "pubDate": "Tue, 26 Aug 2025 02:22:52 GMT",
            "description": "USD: DXY consolidates near 104.80.<br>EUR/USD: 1.1420 support, 1.1500 resistance."
        }
    ]
    generate_feed(items)
