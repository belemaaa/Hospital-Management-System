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
                return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.save(password=hashed_password)
            doctor = models.Doctor.objects.create(user=user, specialty=specialty)
            return Response({'message': 'Doctor has been created'}, status=status.HTTP_201_CREATED)
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
                user = models.User.objects.get(email=email) 
                doctor = models.Doctor.objects.get(user=user) #Retrieve the doctor instance associated with the user
            except models.User.DoesNotExist:
                user=None
            except models.Doctor.DoesNotExist:
                doctor=None
            if doctor is not None and check_password(password, doctor.user.password):
                token = Token.objects.get_or_create(user=doctor)
                return Response({'message': 'login successful', 'access_token': token.key, 'user_id': doctor.id}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
class Patient_signup(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = serializers.PatientSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            validated_data = serializer.validated_data
            existing_user = models.User.objects.get(email=validated_data.get('email'))
            if existing_user:
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            password = validated_data.get('password')
            hashed_password = make_password(password)
            user = serializer.save(password=hashed_password)
            patient = models.Patient.objects.create(user=user)
            return Response({'message': 'Patient has been created.'}, status=status.HTTP_201_CREATED)
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
                user = models.User.objects.get(email=email)
            except models.User.DoesNotExist:
                user=None
            if user is not None:
                patient = models.Patient.objects.get(user=user) #Retrieve the patient instance associated with the user
            else:
                patient=None
            if patient is not None and check_password(password, patient.user.password):
                token = Token.objects.get_or_create(user=patient)
                return Response({'message': 'login successful', 'access_token': token.key, 'user_id': patient.id}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            