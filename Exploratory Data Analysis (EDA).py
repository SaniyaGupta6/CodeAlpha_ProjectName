import requests
from bs4 import BeautifulSoup
import pandas as pd


url = 'http://books.toscrape.com/catalogue/category/books/science_22/index.html'


response = requests.get(url)
response.raise_for_status()  

soup = BeautifulSoup(response.text, 'html.parser')


books = soup.find_all('article', class_='product_pod')


titles = []
prices = []
availability = []

for book in books:
    
    title = book.h3.a['title']
    titles.append(title)
    
    
    price = book.find('p', class_='price_color').text
    prices.append(price)
    
    
    stock = book.find('p', class_='instock availability').text.strip()
    availability.append(stock)


data = {
    'Title': titles,
    'Price': prices,
    'Availability': availability
}

df = pd.DataFrame(data)


df.to_csv('books_dataset.csv', index=False)

print("Dataset saved as 'books_dataset.csv'.")