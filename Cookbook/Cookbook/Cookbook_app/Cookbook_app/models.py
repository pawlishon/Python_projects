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
