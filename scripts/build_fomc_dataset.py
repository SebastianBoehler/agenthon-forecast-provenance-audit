"""Executive summary: cache official dated FOMC statements and DGS10 outcomes."""
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

ROOT = Path("data/fomc-looped-pilot-v1")
BASE = "https://www.federalreserve.gov"
DATE_PATTERN = re.compile(r"(20\d{6})")
HEADERS = {"User-Agent": "Academic research data collection (contact: sebastian@sebastian-boehler.com)"}


def fetch(url):
    with urlopen(Request(url, headers=HEADERS), timeout=45) as response:
        return response.read()


def statement_links():
    pages = [f"{BASE}/monetarypolicy/fomchistorical{year}.htm" for year in range(2000, 2021)]
    pages.append(f"{BASE}/monetarypolicy/fomccalendars.htm")
    links = {}
    page_record = []
    for url in pages:
        raw = fetch(url)
        page_record.append({"url": url, "sha256": hashlib.sha256(raw).hexdigest()})
        for anchor in BeautifulSoup(raw, "html.parser").find_all("a", href=True):
            target = urljoin(BASE, anchor["href"])
            label = anchor.get_text(" ", strip=True)
            match = DATE_PATTERN.search(target)
            valid_label = (
                label == "HTML" and re.search(r"/monetary20\d{6}a\.htm$", target)
                if url.endswith("fomccalendars.htm") else label == "Statement"
            )
            if match and valid_label:
                stamp = match.group(1)
                if 2000 <= int(stamp[:4]) <= 2025 and stamp <= "2025-09-29".replace("-", ""):
                    links[target] = f"{stamp[:4]}-{stamp[4:6]}-{stamp[6:]}"
    return links, page_record


def get_statement(item):
    url, stamp = item
    raw = fetch(url)
    soup = BeautifulSoup(raw, "html.parser")
    article = soup.select_one("#article") or soup.body
    if article is None:
        raise ValueError(f"Official statement body missing: {url}")
    for bad in article.select("script,style,nav"):
        bad.decompose()
    text = " ".join(article.stripped_strings)
    if len(text) < 200:
        raise ValueError(f"Statement body unexpectedly short: {url}")
    return {"date": stamp, "url": url, "extractor": "article" if soup.select_one("#article") else "body", "sha256": hashlib.sha256(raw).hexdigest(),
            "text_sha256": hashlib.sha256(text.encode()).hexdigest(), "text": text}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    links, pages = statement_links()
    records = []
    failures = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(get_statement, item): item[0] for item in links.items()}
        for future in as_completed(futures):
            try:
                records.append(future.result())
            except Exception as exc:
                failures.append({"url": futures[future], "error": repr(exc)})
    records.sort(key=lambda r: (r["date"], r["url"]))
    csv_url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10"
    csv_bytes = fetch(csv_url)
    (ROOT / "dgs10.csv").write_bytes(csv_bytes)
    (ROOT / "statements.json").write_text(json.dumps(records, indent=2) + "\n")
    manifest = {"source_pages": pages, "statement_count": len(records), "failed_count": len(failures),
                "failures": failures, "dgs10_url": csv_url,
                "dgs10_sha256": hashlib.sha256(csv_bytes).hexdigest(),
                "date_range": [records[0]["date"], records[-1]["date"]]}
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({k: manifest[k] for k in ("statement_count", "failed_count", "date_range")}, indent=2))


if __name__ == "__main__":
    main()
