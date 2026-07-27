import csv
from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    help = 'Import phones from phones.csv'

    def handle(self, *args, **options):
        # Очищаем таблицу перед импортом
        Phone.objects.all().delete()

        # Открываем CSV-файл
        with open('phones.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')

            for row in reader:
                # Создаём телефон
                phone = Phone(
                    id=row['id'],
                    name=row['name'],
                    price=row['price'],
                    image=row['image'],
                    release_date=row['release_date'],
                    lte_exists=row['lte_exists'].lower() == 'true',
                )
                # slug сгенерируется автоматически в методе save() модели
                phone.save()

                self.stdout.write(
                    self.style.SUCCESS(f'Successfully added phone: {phone.name}')
                )