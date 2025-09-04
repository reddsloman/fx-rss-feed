import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import xml.etree.ElementTree as ET

# ---------------------------
# Helper: get timestamp in RFC 822 format
# ---------------------------
def get_rfc822_now():
    return datetime.now(pytz.UTC).strftime("%a, %d %b %Y %H:%M:%S GMT")

# ---------------------------
# Scrape Reuters headlines
# ---------------------------
def fetch_reuters():
    url = "https://www.reuters.com/markets/currencies/"
    resp = requests.get(url, timeout=20)
    soup = BeautifulSoup(resp.text, "html.parser")
    headlines = []
    for h in soup.select("a.story-card__headline__link")[:3]:
        headlines.append(h.get_text(strip=True))
    return headlines

# ---------------------------
# Scrape FXStreet technical levels
# ---------------------------
def fetch_fxstreet(pair_slug):
    url = f"https://www.fxstreet.com/currencies/{pair_slug}"
    resp = requests.get(url, timeout=20)
    soup = BeautifulSoup(resp.text, "html.parser")
    tech = []

    # Pivot levels / support / resistance
    levels = soup.select("table tr")
    for tr in levels[:4]:
        cols = [c.get_text(strip=True) for c in tr.find_all("td")]
        if cols:
            tech.append(" - ".join(cols))

    # Momentum indicators summary
    summary = soup.select_one(".technicalIndicatorsSummary")
    if summary:
        tech.append("Summary: " + summary.get_text(strip=True))

    return tech if tech else ["No data"]

# ---------------------------
# Build structured body
# ---------------------------
def build_item():
    now = get_rfc822_now()
    reuters_news = fetch_reuters()

    pairs = {
        "EUR/USD": "eurusd",
        "GBP/USD": "gbpusd",
        "USD/JPY": "usdjpy"
    }

    body = ""
    for name, slug in pairs.items():
        tech = fetch_fxstreet(slug)
        body += f"<strong>{name}</strong><br>\n"
        body += f"Macro: {reuters_news[0] if reuters_news else 'No fresh macro headline'} (Reuters).<br>\n"
        body += "Tech:<br>\n" + "<br>\n".join(tech) + "<br><br>\n"

    return now, body

# ---------------------------
# Write RSS file
# ---------------------------
def write_feed():
    now, body = build_item()

    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "FX Macro + Technical RSS Feed"
    ET.SubElement(channel, "link").text = "https://reddsloman.github.io/fx-rss-feed/"
    ET.SubElement(channel, "description").text = "Live updates with FX macro fundamentals, sentiment, technicals, and trade setups."
    ET.SubElement(channel, "lastBuildDate").text = now
    ET.SubElement(channel, "language").text = "en-us"

    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = f"FX Market Update {now}"
    ET.SubElement(item, "link").text = "https://www.reuters.com/markets/currencies/"
    ET.SubElement(item, "description").text = body
    ET.SubElement(item, "pubDate").text = now
    ET.SubElement(item, "guid").text = f"fx-{now}"

    tree = ET.ElementTree(rss)
    tree.write("index.xml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    write_feed()
