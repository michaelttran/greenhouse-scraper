# threading
"""
Benchmarks:
    - Pre-threading: 51.41468405723572s || 529 partners
    - Post-threading: 5.155369997024536s || 529 partners
"""
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import re
import requests
import random
import time

from constants import BASE_URL, PARTNERS_URL

ALL_INTEGRATIONS = []

INTEGRATIONS_WITH_JOB_PAGE = []

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    )
}

def get_last_page_number() -> int:
    response = requests.get(f"{PARTNERS_URL}1")
    soup = BeautifulSoup(response.text, "html.parser")
    lis = soup.find("li", class_="last next page-item").select_one("a")
    page_num = lis["href"]
    match = re.search(r"page=(\d+)", page_num)
    if match:
        number = int(match.group(1))
        return number
    else:
        raise Exception(f"Couldn't find last page number with {PARTNERS_URL}")

def scrape_greenhouse_partners(url):
    response = requests.get(url)
    time.sleep(random.uniform(0, 1)) # TODO: Add this so their lb won't ban IP
    soup = BeautifulSoup(response.text, "html.parser")
    classes = soup.find_all(class_="pf-card card-grid__card card-grid__card-flat card-style-shadow")
    for c in classes:
        href = c.get("href")
        if href is None:
            continue
        match = re.search(r'^/[^/]+/(.+)$', href)
        if match:
            name = match.group(1)
            ALL_INTEGRATIONS.append(name)
        else:
            print(f"no match: href -> {href}")    

def get_partners(total_pages):
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scrape_greenhouse_partners, f"{PARTNERS_URL}{page}") for page in range(1, total_pages + 1)]

def check_partner_job_page_200(url, partner):
    response = requests.get(url, headers=HEADERS) # Some companies require headers
    if response.status_code == 200:
        INTEGRATIONS_WITH_JOB_PAGE.append(partner)
    if response.status_code != 200 and response.status_code != 404:
        print(f"{response.status_code} -- {partner}: {url} || {response.reason}")

def get_partner_job_page(BASE_URL):
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(check_partner_job_page_200, f"{BASE_URL}{partner}", partner) for partner in ALL_INTEGRATIONS]

def main():
    total_pages = get_last_page_number()
    print(f"total_pages: {total_pages}")
    
    get_partners(total_pages)

    start = time.time()
    get_partner_job_page(BASE_URL)
    end = time.time()
    print(f"total time: {end-start}")
    INTEGRATIONS_WITH_JOB_PAGE.sort()
    print(f"INTEGRATIONS_WITH_JOB_PAGE: {INTEGRATIONS_WITH_JOB_PAGE}")
    print(f"Found {len(INTEGRATIONS_WITH_JOB_PAGE)} partners' job pages")

if __name__ == "__main__":
    main()

