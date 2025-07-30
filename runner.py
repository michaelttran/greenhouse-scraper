"""
    - Add flags in main
        - output to terminal
        - output to csv
"""
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import requests

from constants import BASE_URL
from filters import (
    allowlist_job_titles, block_list, 
    allowlist_locations, companies
)
from utilities import pretty_print_json

ALL_JOBS = {}

def has_partial_match(string_to_search, list_to_compare=allowlist_job_titles):
    for str_in_list in list_to_compare:
       if str_in_list in string_to_search:
           return True
    return False

def has_blocked_match(string_to_search, list_to_compare=block_list):
    for str_in_list in list_to_compare:
        if str_in_list in string_to_search:
            return True
    return False

def is_paginated(soup):
    page_buttons = soup.find_all("button", class_="pagination__link")
    return len(page_buttons) > 1
   
def get_page_count(soup) -> int:
    page_buttons = soup.find_all("button", class_="pagination__link")
    last_page_numer = int(page_buttons[-1].get_text(strip=True))
    return last_page_numer

def get_pages(company_slug) -> int:
    url = BASE_URL + company_slug
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    if is_paginated(soup):
        num_pages = get_page_count(soup)
        return num_pages
    else:
        return 1

def generate_company_urls_to_scrape(company_slug, total_page_count) -> list:
    urls = []
    for page_num in range(1, total_page_count+1):
        formatted_urls = f"{BASE_URL}{company_slug}?page={page_num}"
        urls.append(formatted_urls)
    return urls

def scrape_greenhouse_job_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    job_rows = soup.select("tr.job-post")
    jobs = []

    for row in job_rows:
        title_tag = row.select_one("p.body.body--medium")
        location_tag = row.select_one("p.body__secondary.body--metadata")
        if title_tag:
            for span in title_tag.select("span"):
                span.decompose()

            job_title = title_tag.get_text(strip=True).lower()
            location = location_tag.get_text(strip=True).lower()

            if has_partial_match(job_title) and not has_blocked_match(job_title) and has_partial_match(location, allowlist_locations):
                link_tag = row.select_one("a")
                job_url = link_tag["href"]
                jobs.append({
                    "job_title": job_title,
                    "location": location,
                    "link": job_url
                })
    return jobs

def scrape_greenhouse_jobs(pages_to_scrape: list):
    jobs_at_company = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(scrape_greenhouse_job_page, url) for url in pages_to_scrape]
        for future in as_completed(futures):
            try:
                jobs_at_company.extend(future.result())
            except Exception as e:
                print(f"Error scraping a page: {e}")
        
    jobs_at_company.append({
        "metadata": {
            "num_pages_scraped": len(pages_to_scrape),
            "pages_scraped": pages_to_scrape
        }
    })
    return jobs_at_company

def main():
    ALL_JOBS["metadata"] = {
        "date_scraped": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "companies_scraped": companies
    }
    for company in companies:
        total_page_count = get_pages(company)
        pages_to_scrape = generate_company_urls_to_scrape(company, total_page_count)
        company_scraped_jobs = scrape_greenhouse_jobs(pages_to_scrape)
        ALL_JOBS[company] = company_scraped_jobs
    pretty_print_json(ALL_JOBS)

if __name__ == "__main__":
    print(f"Starting Script")

    main()

    print(f"Finished Script")