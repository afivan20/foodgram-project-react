import csv
from django.core.management.base import BaseCommand
from foodgram.settings import BASE_DIR
from recipes.models import Ingredient
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):

        Ingredient.objects.all().delete()
        User.objects.all().delete()

        ingredient = f'{BASE_DIR}/data/ingredients.csv'
        with open(ingredient) as file:
            reader = csv.reader(file)
            id = 1
            for row in reader:
                print(row[0])
                Ingredient.objects.create(id=id, name=row[0], measurement_unit=row[1])
                id += 1

        print(f'в базу данных успешно добавлены ингредиенты - {id-1} шт. ✅')
