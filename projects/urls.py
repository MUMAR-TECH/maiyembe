# urls.py (updated)
from django.urls import path
from .views import ProjectListView, ProjectDetailView, ProjectInquiryView, increment_project_views

app_name = 'projects'

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('category/<slug:slug>/', ProjectListView.as_view(), name='category'),
    path('<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path('<slug:slug>/inquiry/', ProjectInquiryView.as_view(), name='project_inquiry'),
    path('<slug:slug>/increment-views/', increment_project_views, name='increment_views'),
]