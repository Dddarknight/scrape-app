import json
from enum import Enum
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


URL = "https://scrapeme.live/shop/"
OUTPUT_FILE = 'products.json'


class Attrs(Enum):
    LINK = 'href'


class Classes(Enum):
    PRODUCT = 'product'
    NEXT_PAGE = 'next'
    PRICE = 'amount'
    SUMMARY = 'summary'
    DESCRIPTION = 'woocommerce-product-details__short-description'
    QUANTITY = 'stock'
    META = 'product_meta'
    CATEGORIES = 'posted_in'
    TAGS = 'tagged_as'


class Tags(Enum):
    PRODUCT_NAME = 'h1'
    URL = 'a'


def scrape():
    products_data = []
    driver = webdriver.Firefox()
    next_page = URL

    while next_page:
        driver.get(next_page)
        products = driver.find_elements(
            By.CLASS_NAME, Classes.PRODUCT.value
        )
        products_urls = []
        for product in products:
            product_url = product.find_element(
                By.TAG_NAME, Tags.URL.value
            ).get_attribute(Attrs.LINK.value)
            products_urls.append(product_url)

        for product_url in products_urls:
            product_data = scrape_product_page(driver, product_url)
            products_data.append(product_data)

        driver.get(next_page)

        try:
            next_page = driver.find_element(
                By.CLASS_NAME, Classes.NEXT_PAGE.value
            ).get_attribute(Attrs.LINK.value)
        except NoSuchElementException:
            next_page = None

    with open(OUTPUT_FILE, 'w') as write_file:
        write_file.write(json.dumps(products_data))


def scrape_product_page(driver, product_url):
    product_data = {}
    driver.get(product_url)

    summary = driver.find_element(
        By.CLASS_NAME, Classes.SUMMARY.value
    )

    name = summary.find_element(
        By.TAG_NAME, Tags.PRODUCT_NAME.value
    ).text
    price = summary.find_element(
        By.CLASS_NAME, Classes.PRICE.value
    ).text
    description = summary.find_element(
        By.CLASS_NAME, Classes.DESCRIPTION.value
    ).text
    quantity = summary.find_element(
        By.CLASS_NAME, Classes.QUANTITY.value
    ).text
    product_meta = summary.find_element(
        By.CLASS_NAME, Classes.META.value
    )

    categories_names = []
    categories = product_meta.find_element(
        By.CLASS_NAME, Classes.CATEGORIES.value
    )
    for element in categories.find_elements(
        By.TAG_NAME, Tags.URL.value
    ):
        categories_names.append(element.text)

    tags_names = []
    tags = product_meta.find_element(
        By.CLASS_NAME, Classes.TAGS.value
    )
    for element in tags.find_elements(
        By.TAG_NAME, Tags.URL.value
    ):
        tags_names.append(element.text)

    product_data = {
        'name': name,
        'price': price,
        'description': description,
        'quantity': quantity,
        'categories': categories_names,
        'tags': tags_names,
    }
    return product_data
