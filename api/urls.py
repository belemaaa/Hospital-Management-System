from django.urls import path
from . import views

urlpatterns = [
    path('doctor/signup', views.Doctor_signup.as_view()),
    path('patient/signup', views.Patient_signup.as_view()),
    path('doctor/login', views.Doctor_login.as_view()),
    path('patient/login', views.Patient_login.as_view()),
]