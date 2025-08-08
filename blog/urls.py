from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('category/<slug:slug>/', views.BlogListView.as_view(), name='category'),
    path('<slug:slug>/', views.BlogDetailView.as_view(), name='post_detail'),
    # Add to urls.py
    path('search/', views.BlogSearchView.as_view(), name='search'),
    path('subscribe/', views.NewsletterSubscribeView.as_view(), name='subscribe'),
]
