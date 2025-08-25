import os
import json
import yaml
from datetime import datetime

def load_sources(file_path="sources.yml"):
    """Load sources from YAML file."""
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def generate_report(sources):
    """Generate a simple structured FX report from sources."""
    report = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "macro": [],
        "technicals": [],
        "setups": []
    }

    # For now we just dump sources — later you can expand to fetch headlines
    for src in sources.get("sources", []):
        report["macro"].append({
            "title": f"Macro update from {src['name']}",
            "url": src.get("url", ""),
            "note": "Placeholder until live fetch implemented."
        })

    return report

def save_report(report, output_file="output.json"):
    """Save the generated report to JSON file."""
    with open(output_file, "w") as f:
        json.dump(report, f, indent=2)

def main():
    sources = load_sources("sources.yml")
    report = generate_report(sources)
    save_report(report, "output.json")
    print("✅ Report generated successfully.")

if __name__ == "__main__":
    main()
