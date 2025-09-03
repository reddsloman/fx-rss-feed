import datetime

def generate_rss():
    now = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>FX Macro + Technical RSS Feed</title>
<link>https://reddsloman.github.io/fx-rss-feed/</link>
<atom:link href="https://reddsloman.github.io/fx-rss-feed/index.xml" rel="self" type="application/rss+xml"/>
<description>Live updates with FX macro fundamentals, sentiment, technicals, and trade setups.</description>
<lastBuildDate>{now}</lastBuildDate>
<language>en-us</language>
<item>
<title>FX Market Update {now[:16]}</title>
<link>https://www.reuters.com/markets/currencies/</link>
<description>Macro fundamentals, sentiment, and technical trade setups updated.</description>
<pubDate>{now}</pubDate>
<guid isPermaLink="false">fx-{now}</guid>
</item>
</channel>
</rss>"""
    return rss

if __name__ == "__main__":
    content = generate_rss()
    with open("index.xml", "w", encoding="utf-8") as f:
        f.write(content)
