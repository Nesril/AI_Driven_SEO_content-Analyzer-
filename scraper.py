from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import html2text
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import html2text
import re


def perform_google_search(query):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)

    n_pages = 5
    results = []
    counter = 0
    for page in range(1, n_pages):
        url = "http://www.google.com/search?q=" + str(query) + "&start=" + str((page - 1) * 10)

        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        search = soup.find_all('div', class_="yuRUbf")
        for h in search:
            counter = counter + 1
            title = h.a.h3.text
            link = h.a.get('href')
            rank = counter
            results.append({'title': h.a.h3.text, 'url': link,
                            'domain': urlparse(link).netloc, 'rank': rank})
    print(results)
    return results[:5]

def get_brand_mentions(text, keyword):
    # Split the text into sentences
    sentences = re.split('(?<=[.!?]) +', text)

    # Find and return sentences that contain the keyword
    keyword_sentences = [sentence for sentence in sentences if keyword.lower() in sentence.lower()]

    return keyword_sentences


def get_article_from_url(url):
    try:
        # Set a User-Agent header to mimic a web browser
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        req = Request(url, headers=headers)
        
        html = urlopen(req).read()
        print("Parsing Content...")
        soup = BeautifulSoup(html, features="html.parser")
        extractedText = soup.get_text()
        print("Extract Text...")
        h = html2text.HTML2Text()
        h.ignore_links = True
        article_text = h.handle(extractedText)
        return article_text
    except Exception as e:
        print(f"Error: {e}")
        return None

       
#print(get_article_from_url("https://www.techtarget.com/searchenterpriseai/definition/AI-prompt-engineer"))