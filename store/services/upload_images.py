from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from requests import RequestException, Session

from store.models import Image, Product


def worker(queue: Queue, session: Session):
    while queue.qsize():
        product = queue.get()
        print(queue.qsize())
        for i, image_url in enumerate(product.image_urls, start=1):
            print('IMAGE URL', image_url)
            try:
                response = session.get(image_url, timeout=10)
                with open(f'media/images/product/{product.slug}-{i}.jpg', 'wb') as file:
                    file.write(response.content)

                Image.objects.create(
                    product=product,
                    image=f'images/product/{product.slug}-{i}.jpg',
                    url=image_url,
                    size=len(response.content)
                )
            except RequestException as error:
                print('Error', error)
                queue.put(product)

        product.is_images_uploaded = True
        product.save(update_fields=('is_images_uploaded',))


def main():
    products = Product.objects.filter(is_images_uploaded=False)

    que = Queue()
    for product in products:
        que.put(product)

    session = Session()

    with ThreadPoolExecutor(max_workers=20) as executor:
        for i in range(products.count()):
            executor.submit(worker, que, session)
