from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login
from django.db import IntegrityError
from .models import User, DoctorProfile, DonorProfile, BloodBankProfile
from .serializers import (
    DoctorProfileSerializer,
    DonorProfileSerializer,
    BloodBankProfileSerializer,
    LoginSerializer,
    DonorRegisterSerializer,
    DoctorRegisterSerializer,
    BloodBankRegisterSerializer
)


# -----------------------------
# Registration Views
# -----------------------------
class DonorRegisterView(generics.CreateAPIView):
    serializer_class = DonorRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)  # Add this to see validation errors
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()  # creates User + DonorProfile
        except IntegrityError:
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        profile = DonorProfile.objects.get(user=user)
        output_serializer = DonorProfileSerializer(profile)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class DoctorRegisterView(generics.CreateAPIView):
    serializer_class = DoctorRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
        except IntegrityError:
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        profile = DoctorProfile.objects.get(user=user)
        output_serializer = DoctorProfileSerializer(profile)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class BloodBankRegisterView(generics.CreateAPIView):
    serializer_class = BloodBankRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
        except IntegrityError:
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        profile = BloodBankProfile.objects.get(user=user)
        output_serializer = BloodBankProfileSerializer(profile)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


# -----------------------------
# Profile Views
# -----------------------------
class DoctorProfileView(generics.RetrieveUpdateAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class DonorProfileView(generics.RetrieveUpdateAPIView):
    queryset = DonorProfile.objects.all()
    serializer_class = DonorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class BloodBankProfileView(generics.RetrieveUpdateAPIView):
    queryset = BloodBankProfile.objects.all()
    serializer_class = BloodBankProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


# -----------------------------
# Login View
# -----------------------------
class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({
            "message": "Login successful",
            "email": user.email,
            "role": user.role
        }, status=status.HTTP_200_OK)
