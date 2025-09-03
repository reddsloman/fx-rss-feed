import datetime

def generate_rss():
    now = datetime.datetime.utcnow()
    formatted = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    guid = now.strftime("fx-%Y%m%d-%H%M%S")

    rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>FX Macro + Technical RSS Feed</title>
<link>https://reddsloman.github.io/fx-rss-feed/</link>
<atom:link href="https://reddsloman.github.io/fx-rss-feed/index.xml" rel="self" type="application/rss+xml"/>
<description>Live updates with FX macro fundamentals, sentiment, technicals, and trade setups.</description>
<lastBuildDate>{formatted}</lastBuildDate>
<language>en-us</language>
<item>
<title>FX Market Update {formatted}</title>
<link>https://www.reuters.com/markets/currencies/</link>
<description>Macro fundamentals, sentiment, and technical trade setups updated.</description>
<pubDate>{formatted}</pubDate>
<guid isPermaLink="false">{guid}</guid>
</item>
</channel>
</rss>
"""
    with open("index.xml", "w", encoding="utf-8") as f:
        f.write(rss_content)

if __name__ == "__main__":
    generate_rss()
