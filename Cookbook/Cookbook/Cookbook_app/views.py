from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Recipe
from django.db.models import Q


def home(request):
    recipies = Recipe.objects.all()
    return render(request, 'home.html', {'recipies': recipies})
    # return HttpResponse('<p> Home View </p>')


def recipe_detail(request, file_no):
    try:
        recipe = Recipe.objects.get(file=file_no)
    except Recipe.DoesNotExist:
        raise Http404('Przepis nie istnieje :(')
    return render(request, 'recipe_detail.html', {'recipe': recipe})


def search_results(request):
    title = request.GET.get("title")
    category = request.GET.get("categorylist")
    print(title, category)
    if category == 'Dowolna' and title != '':
        recipies = Recipe.objects.filter(Q(title__icontains=title))
    elif category != 'Dowolna' and title != '':
        recipies = Recipe.objects.filter(Q(title__icontains=title) | Q(category=category))
    elif category != 'Dowolna' and title == '':
        recipies = Recipe.objects.filter(Q(category=category))
    elif category == 'Dowolna' and title == '':
        recipies = Recipe.objects.all()
    return render(request, 'home.html', {'recipies': recipies})
