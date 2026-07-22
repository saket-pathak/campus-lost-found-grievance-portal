from django.core.mail import send_mail
from django.conf import settings

def send_email_notification(user, subject, message):
    """
    Sends an email notification to the user using Django's email backend.
    """
    if not user.email:
        return False
    try:
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'campusportal@localhost')
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[user.email],
            fail_silently=True
        )
        return True
    except Exception:
        return False
