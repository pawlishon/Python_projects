from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Recipe
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    recipies = Recipe.objects.all()
    # Pagination
    paginator = Paginator(recipies, per_page=50)
    page_num = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'page_obj': page_obj})



def recipe_detail(request, file_no):
    try:
        recipe = Recipe.objects.get(file=file_no)
    except Recipe.DoesNotExist:
        raise Http404('Przepis nie istnieje :(')
    return render(request, 'recipe_detail.html', {'recipe': recipe})


def search_results(request):
    title = request.GET.get("title")
    category = request.GET.get("categorylist")
    if category == 'Dowolna' and title != '':
        recipies = Recipe.objects.filter(Q(title__icontains=title))
    elif category != 'Dowolna' and title != '':
        recipies = Recipe.objects.filter(Q(title__icontains=title) | Q(category=category))
    elif category != 'Dowolna' and title == '':
        recipies = Recipe.objects.filter(Q(category=category))
    elif category == 'Dowolna' and title == '':
        recipies = Recipe.objects.all()

    # Pagination
    paginator = Paginator(recipies, per_page=50)
    page_num = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'page_obj': page_obj})
