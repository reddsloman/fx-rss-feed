import os
import json
import datetime
import xml.etree.ElementTree as ET

# ... [rest of your existing code above remains unchanged] ...

def save_json(payload, filename="output.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"💾 JSON saved to {filename}")

def save_rss(payload, filename="feed.xml"):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = "FX Market Feed"
    ET.SubElement(channel, "link").text = "https://github.com/reddsloman/fx-rss-feed"
    ET.SubElement(channel, "description").text = "Automated FX Macro + Technical Analysis Feed"
    ET.SubElement(channel, "lastBuildDate").text = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    for entry in payload.get("entries", []):
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = entry.get("title", "Untitled")
        ET.SubElement(item, "description").text = entry.get("summary", "")
        ET.SubElement(item, "pubDate").text = entry.get("date", datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"))
        ET.SubElement(item, "link").text = entry.get("link", "https://github.com/reddsloman/fx-rss-feed")

    tree = ET.ElementTree(rss)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"💾 RSS feed saved to {filename}")

def main():
    # build the report payload
    payload = build_report("sources.yml")

    # save JSON
    save_json(payload, "output.json")

    # save RSS
    save_rss(payload, "feed.xml")

    print("✅ Report generated successfully.")

if __name__ == "__main__":
    main()
