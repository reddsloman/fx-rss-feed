from datetime import datetime, timezone
import xml.etree.ElementTree as ET

def generate_feed():
    now = datetime.now(timezone.utc)
    # RFC-822 format required by RSS
    now_rfc822 = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    # For GUID uniqueness
    now_iso = now.strftime("%Y%m%d%H%M%S")

    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    # Channel metadata
    ET.SubElement(channel, "title").text = "FX Macro & Technical"
    ET.SubElement(channel, "link").text = "https://reddsloman.github.io/fx-rss-feed/feed.xml"
    ET.SubElement(channel, "description").text = "Auto-updating FX Macro + Technical Analysis feed"
    ET.SubElement(channel, "lastBuildDate").text = now_rfc822
    ET.SubElement(channel, "pubDate").text = now_rfc822
    ET.SubElement(channel, "generator").text = "Custom Python RSS Generator"

    # Example item
    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = f"FX Macro + Technical (Auto) / {now_rfc822}"
    ET.SubElement(item, "link").text = "https://reddsloman.github.io/fx-rss-feed/"
    ET.SubElement(item, "guid", isPermaLink="false").text = f"fx-feed-{now_iso}"
    ET.SubElement(item, "pubDate").text = now_rfc822
    ET.SubElement(item, "description").text = """
    <b>EUR/USD</b><br/>
    Macro: ECB guidance, Bund yields, eurozone data watch.<br/>
    Tech: Key support/resistance levels.<br/><br/>
    <b>GBP/USD</b><br/>
    Macro: BoE policy expectations, gilt curve, UK CPI flows.<br/>
    Tech: GBP/USD support/resistance.<br/><br/>
    <b>USD/JPY</b><br/>
    Macro: BoJ policy stance, JGB yields, risk sentiment flows.<br/>
    Tech: USD/JPY key reference levels.
    """

    # Write to feed.xml
    tree = ET.ElementTree(rss)
    tree.write("feed.xml", encoding="utf-8", xml_declaration=True)
