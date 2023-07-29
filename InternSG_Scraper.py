import time
import requests
from bs4 import BeautifulSoup

filters = ["software", "frontend", "backend"]
for filter in filters:
    for page_num in range(1, 5):
        url = f"https://www.internsg.com/jobs/{page_num}/?f_p&f_i&filter_s={filter}#isg-top"

        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        print(f"{filter}, {page_num}")

        pages = soup.find_all("div", class_="ast-row ast-pagination-square")

        if not pages:
            break
        else:
            even_row = soup.find_all("div", class_="ast-row list-even")
            for row in even_row:
                post_date = row.find_all("span")[-1].contents[0]
                if post_date != "Closed":
                    row = row.find_all("div")
                    company_name = row[0].contents[0]
                    title = row[1].contents[0].get_text()

                    print(f"\t{company_name}, {title}")

                time.sleep(0.1)

            odd_row = soup.find_all("div", class_="ast-row list-odd")
            for row in odd_row:
                post_date = row.find_all("span")[-1].contents[0]
                if post_date != "Closed":
                    row = row.find_all("div")
                    company_name = row[0].contents[0]
                    title = row[1].contents[0].get_text()

                    print(f"\t{company_name}, {title}")

                time.sleep(0.1)
