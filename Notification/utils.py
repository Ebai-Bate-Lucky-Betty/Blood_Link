from .models import Notification

def send_notification(user, title, message):
    """Create a notification for a specific user"""
    if user:
        Notification.objects.create(user=user, title=title, message=message)
