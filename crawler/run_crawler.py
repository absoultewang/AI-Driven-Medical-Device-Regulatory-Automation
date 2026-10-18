# Minimal crawler example using requests (for PoC). Replace with Scrapy + Playwright for production
import requests
import os

TARGETS = [
    "https://www.nmpa.gov.cn/",
]

def run():
    os.makedirs('snapshots', exist_ok=True)
    for url in TARGETS:
        r = requests.get(url)
        h = str(abs(hash(url)))
        path = os.path.join('snapshots', f"{h}.html")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(r.text)
        print('Saved', path)

if __name__ == '__main__':
    run()
