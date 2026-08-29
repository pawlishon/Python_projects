from django.conf import settings
from django.db import models


class Recipe(models.Model):
    file = models.IntegerField()
    category = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=20)
    ingredients = models.CharField(max_length=4000)
    preparation_time = models.CharField(max_length=20)
    quantity = models.CharField(max_length=20)
    tags = models.CharField(max_length=1000)
    title = models.CharField(max_length=100)
    total_time = models.CharField(max_length=20)
    content = models.TextField()

    def __str__(self):
        return self.title


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} favorites {self.recipe.title}'


class ShoppingList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shopping_list')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} shopping list'


class ShoppingListItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='items')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shopping_list_items')
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at', 'name']

    def __str__(self):
        return self.name
