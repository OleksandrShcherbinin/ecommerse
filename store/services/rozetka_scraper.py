import re
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from anyascii import anyascii
from django.utils.text import slugify
from requests import RequestException, Session
from selectolax.parser import HTMLParser


class RozetkaParser:
    TIMEOUT = 10
    LOCK = threading.Lock()

    def __init__(self, main_url: str):
        self._main_url = main_url
        self.session = Session()
        self._id_counter = 0
        self._number_of_items = 0

    def scrape(self):
        que = self._fill_queue()

        with ThreadPoolExecutor(max_workers=20) as executor:
            for i in range(self._number_of_items):
                executor.submit(self._scrape, que)

        print('Finished scrapper...')

    def _fill_queue(self):
        response = self._get_response(self._main_url)
        tree = HTMLParser(response)
        links = tree.css('.tile-title')
        product_links = [
            link.attrs.get('href') for link in links if
            link.attrs.get('href')
        ]
        self._number_of_items = len(product_links)
        que = Queue()
        for link in product_links:
            que.put(link)
        return que

    def _scrape(self, que: Queue):
        while que.qsize():
            url = que.get()
            print(que.qsize(), url)
            try:
                response_text = self._get_response(url)  # Waiting
                self._parse(response_text, url)
            except Exception as error:
                print('Error', error)
                que.put(url)

    def _get_response(self, url: str) -> str | None:
        try:
            response = self.session.get(url, timeout=self.TIMEOUT)
            return response.text
        except RequestException as error:
            print('Request error', error)

    def _parse(self, html_string: str, url: str) -> None:
        tree = HTMLParser(html_string)
        title = tree.css('h1')[0].text()
        slug = slugify(anyascii(title))
        categories = tree.css('div[data-testid="crumb_item"]')
        categories = [category.text().strip().lstrip('/\xa0 ') for category in categories]
        availability = tree.css('.product-price__item p')[0].text()
        old_price = tree.css('.product-price__small')
        old_price = old_price[0].text() if old_price else None
        price = tree.css('.product-price__big')[0].text()
        images = tree.css('.simple-slider__item img')
        image_links = [
            link.attrs.get('src').replace('medium', 'big') for link in images if
            link.attrs.get('src')
        ]
        response = self._get_response(f'{url}characteristics/')
        tree = HTMLParser(response)
        characteristics = tree.css('main .item')
        char_data = {}
        for row in characteristics:
            name = row.css('.label span')[0].text()
            value = row.css('.value span')[0].text()
            if name and value:
                char_data[name.strip()] = value.strip()

        response = self._get_response(f'{url}comments/')
        tree = HTMLParser(response)
        comments = tree.css('.product-comments__list-item')
        comments_data = {}
        for row in comments:
            name = row.css('.text-base')[0].text()
            comment = row.css('.comment__body')
            if name and comment:
                comments_data[name.strip()] = [text.text() for text in comment]

        data = {
            'title': title,
            'slug': slug,
            'availability': availability.strip(),
            'old_price': self._extruct_price(old_price),
            'price': self._extruct_price(price),
            'categories': categories[1:],
            'images': image_links,
            'characteristics': char_data,
            'comments': comments_data
        }
        print(data)

    @staticmethod
    def _extruct_price(value):
        if not value:
            return value
        digits = re.sub(r'[^\d]', '', value)
        return int(digits) if digits else None
