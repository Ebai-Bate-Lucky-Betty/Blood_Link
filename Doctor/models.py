from django.db import models
from django.conf import settings

class DemandeSang(models.Model):
    URGENCY_CHOICES = [
        ('Normal', 'Normal'),
        ('Urgent', 'Urgent'),
        ('Extremely Urgent', 'Extremely Urgent'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]

    medecin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='demandes',
        null=True, blank=True
    )
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    quantity = models.PositiveIntegerField()
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES)
    hospital = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.blood_group} ({self.quantity} units) - {self.urgency}"
