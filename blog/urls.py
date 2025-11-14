# blog/urls.py
from django.urls import path
from .views import (
    # Public URLs
    BlogListView, BlogDetailView, BlogSearchView,
    
    # Dashboard URLs
    BlogDashboardView, PostCreateView, PostUpdateView, PostDeleteView,
    CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    CommentListView, CommentUpdateView, CommentDeleteView,
    NewsletterListView, NewsletterCreateView,
    approve_comment, unapprove_comment, toggle_subscriber_status,
)

app_name = 'blog'

urlpatterns = [
    # Dashboard URLs - THESE MUST COME FIRST
    path('dashboard/', BlogDashboardView.as_view(), name='blog_dashboard'),
    path('dashboard/posts/create/', PostCreateView.as_view(), name='post_create'),
    path('dashboard/posts/update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('dashboard/posts/delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('dashboard/categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('dashboard/categories/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('dashboard/categories/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    path('dashboard/comments/', CommentListView.as_view(), name='comment_list'),
    path('dashboard/comments/update/<int:pk>/', CommentUpdateView.as_view(), name='comment_update'),
    path('dashboard/comments/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),
    path('dashboard/comments/approve/<int:pk>/', approve_comment, name='approve_comment'),
    path('dashboard/comments/unapprove/<int:pk>/', unapprove_comment, name='unapprove_comment'),
    path('dashboard/newsletter/', NewsletterListView.as_view(), name='newsletter_list'),
    path('dashboard/newsletter/create/', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('dashboard/newsletter/toggle/<int:pk>/', toggle_subscriber_status, name='toggle_subscriber'),
    
    # Public URLs - THESE COME AFTER DASHBOARD URLS
    path('', BlogListView.as_view(), name='blog_list'),
    path('category/<slug:slug>/', BlogListView.as_view(), name='category'),
    path('search/', BlogSearchView.as_view(), name='search'),
    
    # This MUST BE LAST - it catches any slug, so it should be the last pattern
    path('<slug:slug>/', BlogDetailView.as_view(), name='post_detail'),
]