import yaml
import json
import re

with open("raw_nodes.yaml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

translated_nodes = []

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

for node in data:
    # 避免重复字段
    if not node.get("server"):
        continue
    name = translate(str(node.get("name", "")))
    country = translate(str(node.get("country", "")))
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

with open("vpn_nodes.json", "w", encoding="utf-8") as f:
    json.dump(translated_nodes, f, indent=2, ensure_ascii=False)
