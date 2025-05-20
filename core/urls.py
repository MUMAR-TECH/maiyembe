from django.urls import path
from .views import (
    HomePageView,
    AboutView,
    ServicesView,
    ServiceDetailView,
    ContactView,
    subscribe_newsletter,
    TeamListView,
)


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('services/', ServicesView.as_view(), name='services'),
    path('services/<slug:slug>/', ServiceDetailView.as_view(), name='service_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('subscribe/', subscribe_newsletter, name='subscribe'),
    path('team/', TeamListView.as_view(), name='team'),
]
