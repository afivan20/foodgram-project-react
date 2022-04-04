from django.db import models
from django.core import validators
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = models.CharField(max_length=7, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='ingredient_in_recipe'
                                   )
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE,
                               related_name='recipe_ingredients'
                               )
    amount = models.SmallIntegerField(
        verbose_name='Количество ингредиента',
        validators=(
            validators.MinValueValidator(
                1, 'Добавьте необходимое количество для ингредиента'),))


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(
        Ingredient, through=IngredientAmount,
        through_fields=('recipe', 'ingredient', ),
        )
    tags = models.ManyToManyField(Tag, blank=True, related_name='recipe')
    image = models.ImageField(upload_to='recipes/images/')
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(1, message='минимальное время 1 минута'),
                   ),
                )


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
        verbose_name = 'Избранное'
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
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='cart-user uniq')
        ]