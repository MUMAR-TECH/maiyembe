# blog/context_processors.py
from .models import Comment

def blog_context(request):
    if request.user.is_authenticated:
        pending_comments = Comment.objects.filter(is_approved=False).count()
    else:
        pending_comments = 0
    
    return {
        'comment_count': pending_comments,
    }