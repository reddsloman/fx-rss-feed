import feedgenerator
from datetime import datetime, timezone
import os

def generate_feed():
    # Always use current UTC time for feed freshness
    now = datetime.now(timezone.utc)

    feed = feedgenerator.Rss201rev2Feed(
        title="FX Macro + Technical Analysis Feed",
        link="https://reddsloman.github.io/fx-rss-feed/",
        description="Automated updates on EUR/USD, GBP/USD, and USD/JPY with macro fundamentals and technical analysis.",
        language="en",
        lastBuildDate=now  # Force refresh each run
    )

    # Example items - in real workflow you’ll fetch from your scraping/summary logic
    items = [
        {
            "title": "EUR/USD Technical Levels & Macro Update",
            "link": "https://reddsloman.github.io/fx-rss-feed/eurusd",
            "description": "Latest EUR/USD support, resistance, and macro drivers.",
        },
        {
            "title": "GBP/USD Trading Setup & Market Sentiment",
            "link": "https://reddsloman.github.io/fx-rss-feed/gbpusd",
            "description": "Updated GBP/USD orderflow levels with fundamental bias.",
        },
        {
            "title": "USD/JPY Key Levels & Policy Divergence Watch",
            "link": "https://reddsloman.github.io/fx-rss-feed/usdjpy",
            "description": "USD/JPY focus on Fed-BoJ divergence and near-term pivot levels.",
        }
    ]

    # Add feed items with fresh pubDate
    for item in items:
        feed.add_item(
            title=item["title"],
            link=item["link"],
            description=item["description"],
            pubdate=now  # Always new timestamp
        )

    # Write feed.xml
    output_path = os.path.join(os.path.dirname(__file__), "feed.xml")
    with open(output_path, "w", encoding="utf-8") as f:
        feed.write(f, "utf-8")

if __name__ == "__main__":
    generate_feed()
