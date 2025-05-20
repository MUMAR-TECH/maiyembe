from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse


class TeamMember(models.Model):
    """Model for team members displayed on the website"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='team/')
    is_leadership = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name


class Service(models.Model):
    """Model for services offered by the company"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})


class SliderImage(models.Model):
    """Model for hero section slider images"""
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    image = models.ImageField(upload_to='slider/')
    button_text = models.CharField(max_length=50, default='Get Started')
    button_url = models.CharField(max_length=200, default='#contact')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title


class Testimonial(models.Model):
    """Model for client testimonials"""
    client_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    testimonial = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Testimonial from {self.client_name}"


class ContactMessage(models.Model):
    """Model for storing contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class Subscriber(models.Model):
    """Model for newsletter subscribers"""
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email

class About(models.Model):
    """Model for the About section content"""
    title = models.CharField(max_length=200, default="ABOUT MAIYEMBE")
    main_content = models.TextField(help_text="Main introduction paragraph")
    secondary_content = models.TextField(help_text="Team experience paragraph")
    additional_content = models.TextField(help_text="Project approach paragraph")
    image = models.ImageField(upload_to='about/', help_text="About section image")
    button_text = models.CharField(max_length=50, default="MEET OUR TEAM")
    button_url = models.CharField(max_length=100, default="#team")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"

    def __str__(self):
        return "About Section Content"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if About.objects.exists() and not self.pk:
            raise ValidationError('Only one About instance is allowed')
        return super().save(*args, **kwargs)