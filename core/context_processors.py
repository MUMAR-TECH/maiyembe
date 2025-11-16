from .models import ContactMessage

def core_context(request):
    if request.user.is_authenticated:
        new_messages_count = ContactMessage.objects.filter(is_read='False').count()
    else:
        new_messages_count = 0
    
    return {
        'new_messages_count': new_messages_count,
    }