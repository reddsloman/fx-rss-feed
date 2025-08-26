import datetime
import os

FEED_FILE = "feed.xml"
FEED_TITLE = "FX RSS Feed"
FEED_LINK = "https://reddsloman.github.io/fx-rss-feed/feed.xml"
FEED_DESC = "Automated FX Market Summaries and Technical Analysis"

def generate_item(content: str) -> str:
    now = datetime.datetime.utcnow()
    pub_date = now.strftime("%a, %d %b %Y %H:%M:%S +0000")
    guid = f"fxrss-{now.strftime('%Y%m%d%H%M%S')}"
    title = f"FX Market Update — {now.strftime('%Y-%m-%d %H:%M UTC')}"
    link = f"https://reddsloman.github.io/fx-rss-feed/posts/{guid}.html"

    item = f"""
    <item>
      <title>{title}</title>
      <link>{link}</link>
      <description><![CDATA[
      {content}
      ]]></description>
      <pubDate>{pub_date}</pubDate>
      <guid isPermaLink="false">{guid}</guid>
    </item>
    """
    return item.strip()

def generate_feed(content: str):
    now = datetime.datetime.utcnow()
    build_date = now.strftime("%a, %d %b %Y %H:%M:%S +0000")

    # If feed exists, load old items
    items = []
    if os.path.exists(FEED_FILE):
        with open(FEED_FILE, "r", encoding="utf-8") as f:
            data = f.read()
            start = data.find("<item>")
            if start != -1:
                items_section = data[start:]
                items = items_section.split("</item>")
                items = [i + "</item>" for i in items if "<item>" in i]

    # Prepend new item
    new_item = generate_item(content)
    items.insert(0, new_item)

    # Limit history (optional, keep last 20 posts)
    items = items[:20]

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>{FEED_TITLE}</title>
<link>{FEED_LINK}</link>
<description>{FEED_DESC}</description>
<lastBuildDate>{build_date}</lastBuildDate>
{''.join(items)}
</channel>
</rss>
"""
    with open(FEED_FILE, "w", encoding="utf-8") as f:
        f.write(rss)

if __name__ == "__main__":
    # Example content (replace with actual macro+technical summary)
    sample_content = """
    EUR/USD — Macro & Technical snapshot
    GBP/USD — Macro & Technical snapshot
    USD/JPY — Macro & Technical snapshot
    Generated automatically.
    """
    generate_feed(sample_content)
