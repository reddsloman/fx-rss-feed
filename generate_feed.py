import feedgenerator
import datetime
import json
import os

def build_report(source_file):
    # Placeholder: Replace with actual logic for fetching + consolidating data
    return {
        "title": "FX RSS Feed",
        "link": "https://reddsloman.github.io/fx-rss-feed/rss.xml",
        "description": "Automated FX Macro + Technical Analysis Feed",
        "items": [
            {
                "title": "EUR/USD Technical Update",
                "link": "https://www.fxstreet.com/currencies/eurusd",
                "description": "Latest EUR/USD technical levels and sentiment.",
                "pubdate": datetime.datetime.utcnow(),
            },
            {
                "title": "GBP/USD Technical Update",
                "link": "https://www.fxstreet.com/currencies/gbpusd",
                "description": "Latest GBP/USD technical levels and sentiment.",
                "pubdate": datetime.datetime.utcnow(),
            },
            {
                "title": "USD/JPY Technical Update",
                "link": "https://www.fxstreet.com/currencies/usdjpy",
                "description": "Latest USD/JPY technical levels and sentiment.",
                "pubdate": datetime.datetime.utcnow(),
            },
        ],
    }

def main():
    payload = build_report("sources.yml")

    # Save JSON copy
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=str)

    # Create RSS feed
    feed = feedgenerator.Rss201rev2Feed(
        title=payload["title"],
        link=payload["link"],
        description=payload["description"],
        language="en",
    )

    for item in payload["items"]:
        feed.add_item(
            title=item["title"],
            link=item["link"],
            description=item["description"],
            pubdate=item["pubdate"],
        )

    # Write directly to rss.xml
    with open("rss.xml", "w", encoding="utf-8") as f:
        feed.write(f, "utf-8")

    print("✅ Feed generated successfully: output.json + rss.xml")

if __name__ == "__main__":
    main()
