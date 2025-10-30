from rest_framework import serializers
from .models import DemandeSang

class DemandeSangSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandeSang
        fields = ['id', 'blood_group', 'quantity', 'urgency', 'hospital', 'status', 'date_created']
