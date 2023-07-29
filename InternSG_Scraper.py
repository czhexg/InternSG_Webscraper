import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import os

now = datetime.now()
year = str(now.year)
month = now.strftime("%B")
day = str(now.day)
filePath = f"./{year}/{month}/{day}_{month}_{year}_jobs.doc"
os.makedirs(os.path.dirname(filePath), exist_ok=True)

def find_rows(odd_or_even):
    if odd_or_even == "even":
        rows = soup.find_all("div", class_="ast-row list-even")
    elif odd_or_even == "odd":
        rows = soup.find_all("div", class_="ast-row list-odd")
    
    for row in rows:
            post_date = row.find_all("span")[-1].contents[0]
            if post_date != "Closed":
                row = row.find_all("div")
                company_name = row[0].contents[0]
                title = row[1].contents[0].get_text()
                link = row[1].contents[0].get("href")

                print(f"\tName: {company_name}\n\tJob Title: {title}\n\tLink: {link}\n")
                with open(filePath, "a") as jobFile:
                     jobFile.write(f"\tName: {company_name}\n\tJob Title: {title}\n\tLink: {link}\n\n")

            time.sleep(0.2)

filters = ["software", "frontend", "backend"]
for filter in filters:
    for page_num in range(1, 5):
        url = f"https://www.internsg.com/jobs/{page_num}/?f_p&f_i&filter_s={filter}#isg-top"

        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        print(f"{filter}, page: {page_num}")
        with open(filePath, "a") as jobFile:
            jobFile.write(f"{filter}, page: {page_num}\n")

        pages = soup.find_all("div", class_="ast-row ast-pagination-square")

        find_rows("odd")
        find_rows("even")

        if not pages:
            break
