import requests
import json
from datetime import datetime

def fetch_releases():
    url = "https://api.github.com/repos/bambulab/BambuStudio/releases?per_page=100"
    res = requests.get(url)
    data = res.json()
    results = []

    for r in data:
        name = r.get("name", "").lower()
        if r.get("prerelease") or "beta" in name:
            continue

        tag = r["tag_name"]
        # 去掉前缀 v/V，并按点分割
        version_parts = tag.lstrip("vV").split(".")
        try:
            # 获取前三位数字（去掉前导零）
            version_nums = [str(int(p)) for p in version_parts[:3]]
        except ValueError:
            continue  # 遇到非法版本号，跳过

        # 筛选 1.7.0 及以上版本
        version_tuple = tuple(map(int, version_nums))
        if version_tuple < (1, 7, 0):
            continue

        short_version = "-".join(version_nums)
        github_url = r["html_url"]
        published_at = r.get("published_at", "")
        if published_at:
            release_date = published_at[:10]  # 取日期部分
        else:
            release_date = ""

        assets = {a["name"]: a["browser_download_url"] for a in r["assets"]}
        win = next((v for n, v in assets.items() if n.endswith(".exe")), None)
        mac = next((v for n, v in assets.items() if n.endswith(".dmg")), None)
        if not win or not mac:
            continue

        wiki_zh = f"https://wiki.bambulab.com/zh/software/bambu-studio/release/release-note-{short_version}"
        wiki_en = f"https://wiki.bambulab.com/en/software/bambu-studio/release/release-note-{short_version}"

        results.append({
            "tag": tag,
            "release_date": release_date,
            "github": github_url,
            "wiki_zh": wiki_zh,
            "wiki_en": wiki_en,
            "win": win,
            "mac": mac
        })

    return results

if __name__ == "__main__":
    all_versions = fetch_releases()
    with open("bambu_studio_versions.json", "w", encoding="utf-8") as f:
        json.dump(all_versions, f, indent=2, ensure_ascii=False)
    print("✅ 已保存为 bambu_studio_versions.json，共收录版本数：", len(all_versions))
