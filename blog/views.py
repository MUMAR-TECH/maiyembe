# blog/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Post, Category, Comment, NewsletterSubscriber
from .forms import CategoryForm, PostForm, CommentForm, NewsletterForm

# Public Views
class BlogListView(ListView):
    """Public blog post list"""
    model = Post
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Post.objects.filter(status='published')
        category_slug = self.kwargs.get('slug')
        
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        
        return queryset.select_related('category', 'author')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True).annotate(
            post_count=Count('posts')
        )
        context['featured_posts'] = Post.objects.filter(
            status='published', is_featured=True
        )[:3]
        
        category_slug = self.kwargs.get('slug')
        if category_slug:
            context['current_category'] = get_object_or_404(Category, slug=category_slug)
        
        return context

class BlogDetailView(DetailView):
    """Public blog post detail"""
    model = Post
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return Post.objects.filter(status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Increment views
        post.increment_views()
        
        # Get related posts
        context['related_posts'] = Post.objects.filter(
            category=post.category,
            status='published'
        ).exclude(id=post.id)[:3]
        
        # Get categories
        context['categories'] = Category.objects.filter(is_active=True).annotate(
            post_count=Count('posts')
        )
        
        # Add comment form
        context['comment_form'] = CommentForm()
        context['comments'] = post.comments.filter(is_approved=True)
        
        return context

class BlogSearchView(ListView):
    """Public blog search"""
    model = Post
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Post.objects.filter(status='published')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) |
                Q(excerpt__icontains=query) |
                Q(tags__icontains=query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['categories'] = Category.objects.filter(is_active=True).annotate(
            post_count=Count('posts')
        )
        return context

# Dashboard Views
class BlogDashboardView(LoginRequiredMixin, ListView):
    """Blog dashboard overview"""
    template_name = 'blog/blog_dashboard.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return Post.objects.all().order_by('-created_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['total_posts'] = Post.objects.count()
        context['published_posts'] = Post.objects.filter(status='published').count()
        context['draft_posts'] = Post.objects.filter(status='draft').count()
        context['featured_posts'] = Post.objects.filter(is_featured=True).count()
        context['total_comments'] = Comment.objects.count()
        context['pending_comments'] = Comment.objects.filter(is_approved=False).count()
        context['subscribers_count'] = NewsletterSubscriber.objects.count()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    """Create new blog post"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:blog_dashboard')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    """Update blog post"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:blog_dashboard')
    
    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Delete blog post"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_dashboard')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)

class CategoryCreateView(LoginRequiredMixin, CreateView):
    """Create blog category"""
    model = Category
    form_class = CategoryForm
    template_name = 'blog/category_form.html'
    success_url = reverse_lazy('blog:blog_dashboard')
    
    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully!')
        return super().form_valid(form)

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    """Update blog category"""
    model = Category
    form_class = CategoryForm
    template_name = 'blog/category_form.html'
    success_url = reverse_lazy('blog:blog_dashboard')
    
    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully!')
        return super().form_valid(form)

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    """Delete blog category"""
    model = Category
    template_name = 'blog/category_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_dashboard')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Category deleted successfully!')
        return super().delete(request, *args, **kwargs)

class CommentListView(LoginRequiredMixin, ListView):
    """Manage blog comments"""
    model = Comment
    template_name = 'blog/comment_list.html'
    context_object_name = 'comments'
    paginate_by = 20
    
    def get_queryset(self):
        status = self.request.GET.get('status', 'all')
        queryset = Comment.objects.all().order_by('-created_at')
        
        if status == 'approved':
            queryset = queryset.filter(is_approved=True)
        elif status == 'pending':
            queryset = queryset.filter(is_approved=False)
        
        return queryset.select_related('post', 'user')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_comments'] = Comment.objects.count()
        context['approved_comments'] = Comment.objects.filter(is_approved=True).count()
        context['pending_comments'] = Comment.objects.filter(is_approved=False).count()
        return context

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    """Update comment status"""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Comment updated successfully!')
        return reverse_lazy('blog:comment_list')

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    """Delete comment"""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    success_url = reverse_lazy('blog:comment_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Comment deleted successfully!')
        return super().delete(request, *args, **kwargs)

@require_POST
def approve_comment(request, pk):
    """Approve comment via AJAX"""
    comment = get_object_or_404(Comment, pk=pk)
    comment.is_approved = True
    comment.save()
    return JsonResponse({'success': True})

@require_POST
def unapprove_comment(request, pk):
    """Unapprove comment via AJAX"""
    comment = get_object_or_404(Comment, pk=pk)
    comment.is_approved = False
    comment.save()
    return JsonResponse({'success': True})

class NewsletterListView(LoginRequiredMixin, ListView):
    """Manage newsletter subscribers"""
    model = NewsletterSubscriber
    template_name = 'blog/newsletter_list.html'
    context_object_name = 'subscribers'
    paginate_by = 20
    
    def get_queryset(self):
        return NewsletterSubscriber.objects.all().order_by('-subscribed_at')

@require_POST
def toggle_subscriber_status(request, pk):
    """Toggle subscriber active status"""
    subscriber = get_object_or_404(NewsletterSubscriber, pk=pk)
    subscriber.is_active = not subscriber.is_active
    subscriber.save()
    return JsonResponse({'success': True, 'is_active': subscriber.is_active})

class NewsletterCreateView(LoginRequiredMixin, CreateView):
    """Add newsletter subscriber manually"""
    model = NewsletterSubscriber
    form_class = NewsletterForm
    template_name = 'blog/newsletter_form.html'
    success_url = reverse_lazy('blog:newsletter_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Subscriber added successfully!')
        return super().form_valid(form)