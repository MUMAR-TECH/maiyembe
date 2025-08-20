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


class ProjectDetailView(DetailView):
    """View for project detail"""
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    
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