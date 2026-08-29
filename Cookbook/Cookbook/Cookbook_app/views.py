import ast
import re

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.http import Http404
from .models import FavoriteRecipe, Recipe, ShoppingList, ShoppingListItem
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

User = get_user_model()


def _normalize_ingredient_entries(raw_ingredients):
    entries = []
    if not raw_ingredients:
        return entries

    raw_text = str(raw_ingredients).strip()
    if not raw_text:
        return entries

    if raw_text.startswith('[') and raw_text.endswith(']'):
        try:
            parsed = ast.literal_eval(raw_text)
        except (ValueError, SyntaxError):
            parsed = []
        if isinstance(parsed, list):
            raw_entries = parsed
        else:
            raw_entries = [raw_text]
    else:
        raw_entries = raw_text.splitlines()

    for raw_entry in raw_entries:
        cleaned = str(raw_entry).strip()
        if not cleaned:
            continue
        cleaned = cleaned.strip("'\"")
        cleaned = re.sub(r'^(?:[-*•]\s*|\d+\s*[.)]\s*)', '', cleaned)
        cleaned = cleaned.strip()
        if cleaned:
            entries.append(cleaned)

    return entries


def home(request):
    recipies_list = Recipe.objects.all().order_by('id')
    paginator = Paginator(recipies_list, 50)  # 50 recipes per page
    page = request.GET.get('page')
    try:
        recipies = paginator.page(page)
    except PageNotAnInteger:
        recipies = paginator.page(1)
    except EmptyPage:
        recipies = paginator.page(paginator.num_pages)

    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(
            FavoriteRecipe.objects.filter(user=request.user).values_list('recipe_id', flat=True)
        )

    return render(
        request,
        'home.html',
        {'recipies': recipies, 'page_obj': recipies, 'favorite_ids': favorite_ids}
    )
    # return HttpResponse('<p> Home View </p>')


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '').strip()

        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return render(request, 'register.html')

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'register.html')

        user = User.objects.create_user(username=email, email=email, password=password)
        login(request, user)
        return redirect('home')

    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '').strip()

        # Try authenticating directly using the email as username
        user = authenticate(request, username=email, password=password)
        if user is None:
            # Fallback: find user by email and authenticate using their username
            try:
                user_obj = User.objects.get(email__iexact=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, 'Invalid email or password.')
        return render(request, 'login.html')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def toggle_favorite(request, file_no):
    try:
        recipe = Recipe.objects.get(file=file_no)
    except Recipe.DoesNotExist:
        raise Http404('Przepis nie istnieje :(')

    favorite, created = FavoriteRecipe.objects.get_or_create(user=request.user, recipe=recipe)
    if not created:
        favorite.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def favorites(request):
    favorite_recipes = Recipe.objects.filter(favorited_by__user=request.user).distinct().order_by('title')
    return render(request, 'favorites.html', {'recipies': favorite_recipes})


def recipe_detail(request, file_no):
    try:
        recipe = Recipe.objects.get(file=file_no)
    except Recipe.DoesNotExist:
        raise Http404('Przepis nie istnieje :(')

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = FavoriteRecipe.objects.filter(user=request.user, recipe=recipe).exists()

    return render(request, 'recipe_detail.html', {'recipe': recipe, 'is_favorite': is_favorite})


def search_results(request):
    title = request.GET.get("title", "").strip()
    category = request.GET.get("categorylist", "Dowolna").strip()

    if category == 'Dowolna' and title:
        recipies_list = Recipe.objects.filter(Q(title__icontains=title))
    elif category != 'Dowolna' and title:
        recipies_list = Recipe.objects.filter(Q(title__icontains=title) | Q(category=category))
    elif category != 'Dowolna' and not title:
        recipies_list = Recipe.objects.filter(Q(category=category))
    else:
        recipies_list = Recipe.objects.all()

    paginator = Paginator(recipies_list, 50)
    page = request.GET.get('page')
    try:
        recipies = paginator.page(page)
    except PageNotAnInteger:
        recipies = paginator.page(1)
    except EmptyPage:
        recipies = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'recipies': recipies, 'page_obj': recipies})


@login_required
def shopping_list(request):
    shopping_list, _ = ShoppingList.objects.get_or_create(user=request.user)
    items = shopping_list.items.all()

    if request.method == 'POST':
        cleaned = _normalize_ingredient_entries(request.POST.get('ingredient', ''))

        for name in cleaned:
            if not ShoppingListItem.objects.filter(user=request.user, shopping_list=shopping_list, name__iexact=name).exists():
                ShoppingListItem.objects.create(user=request.user, shopping_list=shopping_list, name=name)

        return redirect('shopping_list')

    return render(request, 'shopping_list.html', {'items': items, 'shopping_list': shopping_list})


@login_required
def shopping_list_remove_item(request, item_id):
    shopping_list, _ = ShoppingList.objects.get_or_create(user=request.user)
    item = shopping_list.items.filter(id=item_id).first()
    if item:
        item.delete()
        messages.success(request, 'Ingredient removed from your shopping list.')
    return redirect('shopping_list')


@login_required
def shopping_list_clear(request):
    shopping_list, _ = ShoppingList.objects.get_or_create(user=request.user)
    deleted_count, _ = shopping_list.items.all().delete()
    if deleted_count:
        messages.success(request, 'All ingredients were removed from your shopping list.')
    else:
        messages.info(request, 'Your shopping list is already empty.')
    return redirect('shopping_list')


@login_required
def shopping_list_add_recipe(request):
    if request.method != 'POST':
        return redirect('home')

    recipe_id = request.POST.get('recipe_id')
    if not recipe_id:
        return redirect('shopping_list')

    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        return redirect('home')

    shopping_list, _ = ShoppingList.objects.get_or_create(user=request.user)
    for name in _normalize_ingredient_entries(recipe.ingredients):
        if not ShoppingListItem.objects.filter(user=request.user, shopping_list=shopping_list, name__iexact=name).exists():
            ShoppingListItem.objects.create(user=request.user, shopping_list=shopping_list, name=name)

    return redirect('shopping_list')


@login_required
def shopping_list_send_email(request):
    shopping_list, _ = ShoppingList.objects.get_or_create(user=request.user)
    items = shopping_list.items.all()
    if not items:
        messages.info(request, 'Your shopping list is empty.')
        return redirect('shopping_list')

    body = '\n'.join(f'{index}. {item.name}' for index, item in enumerate(items, start=1))
    send_mail(
        'Your shopping list',
        body,
        'noreply@example.com',
        [request.user.email],
        fail_silently=False,
    )
    messages.success(request, 'Shopping list sent to your email address.')
    return redirect('shopping_list')
