"""
    scrape <company> reviews given the review page url
    usage: $ python scraper.py <reviews_url>
    :reviews_url: url to the all reviews available for <company> on seek.com.au
    example: https://www.seek.com.au/companies/woolworths-supermarkets-432295/reviews
"""

from sys import argv
from scraper_utlis import fetch_review_link, save_links, fetch_reviews, save_reviews



if len(argv) != 2:
    print ("usage: $ scraper.py <reviews_url>")
else:
    reviews_url = argv[1]


all_links, total_pages, missed_pages, company_name = fetch_review_link(reviews_url)

print("\n--- for {} Company ---".format(company_name))
print("{} pages have been scraped.".format(total_pages))
print("{} pages failed to load. related links missed ...".format(missed_pages))
print("{} links have been collected.\n".format(len(all_links)))

if total_pages == 1 and len(all_links) == 0:
    print("WARNING!!  :  It is likely that the website has failed to load at all. Re-running the process is recommended.!\n")


if all_links:
    save_links(all_links, company_name)

print("fetching reviews ...")

columns, review_number, review_missed = fetch_reviews(all_links)

print("\n{} reviews have been collected.".format(review_number))
print("{} reviews have been missed.\n".format(review_missed))

if columns:
    save_reviews(columns, company_name)

print("Done!")