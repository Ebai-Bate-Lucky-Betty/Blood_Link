# serializers.py
from rest_framework import serializers
from .models import BloodRequest

class BloodRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodRequest
        fields = ['id', 'blood_group', 'quantity', 'urgency', 'status', 'hospital']
