# models.py (updated)
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import os
from accounts.models import User

class ProjectCategory(models.Model):
    """Model for project categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='project_categories/', blank=True, null=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = 'Project Categories'
        ordering = ['order', 'name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Project(models.Model):
    """Model for portfolio projects"""
    PROJECT_STATUS = (
        ('completed', 'Completed'),
        ('ongoing', 'Ongoing'),
        ('upcoming', 'Upcoming'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    client = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    completion_date = models.DateField()
    project_duration = models.CharField(max_length=50, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True)
    featured_image = models.ImageField(upload_to='projects/')
    is_featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=PROJECT_STATUS, default='completed')
    categories = models.ManyToManyField(ProjectCategory, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_projects')
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_projects')
    # SEO fields
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    def get_primary_category(self):
        """Return the first category for display purposes"""
        return self.categories.first() if self.categories.exists() else None


class ProjectImage(models.Model):
    """Model for additional project images"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    is_landscape = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Image for {self.project.title}"
    
    def save(self, *args, **kwargs):
        # Ensure only one primary image per project
        if self.is_primary:
            ProjectImage.objects.filter(project=self.project, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)


class ProjectVideo(models.Model):
    """Model for project videos"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='videos')
    video_url = models.URLField(help_text="YouTube or Vimeo URL")
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Video for {self.project.title}"


class ProjectFeature(models.Model):
    """Model for project features/highlights"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, 
                           help_text="Font Awesome icon class (e.g., 'fas fa-home')")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.title} - {self.project.title}"


class ProjectTestimonial(models.Model):
    """Model for project-specific testimonials"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='testimonials')
    client_name = models.CharField(max_length=100)
    client_position = models.CharField(max_length=100, blank=True)
    testimonial = models.TextField()
    avatar = models.ImageField(upload_to='testimonials/avatars/', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return f"Testimonial by {self.client_name} for {self.project.title}"


class ProjectInquiry(models.Model):
    """Model for project inquiries"""
    INQUIRY_STATUS = (
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    SERVICE_CHOICES = (
        ('residential', 'Residential Construction'),
        ('commercial', 'Commercial Construction'),
        ('renovation', 'Renovation'),
        ('design', 'Architectural Design'),
        ('consultation', 'Consultation'),
        ('other', 'Other'),
    )
    
    BUDGET_CHOICES = (
        ('under-50k', 'Under $50,000'),
        ('50k-100k', '$50,000 - $100,000'),
        ('100k-250k', '$100,000 - $250,000'),
        ('250k-500k', '$250,000 - $500,000'),
        ('500k-1m', '$500,000 - $1 Million'),
        ('over-1m', 'Over $1 Million'),
    )
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='inquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    budget_range = models.CharField(max_length=20, choices=BUDGET_CHOICES)
    timeline = models.CharField(max_length=100, blank=True)
    project_description = models.TextField()
    property_address = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=INQUIRY_STATUS, default='new')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Project Inquiries'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Inquiry from {self.name} for {self.project.title}"