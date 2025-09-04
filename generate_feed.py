import datetime

# Always update timestamp
now = datetime.datetime.utcnow()
timestamp_rfc2822 = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
timestamp_id = now.strftime("%Y%m%d-%H%M%S")

rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>FX Macro + Technical RSS Feed</title>
<link>https://reddsloman.github.io/fx-rss-feed/</link>
<atom:link href="https://reddsloman.github.io/fx-rss-feed/index.xml" rel="self" type="application/rss+xml"/>
<description>
Live updates with FX macro fundamentals, sentiment, technicals, and trade setups.
</description>
<lastBuildDate>{timestamp_rfc2822}</lastBuildDate>
<language>en-us</language>

<item>
<title>FX Market Update {timestamp_rfc2822}</title>
<link>https://www.reuters.com/markets/currencies/</link>
<description>Macro fundamentals, sentiment, and technical trade setups updated.</description>
<pubDate>{timestamp_rfc2822}</pubDate>
<guid isPermaLink="false">{timestamp_id}</guid>
</item>

</channel>
</rss>
"""

# Write out new index.xml
with open("index.xml", "w", encoding="utf-8") as f:
    f.write(rss_content)

print(f"index.xml updated with timestamp {timestamp_rfc2822}")
