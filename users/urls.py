from django.urls import path
# from django.conf.urls import include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django import template
# from .views import (PostListView,UserPostListView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView)

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/home.html'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('about/', views.about, name='about'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
    path('contact/', views.contact, name='contact'),
    path('active_email/', views.verify_email_page, name='active_email'),
    path('profile/', views.profile, name='profile'),
    path('userUpload/', views.userUpload, name='userUpload'),
    path('terms/', views.terms, name='terms'),
    path('faq/', views.faq, name='faq'),
    path('rating/', views.rating, name='rating'),
    path('comments/', views.comments, name='comment'),
    # path('addpost/', views.)
    path('watchlist/', views.watchlist, name='watchlist'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)