from django.contrib import admin
from .models import About, TeamMember,Service, SliderImage, Testimonial,ContactMessage,Subscriber

admin.site.register(TeamMember)
admin.site.register(Service)
admin.site.register(SliderImage)
admin.site.register(Testimonial)
admin.site.register(ContactMessage)
admin.site.register(Subscriber)
admin.site.register(About)