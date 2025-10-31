from rest_framework import generics, permissions
from .models import BloodRequest
from .serializers import BloodRequestSerializer

class DoctorBloodRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = BloodRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Doctor only sees their own requests
        return BloodRequest.objects.filter(doctor=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)
