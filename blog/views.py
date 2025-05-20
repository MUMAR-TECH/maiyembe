from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Post, Category


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