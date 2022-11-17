import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException


URL = "https://scrapeme.live/shop/"


def scrape():
    products_prices = {}
    driver = webdriver.Firefox()
    driver.get(URL)
    while True:
        products = driver.find_elements(By.CLASS_NAME, "product")
        for product in products:
            h2_tag = product.find_element(By.TAG_NAME, 'h2')
            h2_text = h2_tag.text
            price = product.find_element(
                By.CLASS_NAME, 'amount'
            ).text
            products_prices[h2_text] = price
        try:
            next_page = driver.find_element(By.CLASS_NAME, 'next').get_attribute('href')
            driver.get(next_page)
        except (TimeoutException, WebDriverException):
            break
    with open('result.json', 'w') as wf:
        wf.write(json.dumps(products_prices))


scrape()
