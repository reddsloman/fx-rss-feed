import json
from datetime import datetime, timezone
from feedgenerator import Rss201rev2Feed

# Generate RSS feed
feed = Rss201rev2Feed(
    title="FX RSS Feed",
    link="https://reddsloman.github.io/fx-rss-feed/rss.xml",
    description="Automated FX Macro + Technical Analysis Feed",
    language="en",
)

# Example items (replace these with dynamic content later)
items = [
    {
        "title": "EUR/USD Market Update",
        "link": "https://www.reuters.com",
        "description": "EUR/USD consolidates near key levels as traders watch ECB commentary.",
        "pubdate": datetime.now(timezone.utc),
    },
    {
        "title": "GBP/USD Market Update",
        "link": "https://www.bloomberg.com",
        "description": "GBP/USD edges higher on UK data surprises and BoE outlook.",
        "pubdate": datetime.now(timezone.utc),
    },
    {
        "title": "USD/JPY Market Update",
        "link": "https://www.fxstreet.com",
        "description": "USD/JPY trades steady with focus on BoJ policy stance.",
        "pubdate": datetime.now(timezone.utc),
    },
]

# Add items to RSS feed
for item in items:
    feed.add_item(**item)

# Write RSS XML
with open("rss.xml", "w", encoding="utf-8") as f:
    feed.write(f, "utf-8")

# Also create JSON output
json_output = {"items": items}
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(json_output, f, indent=4, default=str)

print("✅ Feed generated successfully: output.json + rss.xml")
