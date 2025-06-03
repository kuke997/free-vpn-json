import yaml
import json
from pathlib import Path

def convert():
    with open("raw_nodes.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    proxies = data.get("proxies", [])
    simplified = []
    for p in proxies:
        simplified.append({
            "name": p.get("name", "Free Node"),
            "type": p.get("type"),
            "server": p.get("server"),
            "port": p.get("port"),
            "uuid": p.get("uuid"),
            "cipher": p.get("cipher"),
            "link": p.get("link"),
            "country": p.get("country", "Unknown")
        })

    Path("public").mkdir(exist_ok=True)
    with open("public/vpn_nodes.json", "w", encoding="utf-8") as f:
        json.dump(simplified, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(simplified)} nodes to public/vpn_nodes.json")

if __name__ == "__main__":
    convert()
