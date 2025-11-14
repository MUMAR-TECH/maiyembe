from django.urls import path
from . import views
from .views import (
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
    TeamMemberCreateView,
    TeamMemberDeleteView,
    TeamMemberListView,
    TeamMemberUpdateView,
    TestimonialCreateView,
    TestimonialDeleteView,
    TestimonialListView,
    TestimonialUpdateView,
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
]