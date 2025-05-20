# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('projects/', views.projects, name='projects'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('team/', views.team, name='team'),
    path('contact/', views.contact, name='contact'),
    path('subscribe/', views.subscribe, name='subscribe'),



        # Service URLs
    path('services/create/', views.create_service, name='create_service'),
    path('services/<slug:slug>/edit/', views.edit_service, name='edit_service'),
    path('services/<slug:slug>/delete/', views.delete_service, name='delete_service'),
    path('services/<slug:slug>/toggle-status/', views.toggle_service_status, name='toggle_service_status'),
    
    # Blog URLs
    path('blog/create/', views.create_blog_post, name='create_blog_post'),
    path('blog/<slug:slug>/edit/', views.edit_blog_post, name='edit_blog_post'),
    path('blog/<slug:slug>/delete/', views.delete_blog_post, name='delete_blog_post'),
    path('blog/<slug:slug>/toggle-status/', views.toggle_blog_post_status, name='toggle_blog_post_status'),
    
    # Project URLs
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<slug:slug>/edit/', views.edit_project, name='edit_project'),
    path('projects/<slug:slug>/delete/', views.delete_project, name='delete_project'),
    path('projects/<slug:slug>/toggle-status/', views.toggle_project_status, name='toggle_project_status'),
    
    # Testimonial URLs
    path('testimonials/create/', views.create_testimonial, name='create_testimonial'),
    path('testimonials/<int:pk>/edit/', views.edit_testimonial, name='edit_testimonial'),
    path('testimonials/<int:pk>/delete/', views.delete_testimonial, name='delete_testimonial'),
    path('testimonials/<int:pk>/toggle-status/', views.toggle_testimonial_status, name='toggle_testimonial_status'),
    
    # Team URLs
    path('team/create/', views.create_team_member, name='create_team_member'),
    path('team/<int:pk>/edit/', views.edit_team_member, name='edit_team_member'),
    path('team/<int:pk>/delete/', views.delete_team_member, name='delete_team_member'),
    path('team/<int:pk>/toggle-status/', views.toggle_team_member_status, name='toggle_team_member_status'),

]