from django.contrib import admin
from recipes.models import Ingredient, Tag, Recipe, IngredientAmount, Favorite, ShoppingCart


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')



class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = ('id','name', 'author',)

class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe','ingredient', 'amount',)

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientAmount, IngredientInRecipeAdmin)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
