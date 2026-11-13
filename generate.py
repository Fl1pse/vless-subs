import requests
import base64
import json
from datetime import datetime

URL = "https://tiagorrg.github.io/vless-checker/keys.json"

def get_keys():
    r = requests.get(URL, timeout=15)
    r.raise_for_status()
    return r.json()

def make_subscription(keys_list):
    # Один ключ на строку
    content = "\n".join(keys_list)
    # Для совместимости делаем base64
    return base64.b64encode(content.encode("utf-8")).decode("utf-8")

def main():
    data = get_keys()
    
    normal_keys = []
    white_keys = []

    for key, value in data.items():
        if key == "updated_at":
            continue
            
        top10 = value.get("top10", [])
        if not top10:
            continue

        is_white = key.startswith("W_") or key.startswith("w_")
        
        for item in top10:
            vless = item.get("key")
            if vless and vless.startswith("vless://"):
                if is_white:
                    white_keys.append(vless)
                else:
                    normal_keys.append(vless)

    # Убираем дубликаты, сохраняя порядок
    normal_keys = list(dict.fromkeys(normal_keys))
    white_keys = list(dict.fromkeys(white_keys))

    with open("normal.txt", "w", encoding="utf-8") as f:
        f.write(make_subscription(normal_keys))

    with open("whitelist.txt", "w", encoding="utf-8") as f:
        f.write(make_subscription(white_keys))

    print(f"Normal keys: {len(normal_keys)}")
    print(f"Whitelist keys: {len(white_keys)}")
    print(f"Updated at: {datetime.utcnow().isoformat()}")

if __name__ == "__main__":
    main()
