from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    first_name =models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(default='noemail@example.com')
    password = models.CharField(max_length=255)
    def __str__(self):
        return f'{self.first_name} - {self.specialty}'
    
class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    first_name =models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number =models.CharField(max_length=20)
    email= models.EmailField(default='noemail@example.com')
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True)
    password = models.CharField(max_length=255)
    def __str__(self):
        return self.first_name

class Appointment(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    app_id = models.CharField(max_length=10)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient =models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.doctor} - appointment with {self.patient}'
    # def save(self, *args, **kwargs):
    #     existing_appointment = Appointment.objects.filter(doctor=self.doctor, date=self.date, time=self.time).exclude(id=self.id).first()    
    #     if existing_appointment:
    #         raise ValueError("Doctor is already booked for this time slot.")  
    #     super().save(*args, **kwargs)

