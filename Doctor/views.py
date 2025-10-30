from rest_framework import generics
from .models import DemandeSang
from .serializers import DemandeSangSerializer

class DemandeSangListCreateView(generics.ListCreateAPIView):
    queryset = DemandeSang.objects.all().order_by('-date_created')
    serializer_class = DemandeSangSerializer
