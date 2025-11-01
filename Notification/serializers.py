from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'read', 'type', 'time']

    def get_time(self, obj):
        from django.utils.timesince import timesince
        return f"{timesince(obj.created_at).split(',')[0]} ago"
