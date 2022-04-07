from django.db import models
from django.core import validators
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        "Название", max_length=200, unique=True, help_text="введите имя"
    )
    color = models.CharField(
        "Цвет",
        max_length=7,
        unique=True,
        help_text="цвет в формате HEX (например #0213ab)",
    )
    slug = models.SlugField(
        max_length=200, unique=True, help_text="уникальное имя латиницей"
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        "название продукта", max_length=200, help_text="введите имя"
    )
    measurement_unit = models.CharField(
        "единицы измерения",
        max_length=200,
        help_text="введите ед.и (например, кг)"
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredient_amounts",
        verbose_name="ингредиент",
        help_text="выберите ингредиент",
    )
    recipe = models.ForeignKey(
        "Recipe",
        on_delete=models.CASCADE,
        related_name="recipe_amounts",
        verbose_name="рецепт",
        help_text="выберите рецепт",
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество ингредиента",
        help_text="введите кол-во",
        validators=(
            validators.MinValueValidator(
                1, "Добавьте необходимое количество для ингредиента"
            ),
        ),
    )

    class Meta:
        verbose_name = "Кол-во ингредиента"
        verbose_name_plural = "Кол-во ингредиентов"

    def __str__(self):
        return self.ingredient.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name="Автор рецепта",
        help_text="выберите автора",
        on_delete=models.CASCADE,
        related_name="recipes_author",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through=IngredientAmount,
        blank=False,
        through_fields=(
            "recipe",
            "ingredient",
        ),
        verbose_name="Ингредиенты",
        help_text="выберите ингредиенты",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=False,
        related_name="recipes",
        verbose_name="теги",
        help_text="выберите теги",
    )
    image = models.ImageField(
        upload_to="recipes/images/",
        verbose_name="картинка",
        help_text="загрузите картинку",
    )
    name = models.CharField(
        "Название",
        max_length=200,
        help_text="введите название",
    )
    text = models.TextField(
        "Описание рецепта",
        help_text="Расскажите как готовить это блюдо...",
    )
    cooking_time = models.PositiveSmallIntegerField(
        "время приготовления",
        help_text="время приготоваления в минутах",
        validators=(
            validators.MinValueValidator(
                1, message="пожалуйста, укажите время приготовления"
            ),
        ),
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="выберите пользователя",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Рецепт",
        help_text="выберите рецепт",
    )

    class Meta:
        verbose_name = "Избранные"
        verbose_name_plural = "Избранные"
        constraints = [
            models.UniqueConstraint(fields=["user", "recipe"], name="fav uniq")
        ]

    def __str__(self):
        return f"{self.user.username}-{self.recipe}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shoppingcart",
        verbose_name="Пользователь",
        help_text="выберите пользователя",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shoppingcart",
        verbose_name="Рецепт",
        help_text="выберите рецепт",
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Список покупок"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="cart-user uniq"
            )
        ]

    def __str__(self):
        return f"{self.user.username}: {self.recipe.name}"
