from django.urls import path
from .views import BlogListView, BlogDetailView

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('category/<slug:slug>/', BlogListView.as_view(), name='category'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='post_detail'),
]
