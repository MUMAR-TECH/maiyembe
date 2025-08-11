from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView, DetailView, CreateView, ListView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import ServiceFeature, ServiceRequest, TeamMember, Service, SliderImage, Testimonial, Subscriber,About
from blog.models import Post
from projects.models import Project
from .forms import ContactForm, ServiceCreateForm, ServiceFeatureForm, ServiceRequestForm, ServiceUpdateForm, SubscriberForm


class HomePageView(TemplateView):
    """View for the home page"""
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add required data for each section
        context['slider_images'] = SliderImage.objects.filter(is_active=True)
        context['about'] = About.objects.first()
        context['services'] = Service.objects.all()[:6]  # Limit to 6 services
        context['featured_projects'] = Project.objects.filter(is_featured=True)[:8]  # Limit to 8 projects
        context['recent_posts'] = Post.objects.filter(is_published=True)[:5]  # Limit to 5 blog posts
        context['testimonials'] = Testimonial.objects.filter(is_featured=True)[:3]  # Limit to 3 testimonials
        context['leadership_team'] = TeamMember.objects.filter(is_leadership=True)[:4]  # Limit to 4 team members
        
        # Add forms
        context['contact_form'] = ContactForm()
        context['subscriber_form'] = SubscriberForm()
        
        return context


class AboutView(TemplateView):
    """View for the about page"""
    template_name = 'about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.all()
        return context


class ServiceListView(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Service.objects.filter(is_active=True).order_by('display_order')
        
        # Filter by category if specified
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Service.SERVICE_CATEGORIES
        context['current_category'] = self.request.GET.get('category')
        return context
    
class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.object
        
        # Get related services (same category, excluding current)
        related_services = Service.objects.filter(
            category=service.category,
            is_active=True
        ).exclude(id=service.id)[:4]
        
        # Initialize the service request form with the current service pre-selected
        initial_data = {'service': service.id}
        context['service_request_form'] = ServiceRequestForm(initial=initial_data)
        context['related_services'] = related_services
        return context

class ServiceRequestView(CreateView):
    """View for handling service request form submissions"""
    form_class = ServiceRequestForm
    template_name = 'services/service_detail.html'  # or create a separate template
    success_url = reverse_lazy('core:service_request_success')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your service request has been submitted. We will contact you soon!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors in the form.')
        return super().form_invalid(form)
    
def service_request_success(request):
    return render(request, 'services/service_request_success.html')

class ContactView(CreateView):
    """View for handling contact form submissions"""
    form_class = ContactForm
    template_name = 'contact.html'
    success_url = reverse_lazy('contact')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your message has been sent. We will get back to you soon!')
        return super().form_valid(form)


def subscribe_newsletter(request):
    """View for handling newsletter subscriptions"""
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Check if already subscribed
            if not Subscriber.objects.filter(email=email).exists():
                form.save()
                messages.success(request, 'Thank you for subscribing to our newsletter!')
            else:
                messages.info(request, 'You are already subscribed to our newsletter.')
    
    # Redirect back to the referring page or home
    return redirect(request.META.get('HTTP_REFERER', 'home'))


class TeamListView(ListView):
    """View for displaying all team members"""
    model = TeamMember
    template_name = 'team.html'
    context_object_name = 'team_members'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Split team members into leadership and regular team members
        context['leadership_team'] = TeamMember.objects.filter(is_leadership=True)
        context['regular_team'] = TeamMember.objects.filter(is_leadership=False)
        return context

class AboutView(TemplateView):
    """View for the about page"""
    template_name = 'about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = About.objects.first()  # Get the single About instance
        context['team_members'] = TeamMember.objects.all()
        return context



from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'services'
    
    def get_queryset(self):
        return Service.objects.filter(created_by=self.request.user).order_by('-updated_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_requests'] = ServiceRequest.objects.all().order_by('-created_at')
        return context

class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = ServiceCreateForm
    template_name = 'dashboard/service_form.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.last_updated_by = self.request.user
        messages.success(self.request, 'Service created successfully!')
        return super().form_valid(form)

class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceUpdateForm
    template_name = 'dashboard/service_form.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        messages.success(self.request, 'Service updated successfully!')
        return super().form_valid(form)

class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'dashboard/service_confirm_delete.html'
    success_url = reverse_lazy('dashboard')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Service deleted successfully!')
        return super().delete(request, *args, **kwargs)

class ServiceFeatureCreateView(LoginRequiredMixin, CreateView):
    model = ServiceFeature
    form_class = ServiceFeatureForm
    template_name = 'dashboard/feature_form.html'
    
    def get_success_url(self):
        return reverse_lazy('service_update', kwargs={'pk': self.kwargs['service_pk']})
    
    def form_valid(self, form):
        service = get_object_or_404(Service, pk=self.kwargs['service_pk'])
        form.instance.service = service
        messages.success(self.request, 'Feature added successfully!')
        return super().form_valid(form)

class ServiceFeatureDeleteView(LoginRequiredMixin, DeleteView):
    model = ServiceFeature
    template_name = 'dashboard/feature_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('service_update', kwargs={'pk': self.object.service.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Feature deleted successfully!')
        return super().delete(request, *args, **kwargs)