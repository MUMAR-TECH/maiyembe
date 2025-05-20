from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Project, ProjectCategory


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
        
        return context