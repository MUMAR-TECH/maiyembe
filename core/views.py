from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView, CreateView, ListView
from django.urls import reverse_lazy
from .models import TeamMember, Service, SliderImage, Testimonial, Subscriber,About
from blog.models import Post
from projects.models import Project
from .forms import ContactForm, SubscriberForm


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


class ServicesView(ListView):
    """View for the services page"""
    model = Service
    template_name = 'services.html'
    context_object_name = 'services'


class ServiceDetailView(TemplateView):
    """View for the service detail page"""
    template_name = 'service_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs.get('slug')
        context['service'] = Service.objects.get(slug=slug)
        return context


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
