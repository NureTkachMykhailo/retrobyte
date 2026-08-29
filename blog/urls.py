from django.urls import path

from . import views

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    path('articles/new/', views.article_create, name='article_create'),
    path('articles/<int:pk>/edit/', views.article_update, name='article_update'),
    path('articles/<int:pk>/delete/', views.article_delete, name='article_delete'),
    path('comments/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('my-articles/', views.my_articles, name='my_articles'),
    path('register/', views.register, name='register'),
]
