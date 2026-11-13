import requests
import base64
from datetime import datetime

URL = "https://tiagorrg.github.io/vless-checker/keys.json"

def main():
    r = requests.get(URL, timeout=15)
    r.raise_for_status()
    data = r.json()

    normal_keys = []
    white_keys = []

    for key, value in data.items():
        if key == "updated_at":
            continue

        top10 = value.get("top10", [])
        if not top10:
            continue

        is_white = key.lower().startswith("w_")

        for item in top10:
            vless = item.get("key")
            if vless and vless.startswith("vless://"):
                if is_white:
                    white_keys.append(vless)
                else:
                    normal_keys.append(vless)

    # Убираем дубликаты
    normal_keys = list(dict.fromkeys(normal_keys))
    white_keys = list(dict.fromkeys(white_keys))

    def to_b64(keys):
        content = "\n".join(keys)
        return base64.b64encode(content.encode("utf-8")).decode("utf-8")

    with open("normal.txt", "w", encoding="utf-8") as f:
        f.write(to_b64(normal_keys))

    with open("whitelist.txt", "w", encoding="utf-8") as f:
        f.write(to_b64(white_keys))

    print(f"Normal: {len(normal_keys)} | White: {len(white_keys)}")

if __name__ == "__main__":
    main()
