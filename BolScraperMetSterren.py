import requests
import csv
from bs4 import BeautifulSoup
import threading
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

lock = threading.Lock()

def get_reviews(start_page, end_page):
    with open('Bol_com_reviews_metSterren.csv', 'a', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['name', 'review', 'image', 'sentiment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if start_page == 1:
            writer.writeheader()

        seen_reviews = set()

        for page in range(start_page, end_page+1):
            print(f'huidige pagina: {page}')
            url = f'https://www.bol.com/nl/nl/l/outdoorschoenen/39510/?page={page}'
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            product_tags = soup.find_all('li', {'class': 'product-item--column'})

            for tag in product_tags:
                name = tag.find('span', {'class': 'truncate'}).text.strip()
                url = tag.find('a', {'class': 'hit-area-listpage'})['href']
                print (url)
                
                visit_url = f'https://www.bol.com{url}'
                response = requests.get(visit_url)
                soup = BeautifulSoup(response.content, 'html.parser')
                image = soup.find('img', {'class': 'js_selected_image'})['src']
                review_block = soup.find_all('li',{'class': 'review js-review'})
                for block in  review_block:
                    rating = re.findall('<div class="star-rating" role="text" aria-label="klantbeoordeling: (.+?) van de 5 sterren">' , block.text, re.S)
                    sentiment = 0
                    if rating == 4 or rating == 5:
                        sentiment = 1
                    elif rating == 1 or rating == 2:
                        sentiment = -1
                    else:
                        sentiment = 0
                    
                    review_tags = soup.find_all('div', {'class': 'review__body'})

                    for review_tag in review_tags:
                        review = review_tag.text.strip()
                        review_id = f"{name}__{review}"
                        if review_id not in seen_reviews:
                            with lock:
                                try:
                                    writer.writerow({'name': name, 'review': review.replace('\uFFFD', ''), 'image': image.replace('\uFFFD', ''), 'sentiment': sentiment})
                                    seen_reviews.add(review_id)
                                except UnicodeEncodeError:
                                    print("Unicode error has occurred. Oh No. Anyways, lets continue")

threads = []
num_pages = 400
pages_per_thread = 80

for i in range(0, num_pages, pages_per_thread):
    start_page = i+1
    end_page = min(i+pages_per_thread, num_pages)
    t = threading.Thread(target=get_reviews, args=(start_page, end_page))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
