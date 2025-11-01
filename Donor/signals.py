from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DonorAlertResponse
from Notification.utils import send_notification

@receiver(post_save, sender=DonorAlertResponse)
def notify_doctor_on_donor_response(sender, instance, created, **kwargs):
    if created:
        status = "accepted" if instance.accepted else "rejected"
        doctor = instance.alert.doctor
        donor = instance.donor

        send_notification(
            user=doctor.user,
            title=f"Donor {status.capitalize()} Request",
            message=f"Donor {donor.user.username} has {status} your blood request for {instance.alert.blood_group}."
        )
