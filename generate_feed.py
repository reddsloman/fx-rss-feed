from datetime import datetime

def generate_feed(items):
    # Always use current UTC time for lastBuildDate
    build_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>FX RSS Feed</title>
  <link>https://reddsloman.github.io/fx-rss-feed/</link>
  <description>Automated FX Market Summaries and Technical Analysis</description>
  <lastBuildDate>{build_date}</lastBuildDate>
  <atom:link href="https://reddsloman.github.io/fx-rss-feed/feed.xml"
             rel="self"
             type="application/rss+xml" />
"""

    for item in items:
        rss += f"""
  <item>
    <title>{item['title']}</title>
    <link>{item['link']}</link>
    <description><![CDATA[{item['description']}]]></description>
    <pubDate>{item['pubDate']}</pubDate>
    <guid>{item['link']}</guid>
  </item>
"""

    rss += """
</channel>
</rss>
"""
    return rss
