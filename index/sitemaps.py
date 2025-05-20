# website/sitemaps.py
from django.contrib.sitemaps import Sitemap
from .models import BlogPost, Project, Service
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return ['home', 'team', 'blog_list']

    def location(self, item):
        return reverse(item)

class BlogPostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_date

class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Project.objects.filter(is_featured=True)

class ServiceSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.9

    def items(self):
        return Service.objects.filter(is_featured=True)