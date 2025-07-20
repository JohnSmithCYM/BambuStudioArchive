import os
import requests
from tqdm import tqdm
import json


# 下载文件的函数
def download_file(url, output_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total = int(r.headers.get('content-length', 0))
        with open(output_path, 'wb') as f, tqdm(
            desc=output_path,
            total=total,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))

# 从 JSON 获取下载链接并下载
def batch_download_from_json(json_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        versions = json.load(f)
    
    for v in versions:
        for key in ['win', 'mac']:
            url = v.get(key)
            if not url:
                continue
            filename = os.path.basename(url)
            output_path = os.path.join(output_dir, filename)

            if not os.path.exists(output_path):
                print(f"Downloading {key} for version {v['github'].split('/')[-1]}")
                try:
                    download_file(url, output_path)
                except Exception as e:
                    print(f"Failed to download {url}: {e}")
            else:
                print(f"{filename} already exists. Skipping download.")
                
# 用法
batch_download_from_json('C:/Users/malkey3/Documents/GitHub/BambuStudioArchive/python/bambu_studio_versions.json', 'E:/StudioDownload')
