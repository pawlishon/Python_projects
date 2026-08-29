"""Cookbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from Cookbook_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('recipe/<int:file_no>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:file_no>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites, name='favorites'),
    path('search/', views.search_results, name='search_results'),
    path('shopping-list/', views.shopping_list, name='shopping_list'),
    path('shopping-list/remove-item/<int:item_id>/', views.shopping_list_remove_item, name='shopping_list_remove_item'),
    path('shopping-list/clear/', views.shopping_list_clear, name='shopping_list_clear'),
    path('shopping-list/add-recipe/', views.shopping_list_add_recipe, name='shopping_list_add_recipe'),
    path('shopping-list/send-email/', views.shopping_list_send_email, name='shopping_list_send_email'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
        # Password reset urls
        path('password-reset/',
            auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
            name='password_reset'),
        path('password-reset/done/',
            auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
            name='password_reset_done'),
        path('password-reset-confirm/<uidb64>/<token>/',
            auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
            name='password_reset_confirm'),
        path('password-reset-complete/',
            auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
            name='password_reset_complete'),
]
