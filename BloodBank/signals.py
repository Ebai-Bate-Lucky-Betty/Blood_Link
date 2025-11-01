from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Alert
from users.models import DonorProfile
from Notification.utils import send_notification

@receiver(post_save, sender=Alert)
def notify_donors_on_new_alert(sender, instance, created, **kwargs):
    if created:
        donors = DonorProfile.objects.filter(blood_group=instance.blood_group)
        for donor in donors:
            send_notification(
                user=donor.user,
                title="New Blood Alert",
                message= f"An alert was launched for {instance.blood_group} blood urgently."
            )
