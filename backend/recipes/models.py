from django.db import models
from django.core import validators
from users.models import User


class Tag(models.Model):
    name = models.CharField('Название', max_length=200, unique=True)
    color = models.CharField('Цвет', max_length=7, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('название продукта', max_length=200)
    measurement_unit = models.CharField('единицы измерения', max_length=200)

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
    
    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='ingredient_in_recipe',
                                   verbose_name='ингредиент',
                                   )
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE,
                               related_name='recipe_ingredients',
                               verbose_name='рецепт',
                               )
    amount = models.SmallIntegerField(
        verbose_name='Количество ингредиента',
        validators=(
            validators.MinValueValidator(
                1, 'Добавьте необходимое количество для ингредиента'),))

    class Meta:
        verbose_name = 'Кол-во ингредиента'
        verbose_name_plural = 'Кол-во ингредиентов'                


class Recipe(models.Model):
    author = models.ForeignKey(User, verbose_name='Автор рецепта', on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(
        Ingredient, through=IngredientAmount, blank=False,
        through_fields=('recipe', 'ingredient', ),
        verbose_name='Ингредиенты',
        )
    tags = models.ManyToManyField(Tag, blank=False, related_name='recipe', verbose_name='теги')
    image = models.ImageField(upload_to='recipes/images/', verbose_name='картинка')
    name = models.CharField('Название', max_length=200)
    text = models.TextField('Описание рецепта')
    cooking_time = models.PositiveSmallIntegerField('время приготовления',
        validators=(
            validators.MinValueValidator(1, message='минимальное время 1 минута'),
                   ),
                )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранные'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='fav uniq')
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppingcart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppingcart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='cart-user uniq')
        ]
