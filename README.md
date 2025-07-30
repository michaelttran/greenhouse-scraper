# greenhouse-scraper

----------------------
## Summary:
- Scrapes for jobs from different companies that use Greenhouse

----------------------

## How to use:
- Input companies you want to scrape jobs for in the filters file
- Filter the titles you want with `allowlist_job_titles` and `block_list`
- Filter the locations you want in `allowlist_locations`

- `find_greenhouse_partners.py` -> Scrapes through their partners, checks if the partner has a job page on Greenhouse with a 200 status, creates a list 
- `runner.py` -> Hits the partners' job page and parses through the page to filter for specific roles and locations

----------------------
## Installation
- `python3 -m virtualenv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `python runner.py`


----------------------
## TODO:
- CSV support
- Logging
- Flags to enable features from terminal
- Functionality to detect when partners' job pages have extra steps to get to the list of their roles
