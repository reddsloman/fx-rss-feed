import feedparser
from datetime import datetime, timezone
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import requests

# ---------- CONFIG ----------
FEED_TITLE = "FX Macro + Technical RSS Feed"
FEED_LINK = "https://reddsloman.github.io/fx-rss-feed/feed.xml"
FEED_DESCRIPTION = "Live updates with FX macro fundamentals, sentiment, technicals, and trade setups."
OUTPUT_FILE = "feed.xml"

# ---------- UTILS ----------
def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = tostring(elem, "utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def fetch_articles():
    """Stub for fetching live FX news & analysis (replace with API calls if needed)."""
    # Example placeholder entries to test updates
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    return [
        {
            "title": f"FX Market Update {now}",
            "link": "https://www.reuters.com/markets/currencies/",
            "description": "Macro fundamentals, sentiment, and technical trade setups updated.",
            "pubDate": now,
        }
    ]

# ---------- MAIN ----------
def generate_feed():
    rss = Element("rss", version="2.0")
    channel = SubElement(rss, "channel")

    # Metadata
    SubElement(channel, "title").text = FEED_TITLE
    SubElement(channel, "link").text = FEED_LINK
    SubElement(channel, "description").text = FEED_DESCRIPTION

    # Force-update timestamp every run
    now = datetime.now(timezone.utc)
    SubElement(channel, "lastBuildDate").text = now.strftime("%a, %d %b %Y %H:%M:%S %z")

    # Articles
    articles = fetch_articles()
    for art in articles:
        item = SubElement(channel, "item")
        SubElement(item, "title").text = art["title"]
        SubElement(item, "link").text = art["link"]
        SubElement(item, "description").text = art["description"]
        SubElement(item, "pubDate").text = art["pubDate"]

    # Save XML
    xml_str = prettify_xml(rss)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(xml_str)

if __name__ == "__main__":
    generate_feed()
