from django.contrib import admin
from recipes.models import (
    Ingredient,
    Tag,
    Recipe,
    IngredientAmount,
    Favorite,
    ShoppingCart,
)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("measurement_unit",)


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color")
    search_fields = ("name", "slug",)


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = ("id", "name", "author", "fav_count")
    search_fields = (
        "name",
        "author__username",
    )
    list_filter = (
        "author",
        "tags",
    )

    def fav_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    fav_count.short_description = "Общее число добавлений в избранное"


class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "recipe",
        "ingredient",
        "amount",
    )


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
    )
    search_fields = (
        "user__username",
        "recipe__name",
    )


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientAmount, IngredientInRecipeAdmin)
admin.site.register(Favorite)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
