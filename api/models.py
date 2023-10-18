from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    specialty = models.CharField(max_length=255)
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.specialty}'
    
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.user.first_name

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

