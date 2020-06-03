from sys import argv
from selenium import webdriver
from bs4 import BeautifulSoup
from tqdm import tqdm
import csv
import sys
sys.path.append("..")
from pathlib import Path


# HTML attributes used to scrape review links
LAST_REVIEW_PAGE_SELECTOR = "FQBghMU"
REVIEW_DIV_SELECTOR = "_1Y5kUMd"
REVIEW_LINK_SELECTOR = "_2gLKVsp"
COMPANY_NAME_SELECTOR = "_3FrNV7v _2e92Zkf E6m4BZb"


# HTML attributes used to scrape review data
TITLE_SELECTOR = "reviewCardFull-title"
ROLE_SELECTOR = "reviewCardFull-jobTitle"
REVIEW_SELECTOR_PROS = "reviewCardFull-pros"
REVIEW_SELECTOR_CONS = "reviewCardFull-cons"
RECOMMEND_SELECTOR = "reviewCardFull-companyRecommended"
SALARY_SELECTOR = "reviewCardFull-salarySummary"
DATE_SELECTOR = "reviewCardFull-dateCreated"
LOCATION_SELECTOR = "reviewCardFull-workLocation"
RATING_SELECTOR = "_1erK2ob"
RATING_SELECTOR_OVERALL = "reviewCardFull-starRatingCompanyOverall"
RATING_SELECTOR_CAREER = "reviewCardFull-starRatingCareerOpportunity"
RATING_SELECTOR_BALANCE = "reviewCardFull-starRatingWorkLifeBalance"
RATING_SELECTOR_ENVIRONMENT = "reviewCardFull-starRatingWorkEnvironment"
RATING_SELECTOR_MANAGEMENT = "reviewCardFull-starRatingExecutiveManagement"
RATING_SELECTOR_BENEFIT = "reviewCardFull-starRatingBenefitsAndPerks"
RATING_SELECTOR_DIVERSITY = "reviewCardFull-starRatingDiversity"


def fetch_review_link(reviews_url):
    """
    collect all urls each linked to a review for targeted company
    :reviews_url: reviews' page url provided by user
    returns a list of all the urls linked to reviews for targeted company
    """

    print("\nloading browser engine ...\n")
    driver = webdriver.Firefox()

    print("fetching all urls linked to reviews ...")

    page_number = 1
    page_missed = 0
    link_collection = []
    company_name = ""

    while(True):
        url = reviews_url + '?page={}'.format(page_number)
        driver.get(url)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        try:
            # to check if the page has been loaded completely
            links = soup.find('div', {'class' : REVIEW_DIV_SELECTOR}).find_all(
                'a', {'class' : REVIEW_LINK_SELECTOR})
        except:
            try:
                # try again to load the page if it fails at first attemp
                driver.get(url)
                html_content = driver.page_source
                soup = BeautifulSoup(html_content, 'html.parser')
                links = soup.find('div', {'class' : REVIEW_DIV_SELECTOR}).find_all(
                    'a', {'class' : REVIEW_LINK_SELECTOR})
            except:
                links = ""
                pass

        if not company_name:
            company_name = soup.find('span', {'class' : COMPANY_NAME_SELECTOR}).find('span').text

        if not links:
            page_missed += 1
        else:
            print("\nCollecting links ...")
            for link in tqdm(links):
                link_collection.append("https://www.seek.com.au{}".format(link['href']))

        if not soup.find('a', {'class' : LAST_REVIEW_PAGE_SELECTOR}):
            driver.close()
            break
        else:
            page_number += 1

    return link_collection, page_number, page_missed, company_name



