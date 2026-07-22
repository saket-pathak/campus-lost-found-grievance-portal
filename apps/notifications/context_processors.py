def unread_notifications_count(request):
    if request.user.is_authenticated:
        try:
            from .models import Notification
            return {
                'unread_notifications_count': Notification.objects.filter(recipient=request.user, is_read=False).count()
            }
        except Exception:
            return {'unread_notifications_count': 0}
    return {'unread_notifications_count': 0}
