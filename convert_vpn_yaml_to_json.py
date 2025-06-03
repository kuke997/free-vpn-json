
import json
from pathlib import Path

# 假设你已有的爬虫输出文件路径
INPUT_PATH = Path("./raw_nodes.yaml")  # 或 .json，根据你实际情况
OUTPUT_PATH = Path("./public/vpn_nodes.json")

# 示例：从 YAML 加载并提取关键信息
import yaml

def convert_yaml_to_json(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    output = []
    for node in data.get('proxies', []):
        item = {
            "remarks": node.get("name", "Free VPN Node"),
            "type": node.get("type", "vmess"),
            "country": node.get("country", "Unknown"),
            "subscription": node.get("link", "")  # 或 node['url'] 等字段名
        }
        output.append(item)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✅ Exported {len(output)} VPN nodes to {output_path}")

if __name__ == "__main__":
    convert_yaml_to_json(INPUT_PATH, OUTPUT_PATH)
