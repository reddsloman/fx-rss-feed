import os
import datetime

def generate_feed():
    now = datetime.datetime.utcnow()
    timestamp = now.strftime("%Y%m%d-%H%M")
    filename = f"feed-{timestamp}.xml"

    # Example feed content (replace with your actual content build)
    feed_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>FX RSS Feed</title>
  <link>https://reddsloman.github.io/fx-rss-feed/</link>
  <description>Live FX Macro + Technical Analysis</description>
  <lastBuildDate>{now.strftime("%a, %d %b %Y %H:%M:%S +0000")}</lastBuildDate>
  <atom:link href="https://reddsloman.github.io/fx-rss-feed/{filename}" rel="self" type="application/rss+xml" />

  <item>
    <title>FX Market Update {now.strftime("%Y-%m-%d %H:%M UTC")}</title>
    <link>https://reddsloman.github.io/fx-rss-feed/{filename}</link>
    <guid isPermaLink="false">{timestamp}</guid>
    <pubDate>{now.strftime("%a, %d %b %Y %H:%M:%S +0000")}</pubDate>
    <description>Auto-generated FX update</description>
  </item>
</channel>
</rss>
"""

    # Write rotating file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(feed_content)

    # Also write index.xml (always points to latest)
    with open("index.xml", "w", encoding="utf-8") as f:
        f.write(feed_content)

    print(f"Generated {filename} and updated index.xml")

if __name__ == "__main__":
    generate_feed()
