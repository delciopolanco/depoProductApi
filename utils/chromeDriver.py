import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def chromeDriver(url: str):

    chromeOptions = Options()

    chromeOptions.add_argument("--headless=new")
    chromeOptions.add_argument("--disable-dev-shm-usage")
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument("--disable-gpu")

    with Chrome(options=chromeOptions, service=Service(ChromeDriverManager().install())) as browser:
        browser.get(url)
        browser.maximize_window()
        html = browser.page_source

        return BeautifulSoup(html, "lxml")
