from rest_framework import serializers
from . import models

class DoctorSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Doctor
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'specialty',
        ]

class DoctorLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
class PatientSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Patient
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number'
        ]

class PatientLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)