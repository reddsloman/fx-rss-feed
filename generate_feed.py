import datetime
from xml.sax.saxutils import escape

def generate_feed():
    # Strict UTC timestamp
    now = datetime.datetime.now(datetime.timezone.utc)
    timestamp = now.strftime("%a, %d %b %Y %H:%M:%S GMT")

    # Channel metadata
    channel_title = "FX Macro + Technical"
    channel_link = "https://reddsloman.github.io/fx-rss-feed/"
    channel_description = "Automated FX Macro + Technical Analysis Feed"

    # Example items — can be replaced by live scrapes later
    items = [
        {
            "title": "EUR/USD",
            "description": "Macro: ECB guidance, Bund yields, eurozone data watch.<br/>Tech: key rails around spot EUR/USD (support/resistance).",
            "link": "https://reddsloman.github.io/fx-rss-feed/eurusd",
        },
        {
            "title": "GBP/USD",
            "description": "Macro: BoE policy expectations, gilt curve, UK CPI flows.<br/>Tech: GBP/USD support/resistance rails.",
            "link": "https://reddsloman.github.io/fx-rss-feed/gbpusd",
        },
        {
            "title": "USD/JPY",
            "description": "Macro: BoJ policy stance, JGB yields, risk sentiment flows.<br/>Tech: USD/JPY reference rails around spot.",
            "link": "https://reddsloman.github.io/fx-rss-feed/usdjpy",
        }
    ]

    # Build RSS feed
    rss_parts = []
    rss_parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    rss_parts.append('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">')
    rss_parts.append("<channel>")
    rss_parts.append(f"<title>{escape(channel_title)}</title>")
    rss_parts.append(f"<link>{channel_link}</link>")
    rss_parts.append(f"<description>{escape(channel_description)}</description>")
    rss_parts.append(f"<lastBuildDate>{timestamp}</lastBuildDate>")
    rss_parts.append(
        f'<atom:link href="{channel_link}feed.xml" rel="self" type="application/rss+xml" />'
    )

    # Add each item
    for item in items:
        rss_parts.append("<item>")
        rss_parts.append(f"<title>{escape(item['title'])}</title>")
        rss_parts.append(f"<link>{item['link']}</link>")
        rss_parts.append(f"<description>{item['description']}</description>")
        rss_parts.append(f"<pubDate>{timestamp}</pubDate>")
        rss_parts.append("</item>")

    rss_parts.append("</channel>")
    rss_parts.append("</rss>")

    return "\n".join(rss_parts)


if __name__ == "__main__":
    feed_content = generate_feed()
    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(feed_content)
