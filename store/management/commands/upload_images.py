from django.core.management.base import BaseCommand, CommandError

from store.services.upload_images import main


class Command(BaseCommand):
    help = 'Upload images for products'

    def handle(self, *args, **options):
        try:
            print('Upload images!!!')
            main()
        except Exception as error:
            raise CommandError(error)

        self.stdout.write(self.style.SUCCESS('Successfully uploaded images!!!'))
