import yaml
import json
import re
import os

INPUT_YAML = "raw_nodes.yaml"
OUTPUT_JSON = os.path.join("public", "vpn_nodes.json")

# 简单关键词翻译映射
country_map = {
    "日本": "Japan",
    "香港": "Hong Kong",
    "新加坡": "Singapore",
    "美国": "United States",
    "印度": "India",
    "德国": "Germany",
    "广东省移动": "China Mobile Guangdong",
    "节点": "Node",
}

def translate(text):
    for zh, en in country_map.items():
        text = text.replace(zh, en)
    return text

def main():
    if not os.path.exists(INPUT_YAML):
        print(f"Error: {INPUT_YAML} not found.")
        return

    with open(INPUT_YAML, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, list):
        print(f"Error: Expected a list in {INPUT_YAML}, got {type(data)}")
        return

    translated_nodes = []

    for i, node in enumerate(data):
        if not isinstance(node, dict):
            print(f"Warning: Skipping item {i} because it's not a dict: {node}")
            continue

        if not node.get("server"):
            print(f"Warning: Skipping item {i} because 'server' field missing")
            continue

        name = translate(str(node.get("name", "")))
        country = translate(str(node.get("country", "Unknown")))
        server = node.get("server")
        port = node.get("port", 0)

        # 清除掉 '@ripaojiedian' 和类似标记
        name = re.sub(r"@[\w\-_.]+", "Telegram Group", name)

        translated_nodes.append({
            "name": name,
            "country": country,
            "server": server,
            "port": port
        })

    if not translated_nodes:
        print("Warning: No valid VPN nodes found.")

    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(translated_nodes, f, indent=2, ensure_ascii=False)

    print(f"Converted {len(translated_nodes)} nodes to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
