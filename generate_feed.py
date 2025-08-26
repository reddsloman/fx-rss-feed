import datetime
import xml.etree.ElementTree as ET
import os

FEED_PATH = "rss.xml"
SITE_LINK = "https://reddsloman.github.io/fx-rss-feed/feed.xml"

def build_feed():
    # Current UTC timestamp
    now = datetime.datetime.utcnow()
    now_rfc2822 = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    now_iso = now.strftime("%Y-%m-%d %H:%M:%S UTC")

    # --------- CONTENT PLACEHOLDER (replace with live data later) ---------
    eurusd_macro = "Macro: ECB guidance, Bund yields, eurozone data watch."
    eurusd_tech = "Tech: key rails around spot EUR/USD (support/resistance)."

    gbpusd_macro = "Macro: BoE policy expectations, gilt curve, UK CPI flows."
    gbpusd_tech = "Tech: GBP/USD support/resistance rails."

    usdjpy_macro = "Macro: BoJ policy stance, JGB yields, risk sentiment flows."
    usdjpy_tech = "Tech: USD/JPY reference rails around spot."

    # Combined body
    body = f"""
    <h3>EUR/USD</h3>
    <p>{eurusd_macro}</p>
    <p>{eurusd_tech}</p>

    <h3>GBP/USD</h3>
    <p>{gbpusd_macro}</p>
    <p>{gbpusd_tech}</p>

    <h3>USD/JPY</h3>
    <p>{usdjpy_macro}</p>
    <p>{usdjpy_tech}</p>
    """

    # --------- BUILD RSS ---------
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = "FX RSS Feed"
    ET.SubElement(channel, "link").text = SITE_LINK
    ET.SubElement(channel, "description").text = "Automated FX Market Summaries and Technical Analysis"
    ET.SubElement(channel, "lastBuildDate").text = now_rfc2822

    # Single combined item
    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = f"FX Macro & Technical — {now_iso}"
    ET.SubElement(item, "link").text = SITE_LINK
    ET.SubElement(item, "pubDate").text = now_rfc2822
    ET.SubElement(item, "description").text = body

    # Save to file
    tree = ET.ElementTree(rss)
    tree.write(FEED_PATH, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    build_feed()
