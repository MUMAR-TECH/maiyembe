from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView, DetailView, CreateView, ListView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import ContactMessage, ServiceFeature, ServiceRequest, TeamMember, Service, SliderImage, Testimonial, Subscriber,About
from blog.models import Post
from projects.models import Project

from .forms import AboutForm, ContactForm, ContactMessageForm, ServiceCreateForm, ServiceFeatureForm, ServiceRequestForm, ServiceUpdateForm, SliderImageForm, SubscriberForm, TeamMemberForm, TestimonialForm


from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import logging
logger = logging.getLogger(__name__)

# Email imports
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone



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
        context['recent_posts'] = Post.objects.filter(status='published')[:5]
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
        return Service.objects.filter(created_by=self.request.user).order_by('-updated_at')[:5]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_requests'] = ServiceRequest.objects.all().order_by('-created_at')[:5]
        context['total_services'] = Service.objects.count()
        context['active_services'] = Service.objects.filter(is_active=True).count()
        context['total_requests'] = ServiceRequest.objects.count()
        context['new_requests'] = ServiceRequest.objects.filter(is_processed=False).count()
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


# Direct Booking View
@require_POST
def book_service_directly(request, service_id):
    """View for direct service booking without custom quote"""
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        # Create service request with direct booking flag
        service_request = ServiceRequest.objects.create(
            service=service,
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            message=f"DIRECT BOOKING - I want to book this service at the listed price: {service.get_price_display()}. {request.POST.get('message', '')}",
            contact_method=request.POST.get('contact_method', 'whatsapp'),
            budget_range='custom',
            custom_budget=service.starting_price if service.starting_price else None,
            project_location=request.POST.get('project_location', ''),
            project_timeline=request.POST.get('project_timeline', '')
        )
        
        # Send booking confirmation (with error handling)
        try:
            subject = f"Direct Booking: {service.title}"
            html_message = render_to_string('emails/direct_booking_admin.html', {
                'service_request': service_request,
                'service': service,
            })
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject,
                plain_message,
                getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@maiyembe.com'),
                [getattr(settings, 'ADMIN_EMAIL', 'admin@maiyembe.com')],
                html_message=html_message,
                fail_silently=True,
            )
        except Exception as e:
            logger.error(f"Failed to send booking email: {str(e)}")
        
        messages.success(request, f'Your booking for {service.title} has been received! We will confirm shortly.')
        return redirect('core:service_request_success')


# Add these imports at the top
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from .models import ServiceRequest

# Add these new views after existing views

class ServiceListDashboardView(LoginRequiredMixin, ListView):
    """Dashboard view for managing services"""
    model = Service
    template_name = 'dashboard/service_list.html'
    context_object_name = 'services'
    paginate_by = 10
    
    def get_queryset(self):
        return Service.objects.all().order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_services'] = Service.objects.filter(is_active=True).count()
        context['featured_services'] = Service.objects.filter(is_featured=True).count()
        context['service_requests_count'] = ServiceRequest.objects.count()
        return context

class ServiceRequestListView(LoginRequiredMixin, ListView):
    """Dashboard view for service requests"""
    model = ServiceRequest
    template_name = 'dashboard/service_request_list.html'
    context_object_name = 'service_requests'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = ServiceRequest.objects.all().order_by('-created_at')
        status = self.request.GET.get('status')
        
        if status == 'new':
            queryset = queryset.filter(is_processed=False)
        elif status == 'processed':
            queryset = queryset.filter(is_processed=True)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_requests'] = ServiceRequest.objects.count()
        context['new_requests'] = ServiceRequest.objects.filter(is_processed=False).count()
        context['processed_requests'] = ServiceRequest.objects.filter(is_processed=True).count()
        context['this_month_requests'] = ServiceRequest.objects.filter(
            created_at__month=timezone.now().month
        ).count()
        return context

class ServiceRequestDetailView(LoginRequiredMixin, DetailView):
    """Detail view for service requests"""
    model = ServiceRequest
    template_name = 'dashboard/service_request_detail.html'
    context_object_name = 'service_request'

class ServiceRequestUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for service requests"""
    model = ServiceRequest
    fields = ['notes']
    template_name = 'dashboard/service_request_detail.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Notes updated successfully!')
        return reverse_lazy('core:service_request_detail', kwargs={'pk': self.object.pk})

class ServiceRequestDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for service requests"""
    model = ServiceRequest
    template_name = 'dashboard/service_request_confirm_delete.html'
    success_url = reverse_lazy('core:service_request_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Service request deleted successfully!')
        return super().delete(request, *args, **kwargs)

