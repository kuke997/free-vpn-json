import requests
import yaml
import base64
import re
import socket

from pathlib import Path

# 示例：从订阅地址中提取 vmess/clash 格式节点
SUBSCRIPTION_URLS = [
    "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2",
    "https://raw.githubusercontent.com/freefq/free/master/v2",
]

def decode_base64(data: str) -> str:
    data += '=' * (-len(data) % 4)  # 修复 padding
    return base64.b64decode(data).decode('utf-8', errors='ignore')

def extract_vmess_links(content: str) -> list:
    return re.findall(r'vmess://[a-zA-Z0-9+/=]+', content)

def get_country_from_host(host):
    try:
        ip = socket.gethostbyname(host)
        # 简化判断，可对接 IP 归属库
        if ip.startswith("104.") or ip.startswith("172."): return "US"
        elif ip.startswith("203.") or ip.startswith("182."): return "India"
        return "Unknown"
    except:
        return "Unknown"

def parse_vmess_link(link: str) -> dict:
    raw = decode_base64(link[8:])
    data = yaml.safe_load(raw) if '{' in raw else {}
    return {
        "name": data.get("ps", "Free Node"),
        "type": "vmess",
        "server": data.get("add"),
        "port": data.get("port"),
        "uuid": data.get("id"),
        "alterId": data.get("aid", 0),
        "cipher": data.get("scy", "auto"),
        "link": link,
        "country": get_country_from_host(data.get("add", "")) if data.get("add") else "Unknown"
    }

def fetch_all_nodes():
    all_nodes = []
    for url in SUBSCRIPTION_URLS:
        try:
            print(f"🔗 Fetching from {url}")
            resp = requests.get(url, timeout=10)
            text = decode_base64(resp.text.strip())
            links = extract_vmess_links(text)
            nodes = [parse_vmess_link(link) for link in links]
            all_nodes.extend(nodes)
        except Exception as e:
            print(f"⚠️ Failed to fetch {url}: {e}")
    return all_nodes

if __name__ == '__main__':
    proxies = fetch_all_nodes()
    print(f"✅ Total nodes parsed: {len(proxies)}")

    output = {"proxies": proxies}
    Path("raw_nodes.yaml").write_text(yaml.safe_dump(output, allow_unicode=True))

