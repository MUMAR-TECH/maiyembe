from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class TeamMember(models.Model):
    """Model for team members"""
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='team/')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    is_leadership = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class Service(models.Model):
    """Model for services offered by the company"""
    # Basic Information
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField(help_text="Brief description for cards and listings", null=True, blank=True)
    full_description = models.TextField(help_text="Detailed description for service page", null=True, blank=True)
    image = models.ImageField(upload_to='services/')
    
    # Service Categories
    SERVICE_CATEGORIES = [
        ('design', 'Design & Planning'),
        ('construction', 'Construction'),
        ('electrical', 'Electrical'),
        ('plumbing', 'Plumbing'),
        ('management', 'Property Management'),
        ('other', 'Other Services'),
    ]
    category = models.CharField(
        max_length=50,
        choices=SERVICE_CATEGORIES,
        default='construction'
    )
    
    # Service Details
    icon = models.CharField(
        max_length=50,
        help_text="Font Awesome icon class (e.g. 'fas fa-home')",
        blank=True
    )
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='services_created'
    )
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='services_updated'
    )

    # Enhanced Pricing Information
    starting_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Starting price for this service"
    )
    price_unit = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g., per square meter, per project, etc."
    )
    price_description = models.TextField(
        blank=True,
        help_text="Description of what's included in the starting price"
    )
    is_price_negotiable = models.BooleanField(default=True)
    price_display_type = models.CharField(
        max_length=20,
        choices=[
            ('starting_from', 'Starting From'),
            ('fixed', 'Fixed Price'),
            ('custom', 'Custom Quote'),
            ('free_consultation', 'Free Consultation'),
        ],
        default='starting_from'
    )
    
    # Detailed Pricing Breakdown
    pricing_breakdown = models.TextField(
        blank=True,
        help_text="Detailed breakdown of what's included in the price (one per line)"
    )
    
    # Service Duration
    estimated_duration = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g., 2-4 weeks, 1-2 days, etc."
    )
    
    # What's Included
    includes_services = models.TextField(
        blank=True,
        help_text="List of services included (one per line)"
    )
    
    # Optional Add-ons
    optional_addons = models.TextField(
        blank=True,
        help_text="Optional additional services with prices (one per line)"
    )

    class Meta:
        ordering = ['display_order']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})
    
    def get_price_display(self):
        """Get formatted price display"""
        if not self.starting_price:
            return "Contact for pricing"
        
        if self.price_display_type == 'starting_from':
            return f"Starting from ZMW {self.starting_price:,.2f}"
        elif self.price_display_type == 'fixed':
            return f"ZMW {self.starting_price:,.2f}"
        elif self.price_display_type == 'custom':
            return "Custom Quote"
        elif self.price_display_type == 'free_consultation':
            return "Free Consultation"
        return f"ZMW {self.starting_price:,.2f}"
    
    def get_pricing_breakdown_list(self):
        """Convert pricing breakdown to list"""
        if self.pricing_breakdown:
            return [line.strip() for line in self.pricing_breakdown.split('\n') if line.strip()]
        return []
    
    def get_includes_list(self):
        """Convert included services to list"""
        if self.includes_services:
            return [line.strip() for line in self.includes_services.split('\n') if line.strip()]
        return []
    
    def get_optional_addons_list(self):
        """Convert optional addons to list"""
        if self.optional_addons:
            return [line.strip() for line in self.optional_addons.split('\n') if line.strip()]
        return []

class ServiceFeature(models.Model):
    """Model for features/benefits of each service"""
    service = models.ForeignKey(
        Service,
        related_name='features',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Font Awesome icon class (e.g. 'fas fa-check')"
    )
    
    def __str__(self):
        return f"{self.service.title} - {self.title}"

class ServiceRequest(models.Model):
    """Model for service requests from clients"""
    SERVICE_TYPES = [
        ('general', 'General Inquiry'),
        ('design', 'Design Consultation'),
        ('construction', 'Construction Project'),
        ('electrical', 'Electrical Work'),
        ('plumbing', 'Plumbing Work'),
        ('management', 'Property Management'),
        ('other', 'Other'),
    ]
    
    CONTACT_METHODS = [
        ('phone', 'Phone Call'),
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('in-person', 'In-Person Meeting'),
    ]
    
    BUDGET_RANGES = [
        ('under_10k', 'Under ZMW 10,000'),
        ('10k_50k', 'ZMW 10,000 - 50,000'),
        ('50k_100k', 'ZMW 50,000 - 100,000'),
        ('100k_250k', 'ZMW 100,000 - 250,000'),
        ('250k_500k', 'ZMW 250,000 - 500,000'),
        ('500k_1m', 'ZMW 500,000 - 1,000,000'),
        ('over_1m', 'Over ZMW 1,000,000'),
        ('custom', 'Custom Budget'),
    ]
    
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='requests'
    )
    service_type = models.CharField(
        max_length=50,
        choices=SERVICE_TYPES,
        default='general'
    )
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    contact_method = models.CharField(
        max_length=50,
        choices=CONTACT_METHODS,
        default='whatsapp'
    )
    
    # Enhanced Budget Information
    budget_range = models.CharField(
        max_length=50,
        choices=BUDGET_RANGES,
        default='custom'
    )
    custom_budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Specific budget amount if custom range selected"
    )
    
    # Project Details
    project_location = models.CharField(
        max_length=200,
        blank=True,
        help_text="Where is the project located?"
    )
    project_timeline = models.CharField(
        max_length=100,
        blank=True,
        help_text="Desired timeline for project completion"
    )
    
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seen = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Service Request #{self.id} - {self.name}"
    
    def get_budget_display(self):
        """Get formatted budget display"""
        if self.budget_range == 'custom' and self.custom_budget:
            return f"ZMW {self.custom_budget:,.2f}"
        return dict(self.BUDGET_RANGES).get(self.budget_range, 'Not specified')

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
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )
    
    client_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    testimonial = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
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