import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

# Updated to current working URL (without `www` and with correct path)
BASE_URL = "https://uhcprovider.com/en/policies-protocols/commercial-policies/commercial-medical-drug-policies.html"
# Save PDFs inside this project under ./data/uhc_policies
DOWNLOAD_DIR = "./data/uhc_policies"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

print(f"Requesting BASE_URL: {BASE_URL}")
response = requests.get(BASE_URL)
print(f"Initial page status code: {response.status_code}")

if not response.ok:
    print("Non-200 response received; exiting early.")
    exit(1)

soup = BeautifulSoup(response.text, "html.parser")

all_links = soup.find_all("a", href=True)
print(f"Total <a> tags with href found: {len(all_links)}")

pdf_links = []

for idx, link in enumerate(all_links):
    href = link["href"]

    # Debug: show a sample of hrefs being processed
    if idx < 20:
        print(f"[DEBUG] Link {idx} raw href: {href}")

    if ".pdf" in href.lower():
        print(f"[DEBUG] Potential PDF link found: {href}")
        if href.startswith("/"):
            # Fix scheme typo and make absolute
            href = "https://www.uhcprovider.com" + href
            print(f"[DEBUG] Converted relative to absolute: {href}")

        pdf_links.append(href)

print(f"Found {len(pdf_links)} PDFs after filtering for '.pdf' in href.")

for pdf_url in tqdm(pdf_links):
    file_name = pdf_url.split("/")[-1]
    file_path = os.path.join(DOWNLOAD_DIR, file_name)
    print(f"[DOWNLOAD] Fetching: {pdf_url} -> {file_path}")
    try:
        r = requests.get(pdf_url)
        print(f"[DOWNLOAD] Status code for {pdf_url}: {r.status_code}")

        if not r.ok:
            print(f"[ERROR] Skipping {pdf_url} due to non-200 status.")
            continue

        with open(file_path, "wb") as f:
            f.write(r.content)

    except Exception as e:
        print(f"[ERROR] Failed to download {pdf_url}: {e}")