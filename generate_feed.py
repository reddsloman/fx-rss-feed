import requests
from bs4 import BeautifulSoup
from datetime import datetime
from xml.sax.saxutils import escape

PAIRS = {
    'EUR/USD': 'eur-usd',
    'GBP/USD': 'gbp-usd',
    'USD/JPY': 'usd-jpy'
}
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def fetch_fxstreet_technical(pair_slug):
    url = f'https://www.fxstreet.com/rates-charts/{pair_slug}/technical'
    res = requests.get(url, headers=HEADERS, timeout=10)
    if res.status_code != 200:
        return None
    soup = BeautifulSoup(res.text, 'html.parser')
    levels, indicators = {}, {}

    for row in soup.select('table tr'):
        cols = row.find_all('td')
        if len(cols) == 2:
            label = cols[0].get_text(strip=True)
            value = cols[1].get_text(strip=True)
            if 'Support' in label or 'Resistance' in label:
                levels[label] = value

    for row in soup.select('.technicalIndicatorsTable tr'):
        cols = row.find_all('td')
        if len(cols) == 3:
            name = cols[0].get_text(strip=True)
            value = cols[1].get_text(strip=True)
            signal = cols[2].get_text(strip=True)
            indicators[name] = f"{value} ({signal})"
    return levels, indicators

def generate_item(pair_name, levels, indicators, updated_time):
    content_lines = []
    for k in sorted(levels): content_lines.append(f"{k}: {levels[k]}")
    for k in sorted(indicators): content_lines.append(f"{k}: {indicators[k]}")
    content_lines.append(f"\nLast Updated: {updated_time} UTC")
    description = escape("\n".join(content_lines))
    return f"""
    <item>
        <title>{pair_name} Technical Update – {levels.get('Support 1', 'N/A')} holds as key support</title>
        <link>https://www.fxstreet.com/rates-charts/{PAIRS[pair_name]}/technical</link>
        <description>{description}</description>
        <pubDate>{updated_time} GMT</pubDate>
        <guid isPermaLink="false">{pair_name}-{updated_time}</guid>
    </item>
    """

def generate_rss():
    now = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S')
    items = []
    for name, slug in PAIRS.items():
        try:
            levels, indicators = fetch_fxstreet_technical(slug)
            item = generate_item(name, levels, indicators, now)
            items.append(item)
        except:
            continue

    rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
    <channel>
        <title>FX Technical Analysis Feed</title>
        <link>https://reddsloman.github.io/fx-rss-feed</link>
        <description>Live EUR/USD, GBP/USD, USD/JPY technical analysis feed</description>
        <lastBuildDate>{now} GMT</lastBuildDate>
        {''.join(items)}
    </channel>
    </rss>"""

    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(rss_content)

if __name__ == "__main__":
    generate_rss()