def fetch_reviews(all_links, company_name):
    """
    collect reviews text and other data related to them
    :all_links: a list of all urls ecah linked to a review
    returns a dictionary of all reviews collected
    """

    columns = {
        "title": [],
        "job_title": [],
        "pros": [],
        "cons": [],
        "recommendation": [],
        "salary": [],
        "date": [],
        "location": [],
        "career_opportunity_rating": [],
        "work_life_balance_rating": [],
        "work_env_rating": [],
        "management_rating": [],
        "benefits_rating": [],
        "diversity_rating": [],
        "overall_rating": [],
        "company": []
    }

    review_number = 0
    review_missed = 0

    print("\nLoading browser engine ...\n")
    driver = webdriver.Firefox()

    for url in tqdm(all_links):
        driver.get(url)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        try:
            # to check if the page has been loaded completely
            load_check = soup.find('span', {'data-automation': TITLE_SELECTOR}).text
        except:
            try:
                # try again to load the page if it fails at first attemp
                driver.get(url)
                html_content = driver.page_source
                soup = BeautifulSoup(html_content, 'html.parser')
                load_check = soup.find('span', {'data-automation': TITLE_SELECTOR}).text
            except:
                load_check = False
                review_missed += 1
                pass

        if load_check:
            review_number += 1
            columns['title'].append(soup.find('span', {'data-automation': TITLE_SELECTOR}).text)
            columns['job_title'].append(soup.find('span', {'data-automation': ROLE_SELECTOR}).text)
            columns['pros'].append(soup.find('span', {'data-automation': REVIEW_SELECTOR_PROS}).text)
            columns['cons'].append(soup.find('span', {'data-automation': REVIEW_SELECTOR_CONS}).text)
            columns['recommendation'].append(soup.find('span', {'data-automation': RECOMMEND_SELECTOR}).text)
            columns['salary'].append(soup.find('span', {'data-automation': SALARY_SELECTOR}).text)
            columns['date'].append(soup.find('span', {'data-automation': DATE_SELECTOR}).text)
            columns['location'].append(soup.find('span', {'data-automation': LOCATION_SELECTOR}).text)
            columns['career_opportunity_rating'].append(
                soup.find('div', {'data-automation': RATING_SELECTOR_CAREER}).find('span', {'class': RATING_SELECTOR}).text)
            columns['work_life_balance_rating'].append(
                soup.find('div', {'data-automation': RATING_SELECTOR_BALANCE}).find('span', {'class': RATING_SELECTOR}).text)
            columns['work_env_rating'].append(
                soup.find('div', {'data-automation': RATING_SELECTOR_ENVIRONMENT}).find('span', {'class': RATING_SELECTOR}).text)
            columns['management_rating'].append(
                soup.find('div', {'data-automation': RATING_SELECTOR_MANAGEMENT}).find('span', {'class': RATING_SELECTOR}).text)
            columns['benefits_rating'].append(
                soup.find('div', {'data-automation': RATING_SELECTOR_BENEFIT}).find('span', {'class': RATING_SELECTOR}).text)
            columns['diversity_rating'].append(
                soup.find('div', {'data-automation': RATING_SELECTOR_DIVERSITY}).find('span', {'class': RATING_SELECTOR}).text)
            columns['overall_rating'].append(
                soup.find('div', {'data-automation': RATING_SELECTOR_OVERALL}).find('span', {'class': RATING_SELECTOR}).text)
            columns['company'].append(company_name)
            

    driver.close()
    return columns, review_number, review_missed


def save_links(all_links, company_name, save_path=None):
    """
    save all links into text file
    :all_links: list of all the reviews' link collected
    :company_name: nameof targeted company    
    :save_path: path to saving location
    """
    print("Writing links into a text file named {}.txt ...".format(company_name))
    with open(Path('{}/{}.txt'.format(save_path, company_name)), 'w') as file:
        for url in tqdm(all_links):
            file.write('{}\n'.format(url))
        print("\n")


def save_reviews(columns, company_name, save_path=None):
    """
    save collected data in a csv file
    :columns: dictionary containing all data collected
    :company_name: name of company targeted for data collection
    :save_path: path to saving location
    """

    print("\nWritting data into a CSV file named {}.csv ...\n".format(company_name))
    with open (Path('{}/{}.csv'.format(save_path ,company_name)), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns.keys())
        writer.writerows(zip(*columns.values()))