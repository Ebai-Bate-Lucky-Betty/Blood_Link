from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BloodRequest
from Notification.utils import send_notification

@receiver(post_save, sender=BloodRequest)
def notify_bloodbank_on_doctor_request(sender, instance, created, **kwargs):
    if created:
        bloodbank = instance.bloodbank
        send_notification(
            user=bloodbank.user,
            title="New Blood Request",
            message=f"Dr. {instance.doctor.user.username} requested {instance.blood_group} blood for {instance.patient_name}."
        )
