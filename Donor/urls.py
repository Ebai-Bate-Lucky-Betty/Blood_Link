from django.urls import path
from .views import AlertListView, DonorAvailabilityUpdate, RespondToAlert

urlpatterns = [
    path('alerts/', AlertListView.as_view(), name='alerts'),
    path('availability/<int:pk>/', DonorAvailabilityUpdate.as_view(), name='update-availability'),
    path('alerts/<int:alert_id>/<str:action>/', RespondToAlert.as_view(), name='respond-alert'),
]