class ServiceRequestMarkProcessedView(LoginRequiredMixin, UpdateView):
    """Mark service request as processed"""
    model = ServiceRequest
    fields = []
    
    def form_valid(self, form):
        form.instance.is_processed = True
        messages.success(self.request, 'Service request marked as processed!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('core:service_request_detail', kwargs={'pk': self.object.pk})

class ServiceRequestMarkNewView(LoginRequiredMixin, UpdateView):
    """Mark service request as new"""
    model = ServiceRequest
    fields = []
    
    def form_valid(self, form):
        form.instance.is_processed = False
        messages.success(self.request, 'Service request marked as new!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('core:service_request_detail', kwargs={'pk': self.object.pk})
    





































# core/views.py - Add these views
class TestimonialListView(LoginRequiredMixin, ListView):
    """Dashboard view for testimonials"""
    model = Testimonial
    template_name = 'dashboard/testimonial_list.html'
    context_object_name = 'testimonials'
    paginate_by = 10
    
    def get_queryset(self):
        return Testimonial.objects.all().order_by('order', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_testimonials'] = Testimonial.objects.count()
        context['published_testimonials'] = Testimonial.objects.filter(status='published').count()
        context['featured_testimonials'] = Testimonial.objects.filter(is_featured=True).count()
        return context

class TestimonialCreateView(LoginRequiredMixin, CreateView):
    """Create testimonial"""
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'dashboard/testimonial_form.html'
    success_url = reverse_lazy('core:testimonial_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Testimonial created successfully!')
        return super().form_valid(form)

class TestimonialUpdateView(LoginRequiredMixin, UpdateView):
    """Update testimonial"""
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'dashboard/testimonial_form.html'
    success_url = reverse_lazy('core:testimonial_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Testimonial updated successfully!')
        return super().form_valid(form)

class TestimonialDeleteView(LoginRequiredMixin, DeleteView):
    """Delete testimonial"""
    model = Testimonial
    template_name = 'dashboard/testimonial_confirm_delete.html'
    success_url = reverse_lazy('core:testimonial_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Testimonial deleted successfully!')
        return super().delete(request, *args, **kwargs)

class TeamMemberListView(LoginRequiredMixin, ListView):
    """Dashboard view for team members"""
    model = TeamMember
    template_name = 'dashboard/team_list.html'
    context_object_name = 'team_members'
    paginate_by = 10
    
    def get_queryset(self):
        return TeamMember.objects.all().order_by('order', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_members'] = TeamMember.objects.count()
        context['active_members'] = TeamMember.objects.filter(status='active').count()
        context['leadership_members'] = TeamMember.objects.filter(is_leadership=True).count()
        return context

class TeamMemberCreateView(LoginRequiredMixin, CreateView):
    """Create team member"""
    model = TeamMember
    form_class = TeamMemberForm
    template_name = 'dashboard/team_form.html'
    success_url = reverse_lazy('core:team_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Team member created successfully!')
        return super().form_valid(form)

class TeamMemberUpdateView(LoginRequiredMixin, UpdateView):
    """Update team member"""
    model = TeamMember
    form_class = TeamMemberForm
    template_name = 'dashboard/team_form.html'
    success_url = reverse_lazy('core:team_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Team member updated successfully!')
        return super().form_valid(form)

class TeamMemberDeleteView(LoginRequiredMixin, DeleteView):
    """Delete team member"""
    model = TeamMember
    template_name = 'dashboard/team_confirm_delete.html'
    success_url = reverse_lazy('core:team_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Team member deleted successfully!')
        return super().delete(request, *args, **kwargs)
    













# core/views.py - Add these views
class SliderListView(LoginRequiredMixin, ListView):
    """Dashboard view for slider images"""
    model = SliderImage
    template_name = 'dashboard/slider_list.html'
    context_object_name = 'sliders'
    paginate_by = 10
    
    def get_queryset(self):
        return SliderImage.objects.all().order_by('order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_sliders'] = SliderImage.objects.count()
        context['active_sliders'] = SliderImage.objects.filter(is_active='True').count()
        return context

class SliderCreateView(LoginRequiredMixin, CreateView):
    """Create slider image"""
    model = SliderImage
    form_class = SliderImageForm
    template_name = 'dashboard/slider_form.html'
    success_url = reverse_lazy('core:slider_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Slider image created successfully!')
        return super().form_valid(form)

class SliderUpdateView(LoginRequiredMixin, UpdateView):
    """Update slider image"""
    model = SliderImage
    form_class = SliderImageForm
    template_name = 'dashboard/slider_form.html'
    success_url = reverse_lazy('core:slider_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Slider image updated successfully!')
        return super().form_valid(form)

class SliderDeleteView(LoginRequiredMixin, DeleteView):
    """Delete slider image"""
    model = SliderImage
    template_name = 'dashboard/slider_confirm_delete.html'
    success_url = reverse_lazy('core:slider_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Slider image deleted successfully!')
        return super().delete(request, *args, **kwargs)

class ContactMessageListView(LoginRequiredMixin, ListView):
    """Dashboard view for contact messages"""
    model = ContactMessage
    template_name = 'dashboard/contact_message_list.html'
    context_object_name = 'messages'
    paginate_by = 20
    
    def get_queryset(self):
        status = self.request.GET.get('is_read', 'all')
        queryset = ContactMessage.objects.all().order_by('-created_at')
        
        if status != 'all':
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_messages'] = ContactMessage.objects.count()
        context['new_messages'] = ContactMessage.objects.filter(is_read='False').count()
        context['read_messages'] = ContactMessage.objects.filter(is_read='True').count()
        return context

class ContactMessageDetailView(LoginRequiredMixin, DetailView):
    """Detail view for contact messages"""
    model = ContactMessage
    template_name = 'dashboard/contact_message_detail.html'
    context_object_name = 'message'
    
    def get(self, request, *args, **kwargs):
        # Mark as read when viewed
        message = self.get_object()
        if message.status == 'new':
            message.status = 'read'
            message.save()
        return super().get(request, *args, **kwargs)

class ContactMessageUpdateView(LoginRequiredMixin, UpdateView):
    """Update contact message status"""
    model = ContactMessage
    form_class = ContactMessageForm
    template_name = 'dashboard/contact_message_detail.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Message status updated!')
        return reverse_lazy('core:contact_message_detail', kwargs={'pk': self.object.pk})

class ContactMessageDeleteView(LoginRequiredMixin, DeleteView):
    """Delete contact message"""
    model = ContactMessage
    template_name = 'dashboard/contact_message_confirm_delete.html'
    success_url = reverse_lazy('core:contact_message_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Message deleted successfully!')
        return super().delete(request, *args, **kwargs)

class SubscriberListView(LoginRequiredMixin, ListView):
    """Dashboard view for subscribers"""
    model = Subscriber
    template_name = 'dashboard/subscriber_list.html'
    context_object_name = 'subscribers'
    paginate_by = 20
    
    def get_queryset(self):
        status = self.request.GET.get('status', 'all')
        queryset = Subscriber.objects.all().order_by('-subscribed_at')
        
        if status != 'all':
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_subscribers'] = Subscriber.objects.count()
        context['active_subscribers'] = Subscriber.objects.filter(is_active='True').count()
        context['inactive_subscribers'] = Subscriber.objects.filter(is_active='False').count()
        return context

class SubscriberUpdateView(LoginRequiredMixin, UpdateView):
    """Update subscriber"""
    model = Subscriber
    form_class = SubscriberForm
    template_name = 'dashboard/subscriber_form.html'
    success_url = reverse_lazy('core:subscriber_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Subscriber updated successfully!')
        return super().form_valid(form)

class SubscriberDeleteView(LoginRequiredMixin, DeleteView):
    """Delete subscriber"""
    model = Subscriber
    template_name = 'dashboard/subscriber_confirm_delete.html'
    success_url = reverse_lazy('core:subscriber_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Subscriber deleted successfully!')
        return super().delete(request, *args, **kwargs)

class AboutUpdateView(LoginRequiredMixin, UpdateView):
    """Update about section"""
    model = About
    form_class = AboutForm
    template_name = 'dashboard/about_form.html'
    success_url = reverse_lazy('core:dashboard')
    
    def get_object(self):
        # Get or create the about instance
        about, created = About.objects.get_or_create(pk=1)
        return about
    
    def form_valid(self, form):
        messages.success(self.request, 'About section updated successfully!')
        return super().form_valid(form)

# AJAX actions
@require_POST
def mark_message_replied(request, pk):
    """Mark message as replied via AJAX"""
    message = get_object_or_404(ContactMessage, pk=pk)
    message.status = 'replied'
    message.save()
    return JsonResponse({'success': True})

@require_POST
def mark_message_archived(request, pk):
    """Mark message as archived via AJAX"""
    message = get_object_or_404(ContactMessage, pk=pk)
    message.status = 'archived'
    message.save()
    return JsonResponse({'success': True})

@require_POST
def toggle_subscriber_status(request, pk):
    """Toggle subscriber active status"""
    subscriber = get_object_or_404(Subscriber, pk=pk)
    if subscriber.status == 'active':
        subscriber.status = 'inactive'
        subscriber.unsubscribed_at = timezone.now()
    else:
        subscriber.status = 'active'
        subscriber.unsubscribed_at = None
    subscriber.save()
    return JsonResponse({'success': True, 'status': subscriber.status})