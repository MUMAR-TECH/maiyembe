from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView, DetailView, CreateView, ListView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import ServiceFeature, ServiceRequest, TeamMember, Service, SliderImage, Testimonial, Subscriber,About
from blog.models import Post
from projects.models import Project

from .forms import ContactForm, ServiceCreateForm, ServiceFeatureForm, ServiceRequestForm, ServiceUpdateForm, SubscriberForm


from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Email imports
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags



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
        context['about'] = About.objects.first()  # Get the single About instance
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
        context['service_request_form'] = ServiceRequestForm(
            initial={'service': self.object.id}
        )
        return context


@require_POST
def submit_service_request(request):
    form = ServiceRequestForm(request.POST)
    if form.is_valid():
        service_request = form.save()
        
        # Send email notification to admin
        subject = f"New Service Request: {service_request.service.title if service_request.service else 'General Inquiry'}"
        html_message = render_to_string('emails/service_request_admin.html', {
            'service_request': service_request,
        })
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Send confirmation email to user
        user_subject = "Thank you for your service request"
        user_html_message = render_to_string('emails/service_request_user.html', {
            'service_request': service_request,
            'site_name': settings.SITE_NAME,
        })
        user_plain_message = strip_tags(user_html_message)
        
        send_mail(
            user_subject,
            user_plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [service_request.email],
            html_message=user_html_message,
            fail_silently=False,
        )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Your request has been submitted successfully! You will receive a confirmation email shortly.'
            })
        messages.success(request, 'Your request has been submitted successfully!')
        return redirect('core:service_request_success')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': False,
            'errors': form.errors.get_json_data()
        })
    messages.error(request, 'Please correct the errors below.')
    return redirect('core:service_detail', slug=form.cleaned_data.get('service').slug)



def service_request_success(request):
    return render(request, 'services/service_request_success.html')

class ContactView(CreateView):
    """View for handling contact form submissions"""
    form_class = ContactForm
    template_name = 'contact.html'
    success_url = reverse_lazy('core:service_request_success')  # Changed to success page
    
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
    success_url = reverse_lazy('core:dashboard')
    
   
    
    def form_valid(self, form):
        # Save the service first
        service = form.save(commit=False)
        service.created_by = self.request.user
        service.last_updated_by = self.request.user
        service.save()
        
        # Process features
        feature_titles = self.request.POST.getlist('feature_titles')
        feature_icons = self.request.POST.getlist('feature_icons')
        feature_descriptions = self.request.POST.getlist('feature_descriptions')
        feature_ids = self.request.POST.getlist('feature_ids')
        
        # Update or create features
        for i in range(len(feature_titles)):
            if feature_titles[i]:  # Only save if there's a title
                if i < len(feature_ids) and feature_ids[i]:
                    # Update existing feature
                    feature = ServiceFeature.objects.get(id=feature_ids[i])
                    feature.title = feature_titles[i]
                    feature.icon = feature_icons[i]
                    feature.description = feature_descriptions[i]
                    feature.save()
                else:
                    # Create new feature
                    ServiceFeature.objects.create(
                        service=service,
                        title=feature_titles[i],
                        icon=feature_icons[i],
                        description=feature_descriptions[i]
                    )
        
        # Delete features that were removed
        if self.object:
            current_feature_ids = [int(id) for id in feature_ids if id]
            self.object.features.exclude(id__in=current_feature_ids).delete()
        
        messages.success(self.request, 'Service saved successfully!')
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

# views.py - Update the ServiceFeatureCreateView
class ServiceFeatureCreateView(LoginRequiredMixin, CreateView):
    model = ServiceFeature
    form_class = ServiceFeatureForm
    template_name = 'dashboard/feature_form.html'
    
    def get_success_url(self):
        return reverse_lazy('core:service_update', kwargs={'pk': self.kwargs['service_pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the service to the context
        context['service'] = get_object_or_404(Service, pk=self.kwargs['service_pk'])
        return context
    
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


# Custom error handlers
def custom_404_view(request, exception):
    """Render a friendly animated 404 page."""
    context = {
        'request_path': request.path,
    }
    return render(request, '404.html', context=context, status=404)