# greenhouse-scraper

----------------------
## Summary:
- Scrapes for jobs from different companies that use Greenhouse

----------------------

## How to use:
- Input companies you want to scrape jobs for in the filters file
- Filter the titles you want with `allowlist_job_titles` and `block_list`
- Filter the locations you want in `allowlist_locations`


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
