import requests
from bs4 import BeautifulSoup
import json

def get_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = {a['href']: [] for a in soup.find_all('a', href=True, limit=10) if a['href'].startswith('http')}
    for link in links:
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            headers_and_paragraphs = [str(tag) for tag in soup.find_all(['h1', 'p'])]
            links[link] = headers_and_paragraphs
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {link}: {e}")
    with open('results.json', 'w', encoding='utf-8') as json_file:
        json.dump(links, json_file, ensure_ascii=False, indent=4)

# url elegida
url = 'https://www.mercadolibre.com.ar/c/computacion#menu=categories'
get_data(url)