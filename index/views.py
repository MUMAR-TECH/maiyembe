# core/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from .models import *
from .forms import ContactForm, NewsletterForm

def index(request):
    services = Service.objects.filter(is_featured=True)[:6]
    projects = Project.objects.filter(is_featured=True)[:6]
    blog_posts = BlogPost.objects.filter(is_featured=True)[:5]
    testimonials = Testimonial.objects.filter(is_active=True)
    team_members = TeamMember.objects.filter(is_active=True).order_by('order')[:4]
    
    context = {
        'services': services,
        'projects': projects,
        'blog_posts': blog_posts,
        'testimonials': testimonials,
        'team_members': team_members,
    }
    return render(request, 'core/index.html', context)

def about(request):
    about_content = About.objects.first()
    team_members = TeamMember.objects.filter(is_active=True).order_by('order')
    testimonials = Testimonial.objects.filter(is_active=True)
    
    context = {
        'about': about_content,
        'team_members': team_members,
        'testimonials': testimonials,
    }
    return render(request, 'core/about.html', context)

def services(request):
    services = Service.objects.all()
    
    context = {
        'services': services,
    }
    return render(request, 'core/services.html', context)








def projects(request):
    categories = ProjectCategory.objects.all()
    projects_list = Project.objects.filter(is_active=True).order_by('-created_at')
    
    # Filter by category if specified
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(ProjectCategory, slug=category_slug)
        projects_list = projects_list.filter(category=category)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        projects_list = projects_list.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(projects_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'categories': categories,
        'projects': page_obj,
        'selected_category': category_slug,
        'search_query': query,
    }
    return render(request, 'core/projects.html', context)

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related_projects = Project.objects.filter(category=project.category).exclude(id=project.id)[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'core/project_detail.html', context)

from .forms import ProjectForm

@login_required
@permission_required('core.add_project', raise_exception=True)
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            return redirect('project_detail', slug=project.slug)
    else:
        form = ProjectForm()
    
    context = {'form': form}
    return render(request, 'core/project_form.html', context)

@login_required
@permission_required('core.change_project', raise_exception=True)
def edit_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            return redirect('project_detail', slug=project.slug)
    else:
        form = ProjectForm(instance=project)
    
    context = {'form': form, 'project': project}
    return render(request, 'core/project_form.html', context)

@login_required
@permission_required('core.delete_project', raise_exception=True)
def delete_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    
    context = {'project': project}
    return render(request, 'core/project_confirm_delete.html', context)

@login_required
@permission_required('core.change_project', raise_exception=True)
def toggle_project_status(request, slug):
    project = get_object_or_404(Project, slug=slug)
    project.is_active = not project.is_active
    project.save()
    return redirect('project_detail', slug=project.slug)





















