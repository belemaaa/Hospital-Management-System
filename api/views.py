from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework  import status
from . import models
from . import serializers
from django.contrib.auth.hashers import check_password, make_password 
from .authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

class Doctor_signup(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = serializers.DoctorSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            email = serializer.validated_data.get('email')
            phone_number = serializer.validated_data.get('phone_number')
            specialty = serializer.validated_data.get('specialty')
            raw_pwd = serializer.validated_data.get('password')
            hashed_password = make_password(raw_pwd)
            existing_user = models.User.objects.filter(email=email)
            if existing_user:
                return Response({'error': 'doctor with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.save(password=hashed_password)
            doctor = models.Doctor.objects.create(user=user)
            return Response({'message': 'doctor signup successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Doctor_login(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = serializers.DoctorLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            try:
                doctor = models.Doctor.objects.get(email=email)
            except models.Doctor.DoesNotExist:
                doctor=None
            if doctor is not None and check_password(password, doctor.password):
                token = Token.objects.get_or_create(user=doctor)
                return Response({'message': 'login successful', 'access_token': token.key, 'user_id': doctor.id}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid login credentials', 'email': doctor.email, 'password': doctor.password}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
class Patient_signup(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = serializers.PatientSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            validated_data = serializer.validated_data
            existing_patient = models.Patient.objects.filter(email=validated_data.get('email'))
            if existing_patient:
                return Response({'error': 'patient with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            password = validated_data.get('password')
            hashed_password = make_password(password)
            serializer.save(password=hashed_password)
            return Response({'message': 'patient signup successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class Patient_login(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = serializers.PatientLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            try:
                patient = models.Patient.objects.get(email=email)
                if patient and check_password(password, patient.password):
                    token = Token.objects.get_or_create(user=patient)
                    return Response({'message': 'login successful', 'access_token': token.key, 'user_id': patient.id}, status=status.HTTP_200_OK)
                return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            except models.Doctor.DoesNotExist:
                return Response({'error': 'Patient object not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            