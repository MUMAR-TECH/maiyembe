# projects/urls.py
from django.urls import path
from .views import (
    ProjectListView, ProjectDetailView, ProjectInquiryView, increment_project_views,
    ProjectDashboardView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView,
    ProjectImageCreateView, ProjectImageDeleteView, ProjectVideoCreateView,
    ProjectVideoDeleteView, ProjectFeatureCreateView, ProjectFeatureDeleteView,
    ProjectTestimonialCreateView, ProjectTestimonialDeleteView,
    ProjectCategoryCreateView, ProjectCategoryUpdateView, ProjectCategoryDeleteView
)

app_name = 'projects'

urlpatterns = [
    # Public URLs (should come first with specific patterns)
    path('', ProjectListView.as_view(), name='project_list'),
    path('category/<slug:slug>/', ProjectListView.as_view(), name='category'),
    path('project/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path('project/<slug:slug>/inquiry/', ProjectInquiryView.as_view(), name='project_inquiry'),
    path('project/<slug:slug>/increment-views/', increment_project_views, name='increment_views'),
    
    # Dashboard URLs (should use different patterns to avoid conflicts)
    path('dashboard/', ProjectDashboardView.as_view(), name='project_dashboard'),
    path('dashboard/create/', ProjectCreateView.as_view(), name='project_create'),
    path('dashboard/update/<int:pk>/', ProjectUpdateView.as_view(), name='project_update'),
    path('dashboard/delete/<int:pk>/', ProjectDeleteView.as_view(), name='project_delete'),
    
    # Project Images
    path('dashboard/image/add/<int:project_pk>/', ProjectImageCreateView.as_view(), name='project_image_create'),
    path('dashboard/image/delete/<int:pk>/', ProjectImageDeleteView.as_view(), name='project_image_delete'),
    
    # Project Videos
    path('dashboard/video/add/<int:project_pk>/', ProjectVideoCreateView.as_view(), name='project_video_create'),
    path('dashboard/video/delete/<int:pk>/', ProjectVideoDeleteView.as_view(), name='project_video_delete'),
    
    # Project Features
    path('dashboard/feature/add/<int:project_pk>/', ProjectFeatureCreateView.as_view(), name='project_feature_create'),
    path('dashboard/feature/delete/<int:pk>/', ProjectFeatureDeleteView.as_view(), name='project_feature_delete'),
    
    # Project Testimonials
    path('dashboard/testimonial/add/<int:project_pk>/', ProjectTestimonialCreateView.as_view(), name='project_testimonial_create'),
    path('dashboard/testimonial/delete/<int:pk>/', ProjectTestimonialDeleteView.as_view(), name='project_testimonial_delete'),
    
    # Project Categories
    path('dashboard/category/create/', ProjectCategoryCreateView.as_view(), name='project_category_create'),
    path('dashboard/category/update/<int:pk>/', ProjectCategoryUpdateView.as_view(), name='project_category_update'),
    path('dashboard/category/delete/<int:pk>/', ProjectCategoryDeleteView.as_view(), name='project_category_delete'),
]