from django.urls import path
from .views import ProjectListView, ProjectDetailView

app_name = 'projects'

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('category/<slug:slug>/', ProjectListView.as_view(), name='category'),
    path('<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
]