def blog(request):
    categories = BlogCategory.objects.all()
    blog_posts = BlogPost.objects.filter(is_active=True).order_by('-created_at')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        blog_posts = blog_posts.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(author__icontains=query) |
            Q(tags__icontains=query)
        )
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(BlogCategory, slug=category_slug)
        blog_posts = blog_posts.filter(category=category)
    
    # Pagination
    paginator = Paginator(blog_posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    popular_posts = BlogPost.objects.filter(is_active=True).order_by('-views')[:5]
    
    context = {
        'categories': categories,
        'blog_posts': page_obj,
        'popular_posts': popular_posts,
        'selected_category': category_slug,
        'search_query': query,
    }
    return render(request, 'core/blog.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_active=True)
    
    # Increment view count
    post.views += 1
    post.save()
    
    # Get related posts
    related_posts = BlogPost.objects.filter(
        category=post.category,
        is_active=True
    ).exclude(id=post.id).order_by('-created_at')[:3]
    
    # Get all categories for sidebar
    categories = BlogCategory.objects.all()
    
    # Get popular posts for sidebar
    popular_posts = BlogPost.objects.filter(is_active=True).order_by('-views')[:5]
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'categories': categories,
        'popular_posts': popular_posts,
    }
    return render(request, 'core/blog_detail.html', context)

# core/views.py
from .forms import BlogPostForm

@login_required
@permission_required('core.add_blogpost', raise_exception=True)
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.get_full_name()
            post.save()
            return redirect('blog_detail', slug=post.slug)
    else:
        form = BlogPostForm()
    
    context = {'form': form}
    return render(request, 'core/blog_post_form.html', context)

@login_required
@permission_required('core.change_blogpost', raise_exception=True)
def edit_blog_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('blog_detail', slug=post.slug)
    else:
        form = BlogPostForm(instance=post)
    
    context = {'form': form, 'post': post}
    return render(request, 'core/blog_post_form.html', context)

@login_required
@permission_required('core.delete_blogpost', raise_exception=True)
def delete_blog_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if request.method == 'POST':
        post.delete()
        return redirect('blog')
    
    context = {'post': post}
    return render(request, 'core/blog_post_confirm_delete.html', context)

@login_required
@permission_required('core.change_blogpost', raise_exception=True)
def toggle_blog_post_status(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    post.is_active = not post.is_active
    post.save()
    return redirect('blog_detail', slug=post.slug)












# core/views.py
def services(request):
    services = Service.objects.filter(is_active=True).order_by('order')
    featured_services = Service.objects.filter(is_featured=True, is_active=True)
    
    context = {
        'services': services,
        'featured_services': featured_services,
    }
    return render(request, 'core/services.html', context)

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    related_services = Service.objects.filter(
        is_active=True
    ).exclude(id=service.id).order_by('?')[:3]
    
    context = {
        'service': service,
        'related_services': related_services,
    }
    return render(request, 'core/service_detail.html', context)

# core/views.py
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect
from .forms import ServiceForm

@login_required
@permission_required('core.add_service', raise_exception=True)
def create_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save()
            return redirect('service_detail', slug=service.slug)
    else:
        form = ServiceForm()
    
    context = {'form': form}
    return render(request, 'core/service_form.html', context)

@login_required
@permission_required('core.change_service', raise_exception=True)
def edit_service(request, slug):
    service = get_object_or_404(Service, slug=slug)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            service = form.save()
            return redirect('service_detail', slug=service.slug)
    else:
        form = ServiceForm(instance=service)
    
    context = {'form': form, 'service': service}
    return render(request, 'core/service_form.html', context)

@login_required
@permission_required('core.delete_service', raise_exception=True)
def delete_service(request, slug):
    service = get_object_or_404(Service, slug=slug)
    if request.method == 'POST':
        service.delete()
        return redirect('services')
    
    context = {'service': service}
    return render(request, 'core/service_confirm_delete.html', context)

@login_required
@permission_required('core.change_service', raise_exception=True)
def toggle_service_status(request, slug):
    service = get_object_or_404(Service, slug=slug)
    service.is_active = not service.is_active
    service.save()
    return redirect('service_detail', slug=service.slug)










def team(request):
    team_members = TeamMember.objects.filter(is_active=True).order_by('order')
    
    context = {
        'team_members': team_members,
    }
    return render(request, 'core/team.html', context)

# core/views.py
from .forms import TeamMemberForm

@login_required
@permission_required('core.add_teammember', raise_exception=True)
def create_team_member(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save()
            return redirect('team')
    else:
        form = TeamMemberForm()
    
    context = {'form': form}
    return render(request, 'core/team_member_form.html', context)

@login_required
@permission_required('core.change_teammember', raise_exception=True)
def edit_team_member(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            member = form.save()
            return redirect('team')
    else:
        form = TeamMemberForm(instance=member)
    
    context = {'form': form, 'member': member}
    return render(request, 'core/team_member_form.html', context)

@login_required
@permission_required('core.delete_teammember', raise_exception=True)
def delete_team_member(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        member.delete()
        return redirect('team')
    
    context = {'member': member}
    return render(request, 'core/team_member_confirm_delete.html', context)

@login_required
@permission_required('core.change_teammember', raise_exception=True)
def toggle_team_member_status(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    member.is_active = not member.is_active
    member.save()
    return redirect('team')






























def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_request = form.save()
            # Here you can add email sending logic
            return render(request, 'core/contact_success.html')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'core/contact.html', context)

def subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})



# core/models.py
class ProcessStep(models.Model):
    service = models.ForeignKey(Service, related_name='process_steps', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.service.title} - Step {self.order}"
    






# core/views.py
from .forms import TestimonialForm

@login_required
@permission_required('core.add_testimonial', raise_exception=True)
def create_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            testimonial = form.save()
            return redirect('index')  # Or testimonial list page if you have one
    else:
        form = TestimonialForm()
    
    context = {'form': form}
    return render(request, 'core/testimonial_form.html', context)

@login_required
@permission_required('core.change_testimonial', raise_exception=True)
def edit_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            testimonial = form.save()
            return redirect('index')  # Or testimonial list page if you have one
    else:
        form = TestimonialForm(instance=testimonial)
    
    context = {'form': form, 'testimonial': testimonial}
    return render(request, 'core/testimonial_form.html', context)

@login_required
@permission_required('core.delete_testimonial', raise_exception=True)
def delete_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        testimonial.delete()
        return redirect('index')  # Or testimonial list page if you have one
    
    context = {'testimonial': testimonial}
    return render(request, 'core/testimonial_confirm_delete.html', context)

@login_required
@permission_required('core.change_testimonial', raise_exception=True)
def toggle_testimonial_status(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.is_active = not testimonial.is_active
    testimonial.save()
    return redirect('index')  # Or testimonial list page if you have one