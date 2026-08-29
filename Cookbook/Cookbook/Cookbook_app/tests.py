from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import FavoriteRecipe, Recipe, ShoppingList, ShoppingListItem

User = get_user_model()


class SearchResultsTests(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(
            file=1,
            category='Dessert',
            difficulty='Easy',
            ingredients='Sugar, flour, eggs',
            preparation_time='20 min',
            quantity='2',
            tags='sweet',
            title='Chocolate Cake',
            total_time='30 min',
            content='A tasty cake recipe.',
        )

    def test_search_trims_whitespace_in_title(self):
        response = self.client.get(reverse('search_results'), {'title': 'chocolate ', 'categorylist': 'Dowolna'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chocolate Cake')


class UserAuthTests(TestCase):
    def test_user_can_register_with_email_and_password(self):
        response = self.client.post(
            reverse('register'),
            {'email': 'newuser@example.com', 'password': 'StrongPass123!'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser@example.com', email='newuser@example.com').exists())

    def test_user_can_login_with_email_and_password(self):
        User.objects.create_user(
            username='existing@example.com',
            email='existing@example.com',
            password='StrongPass123!',
        )

        response = self.client.post(
            reverse('login'),
            {'email': 'existing@example.com', 'password': 'StrongPass123!'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('_auth_user_id', self.client.session)


class FavoriteRecipeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='favorite@example.com',
            email='favorite@example.com',
            password='StrongPass123!',
        )
        self.recipe = Recipe.objects.create(
            file=42,
            category='Dessert',
            difficulty='Easy',
            ingredients='Sugar, flour, eggs',
            preparation_time='20 min',
            quantity='2',
            tags='sweet',
            title='Favorite Cake',
            total_time='30 min',
            content='A tasty cake recipe.',
        )

    def test_user_can_add_favorite_recipe(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('toggle_favorite', args=[self.recipe.file]), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(FavoriteRecipe.objects.filter(user=self.user, recipe=self.recipe).exists())

    def test_favorites_page_lists_saved_recipes(self):
        self.client.force_login(self.user)
        FavoriteRecipe.objects.create(user=self.user, recipe=self.recipe)

        response = self.client.get(reverse('favorites'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.recipe.title)


class ShoppingListTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='shopping@example.com',
            email='shopping@example.com',
            password='StrongPass123!',
        )
        self.recipe = Recipe.objects.create(
            file=99,
            category='Main dish',
            difficulty='Medium',
            ingredients='Tomatoes, garlic, basil, olive oil',
            preparation_time='35 min',
            quantity='4',
            tags='italian',
            title='Pasta',
            total_time='45 min',
            content='A simple pasta recipe.',
        )

    def test_user_can_add_recipe_ingredients_to_shopping_list(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('shopping_list_add_recipe'), {'recipe_id': self.recipe.id}, follow=True)

        self.assertEqual(response.status_code, 200)
        shopping_list = ShoppingList.objects.get(user=self.user)
        self.assertEqual(ShoppingListItem.objects.filter(shopping_list=shopping_list).count(), 1)
        self.assertTrue(ShoppingListItem.objects.filter(shopping_list=shopping_list, name__icontains='tomatoes').exists())

    def test_recipe_ingredients_with_internal_comma_stay_together(self):
        self.client.force_login(self.user)
        self.recipe.ingredients = "['5 - 10 g liści mięty, świeżych (ok. 1 pęczek)', '1 cytryna']"
        self.recipe.save()

        response = self.client.post(reverse('shopping_list_add_recipe'), {'recipe_id': self.recipe.id}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(ShoppingListItem.objects.filter(user=self.user, name='5 - 10 g liści mięty, świeżych (ok. 1 pęczek)').exists())
        self.assertTrue(ShoppingListItem.objects.filter(user=self.user, name='1 cytryna').exists())
        self.assertFalse(ShoppingListItem.objects.filter(user=self.user, name='5 - 10 g liści mięty').exists())

    def test_user_can_add_freeform_ingredients_to_shopping_list(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('shopping_list'),
            {'ingredient': 'milk\n bread\n eggs'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(ShoppingListItem.objects.filter(user=self.user, name__icontains='milk').exists())
        self.assertTrue(ShoppingListItem.objects.filter(user=self.user, name__icontains='bread').exists())

    def test_manual_input_does_not_split_on_commas(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('shopping_list'),
            {'ingredient': 'milk, bread, eggs'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(ShoppingListItem.objects.filter(user=self.user, name='milk, bread, eggs').exists())

    def test_user_can_remove_one_item_from_shopping_list(self):
        self.client.force_login(self.user)
        shopping_list = ShoppingList.objects.create(user=self.user)
        item = ShoppingListItem.objects.create(user=self.user, shopping_list=shopping_list, name='milk')

        response = self.client.post(reverse('shopping_list_remove_item', args=[item.id]), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(ShoppingListItem.objects.filter(id=item.id).exists())

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_user_can_send_shopping_list_to_email(self):
        self.client.force_login(self.user)
        ShoppingList.objects.create(user=self.user)
        ShoppingListItem.objects.create(user=self.user, shopping_list=ShoppingList.objects.get(user=self.user), name='milk')

        response = self.client.post(reverse('shopping_list_send_email'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('milk', mail.outbox[0].body.lower())
