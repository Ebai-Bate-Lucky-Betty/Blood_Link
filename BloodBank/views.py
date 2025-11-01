from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Alert
from Doctor.models import BloodRequest  # ✅ get doctor requests
from Donor.models import DonorAlertResponse  # ✅ to count accepted donors
from .serializers import BloodRequestSerializer, AlertSerializer


class BloodRequestListView(generics.ListAPIView):
    """GET /api/bloodbank/requests/ — list all active requests"""
    queryset = BloodRequest.objects.filter(status='pending')
    serializer_class = BloodRequestSerializer
    permission_classes = [IsAuthenticated]


class BloodRequestUpdateView(generics.UpdateAPIView):
    """PATCH /api/bloodbank/requests/<id>/ — mark request as processed"""
    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = request.data.get('status', instance.status)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AlertListCreateView(generics.ListCreateAPIView):
    """
    GET /api/bloodbank/alerts/ — List active alerts
    POST /api/bloodbank/alerts/ — Create new alert

    When listing, also show statistics for:
    - total active alerts
    - total pending requests from doctors
    - total donors who accepted alerts
    """
    queryset = Alert.objects.filter(is_active=True)
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """Add statistics to the alerts list response"""
        alerts = self.get_queryset()
        serializer = self.get_serializer(alerts, many=True)

        # ✅ Count total pending doctor requests
        pending_requests = BloodRequest.objects.filter(status='pending').count()

        # ✅ Count donors who accepted at least one alert
        accepted_donors = DonorAlertResponse.objects.filter(accepted=True).values('donor').distinct().count()

        data = {
            "alerts": serializer.data,
            "stats": {
                "total_alerts": alerts.count(),
                "pending_requests": pending_requests,
                "accepted_donors": accepted_donors
            }
        }
        return Response(data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """When a bank creates an alert"""
        serializer.save(blood_bank=self.request.user, donor_count=0)


class AlertDeleteView(generics.DestroyAPIView):
    """DELETE /api/bloodbank/alerts/<blood_group>/ — deactivate an alert"""
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        blood_group = self.kwargs['blood_group']
        return Alert.objects.filter(blood_group=blood_group, is_active=True).first()

    def destroy(self, request, *args, **kwargs):
        alert = self.get_object()
        if not alert:
            return Response({"detail": "Alert not found."}, status=status.HTTP_404_NOT_FOUND)
        alert.is_active = False
        alert.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
