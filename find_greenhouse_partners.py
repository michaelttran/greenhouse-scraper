"""
Benchmarks:
    - Pre-threading: 51.41468405723572s
"""
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import requests
import random
import time

from constants import PARTNERS_URL

def get_last_page_number() -> int:
    response = requests.get(f"{PARTNERS_URL}1")
    soup = BeautifulSoup(response.text, "html.parser")
    # HTML code: line number 13391
    lis = soup.find("li", class_="last next page-item").select_one("a")
    page_num = lis["href"]
    match = re.search(r"page=(\d+)", page_num)
    if match:
        number = int(match.group(1))
        return number
    else:
        raise Exception(f"Couldn't find last page number with {PARTNERS_URL}")

def scrape_greenhouse_partners(url):
    pass

def get_partners(total_pages):
    all_integrations = []
    for page in range(1, total_pages + 1):
        url = f"{PARTNERS_URL}{page}"
        response = requests.get(url)
        # time.sleep(random.uniform(0, 1)) # TODO: Add this so their lb won't ban IP
        soup = BeautifulSoup(response.text, "html.parser")
        classes = soup.find_all(class_="pf-card card-grid__card card-grid__card-flat card-style-shadow")
        for c in classes:
            href = c.get("href")
            if href is None:
                continue
            match = re.search(r'^/[^/]+/(.+)$', href)
            if match:
                name = match.group(1)
                print(f"matched: {name}")
                all_integrations.append(name)
            else:
                print(f"no match: href -> {href}")
    return all_integrations

def main():
    total_pages = get_last_page_number()
    print(f"total_pages: {total_pages}")
    start = time.time()
    partners = get_partners(total_pages)
    end = time.time()
    print(f"partners: {partners}")
    print(f"total time: {end-start}")

if __name__ == "__main__":
    main()

