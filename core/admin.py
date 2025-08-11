from django.contrib import admin
from .models import About, TeamMember,ServiceFeature,ServiceRequest, Service, SliderImage, Testimonial,ContactMessage,Subscriber

admin.site.register(TeamMember)
admin.site.register(Service)
admin.site.register(ServiceFeature)
admin.site.register(SliderImage)
admin.site.register(Testimonial)
admin.site.register(ContactMessage)
admin.site.register(Subscriber)
admin.site.register(About)
admin.site.register(ServiceRequest)