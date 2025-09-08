from django.views.generic import ListView, DetailView, FormView
from django.shortcuts import get_object_or_404
from .models import Project, ProjectCategory
from .forms import ProjectInquiryForm
from django.http import JsonResponse
from django.contrib import messages


class ProjectListView(ListView):
    """View for project list/gallery"""
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Project.objects.all()
        category_slug = self.kwargs.get('slug')
        
        if category_slug:
            category = get_object_or_404(ProjectCategory, slug=category_slug)
            queryset = queryset.filter(categories=category)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProjectCategory.objects.all()
        
        category_slug = self.kwargs.get('slug')
        if category_slug:
            context['current_category'] = get_object_or_404(ProjectCategory, slug=category_slug)
        
        return context


# projects/views.py (update ProjectDetailView)
class ProjectDetailView(DetailView):
    """View for project detail"""
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    
    def get_object(self, queryset=None):
        # Try to get by slug first, then by pk
        if 'slug' in self.kwargs:
            return get_object_or_404(Project, slug=self.kwargs['slug'])
        return super().get_object(queryset)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        
        # Get related projects
        related_categories = project.categories.all()
        context['related_projects'] = Project.objects.filter(
            categories__in=related_categories
        ).exclude(id=project.id).distinct()[:4]
        
        # Add inquiry form to context
        context['inquiry_form'] = ProjectInquiryForm()
        
        return context
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Increment views on GET request
        project = self.get_object()
        project.increment_views()
        return response

class ProjectInquiryView(FormView):
    """View for project inquiries"""
    form_class = ProjectInquiryForm
    template_name = 'projects/project_inquiry.html'
    
    def form_valid(self, form):
        project = get_object_or_404(Project, slug=self.kwargs['slug'])
        inquiry = form.save(commit=False)
        inquiry.project = project
        inquiry.save()
        
        messages.success(self.request, 'Your inquiry has been submitted successfully! We will contact you soon.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('projects:project_detail', kwargs={'slug': self.kwargs['slug']})


def increment_project_views(request, slug):
    """Increment project view count"""
    if request.method == 'POST':
        project = get_object_or_404(Project, slug=slug)
        project.increment_views()
        return JsonResponse({'status': 'success', 'views': project.views})
    return JsonResponse({'status': 'error'}, status=400)



#------------------------------------------------------------------------------
#               Dashboard
#------------------------------------------------------------------------------


# projects/views.py (add these views)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .forms import (
    ProjectForm, ProjectImageForm, ProjectVideoForm, 
    ProjectFeatureForm, ProjectTestimonialForm, ProjectCategoryForm
)
from .models import Project, ProjectCategory, ProjectImage, ProjectVideo, ProjectFeature, ProjectTestimonial


class ProjectDashboardView(LoginRequiredMixin, ListView):
    """Dashboard view for managing projects"""
    model = Project
    template_name = 'projects/project_dashboard.html'
    context_object_name = 'projects'
    paginate_by = 10
    
    def get_queryset(self):
        return Project.objects.all().order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProjectCategory.objects.all()
        context['total_projects'] = Project.objects.count()
        context['featured_projects'] = Project.objects.filter(is_featured=True).count()
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """View for creating new projects"""
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:project_dashboard')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.last_updated_by = self.request.user
        messages.success(self.request, 'Project created successfully!')
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating projects"""
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:project_dashboard')
    
    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        messages.success(self.request, 'Project updated successfully!')
        return super().form_valid(form)


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting projects"""
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('projects:project_dashboard')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Project deleted successfully!')
        return super().delete(request, *args, **kwargs)


class ProjectImageCreateView(LoginRequiredMixin, CreateView):
    """View for adding project images"""
    model = ProjectImage
    form_class = ProjectImageForm
    template_name = 'projects/project_image_form.html'
    
    def get_success_url(self):
        return reverse_lazy('projects:project_update', kwargs={'pk': self.kwargs['project_pk']})
    
    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        form.instance.project = project
        messages.success(self.request, 'Image added successfully!')
        return super().form_valid(form)


class ProjectImageDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting project images"""
    model = ProjectImage
    template_name = 'projects/project_image_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('projects:project_update', kwargs={'pk': self.object.project.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Image deleted successfully!')
        return super().delete(request, *args, **kwargs)


class ProjectVideoCreateView(LoginRequiredMixin, CreateView):
    """View for adding project videos"""
    model = ProjectVideo
    form_class = ProjectVideoForm
    template_name = 'projects/project_video_form.html'
    
    def get_success_url(self):
        return reverse_lazy('projects:project_update', kwargs={'pk': self.kwargs['project_pk']})
    
    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        form.instance.project = project
        messages.success(self.request, 'Video added successfully!')
        return super().form_valid(form)


class ProjectVideoDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting project videos"""
    model = ProjectVideo
    template_name = 'projects/project_video_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('projects:project_update', kwargs={'pk': self.object.project.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Video deleted successfully!')
        return super().delete(request, *args, **kwargs)


class ProjectFeatureCreateView(LoginRequiredMixin, CreateView):
    """View for adding project features"""
    model = ProjectFeature
    form_class = ProjectFeatureForm
    template_name = 'projects/project_feature_form.html'
    
    def get_success_url(self):
        return reverse_lazy('projects:project_update', kwargs={'pk': self.kwargs['project_pk']})
    
    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        form.instance.project = project
        messages.success(self.request, 'Feature added successfully!')
        return super().form_valid(form)


class ProjectFeatureDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting project features"""
    model = ProjectFeature
    template_name = 'projects/project_feature_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('projects:project_update', kwargs={'pk': self.object.project.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Feature deleted successfully!')
        return super().delete(request, *args, **kwargs)


class ProjectTestimonialCreateView(LoginRequiredMixin, CreateView):
    """View for adding project testimonials"""
    model = ProjectTestimonial
    form_class = ProjectTestimonialForm
    template_name = 'projects/project_testimonial_form.html'
    
    def get_success_url(self):
        return reverse_lazy('projects:project_update', kwargs={'pk': self.kwargs['project_pk']})
    
    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        form.instance.project = project
        messages.success(self.request, 'Testimonial added successfully!')
        return super().form_valid(form)


class ProjectTestimonialDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting project testimonials"""
    model = ProjectTestimonial
    template_name = 'projects/project_testimonial_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('projects:project_update', kwargs={'pk': self.object.project.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Testimonial deleted successfully!')
        return super().delete(request, *args, **kwargs)


class ProjectCategoryCreateView(LoginRequiredMixin, CreateView):
    """View for creating project categories"""
    model = ProjectCategory
    form_class = ProjectCategoryForm
    template_name = 'projects/project_category_form.html'
    success_url = reverse_lazy('projects:project_dashboard')
    
    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully!')
        return super().form_valid(form)


class ProjectCategoryUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating project categories"""
    model = ProjectCategory
    form_class = ProjectCategoryForm
    template_name = 'projects/project_category_form.html'
    success_url = reverse_lazy('projects:project_dashboard')
    
    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully!')
        return super().form_valid(form)


class ProjectCategoryDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting project categories"""
    model = ProjectCategory
    template_name = 'projects/project_category_confirm_delete.html'
    success_url = reverse_lazy('projects:project_dashboard')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Category deleted successfully!')
        return super().delete(request, *args, **kwargs)