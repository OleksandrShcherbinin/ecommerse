from unicodedata import category

from django.core.management.base import BaseCommand, CommandError

from store.services.rozetka_scraper import RozetkaParser


class Command(BaseCommand):
    help = 'Scrape data from source'
    BASE_CATEGORY = 'notebooks/c80004/'

    def add_arguments(self, parser):
        parser.add_argument(
            "--category_url",
            action='store',
            dest='category_url',
            help="Url of a category",
        )

    def handle(self, *args, **options):
        category_url = options.get('category_url')
        print(category_url)
        if not category_url:
            category_url = self.BASE_CATEGORY
        try:
            print('Scrape command!!!')
            url = f'https://rozetka.com.ua/ua/{category_url}'
            RozetkaParser(url).scrape()
        except Exception as error:
            raise CommandError(error)

        self.stdout.write(self.style.SUCCESS('Successfully scraped data!!!'))
