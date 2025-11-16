from django.urls import path
from . import views
from .views import (
    AboutUpdateView,
    ContactMessageDeleteView,
    ContactMessageDetailView,
    ContactMessageListView,
    ContactMessageUpdateView,
    DashboardView,
    HomePageView,
    AboutView,
    ServiceCreateView,
    ServiceDeleteView,
    ServiceFeatureCreateView,
    ServiceFeatureDeleteView,
    ServiceListView,
    ServiceDetailView,
    ContactView,
    ServiceUpdateView,
    SliderCreateView,
    SliderDeleteView,
    SliderListView,
    SliderUpdateView,
    SubscriberDeleteView,
    SubscriberListView,
    SubscriberUpdateView,
    TeamMemberCreateView,
    TeamMemberDeleteView,
    TeamMemberListView,
    TeamMemberUpdateView,
    TestimonialCreateView,
    TestimonialDeleteView,
    TestimonialListView,
    TestimonialUpdateView,
    mark_message_archived,
    mark_message_replied,
    service_request_success,
    subscribe_newsletter,
    TeamListView,
    book_service_directly,
    # New dashboard views
    ServiceListDashboardView,
    ServiceRequestListView,
    ServiceRequestDetailView,
    ServiceRequestUpdateView,
    ServiceRequestDeleteView,
    ServiceRequestMarkProcessedView,
    ServiceRequestMarkNewView,
    toggle_subscriber_status,
)

app_name = 'core'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('subscribe/', subscribe_newsletter, name='subscribe'),
    path('team/', TeamListView.as_view(), name='team'),

    # Services URLs
    path('services/', ServiceListView.as_view(), name='service_list'),
    path('services/<slug:slug>/', ServiceDetailView.as_view(), name='service_detail'),
    path('services/request/success/', service_request_success, name='service_request_success'),
    path('services/request/submit/', views.submit_service_request, name='submit_service_request'),
    path('services/<int:service_id>/book-directly/', book_service_directly, name='book_service_directly'),

    # Dashboard URLs
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/services/', ServiceListDashboardView.as_view(), name='service_list_dashboard'),
    path('dashboard/services/create/', ServiceCreateView.as_view(), name='service_create'),
    path('dashboard/services/<int:pk>/edit/', ServiceUpdateView.as_view(), name='service_update'),
    path('dashboard/services/<int:pk>/delete/', ServiceDeleteView.as_view(), name='service_delete'),
    
    # Service Feature URLs
    path('dashboard/services/<int:service_pk>/features/add/', 
         ServiceFeatureCreateView.as_view(), name='feature_create'),
    path('dashboard/features/<int:pk>/delete/', 
         ServiceFeatureDeleteView.as_view(), name='feature_delete'),
    
    # Service Request Management URLs
    path('dashboard/service-requests/', ServiceRequestListView.as_view(), name='service_request_list'),
    path('dashboard/service-requests/<int:pk>/', ServiceRequestDetailView.as_view(), name='service_request_detail'),
    path('dashboard/service-requests/<int:pk>/update/', ServiceRequestUpdateView.as_view(), name='service_request_update'),
    path('dashboard/service-requests/<int:pk>/delete/', ServiceRequestDeleteView.as_view(), name='service_request_delete'),
    path('dashboard/service-requests/<int:pk>/mark-processed/', ServiceRequestMarkProcessedView.as_view(), name='service_request_mark_processed'),
    path('dashboard/service-requests/<int:pk>/mark-new/', ServiceRequestMarkNewView.as_view(), name='service_request_mark_new'),


    # Testimonial Management URLs
    path('dashboard/testimonials/', TestimonialListView.as_view(), name='testimonial_list'),
    path('dashboard/testimonials/create/', TestimonialCreateView.as_view(), name='testimonial_create'),
    path('dashboard/testimonials/update/<int:pk>/', TestimonialUpdateView.as_view(), name='testimonial_update'),
    path('dashboard/testimonials/delete/<int:pk>/', TestimonialDeleteView.as_view(), name='testimonial_delete'),
    
    # Team Management URLs
    path('dashboard/team/', TeamMemberListView.as_view(), name='team_list'),
    path('dashboard/team/create/', TeamMemberCreateView.as_view(), name='team_create'),
    path('dashboard/team/update/<int:pk>/', TeamMemberUpdateView.as_view(), name='team_update'),
    path('dashboard/team/delete/<int:pk>/', TeamMemberDeleteView.as_view(), name='team_delete'),

    # Slider Management URLs
    path('dashboard/sliders/', SliderListView.as_view(), name='slider_list'),
    path('dashboard/sliders/create/', SliderCreateView.as_view(), name='slider_create'),
    path('dashboard/sliders/update/<int:pk>/', SliderUpdateView.as_view(), name='slider_update'),
    path('dashboard/sliders/delete/<int:pk>/', SliderDeleteView.as_view(), name='slider_delete'),
    
    # Contact Message Management URLs
    path('dashboard/contact-messages/', ContactMessageListView.as_view(), name='contact_message_list'),
    path('dashboard/contact-messages/<int:pk>/', ContactMessageDetailView.as_view(), name='contact_message_detail'),
    path('dashboard/contact-messages/update/<int:pk>/', ContactMessageUpdateView.as_view(), name='contact_message_update'),
    path('dashboard/contact-messages/delete/<int:pk>/', ContactMessageDeleteView.as_view(), name='contact_message_delete'),
    path('dashboard/contact-messages/mark-replied/<int:pk>/', mark_message_replied, name='mark_message_replied'),
    path('dashboard/contact-messages/mark-archived/<int:pk>/', mark_message_archived, name='mark_message_archived'),
    
    # Subscriber Management URLs
    path('dashboard/subscribers/', SubscriberListView.as_view(), name='subscriber_list'),
    path('dashboard/subscribers/update/<int:pk>/', SubscriberUpdateView.as_view(), name='subscriber_update'),
    path('dashboard/subscribers/delete/<int:pk>/', SubscriberDeleteView.as_view(), name='subscriber_delete'),
    path('dashboard/subscribers/toggle-status/<int:pk>/', toggle_subscriber_status, name='toggle_subscriber_status'),
    
    # About Management URL
    path('dashboard/about/', AboutUpdateView.as_view(), name='about_update'),
]