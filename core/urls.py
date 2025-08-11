from django.urls import path
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
    ServiceRequestView,
    ServiceUpdateView,
    service_request_success,
    subscribe_newsletter,
    TeamListView,
)

app_name = 'core'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('services/', ServiceListView.as_view(), name='services'),
    #path('services/<slug:slug>/', ServiceDetailView.as_view(), name='service_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('subscribe/', subscribe_newsletter, name='subscribe'),
    path('team/', TeamListView.as_view(), name='team'),


    path('services/', ServiceListView.as_view(), name='services'),
    path('services/<slug:slug>/', ServiceDetailView.as_view(), name='service_detail'),
    #path('services/request/', ServiceRequestView.as_view(), name='service_request'),
    path('services/request/success/', service_request_success, name='service_request_success'),
    path('services/request/', ServiceRequestView.as_view(), name='service_request'),

    # Dashboard URLs
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/services/create/', ServiceCreateView.as_view(), name='service_create'),
    path('dashboard/services/<int:pk>/edit/', ServiceUpdateView.as_view(), name='service_update'),
    path('dashboard/services/<int:pk>/delete/', ServiceDeleteView.as_view(), name='service_delete'),
    
    # Service Feature URLs
    path('dashboard/services/<int:service_pk>/features/add/', 
         ServiceFeatureCreateView.as_view(), name='feature_create'),
    path('dashboard/features/<int:pk>/delete/', 
         ServiceFeatureDeleteView.as_view(), name='feature_delete'),
]
