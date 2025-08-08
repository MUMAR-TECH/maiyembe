from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Post, Category
from django.views.generic import FormView
from django.contrib import messages
from .forms import NewsletterForm
from django.db import models 

class BlogListView(ListView):
    """View for blog post list"""
    model = Post
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Post.objects.filter(is_published=True)
        category_slug = self.kwargs.get('slug')
        
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        
        category_slug = self.kwargs.get('slug')
        if category_slug:
            context['current_category'] = get_object_or_404(Category, slug=category_slug)
        
        return context

class BlogSearchView(ListView):
    model = Post
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                models.Q(title__icontains=query) | 
                models.Q(content__icontains=query) |
                models.Q(excerpt__icontains=query)
            )
        return queryset

class BlogDetailView(DetailView):
    """View for blog post detail"""
    model = Post
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Get related posts
        context['related_posts'] = Post.objects.filter(
            category=post.category
        ).exclude(id=post.id)[:3]
        
        context['categories'] = Category.objects.all()
        return context
    

class NewsletterSubscribeView(FormView):
    form_class = NewsletterForm
    template_name = 'blog/blog_list.html'
    success_url = '/blog/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Thank you for subscribing to our newsletter!")
        return super().form_valid(form)