import os
import time

from bs4 import BeautifulSoup
import cloudscraper

scraper = cloudscraper.create_scraper()
BASE_URL = "https://www.hopkinsmedicine.org"
top_pages = ["https://www.hopkinsmedicine.org/health/wellness-and-prevention/dieting-and-weight-loss",
             "https://www.hopkinsmedicine.org/health/wellness-and-prevention/exercise",
             "https://www.hopkinsmedicine.org/health/wellness-and-prevention/watch-your-weight"]
skipped = []
for page in top_pages:

    print(f"Getting page: {page}")
    page_contents = scraper.get(page).text
    soup = BeautifulSoup(page_contents, "html.parser")

    # Cloudflare detection :(
    if "Just a moment..." in soup.text:
        print("Captcha detected. Waiting for 5 seconds...")
        time.sleep(5)
        skipped.append(page)
        continue

    # Contents
    article = soup.find("article")

    # Title
    title = str(soup.find('h1', {"class": "main-content__title"}).contents[0]).lower()

    # Save article
    if not os.path.isfile(f"articles/{title}.html"):
        print(f"Saving article: {title}")
        with open(f"articles/{title}.html", "w") as f:
            f.write(str(article))

    # Follow links
    topics = soup.find_all("a", {"class": "topics__link"})
    for topic in topics:
        print(topic.contents)
        print(topic["href"])
        top_pages.append(BASE_URL + topic["href"])

print("Skipped pages:")
for page in skipped:
    print(page)