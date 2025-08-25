import yaml
import json
import os
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

# ---------------------------
# Utility: Load YAML sources
# ---------------------------
def load_sources(yaml_file):
    with open(yaml_file, "r") as f:
        return yaml.safe_load(f)

# ---------------------------
# Build JSON report (debug)
# ---------------------------
def build_json_report(sources):
    report = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "summary": "FX RSS Feed Auto-Update",
        "sources": sources,
    }
    return report

# ---------------------------
# Build RSS XML feed
# ---------------------------
def build_rss_feed(sources):
    rss = Element("rss", version="2.0")
    channel = SubElement(rss, "channel")

    # Channel metadata
    SubElement(channel, "title").text = "FX RSS Feed"
    SubElement(channel, "link").text = "https://reddsloman.github.io/fx-rss-feed/feed.xml"
    SubElement(channel, "description").text = "Automated FX Market Summaries and Technical Analysis"
    SubElement(channel, "lastBuildDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    # Add feed items from sources
    for src in sources.get("feeds", []):
        item = SubElement(channel, "item")
        SubElement(item, "title").text = src.get("title", "No title")
        SubElement(item, "link").text = src.get("url", "")
        SubElement(item, "description").text = src.get("summary", "")
        SubElement(item, "pubDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    return rss

# ---------------------------
# Main entry
# ---------------------------
def main():
    sources = load_sources("sources.yml")

    # Write JSON (debug)
    json_report = build_json_report(sources)
    with open("output.json", "w") as f:
        json.dump(json_report, f, indent=4)

    # Write RSS XML (real feed)
    rss_feed = build_rss_feed(sources)
    tree = ElementTree(rss_feed)
    tree.write("feed.xml", encoding="utf-8", xml_declaration=True)

    print("✅ Feed generated successfully: output.json + feed.xml")

if __name__ == "__main__":
    main()
