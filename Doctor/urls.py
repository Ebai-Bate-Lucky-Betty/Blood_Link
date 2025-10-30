from django.urls import path
from .views import DemandeSangListCreateView

urlpatterns = [
    path('requests/', DemandeSangListCreateView.as_view(), name='blood-requests'),
]
