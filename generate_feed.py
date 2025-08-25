import datetime

# Mock fetch functions (replace with real data fetch)
def fetch_eurusd():
    return {
        "spot": "1.1420",
        "macro": "Central bank guidance, front-end rates, incoming tier-1 data.",
        "sentiment": "Watch risk proxies (equities, credit, volatility) for USD impulses.",
        "calendar": "Next 24–48h data and public remarks.",
        "technical": "Support 1.1380 | Resistance 1.1480"
    }

def fetch_gbpusd():
    return {
        "spot": "1.3550",
        "macro": "BoE guidance, UK data flow, USD drivers.",
        "sentiment": "Track gilt–UST spreads and equity tone.",
        "calendar": "UK data/events in next 48h.",
        "technical": "Support 1.3480 | Resistance 1.3620"
    }

def fetch_usdjpy():
    return {
        "spot": "144.40",
        "macro": "BoJ stance, US–Japan yield gap, risk mood.",
        "sentiment": "Equities/UST yields driving flows.",
        "calendar": "Japan/US releases in 24–48h.",
        "technical": "Support 143.50 | Resistance 145.50"
    }


def generate_post():
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    eurusd = fetch_eurusd()
    gbpusd = fetch_gbpusd()
    usdjpy = fetch_usdjpy()

    content = f"""
**FX Macro & Technical — {now}**

**EUR/USD (Spot: {eurusd['spot']})**  
- **Macro:** {eurusd['macro']}  
- **Sentiment:** {eurusd['sentiment']}  
- **Calendar:** {eurusd['calendar']}  
- **Technical:** {eurusd['technical']}  

**GBP/USD (Spot: {gbpusd['spot']})**  
- **Macro:** {gbpusd['macro']}  
- **Sentiment:** {gbpusd['sentiment']}  
- **Calendar:** {gbpusd['calendar']}  
- **Technical:** {gbpusd['technical']}  

**USD/JPY (Spot: {usdjpy['spot']})**  
- **Macro:** {usdjpy['macro']}  
- **Sentiment:** {usdjpy['sentiment']}  
- **Calendar:** {usdjpy['calendar']}  
- **Technical:** {usdjpy['technical']}  
"""

    return content

if __name__ == "__main__":
    print(generate_post())
