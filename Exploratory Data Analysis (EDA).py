import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

BASE_URL = "http://books.toscrape.com/"
CATEGORY_PATH = "catalogue/category/books/science_22/"

START_URL = urljoin(BASE_URL, CATEGORY_PATH)
NEXT_SELECTOR = "li.next a"

def fetch_page(url):
    r = requests.get(url)
    r.raise_for_status()
    return r.text

def parse_book(article):
    # Title from h3/a title attribute
    title = article.h3.a['title'].strip()

    # Price cleaning: extract numeric value
    price_text = article.find('p', class_='price_color').text.strip()
    price_num = None
    try:
        # e.g., "£51.77"
        price_num = float(price_text.replace('£', '').replace(',', ''))
    except Exception:
        price_num = None

    # Availability text
    stock_text = article.find('p', class_='instock availability').text.strip()

    # Rating (e.g., "One", "Two", ...)
    rating_tag = article.find('p', class_='star-rating')
    rating = rating_tag['class'][1] if rating_tag and len(rating_tag['class']) > 1 else None

    # Product page URL
    a_tag = article.h3.a
    product_url = urljoin(BASE_URL, a_tag['href'])

    return {
        'Title': title,
        'Price': price_text,
        'PriceNum': price_num,
        'Availability': stock_text,
        'Rating': rating,
        'ProductURL': product_url
    }

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    books = soup.find_all('article', class_='product_pod')
    return [parse_book(b) for b in books]

def has_next(soup):
    return soup.select_one(NEXT_SELECTOR) is not None

def get_next_url(soup, current_url):
    nxt = soup.select_one(NEXT_SELECTOR)
    if nxt:
        return urljoin(current_url, nxt['href'])
    return None

def main():
    url = START_URL
    all_books = []

    while url:
        html = fetch_page(url)
        soup = BeautifulSoup(html, 'html.parser')
        all_books.extend(parse_page(html))

        # follow next page if exists
        nxt = get_next_url(soup, url)
        url = nxt

    df = pd.DataFrame(all_books)

    # Optional: drop rows without a numeric price
    df = df.dropna(subset=['PriceNum'])

    df.to_csv('books_dataset.csv', index=False)
    print("Dataset saved as 'books_dataset.csv' with fields:")
    print(df.columns.tolist())

if __name__ == "__main__":
    main()