from rest_framework import serializers
from . import models

class DoctorSignupSerializer(serializers.ModelSerializer):
    specialty = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    class Meta:
        model = models.User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'specialty',
        ]
    def get_specialty(self, obj):
        return obj.specialty
    def get_phone_number(self, obj):
        return obj.phone_number

class DoctorLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
class PatientSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
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