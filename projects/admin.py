from django.contrib import admin
from .models import ProjectCategory, Project, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'location', 'completion_date', 'is_featured')
    list_filter = ('is_featured', 'completion_date', 'categories')
    search_fields = ('title', 'description', 'client', 'location')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)
    date_hierarchy = 'completion_date'
    list_editable = ('is_featured',)
    inlines = [ProjectImageInline]


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'caption', 'is_landscape', 'order')
    list_filter = ('project', 'is_landscape')
    list_editable = ('is_landscape', 'order')
    search_fields = ('project__title', 'caption')