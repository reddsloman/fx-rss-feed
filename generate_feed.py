import os
import sys
import requests
import json
from datetime import datetime

# ==============================
# Utility: Fetch intraday FX data
# ==============================
def fetch_fx_intraday_av(frm: str, to: str, interval: str = "5min"):
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    if not api_key:
        print("⚠️ Warning: ALPHAVANTAGE_API_KEY not set. Skipping intraday fetch.")
        return {
            "from": frm,
            "to": to,
            "interval": interval,
            "data": []
        }

    url = (
        f"https://www.alphavantage.co/query"
        f"?function=FX_INTRADAY&from_symbol={frm}&to_symbol={to}"
        f"&interval={interval}&apikey={api_key}&outputsize=compact"
    )

    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        data = r.json()

        if "Time Series FX" not in data:
            print(f"⚠️ AlphaVantage returned unexpected response for {frm}/{to}: {data}")
            return {"from": frm, "to": to, "interval": interval, "data": []}

        return {
            "from": frm,
            "to": to,
            "interval": interval,
            "data": data["Time Series FX ({})".format(interval)]
        }

    except Exception as e:
        print(f"❌ Error fetching intraday data for {frm}/{to}: {e}")
        return {"from": frm, "to": to, "interval": interval, "data": []}


# ==============================
# Example placeholder snapshot
# ==============================
def tech_snapshot_for_pair(frm: str, to: str):
    intraday = fetch_fx_intraday_av(frm, to, "5min")
    if not intraday["data"]:
        return f"{frm}/{to}: intraday data unavailable (no API key or fetch error)."

    latest_time = sorted(intraday["data"].keys())[-1]
    latest_price = intraday["data"][latest_time]["4. close"]
    return f"{frm}/{to}: Last price {latest_price} at {latest_time}"


# ==============================
# Report builder
# ==============================
def build_report(sources_file: str):
    report = []
    pairs = [("EUR", "USD"), ("GBP", "USD"), ("USD", "JPY")]
    for frm, to in pairs:
        snap = tech_snapshot_for_pair(frm, to)
        report.append(snap)
    return "\n".join(report)


# ==============================
# Main entry point
# ==============================
def main():
    sources_file = os.path.join(os.getcwd(), "sources.yml")
    payload = build_report(sources_file)

    # Save as output.json for RSS workflow
    with open("output.json", "w") as f:
        json.dump({
            "timestamp": datetime.utcnow().isoformat(),
            "report": payload
        }, f, indent=2)

    print("✅ Report generated successfully.")


if __name__ == "__main__":
    main()
